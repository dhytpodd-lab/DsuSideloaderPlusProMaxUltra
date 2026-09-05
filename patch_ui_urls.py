import re

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubScreen.kt', 'r') as f:
    content = f.read()

# Change GsiRom definition
content = content.replace(
    'data class GsiRom(val name: String, val author: String, val url: String, val architecture: String)',
    'data class GsiRom(val name: String, val author: String, val urls: Map<String, String>, val architecture: String)'
)

# Update catalog
content = content.replace(
    'GsiRom("AOSP 14.0 v416", "phhusson / ponces", "https://github.com/ponces/treble_build_aosp/releases/download/v416/aosp-arm64-ab-vanilla-14.0-20240222.img.xz", "arm64-v8a")',
    'GsiRom("AOSP 14.0 v416", "phhusson / ponces", mapOf("GitHub" to "https://github.com/ponces/treble_build_aosp/releases/download/v416/aosp-arm64-ab-vanilla-14.0-20240222.img.xz"), "arm64-v8a")'
)
content = content.replace(
    'GsiRom("LineageOS 21", "AndyCGyan", "https://sourceforge.net/projects/andyyan-gsi/files/lineage-21/lineage-21.0-20240217-UNOFFICIAL-arm64_bgS.img.xz/download", "arm64-v8a")',
    'GsiRom("LineageOS 21", "AndyCGyan", mapOf("SourceForge" to "https://sourceforge.net/projects/andyyan-gsi/files/lineage-21/lineage-21.0-20240217-UNOFFICIAL-arm64_bgS.img.xz/download"), "arm64-v8a")'
)
content = content.replace(
    'GsiRom("Pixel Experience 13", "ponces", "https://github.com/ponces/treble_build_pe/releases/download/v20231104/PixelExperience_arm64-ab-13.0-20231104-UNOFFICIAL.img.xz", "arm64-v8a")',
    'GsiRom("Pixel Experience 13", "ponces", mapOf("GitHub" to "https://github.com/ponces/treble_build_pe/releases/download/v20231104/PixelExperience_arm64-ab-13.0-20231104-UNOFFICIAL.img.xz"), "arm64-v8a")'
)
content = content.replace(
    'GsiRom("LineageOS 20 (ARM32)", "AndyCGyan", "https://sourceforge.net/projects/andyyan-gsi/files/lineage-20/lineage-20.0-20231018-UNOFFICIAL-arm_bvS.img.xz/download", "armeabi-v7a")',
    'GsiRom("LineageOS 20 (ARM32)", "AndyCGyan", mapOf("SourceForge" to "https://sourceforge.net/projects/andyyan-gsi/files/lineage-20/lineage-20.0-20231018-UNOFFICIAL-arm_bvS.img.xz/download"), "armeabi-v7a")'
)

# Add ExpandableSettingsItem import
content = content.replace('import yangfentuozi.dsusideloaderplus.ui.components.SettingsItem', 'import yangfentuozi.dsusideloaderplus.ui.components.SettingsItem\nimport yangfentuozi.dsusideloaderplus.ui.components.ExpandableSettingsItem')

# Replace SettingsItem in LazyColumn
old_settings_item = """                            SettingsItem(
                                title = rom.name,
                                summary = rom.author,
                                onClick = if (viewModel.downloadJobs.containsKey(rom.url)) null else { { viewModel.startDownload(rom.url, rom.name) } },
                                columnTrailingContent = {
                                    val progress = viewModel.downloadProgress[rom.url]
                                    if (progress != null) {
                                        Column(modifier = Modifier.padding(top = 8.dp)) {
                                            LinearProgressIndicator(
                                                progress = { progress },
                                                modifier = Modifier.fillMaxWidth()
                                            )
                                            TextButton(
                                                onClick = { viewModel.cancelDownload(rom.url) },
                                                modifier = Modifier.align(androidx.compose.ui.Alignment.End)
                                            ) {
                                                Text(stringResource(id = R.string.cancel))
                                            }
                                        }
                                    } else if (viewModel.downloadErrors.containsKey(rom.url)) {
                                        Text(
                                            text = viewModel.downloadErrors[rom.url]!!,
                                            color = MaterialTheme.colorScheme.error,
                                            style = MaterialTheme.typography.bodySmall,
                                            modifier = Modifier.padding(top = 4.dp)
                                        )
                                    }
                                }
                            )"""

new_settings_item = """                            var expanded by remember { mutableStateOf(false) }
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
                                            CircularProgressIndicator(
                                                progress = { progress },
                                                modifier = Modifier.size(24.dp)
                                            )
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
                                                        Text("Скачать")
                                                    }
                                                }
                                            }
                                            if (isThisDownloading && progress != null) {
                                                LinearProgressIndicator(
                                                    progress = { progress },
                                                    modifier = Modifier.fillMaxWidth().padding(top = 4.dp)
                                                )
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
                            }"""

content = content.replace(old_settings_item, new_settings_item)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubScreen.kt', 'w') as f:
    f.write(content)

