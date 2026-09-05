import re

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt', 'r') as f:
    content = f.read()

old_fetch = """                    try {
                        var channelUrl = link.url
                        if (!channelUrl.contains("t.me/s/")) {
                            channelUrl = channelUrl.replace("t.me/", "t.me/s/")
                        }
                        if (!channelUrl.startsWith("http")) {
                            channelUrl = "https://$channelUrl"
                        }
                        
                        val connection = URL(channelUrl).openConnection() as HttpURLConnection
                        connection.setRequestProperty("User-Agent", "Mozilla/5.0")
                        connection.connectTimeout = 10000
                        connection.readTimeout = 10000
                        
                        val html = connection.inputStream.bufferedReader().use { it.readText() }
                        
                        val msgRegex = Regex(\"\"\"<div class="tgme_widget_message_text[^>]*>(.*?)</div>\"\"\", RegexOption.DOT_MATCHES_ALL)
                        val linkRegex = Regex(\"\"\"<a[^>]+href="([^"]+)\"\"\"\")
                        
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
                            }
                            
                            if (mirrorLinks.isNotEmpty()) {
                                val cleanText = msgHtml.replace(Regex("(?i)<br[^>]*>"), "\\n").replace(Regex("<[^>]+>"), "").trim()
                                val lines = cleanText.split("\\n").map { it.trim() }.filter { it.isNotBlank() }
                                val title = lines.firstOrNull()?.take(50) ?: "TG Update"
                                val author = link.name + " " + (lines.drop(1).firstOrNull()?.take(30) ?: "")
                                roms.add(GsiRom(title, author.trim(), mirrorLinks, "arm64-v8a"))
                            }
                        }
                    } catch (e: Exception) {
                        e.printStackTrace()
                    }"""

new_fetch = """                    try {
                        var channelUrl: String? = link.url
                        if (!channelUrl!!.contains("t.me/s/")) {
                            channelUrl = channelUrl.replace("t.me/", "t.me/s/")
                        }
                        if (!channelUrl.startsWith("http")) {
                            channelUrl = "https://$channelUrl"
                        }
                        
                        val channelRoms = mutableListOf<GsiRom>()
                        var pagesFetched = 0
                        
                        while (channelUrl != null && pagesFetched < 10) {
                            try {
                                val connection = URL(channelUrl).openConnection() as HttpURLConnection
                                connection.setRequestProperty("User-Agent", "Mozilla/5.0")
                                connection.connectTimeout = 10000
                                connection.readTimeout = 10000
                                
                                val html = connection.inputStream.bufferedReader().use { it.readText() }
                                
                                val msgRegex = Regex(\"\"\"<div class="tgme_widget_message_text[^>]*>(.*?)</div>\"\"\", RegexOption.DOT_MATCHES_ALL)
                                val linkRegex = Regex(\"\"\"<a[^>]+href="([^"]+)\"\"\"\")
                                
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
                                    }
                                    
                                    if (mirrorLinks.isNotEmpty()) {
                                        val cleanText = msgHtml.replace(Regex("(?i)<br[^>]*>"), "\\n").replace(Regex("<[^>]+>"), "").trim()
                                        val lines = cleanText.split("\\n").map { it.trim() }.filter { it.isNotBlank() }
                                        val title = lines.firstOrNull()?.take(50) ?: "TG Update"
                                        val author = link.name + " " + (lines.drop(1).firstOrNull()?.take(30) ?: "")
                                        pageRoms.add(GsiRom(title, author.trim(), mirrorLinks, "arm64-v8a"))
                                    }
                                }
                                
                                channelRoms.addAll(pageRoms.reversed())
                                
                                val beforeRegex = Regex(\"\"\"<a[^>]+href="([^"]*\\?before=\\d+)"\"\"\")
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
                    }"""

content = content.replace(old_fetch, new_fetch)

# Also need to fix the reverse when adding to parsedTgRoms
old_add = "parsedTgRoms.addAll(roms.reversed())"
new_add = "parsedTgRoms.addAll(roms)"
content = content.replace(old_add, new_add)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt', 'w') as f:
    f.write(content)
