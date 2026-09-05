package yangfentuozi.dsusideloaderplus.ui.screen.settings

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.NewReleases
import androidx.compose.material.icons.outlined.WarningAmber
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.hilt.lifecycle.viewmodel.compose.hiltViewModel
import yangfentuozi.dsusideloaderplus.R
import yangfentuozi.dsusideloaderplus.preferences.AppPrefs
import yangfentuozi.dsusideloaderplus.ui.components.ApplicationScreen
import yangfentuozi.dsusideloaderplus.ui.components.DialogLikeBottomSheet
import yangfentuozi.dsusideloaderplus.ui.components.M3ESwitchWidget
import yangfentuozi.dsusideloaderplus.ui.components.SettingsItem
import yangfentuozi.dsusideloaderplus.ui.components.SplicedColumnGroup
import yangfentuozi.dsusideloaderplus.ui.components.TopBar
import yangfentuozi.dsusideloaderplus.ui.screen.Destinations
import yangfentuozi.dsusideloaderplus.util.OperationMode
import yangfentuozi.dsusideloaderplus.util.collectAsStateWithLifecycle
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.appcompat.app.AppCompatDelegate
import androidx.core.os.LocaleListCompat
import androidx.compose.material3.FilterChip
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun Settings(
    navigate: (String) -> Unit,
    settingsViewModel: SettingsViewModel = hiltViewModel(),
) {
    val uiState by settingsViewModel.uiState.collectAsStateWithLifecycle()

    LaunchedEffect(Unit) {
        settingsViewModel.checkDevOpt()
    }

    ApplicationScreen(
        modifier = Modifier.padding(horizontal = 16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
        topBar = {
            TopBar(
                barTitle = stringResource(id = R.string.settings),
                scrollBehavior = it,
                onClickBackButton = { navigate(Destinations.Up) },
            )
        },
    ) {
        SplicedColumnGroup(title = stringResource(id = R.string.installation)) {
            item {
                M3ESwitchWidget(
                    title = stringResource(id = R.string.builtin_installer),
                    summary =
                        if (settingsViewModel.isAndroidQ()) {
                            stringResource(id = R.string.unsupported)
                        } else if (uiState.isRoot) {
                            stringResource(id = R.string.builtin_installer_description)
                        } else {
                            stringResource(R.string.requires_root)
                        },
                    enabled = uiState.isRoot && !settingsViewModel.isAndroidQ(),
                    checked = uiState.preferences[AppPrefs.USE_BUILTIN_INSTALLER]!!,
                    onCheckedChange = {
                        if (it) {
                            settingsViewModel.updateSheetDisplay(DialogSheetState.BUILT_IN_INSTALLER)
                        }
                        settingsViewModel.togglePreference(AppPrefs.USE_BUILTIN_INSTALLER, it)
                    },
                )
            }
            item {
                M3ESwitchWidget(
                    title = stringResource(id = R.string.unmount_sd_title),
                    summary = stringResource(id = R.string.unmount_sd_description),
                    checked = uiState.preferences[AppPrefs.UMOUNT_SD]!!,
                    onCheckedChange = {
                        settingsViewModel.togglePreference(
                            AppPrefs.UMOUNT_SD,
                            it
                        )
                    },
                )
            }
            item {
                M3ESwitchWidget(
                    title = stringResource(id = R.string.keep_screen_on),
                    checked = uiState.preferences[AppPrefs.KEEP_SCREEN_ON]!!,
                    onCheckedChange = {
                        settingsViewModel.togglePreference(
                            AppPrefs.KEEP_SCREEN_ON,
                            it
                        )
                    },
                )
            }
        }

        if (uiState.isDevOptEnabled) {
            SplicedColumnGroup(title = stringResource(id = R.string.developer_options)) {
                item {
                    M3ESwitchWidget(
                        title = stringResource(id = R.string.storage_check_title),
                        summary = stringResource(id = R.string.storage_check_description),
                        checked = uiState.preferences[AppPrefs.DISABLE_STORAGE_CHECK]!!,
                        onCheckedChange = {
                            if (it) {
                                settingsViewModel.updateSheetDisplay(DialogSheetState.DISABLE_STORAGE_CHECK)
                            }
                            settingsViewModel.togglePreference(AppPrefs.DISABLE_STORAGE_CHECK, it)
                        },
                    )
                }
                item(visible = settingsViewModel.getOperationMode() != OperationMode.ADB) {
                    M3ESwitchWidget(
                        title = stringResource(id = R.string.full_logcat_logging_title),
                        summary = stringResource(id = R.string.full_logcat_logging_description),
                        checked = uiState.preferences[AppPrefs.FULL_LOGCAT_LOGGING]!!,
                        onCheckedChange = {
                            settingsViewModel.togglePreference(
                                AppPrefs.FULL_LOGCAT_LOGGING,
                                it
                            )
                        },
                    )
                }
            }
        }

        SplicedColumnGroup(title = stringResource(id = R.string.customization_title)) {
            item {
                val context = LocalContext.current
                val prefs = context.getSharedPreferences("dsu_prefs", android.content.Context.MODE_PRIVATE)
                val accentColor = androidx.compose.runtime.remember {
                    androidx.compose.runtime.mutableStateOf(prefs.getLong("accent_color", 0xFF00E5FF))
                }
                val useMonet = androidx.compose.runtime.remember {
                    androidx.compose.runtime.mutableStateOf(prefs.getBoolean("use_monet", false))
                }
                
                Column(modifier = Modifier.fillMaxWidth().padding(horizontal = 36.dp, vertical = 16.dp)) {
                    Text(stringResource(id = R.string.theme_accent_title), style = MaterialTheme.typography.bodyLarge)
                    Text(stringResource(id = R.string.theme_accent_desc), style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(Modifier.height(16.dp))
                    Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.S) {
                            Box(
                                modifier = Modifier
                                    .size(40.dp)
                                    .background(
                                        androidx.compose.ui.graphics.Brush.sweepGradient(
                                            listOf(Color.Red, Color.Yellow, Color.Green, Color.Cyan, Color.Blue, Color.Magenta, Color.Red)
                                        ),
                                        CircleShape
                                    )
                                    .border(
                                        width = if (useMonet.value) 3.dp else 0.dp,
                                        color = if (useMonet.value) Color.White else Color.Transparent,
                                        shape = CircleShape
                                    )
                                    .clickable {
                                        prefs.edit().putBoolean("use_monet", true).apply()
                                        useMonet.value = true
                                    }
                            )
                        }

                        val colors = listOf(0xFF00E5FF, 0xFFFF2A55, 0xFF00FF66, 0xFFFFAA00, 0xFFB388FF)
                        colors.forEach { colorVal ->
                            Box(
                                modifier = Modifier
                                    .size(40.dp)
                                    .background(
                                        Color(colorVal), 
                                        CircleShape
                                    )
                                    .border(
                                        width = if (!useMonet.value && accentColor.value == colorVal) 3.dp else 0.dp,
                                        color = if (!useMonet.value && accentColor.value == colorVal) Color.White else Color.Transparent,
                                        shape = CircleShape
                                    )
                                    .clickable {
                                        prefs.edit()
                                            .putLong("accent_color", colorVal)
                                            .putBoolean("use_monet", false)
                                            .apply()
                                        accentColor.value = colorVal
                                        useMonet.value = false
                                    }
                            )
                        }
                    }
                }
            }
            item {
                val currentLocales = AppCompatDelegate.getApplicationLocales()
                val currentLang = if (currentLocales.isEmpty) "System" else currentLocales.get(0)?.language ?: "System"
                
                val languages = listOf("System", "en", "ru")
                val languageNames = listOf(stringResource(id = R.string.lang_sys), stringResource(id = R.string.lang_en), stringResource(id = R.string.lang_ru))
                
                Column(modifier = Modifier.fillMaxWidth().padding(horizontal = 36.dp, vertical = 16.dp)) {
                    Text(stringResource(id = R.string.language_title), style = MaterialTheme.typography.bodyLarge)
                    Text(stringResource(id = R.string.language_current, languageNames[languages.indexOf(currentLang).takeIf { it >= 0 } ?: 0]), style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(Modifier.height(8.dp))
                    
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        languages.forEachIndexed { index, langCode ->
                            FilterChip(
                                selected = currentLang == langCode,
                                onClick = {
                                    if (langCode == "System") {
                                        AppCompatDelegate.setApplicationLocales(LocaleListCompat.getEmptyLocaleList())
                                    } else {
                                        AppCompatDelegate.setApplicationLocales(LocaleListCompat.forLanguageTags(langCode))
                                    }
                                },
                                label = { Text(languageNames[index]) }
                            )
                        }
                    }
                }
            }
        }

        SplicedColumnGroup(title = stringResource(id = R.string.other)) {
            item {
                val context = LocalContext.current
                val prefs = context.getSharedPreferences("dsu_prefs", android.content.Context.MODE_PRIVATE)
                val defaultNotSelected = stringResource(id = R.string.not_selected)
                val backupPath = androidx.compose.runtime.remember { 
                    androidx.compose.runtime.mutableStateOf(prefs.getString("backup_dir_uri", defaultNotSelected) ?: defaultNotSelected) 
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
                        backupPath.value = uri.toString()
                    }
                }
                SettingsItem(
                    title = stringResource(id = R.string.backup_dir_title),
                    summary = stringResource(id = R.string.backup_dir_desc, backupPath.value),
                    onClick = { dirPicker.launch(null) },
                )
            }
            item {
                SettingsItem(
                    title = stringResource(id = R.string.operation_mode),
                    summary = settingsViewModel.checkOperationMode(),
                    onClick = null
                )
            }
            item {
                SettingsItem(
                    title = stringResource(id = R.string.about),
                    summary = stringResource(id = R.string.about_description),
                    onClick = { navigate(Destinations.About) },
                )
            }
        }
    }

    when (uiState.dialogSheetDisplay) {
        DialogSheetState.BUILT_IN_INSTALLER ->
            DialogLikeBottomSheet(
                title = stringResource(id = R.string.experimental_feature),
                icon = Icons.Outlined.NewReleases,
                text = stringResource(id = R.string.experimental_feature_description),
                confirmText = stringResource(id = R.string.yes),
                cancelText = stringResource(id = R.string.cancel),
                onClickCancel = {
                    settingsViewModel.togglePreference(AppPrefs.USE_BUILTIN_INSTALLER, false)
                    settingsViewModel.updateSheetDisplay(DialogSheetState.NONE)
                },
                onClickConfirm = { settingsViewModel.updateSheetDisplay(DialogSheetState.NONE) },
            )
        DialogSheetState.DISABLE_STORAGE_CHECK ->
            DialogLikeBottomSheet(
                title = stringResource(id = R.string.warning_storage_check_title),
                icon = Icons.Outlined.WarningAmber,
                text = stringResource(id = R.string.warning_storage_check_description),
                confirmText = stringResource(id = R.string.continue_anyway),
                cancelText = stringResource(id = R.string.cancel),
                onClickCancel = {
                    settingsViewModel.togglePreference(AppPrefs.DISABLE_STORAGE_CHECK, false)
                    settingsViewModel.updateSheetDisplay(DialogSheetState.NONE)
                },
                onClickConfirm = { settingsViewModel.updateSheetDisplay(DialogSheetState.NONE) },
            )
        else -> {}
    }
}
