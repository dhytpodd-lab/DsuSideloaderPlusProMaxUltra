package yangfentuozi.dsusideloaderplus.ui.screen.gsihub

import android.content.Context
import android.net.Uri
import android.os.Environment
import android.util.Log
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlinx.coroutines.isActive
import yangfentuozi.dsusideloaderplus.core.StorageManager
import yangfentuozi.dsusideloaderplus.model.Session
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.asSharedFlow
import java.io.BufferedInputStream
import java.io.FileOutputStream
import java.net.HttpURLConnection
import java.net.URL
import javax.inject.Inject
import java.io.File

@HiltViewModel
class GsiHubViewModel @Inject constructor(
    @ApplicationContext private val context: Context,
    private val storageManager: StorageManager,
    private val session: Session
) : ViewModel() {
    private val _navigateToHome = MutableSharedFlow<Unit>(extraBufferCapacity = 1)
    val navigateToHome = _navigateToHome.asSharedFlow()


    val downloadProgress = mutableStateMapOf<String, Float>()
    val downloadJobs = mutableStateMapOf<String, Job>()
    val downloadErrors = mutableStateMapOf<String, String>()

    val parsedTgRoms = mutableStateListOf<GsiRom>()
    var isParsingTg = mutableStateOf(false)

    fun fetchTelegramChannels(links: List<CustomLink>) {
        if (isParsingTg.value) return
        
        viewModelScope.launch(Dispatchers.IO) {
            isParsingTg.value = true
            parsedTgRoms.clear()
            
            val roms = mutableListOf<GsiRom>()
            
            links.forEach { link ->
                if (link.url.contains("t.me/")) {
                    try {
                        var channelUrl: String? = link.url
                        if (!channelUrl!!.contains("t.me/s/")) {
                            channelUrl = channelUrl.replace("t.me/", "t.me/s/")
                        }
                        if (!channelUrl.startsWith("http")) {
                            channelUrl = "https://$channelUrl"
                        }
                        
                        val channelRoms = mutableListOf<GsiRom>()
                        var pagesFetched = 0
                        
                        while (channelUrl != null && pagesFetched < 50) {
                            try {
                                val connection = URL(channelUrl).openConnection() as HttpURLConnection
                                connection.setRequestProperty("User-Agent", "Mozilla/5.0")
                                connection.connectTimeout = 10000
                                connection.readTimeout = 10000
                                
                                val html = connection.inputStream.bufferedReader().use { it.readText() }
                                
                                val msgRegex = Regex("""<div class="tgme_widget_message_text[^>]*>(.*?)</div>""", RegexOption.DOT_MATCHES_ALL)
                                val linkRegex = Regex("""<a[^>]+href="([^"]+)"""")
                                
                                val pageRoms = mutableListOf<GsiRom>()
                                
                                msgRegex.findAll(html).forEach { match ->
                                    val msgHtml = match.groupValues[1]
                                    val extractedLinks = linkRegex.findAll(msgHtml).map { it.groupValues[1] }.toList()
                                    val mirrorLinks = mutableMapOf<String, String>()
                                    extractedLinks.forEach { dlUrl ->
                                        if (dlUrl.contains("sourceforge.net")) mirrorLinks["SourceForge"] = dlUrl
                                        else if (dlUrl.contains("github.com")) mirrorLinks["GitHub"] = dlUrl
                                        else if (dlUrl.contains("pixeldrain.com/u/")) mirrorLinks["Pixeldrain"] = dlUrl
                                        else if (dlUrl.contains("pling.com")) mirrorLinks["Pling"] = dlUrl
                                        else if (dlUrl.contains("axisgsiru.dolbaeb.me")) mirrorLinks["AxisCloud"] = dlUrl
                                        else if (dlUrl.contains("drive.google.com")) mirrorLinks["Google Drive"] = dlUrl
                                        else if (dlUrl.contains("mega.nz")) mirrorLinks["MEGA"] = dlUrl
                                        else if (dlUrl.contains("mediafire.com")) mirrorLinks["MediaFire"] = dlUrl
                                        else if (dlUrl.contains("t.me/")) mirrorLinks["Telegram"] = dlUrl
                                        else if (dlUrl.contains("yadi.sk") || dlUrl.contains("disk.yandex")) mirrorLinks["Yandex Disk"] = dlUrl
                                        else if (dlUrl.contains("androidfilehost.com")) mirrorLinks["AndroidFileHost"] = dlUrl
                                        else if (dlUrl.contains("terabox.com")) mirrorLinks["TeraBox"] = dlUrl
                                    }
                                    
                                    if (mirrorLinks.isNotEmpty()) {
                                        val cleanText = msgHtml.replace(Regex("(?i)<br[^>]*>"), "\n").replace(Regex("<[^>]+>"), "").trim()
                                        val lines = cleanText.split("\n").map { it.trim() }.filter { it.isNotBlank() }
                                        val isRomPost = Regex("(?i)\\b(ported|port|gsi|rom|treble|erfs)\\b").containsMatchIn(cleanText)
                                        val isNotReview = !Regex("(?i)\\b(review|reviews|chat|group)\\b").containsMatchIn(cleanText)
                                        if (isRomPost && isNotReview && lines.size >= 2) {
                                            val title = lines.firstOrNull()?.take(50) ?: "TG Update"
                                            val author = link.name + " " + (lines.drop(1).firstOrNull()?.take(30) ?: "")
                                            pageRoms.add(GsiRom(title, author.trim(), mirrorLinks, "arm64-v8a"))
                                        }
                                    }
                                }
                                
                                channelRoms.addAll(pageRoms.reversed())
                                
                                val beforeRegex = Regex("""<a[^>]+href="([^"]*\?before=\d+)"""")
                                val beforeMatch = beforeRegex.find(html)
                                if (beforeMatch != null) {
                                    val beforeUrl = beforeMatch.groupValues[1].replace("&amp;", "&")
                                    channelUrl = "https://t.me" + beforeUrl
                                    pagesFetched++
                                } else {
                                    channelUrl = null
                                }
                            } catch (e: Exception) {
                                e.printStackTrace()
                                channelUrl = null
                            }
                        }
                        roms.addAll(channelRoms)
                    } catch (e: Exception) {
                        e.printStackTrace()
                    }
                }
            }
            
            withContext(Dispatchers.Main) {
                parsedTgRoms.addAll(roms)
                isParsingTg.value = false
            }
        }
    }


    fun startDownload(url: String, title: String) {
        if (url.contains("sourceforge.net") || url.contains("drive.google.com")) {
            val intent = android.content.Intent(android.content.Intent.ACTION_VIEW, Uri.parse(url))
            intent.flags = android.content.Intent.FLAG_ACTIVITY_NEW_TASK
            context.startActivity(intent)
            return
        }
        if (downloadJobs.containsKey(url)) return
        
        downloadErrors.remove(url)
        val job = viewModelScope.launch(Dispatchers.IO) {
            downloadProgress[url] = 0f
            try {
                var currentUrl = url
                if (currentUrl.contains("pixeldrain.com/u/")) {
                    currentUrl = currentUrl.replace("pixeldrain.com/u/", "pixeldrain.com/api/file/")
                }
                
                var connection = URL(currentUrl).openConnection() as HttpURLConnection
                connection.setRequestProperty("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
                connection.setRequestProperty("Accept", "*/*")
                connection.instanceFollowRedirects = true
                connection.connectTimeout = 15000
                connection.readTimeout = 15000
                
                var redirectCount = 0
                while (connection.responseCode / 100 == 3 && redirectCount < 10) {
                    var newUrl = connection.getHeaderField("Location")
                    if (newUrl == null) break
                    if (newUrl.startsWith("/")) {
                        val urlObj = URL(currentUrl)
                        newUrl = "${urlObj.protocol}://${urlObj.host}$newUrl"
                    }
                    currentUrl = newUrl.replace(" ", "%20")
                    connection = URL(currentUrl).openConnection() as HttpURLConnection
                    connection.setRequestProperty("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
                    connection.setRequestProperty("Accept", "*/*")
                    connection.instanceFollowRedirects = true
                    connection.connectTimeout = 15000
                    connection.readTimeout = 15000
                    redirectCount++
                }

                if (connection.responseCode != HttpURLConnection.HTTP_OK) {
                    val errorMsg = connection.errorStream?.bufferedReader()?.use { it.readText() } ?: ""
                    throw Exception("HTTP ${connection.responseCode} ${connection.responseMessage}\n$errorMsg")
                }

                val contentLength = connection.contentLength
                val inputStream = BufferedInputStream(connection.inputStream)
                
                var disposition = connection.getHeaderField("Content-Disposition")
                var filename = ""
                if (disposition != null) {
                    val index = disposition.indexOf("filename=")
                    if (index >= 0) {
                        filename = disposition.substring(index + 9).replace("\"", "").replace("'", "")
                        val semicolon = filename.indexOf(";")
                        if (semicolon > 0) filename = filename.substring(0, semicolon)
                    }
                }
                if (filename.isEmpty()) {
                    val path = URL(currentUrl).path
                    filename = path.substring(path.lastIndexOf('/') + 1)
                }
                if (filename.isEmpty() || !filename.contains(".")) {
                    var extension = ".img.xz"
                    if (currentUrl.endsWith(".gz")) extension = ".img.gz"
                    if (currentUrl.endsWith(".zip")) extension = ".zip"
                    if (currentUrl.endsWith(".7z")) extension = ".7z"
                    if (currentUrl.endsWith(".img")) extension = ".img"
                    filename = "${title.replace(" ", "_")}$extension"
                }
                filename = filename.replace("/", "_").replace("\\", "_")
                val documentFile = storageManager.createDownloadFile(filename)
                val outputStream = storageManager.openOutputStream(documentFile.uri)

                val data = ByteArray(8192)
                var total = 0L
                var count: Int = 0
                
                var lastUpdate = System.currentTimeMillis()
                while (isActive && inputStream.read(data).also { count = it } != -1) {
                    total += count
                    outputStream.write(data, 0, count)
                    
                    val now = System.currentTimeMillis()
                    if (now - lastUpdate > 100) { // Throttle UI updates
                        if (contentLength > 0) {
                            downloadProgress[url] = (total.toFloat() / contentLength.toFloat()).coerceIn(0f, 1f)
                        } else {
                            // If contentLength is unknown, use -1f to indicate indeterminate state
                            downloadProgress[url] = -1f
                        }
                        lastUpdate = now
                    }
                }
                
                outputStream.flush()
                outputStream.close()
                inputStream.close()
                
                if (!isActive) {
                    try { documentFile.delete() } catch (e: Exception) {}
                } else {
                    downloadProgress.remove(url)
                    session.autoInstallUri = documentFile.uri
                    _navigateToHome.tryEmit(Unit)
                }
            } catch (e: Exception) {
                e.printStackTrace()
                downloadErrors[url] = e.localizedMessage ?: "Unknown error"
                downloadProgress.remove(url)
            } finally {
                downloadJobs.remove(url)
            }
        }
        downloadJobs[url] = job
    }

    fun cancelDownload(url: String) {
        downloadJobs[url]?.cancel()
        downloadJobs.remove(url)
        downloadProgress.remove(url)
        downloadErrors.remove(url)
    }
}
