with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt', 'r') as f:
    content = f.read()

content = content.replace("import kotlinx.coroutines.withContext", "import kotlinx.coroutines.withContext\nimport kotlinx.coroutines.isActive")

old_loop = """                var lastUpdate = System.currentTimeMillis()
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
                }
                
                outputStream.flush()
                outputStream.close()
                inputStream.close()
                
                downloadProgress.remove(url)"""

new_loop = """                var lastUpdate = System.currentTimeMillis()
                while (isActive && inputStream.read(data).also { count = it } != -1) {
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
                }
                
                outputStream.flush()
                outputStream.close()
                inputStream.close()
                
                if (!isActive) {
                    try { documentFile.delete() } catch (e: Exception) {}
                } else {
                    downloadProgress.remove(url)
                }"""

content = content.replace(old_loop, new_loop)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt', 'w') as f:
    f.write(content)
