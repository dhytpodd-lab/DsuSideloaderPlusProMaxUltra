with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt', 'r') as f:
    content = f.read()

old_logic = """                            val mirrorLinks = mutableMapOf<String, String>()
                            extractedLinks.forEach { dlUrl ->
                                if (dlUrl.contains("sourceforge.net")) mirrorLinks["SourceForge"] = dlUrl
                                else if (dlUrl.contains("github.com")) mirrorLinks["GitHub"] = dlUrl
                                else if (dlUrl.contains("pixeldrain.com/u/")) mirrorLinks["Pixeldrain"] = dlUrl
                                else if (dlUrl.contains("pling.com")) mirrorLinks["Pling"] = dlUrl
                            }"""

new_logic = """                            val mirrorLinks = mutableMapOf<String, String>()
                            extractedLinks.forEach { dlUrl ->
                                if (dlUrl.contains("sourceforge.net")) mirrorLinks["SourceForge"] = dlUrl
                                else if (dlUrl.contains("github.com")) mirrorLinks["GitHub"] = dlUrl
                                else if (dlUrl.contains("pixeldrain.com/u/")) mirrorLinks["Pixeldrain"] = dlUrl
                                else if (dlUrl.contains("pling.com")) mirrorLinks["Pling"] = dlUrl
                                else if (dlUrl.contains("axisgsiru.dolbaeb.me")) mirrorLinks["AxisGSI"] = dlUrl
                            }"""

content = content.replace(old_logic, new_logic)

old_start_download = """                var connection = URL(currentUrl).openConnection() as HttpURLConnection
                connection.instanceFollowRedirects = true
                
                // Manually follow redirects to handle https -> http or vice versa
                var redirectCount = 0
                while (connection.responseCode / 100 == 3 && redirectCount < 5) {
                    val newUrl = connection.getHeaderField("Location")
                    if (newUrl == null) break
                    currentUrl = newUrl
                    connection = URL(currentUrl).openConnection() as HttpURLConnection
                    redirectCount++
                }

                if (connection.responseCode != HttpURLConnection.HTTP_OK) {
                    throw Exception("Server returned HTTP ${connection.responseCode}")
                }"""

new_start_download = """                var connection = URL(currentUrl).openConnection() as HttpURLConnection
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
                    throw Exception("HTTP ${connection.responseCode} ${connection.responseMessage}\\n$errorMsg")
                }"""

content = content.replace(old_start_download, new_start_download)

old_read = """                while (inputStream.read(data).also { count = it } != -1) {
                    total += count
                    outputStream.write(data, 0, count)
                    if (contentLength > 0) {
                        downloadProgress[url] = (total.toFloat() / contentLength.toFloat()).coerceIn(0f, 1f)
                    }
                }"""

new_read = """                var lastUpdate = System.currentTimeMillis()
                while (inputStream.read(data).also { count = it } != -1) {
                    total += count
                    outputStream.write(data, 0, count)
                    
                    val now = System.currentTimeMillis()
                    if (now - lastUpdate > 100) { // Throttle UI updates
                        if (contentLength > 0) {
                            downloadProgress[url] = (total.toFloat() / contentLength.toFloat()).coerceIn(0f, 1f)
                        } else {
                            // If contentLength is unknown, fake a slowly increasing progress up to 90%
                            // or just use 0f to indicate indeterminate. We use an indeterminate fake value:
                            val fakeProgress = (1f - (1f / (1f + (total.toFloat() / 50_000_000f)))).coerceIn(0f, 0.99f)
                            downloadProgress[url] = fakeProgress
                        }
                        lastUpdate = now
                    }
                }"""

content = content.replace(old_read, new_read)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt', 'w') as f:
    f.write(content)
