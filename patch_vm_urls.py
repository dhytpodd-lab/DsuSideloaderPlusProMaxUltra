with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt', 'r') as f:
    content = f.read()

old_logic = """                            val downloadLink = extractedLinks.firstOrNull { 
                                it.contains("sourceforge.net") || 
                                it.contains("github.com") || 
                                it.contains("pixeldrain.com/u/") ||
                                it.contains("pling.com")
                            }
                            
                            if (downloadLink != null) {
                                val cleanText = msgHtml.replace(Regex("(?i)<br[^>]*>"), "\\n").replace(Regex("<[^>]+>"), "").trim()
                                val lines = cleanText.split("\\n").map { it.trim() }.filter { it.isNotBlank() }
                                val title = lines.firstOrNull()?.take(50) ?: "TG Update"
                                val author = link.name + " " + (lines.drop(1).firstOrNull()?.take(30) ?: "")
                                roms.add(GsiRom(title, author.trim(), downloadLink, "arm64-v8a"))
                            }"""

new_logic = """                            val mirrorLinks = mutableMapOf<String, String>()
                            extractedLinks.forEach { dlUrl ->
                                if (dlUrl.contains("sourceforge.net")) mirrorLinks["SourceForge"] = dlUrl
                                else if (dlUrl.contains("github.com")) mirrorLinks["GitHub"] = dlUrl
                                else if (dlUrl.contains("pixeldrain.com/u/")) mirrorLinks["Pixeldrain"] = dlUrl
                                else if (dlUrl.contains("pling.com")) mirrorLinks["Pling"] = dlUrl
                            }
                            
                            if (mirrorLinks.isNotEmpty()) {
                                val cleanText = msgHtml.replace(Regex("(?i)<br[^>]*>"), "\\n").replace(Regex("<[^>]+>"), "").trim()
                                val lines = cleanText.split("\\n").map { it.trim() }.filter { it.isNotBlank() }
                                val title = lines.firstOrNull()?.take(50) ?: "TG Update"
                                val author = link.name + " " + (lines.drop(1).firstOrNull()?.take(30) ?: "")
                                roms.add(GsiRom(title, author.trim(), mirrorLinks, "arm64-v8a"))
                            }"""

content = content.replace(old_logic, new_logic)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt', 'w') as f:
    f.write(content)
