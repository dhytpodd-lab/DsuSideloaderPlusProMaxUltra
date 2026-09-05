sed -i '1i\
import androidx.compose.material3.SnackbarHost\
import androidx.compose.material3.SnackbarHostState\
import androidx.compose.material3.SnackbarResult\
import androidx.compose.material3.SnackbarDuration\
import androidx.compose.runtime.rememberCoroutineScope\
import kotlinx.coroutines.launch\
import yangfentuozi.dsusideloaderplus.ui.screen.about.AboutViewModel\
import yangfentuozi.dsusideloaderplus.ui.screen.about.UpdateStatus' app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/home/HomeScreen.kt
