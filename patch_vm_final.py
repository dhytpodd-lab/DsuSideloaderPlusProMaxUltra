import re

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt', 'r') as f:
    content = f.read()

# 1. Rename AxisGSI to AxisCloud
content = content.replace('mirrorLinks["AxisGSI"] = dlUrl', 'mirrorLinks["AxisCloud"] = dlUrl')

# 2. Fix the filename extraction from headers for Pixeldrain
old_filename_logic = '''                var extension = ".img.xz"
                if (currentUrl.endsWith(".gz")) extension = ".img.gz"
                if (currentUrl.endsWith(".zip")) extension = ".zip"
                if (currentUrl.endsWith(".7z")) extension = ".7z"
                
                val filename = "${title.replace(" ", "_")}$extension"'''

new_filename_logic = '''                var disposition = connection.getHeaderField("Content-Disposition")
                var filename = ""
                if (disposition != null) {
                    val index = disposition.indexOf("filename=")
                    if (index >= 0) {
                        filename = disposition.substring(index + 9).replace("\\"", "").replace("'", "")
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
                filename = filename.replace("/", "_").replace("\\\\", "_")'''

content = content.replace(old_filename_logic, new_filename_logic)

# 3. Fix the progress bar logic
old_progress = '''                        if (contentLength > 0) {
                            downloadProgress[url] = (total.toFloat() / contentLength.toFloat()).coerceIn(0f, 1f)
                        } else {
                            // If contentLength is unknown, fake a slowly increasing progress up to 90%
                            // or just use 0f to indicate indeterminate. We use an indeterminate fake value:
                            val fakeProgress = (1f - (1f / (1f + (total.toFloat() / 50_000_000f)))).coerceIn(0f, 0.99f)
                            downloadProgress[url] = fakeProgress
                        }'''

new_progress = '''                        if (contentLength > 0) {
                            downloadProgress[url] = (total.toFloat() / contentLength.toFloat()).coerceIn(0f, 1f)
                        } else {
                            // If contentLength is unknown, use -1f to indicate indeterminate state
                            downloadProgress[url] = -1f
                        }'''
content = content.replace(old_progress, new_progress)

# 4. Handle SourceForge specifically
old_start_download = '''    fun startDownload(url: String, title: String) {'''
new_start_download = '''    fun startDownload(url: String, title: String) {
        if (url.contains("sourceforge.net")) {
            val intent = android.content.Intent(android.content.Intent.ACTION_VIEW, Uri.parse(url))
            intent.flags = android.content.Intent.FLAG_ACTIVITY_NEW_TASK
            context.startActivity(intent)
            return
        }'''
content = content.replace(old_start_download, new_start_download)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt', 'w') as f:
    f.write(content)
