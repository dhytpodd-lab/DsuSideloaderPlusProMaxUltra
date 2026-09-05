                    item {
                        DsuInfoCard(
                            onClickViewDocs = { uriHandler.openUri(HomeLinks.DSU_DOCS) },
                            onClickLearnMore = { uriHandler.openUri(HomeLinks.DSU_LEARN_MORE) },
                        )
                    }
                    item {
                        yangfentuozi.dsusideloaderplus.ui.components.SettingsItem(
                            title = "Quick Access to Logs",
                            summary = "View operations logs instantly",
                            onClick = { homeViewModel.showLogsWarning() },
                            icon = androidx.compose.material.icons.Icons.Outlined.Terminal
                        )
                    }
                    item {
                        yangfentuozi.dsusideloaderplus.ui.components.SettingsItem(
                            title = "Current Session Installs",
                            summary = "Installations requested this session: ${uiState.installationLogs.count { it.contains("Installing") }}",
                            onClick = null,
                            icon = androidx.compose.material.icons.Icons.Outlined.Info
                        )
                    }
