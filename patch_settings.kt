        SplicedColumnGroup(title = stringResource(id = R.string.other)) {
            item {
                val context = androidx.compose.ui.platform.LocalContext.current
                val prefs = context.getSharedPreferences("dsu_prefs", android.content.Context.MODE_PRIVATE)
                var backupPath by androidx.compose.runtime.remember { 
                    androidx.compose.runtime.mutableStateOf(prefs.getString("backup_dir_uri", "Not selected")) 
                }
                val dirPicker = androidx.activity.compose.rememberLauncherForActivityResult(
                    contract = androidx.activity.result.contract.ActivityResultContracts.OpenDocumentTree()
                ) { uri ->
                    if (uri != null) {
                        context.contentResolver.takePersistableUriPermission(
                            uri, 
                            android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION or android.content.Intent.FLAG_GRANT_WRITE_URI_PERMISSION
                        )
                        prefs.edit().putString("backup_dir_uri", uri.toString()).apply()
                        backupPath = uri.toString()
                    }
                }
                SettingsItem(
                    title = "Backup Directory",
                    summary = "Save backups to: $backupPath",
                    onClick = { dirPicker.launch(null) },
                )
            }
