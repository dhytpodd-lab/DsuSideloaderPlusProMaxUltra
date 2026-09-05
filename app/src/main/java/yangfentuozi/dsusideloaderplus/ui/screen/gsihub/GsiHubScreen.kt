package yangfentuozi.dsusideloaderplus.ui.screen.gsihub

import android.app.DownloadManager
import android.content.Context
import android.net.Uri
import android.os.Build
import android.os.Environment
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Clear
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.outlined.ArrowBack
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import yangfentuozi.dsusideloaderplus.R
import yangfentuozi.dsusideloaderplus.ui.components.ApplicationScreen
import yangfentuozi.dsusideloaderplus.ui.components.SettingsItem
import yangfentuozi.dsusideloaderplus.ui.components.ExpandableSettingsItem
import yangfentuozi.dsusideloaderplus.ui.components.TopBar
import yangfentuozi.dsusideloaderplus.ui.screen.Destinations
import androidx.hilt.lifecycle.viewmodel.compose.hiltViewModel
import androidx.compose.foundation.clickable
import java.util.UUID

data class GsiRom(val name: String, val author: String, val urls: Map<String, String>, val architecture: String)
data class CustomLink(val id: String, val name: String, val url: String)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun GsiHubScreen(navigate: (String) -> Unit, viewModel: GsiHubViewModel = hiltViewModel()) {
    val context = LocalContext.current
    var selectedTabIndex by remember { mutableIntStateOf(0) }
    
    LaunchedEffect(Unit) {
        viewModel.navigateToHome.collect {
            navigate(Destinations.Homepage)
        }
    }
    
    // Check Architecture
    val supportedAbis = Build.SUPPORTED_ABIS.toList()
    val isArm64 = supportedAbis.contains("arm64-v8a")
    val isArm32 = supportedAbis.contains("armeabi-v7a") && !isArm64
    
    val catalog = remember {
        listOf(
            GsiRom("AOSP 14.0 v416", "phhusson / ponces", mapOf("GitHub" to "https://github.com/ponces/treble_build_aosp/releases/download/v416/aosp-arm64-ab-vanilla-14.0-20240222.img.xz"), "arm64-v8a"),
            GsiRom("LineageOS 21", "AndyCGyan", mapOf("SourceForge" to "https://sourceforge.net/projects/andyyan-gsi/files/lineage-21/lineage-21.0-20240217-UNOFFICIAL-arm64_bgS.img.xz/download"), "arm64-v8a"),
            GsiRom("Pixel Experience 13", "ponces", mapOf("GitHub" to "https://github.com/ponces/treble_build_pe/releases/download/v20231104/PixelExperience_arm64-ab-13.0-20231104-UNOFFICIAL.img.xz"), "arm64-v8a"),
            GsiRom("LineageOS 20 (ARM32)", "AndyCGyan", mapOf("SourceForge" to "https://sourceforge.net/projects/andyyan-gsi/files/lineage-20/lineage-20.0-20231018-UNOFFICIAL-arm_bvS.img.xz/download"), "armeabi-v7a")
        ).filter { 
            (isArm64 && it.architecture == "arm64-v8a") || (isArm32 && it.architecture == "armeabi-v7a") || (!isArm64 && !isArm32)
        }
    }

    val prefs = context.getSharedPreferences("gsi_hub_custom_links", Context.MODE_PRIVATE)
    var customLinks by remember {
        mutableStateOf(
            prefs.all.map { CustomLink(it.key, it.key, it.value.toString()) }
        )
    }

    var showAddLinkDialog by remember { mutableStateOf(false) }

    


    LaunchedEffect(customLinks) {
        viewModel.fetchTelegramChannels(customLinks)
    }

