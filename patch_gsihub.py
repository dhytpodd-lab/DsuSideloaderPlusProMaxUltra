import re

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubScreen.kt', 'r') as f:
    content = f.read()

# Add hiltViewModel import
content = content.replace("import yangfentuozi.dsusideloaderplus.ui.screen.Destinations", "import yangfentuozi.dsusideloaderplus.ui.screen.Destinations\nimport androidx.hilt.navigation.compose.hiltViewModel\nimport androidx.compose.foundation.clickable")

# Change GsiHubScreen signature
content = content.replace("fun GsiHubScreen(navigate: (String) -> Unit) {", "fun GsiHubScreen(navigate: (String) -> Unit, viewModel: GsiHubViewModel = hiltViewModel()) {")

# Remove downloadUrl
content = re.sub(r'fun downloadUrl\(url: String, title: String\) \{.*?\n    \}', '', content, flags=re.DOTALL)

# Replace SettingsItem call for catalog
old_settings_item = """                            SettingsItem(
                                title = rom.name,
                                summary = rom.author,
                                onClick = { downloadUrl(rom.url, rom.name) }
                            )"""

new_settings_item = """                            SettingsItem(
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
content = content.replace(old_settings_item, new_settings_item)

# Change customLinks to be clickable and show progress
old_list_item = """                                ListItem(
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
                                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 4.dp),
                                    colors = ListItemDefaults.colors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
                                )"""
new_list_item = """                                Column(
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
                                }"""
content = content.replace(old_list_item, new_list_item)


with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubScreen.kt', 'w') as f:
    f.write(content)

