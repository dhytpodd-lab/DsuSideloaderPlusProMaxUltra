package yangfentuozi.dsusideloaderplus.ui.theme

import android.app.Activity
import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.*
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat
import androidx.compose.ui.graphics.Color

@Composable
fun rememberThemeConfig(): Pair<Long, Boolean> {
    val context = LocalContext.current
    val prefs = context.getSharedPreferences("dsu_prefs", android.content.Context.MODE_PRIVATE)
    val color = remember { mutableStateOf(prefs.getLong("accent_color", 0xFF00E5FF)) }
    val monet = remember { mutableStateOf(prefs.getBoolean("use_monet", false)) }
    
    DisposableEffect(prefs) {
        val listener = android.content.SharedPreferences.OnSharedPreferenceChangeListener { sharedPreferences, key ->
            if (key == "accent_color") {
                color.value = sharedPreferences.getLong(key, 0xFF00E5FF)
            } else if (key == "use_monet") {
                monet.value = sharedPreferences.getBoolean(key, false)
            }
        }
        prefs.registerOnSharedPreferenceChangeListener(listener)
        onDispose { prefs.unregisterOnSharedPreferenceChangeListener(listener) }
    }
    return Pair(color.value, monet.value)
}

@Composable
fun DSUHelperTheme(
    darkTheme: Boolean = true,
    dynamicColor: Boolean = false,
    content: @Composable () -> Unit,
) {
    val (accentColorLong, useMonet) = rememberThemeConfig()
    val context = LocalContext.current
    
    val colorScheme = if (useMonet && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
        dynamicDarkColorScheme(context)
    } else {
        val primaryColor = Color(accentColorLong)
        
        val colors = when (accentColorLong) {
            0xFFFF2A55 -> listOf(Color(0xFF14080B), Color(0xFF1F1115), Color(0xFF2C1920), Color(0xFF29161B))
            0xFF00FF66 -> listOf(Color(0xFF08140B), Color(0xFF111F15), Color(0xFF192C20), Color(0xFF16291C))
            0xFFFFAA00 -> listOf(Color(0xFF141008), Color(0xFF1F1911), Color(0xFF2C2419), Color(0xFF292116))
            0xFFB388FF -> listOf(Color(0xFF0E0814), Color(0xFF16111F), Color(0xFF22192C), Color(0xFF1E1629))
            else -> listOf(Color(0xFF081014), Color(0xFF11191F), Color(0xFF19242C), Color(0xFF162129))
        }

        darkColorScheme(
            primary = primaryColor,
            secondary = primaryColor.copy(alpha = 0.8f),
            tertiary = primaryColor,
            background = colors[0],
            surface = colors[1],
            surfaceVariant = colors[2],
            surfaceBright = colors[3],
            surfaceContainer = colors[1],
            surfaceContainerHigh = colors[2],
            onPrimary = Color(0xFF050505),
            onSecondary = Color(0xFF050505),
            onBackground = Color(0xFFE0F7FA),
            onSurface = Color(0xFFE0F7FA),
            onSurfaceVariant = Color(0xFFB0BEC5)
        )
    }

    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val window = (view.context as? Activity)?.window ?: return@SideEffect
            WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = false
            WindowCompat.getInsetsController(window, view).isAppearanceLightNavigationBars = false
        }
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = AppTypography,
        content = content,
    )
}