    ApplicationScreen(
        columnContent = false,
        topBar = {
            TopBar(
                barTitle = stringResource(id = R.string.gsi_hub_title),
                icon = Icons.Outlined.ArrowBack,
                scrollBehavior = it,
                onClickIcon = { navigate(Destinations.Up) },
            )
        },
        content = {
            Column(modifier = Modifier.fillMaxSize()) {
                TabRow(selectedTabIndex = selectedTabIndex) {
                    Tab(
                        selected = selectedTabIndex == 0,
                        onClick = { selectedTabIndex = 0 },
                        text = { Text(stringResource(id = R.string.gsi_catalog)) }
                    )
                    Tab(
                        selected = selectedTabIndex == 1,
                        onClick = { selectedTabIndex = 1 },
                        text = { Text(stringResource(id = R.string.custom_links)) }
                    )
                }


                if (selectedTabIndex == 0) {
                    var searchQuery by remember { mutableStateOf("") }
                    var currentPage by remember { mutableStateOf(1) }
                    
                    val allRoms = catalog + viewModel.parsedTgRoms
                    val filteredRoms = allRoms.filter { 
                        it.name.contains(searchQuery, ignoreCase = true) || it.author.contains(searchQuery, ignoreCase = true)
                    }
                    
                    val itemsPerPage = 20
                    val maxPages = if (filteredRoms.isEmpty()) 1 else (filteredRoms.size + itemsPerPage - 1) / itemsPerPage
                    if (currentPage > maxPages) currentPage = maxPages
                    if (currentPage < 1) currentPage = 1
                    
                    val paginatedRoms = filteredRoms.drop((currentPage - 1) * itemsPerPage).take(itemsPerPage)

                    Column(modifier = Modifier.fillMaxSize()) {
                        OutlinedTextField(
                            value = searchQuery,
                            onValueChange = { searchQuery = it; currentPage = 1 },
                            modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
                            label = { Text(stringResource(id = R.string.search)) },
                            singleLine = true,
                            trailingIcon = {
                                if (searchQuery.isNotEmpty()) {
                                    IconButton(onClick = { searchQuery = ""; currentPage = 1 }) {
                                        Icon(Icons.Outlined.Clear, contentDescription = "Clear")
                                    }
                                }
                            }
                        )
                        
                        LazyColumn(modifier = Modifier.weight(1f)) {
                            if (viewModel.isParsingTg.value) {
                                item {
                                    Box(modifier = Modifier.fillMaxWidth().padding(16.dp), contentAlignment = androidx.compose.ui.Alignment.Center) {
                                        CircularProgressIndicator()
                                    }
                                }
                            }
                            
                            items(paginatedRoms) { rom ->
                                var expanded by remember { mutableStateOf(false) }
                                val isAnyDownloading = rom.urls.values.any { viewModel.downloadJobs.containsKey(it) }
                                val downloadingUrl = rom.urls.values.find { viewModel.downloadJobs.containsKey(it) }
                                
                                ExpandableSettingsItem(
                                    title = rom.name,
                                    summary = rom.author,
                                    expanded = expanded || isAnyDownloading,
                                    onExpandedChange = { expanded = it },
                                    rowTrailingContent = {
                                        if (downloadingUrl != null) {
                                            val progress = viewModel.downloadProgress[downloadingUrl]
                                            if (progress != null) {
                                                if (progress < 0f) {
                                                    CircularProgressIndicator(
                                                        modifier = Modifier.size(24.dp)
                                                    )
                                                } else {
                                                    CircularProgressIndicator(
                                                        progress = { progress },
                                                        modifier = Modifier.size(24.dp)
                                                    )
                                                }
                                            }
                                        }
                                    }
                                ) {
                                    Column(modifier = Modifier.padding(horizontal = 36.dp, vertical = 8.dp)) {
                                        rom.urls.forEach { (mirrorName, url) ->
                                            val isThisDownloading = viewModel.downloadJobs.containsKey(url)
                                            val error = viewModel.downloadErrors[url]
                                            val progress = viewModel.downloadProgress[url]
                            
                                            Column(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                                                Row(verticalAlignment = androidx.compose.ui.Alignment.CenterVertically) {
                                                    Text(
                                                        text = mirrorName,
                                                        modifier = Modifier.weight(1f),
                                                        style = MaterialTheme.typography.bodyMedium
                                                    )
                                                    if (isThisDownloading) {
                                                        TextButton(onClick = { viewModel.cancelDownload(url) }) {
                                                            Text(stringResource(id = R.string.cancel))
                                                        }
                                                    } else {
                                                        Button(
                                                            onClick = { viewModel.startDownload(url, rom.name) },
                                                            enabled = !isAnyDownloading
                                                        ) {
                                                            Text(stringResource(id = R.string.download))
                                                        }
                                                    }
                                                }
                                                if (isThisDownloading && progress != null) {
                                                    if (progress < 0f) {
                                                        LinearProgressIndicator(
                                                            modifier = Modifier.fillMaxWidth().padding(top = 4.dp)
                                                        )
                                                    } else {
                                                        LinearProgressIndicator(
                                                            progress = { progress },
                                                            modifier = Modifier.fillMaxWidth().padding(top = 4.dp)
                                                        )
                                                    }
                                                }
                                                if (error != null) {
                                                    Text(
                                                        text = error,
                                                        color = MaterialTheme.colorScheme.error,
                                                        style = MaterialTheme.typography.bodySmall,
                                                        modifier = Modifier.padding(top = 4.dp)
                                                    )
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        
                        if (maxPages > 1) {
                            Row(
                                modifier = Modifier.fillMaxWidth().padding(16.dp),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = androidx.compose.ui.Alignment.CenterVertically
                            ) {
                                TextButton(
                                    onClick = { if (currentPage > 1) currentPage-- },
                                    enabled = currentPage > 1
                                ) {
                                    Text("< " + stringResource(id = R.string.previous))
                                }
                                Text("$currentPage / $maxPages")
                                TextButton(
                                    onClick = { if (currentPage < maxPages) currentPage++ },
                                    enabled = currentPage < maxPages
                                ) {
                                    Text(stringResource(id = R.string.next) + " >")
                                }
                            }
                        }
                    }
                } else {
                    Box(modifier = Modifier.fillMaxSize()) {
                        LazyColumn(modifier = Modifier.fillMaxSize().padding(bottom = 80.dp)) {
                            items(customLinks) { link ->
                                Column(
                                    modifier = Modifier
                                        .padding(horizontal = 16.dp, vertical = 4.dp)
                                        .clickable(enabled = !viewModel.downloadJobs.containsKey(link.url)) {
                                            viewModel.startDownload(link.url, link.name)
                                        }
                                ) {
                                    ListItem(
                                        headlineContent = { Text(link.name) },
                                        supportingContent = { Text(link.url) },
                                        trailingContent = {
                                            IconButton(onClick = {
                                                prefs.edit().remove(link.id).apply()
                                                customLinks = prefs.all.map { CustomLink(it.key, it.key, it.value.toString()) }
                                            }) {
                                                Icon(Icons.Outlined.Delete, contentDescription = "Delete")
                                            }
                                        },
                                        colors = ListItemDefaults.colors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
                                    )
                                    val progress = viewModel.downloadProgress[link.url]
                                    if (progress != null) {
                                        Column(modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)) {
                                            LinearProgressIndicator(
                                                progress = { progress },
                                                modifier = Modifier.fillMaxWidth()
                                            )
                                            TextButton(
                                                onClick = { viewModel.cancelDownload(link.url) },
                                                modifier = Modifier.align(androidx.compose.ui.Alignment.End)
                                            ) {
                                                Text(stringResource(id = R.string.cancel))
                                            }
                                        }
                                    } else if (viewModel.downloadErrors.containsKey(link.url)) {
                                        Text(
                                            text = viewModel.downloadErrors[link.url]!!,
                                            color = MaterialTheme.colorScheme.error,
                                            style = MaterialTheme.typography.bodySmall,
                                            modifier = Modifier.padding(horizontal = 16.dp, vertical = 4.dp)
                                        )
                                    }
                                }
                                Spacer(modifier = Modifier.height(8.dp))
                            }
                        }
                        FloatingActionButton(
                            onClick = { showAddLinkDialog = true },
                            modifier = Modifier.padding(16.dp).align(androidx.compose.ui.Alignment.BottomEnd)
                        ) {
                            Icon(Icons.Filled.Add, contentDescription = "Add Link")
                        }
                    }
                }
            }
            if (showAddLinkDialog) {
                var newName by remember { mutableStateOf("") }
                var newUrl by remember { mutableStateOf("") }
                AlertDialog(
                    onDismissRequest = { showAddLinkDialog = false },
                    title = { Text(stringResource(id = R.string.add_link)) },
                    text = {
                        Column {
                            OutlinedTextField(
                                value = newName,
                                onValueChange = { newName = it },
                                label = { Text(stringResource(id = R.string.link_name)) },
                                singleLine = true
                            )
                            Spacer(Modifier.height(8.dp))
                            OutlinedTextField(
                                value = newUrl,
                                onValueChange = { newUrl = it },
                                label = { Text(stringResource(id = R.string.link_url)) },
                                singleLine = true
                            )
                        }
                    },
                    confirmButton = {
                        TextButton(onClick = {
                            if (newName.isNotBlank() && newUrl.isNotBlank()) {
                                prefs.edit().putString(newName, newUrl).apply()
                                customLinks = prefs.all.map { CustomLink(it.key, it.key, it.value.toString()) }
                            }
                            showAddLinkDialog = false
                        }) {
                            Text(stringResource(id = R.string.add))
                        }
                    },
                    dismissButton = {
                        TextButton(onClick = { showAddLinkDialog = false }) {
                            Text(stringResource(id = R.string.cancel))
                        }
                    }
                )
            }
        }
    )
}
