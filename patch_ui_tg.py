import re

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubScreen.kt', 'r') as f:
    content = f.read()

# Make sure we have the imports we need
if "import androidx.compose.material.icons.filled.Clear" not in content:
    content = content.replace("import androidx.compose.material.icons.Icons", "import androidx.compose.material.icons.Icons\nimport androidx.compose.material.icons.outlined.Clear")

old_tg_ui = """                if (selectedTab == 0) {
                    if (isParsingTg) {
                        Box(modifier = Modifier.fillMaxSize(), contentAlignment = androidx.compose.ui.Alignment.Center) {
                            CircularProgressIndicator()
                        }
                    } else {
                        LazyColumn(modifier = Modifier.fillMaxSize()) {
                            items(viewModel.parsedTgRoms) { rom ->
                                Card("""

new_tg_ui = """                if (selectedTab == 0) {
                    if (isParsingTg) {
                        Box(modifier = Modifier.fillMaxSize(), contentAlignment = androidx.compose.ui.Alignment.Center) {
                            CircularProgressIndicator()
                        }
                    } else {
                        var searchQuery by remember { mutableStateOf("") }
                        var currentPage by remember { mutableStateOf(1) }
                        
                        val filteredRoms = viewModel.parsedTgRoms.filter { 
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
                                items(paginatedRoms) { rom ->
                                Card("""

content = content.replace(old_tg_ui, new_tg_ui)

old_end_tg_ui = """                                }
                            }
                        }
                    }
                } else {"""

new_end_tg_ui = """                                }
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
                    }
                } else {"""

content = content.replace(old_end_tg_ui, new_end_tg_ui)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubScreen.kt', 'w') as f:
    f.write(content)
