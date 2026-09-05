import re

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubScreen.kt', 'r') as f:
    content = f.read()

# Make sure imports are present
if "androidx.compose.material.icons.outlined.Clear" not in content:
    content = content.replace("import androidx.compose.material.icons.Icons", "import androidx.compose.material.icons.Icons\nimport androidx.compose.material.icons.outlined.Clear\nimport androidx.compose.material3.OutlinedTextField")

# I'll use a regex to match from `if (selectedTabIndex == 0) {` to the matching closing brace before `} else {`

old_code_regex = re.compile(r'                if \(selectedTabIndex == 0\) \{.*?                \} else \{', re.DOTALL)

new_code = """                if (selectedTabIndex == 0) {
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
                } else {"""

content = old_code_regex.sub(new_code, content, count=1)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubScreen.kt', 'w') as f:
    f.write(content)
