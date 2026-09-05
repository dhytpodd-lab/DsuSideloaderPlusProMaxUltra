with open("app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt", "r") as f:
    content = f.read()

old_block = """                                    if (mirrorLinks.isNotEmpty()) {
                                        val cleanText = msgHtml.replace(Regex("(?i)<br[^>]*>"), "\\n").replace(Regex("<[^>]+>"), "").trim()
                                        val lines = cleanText.split("\\n").map { it.trim() }.filter { it.isNotBlank() }
                                        val title = lines.firstOrNull()?.take(50) ?: "TG Update"
                                        val author = link.name + " " + (lines.drop(1).firstOrNull()?.take(30) ?: "")
                                        pageRoms.add(GsiRom(title, author.trim(), mirrorLinks, "arm64-v8a"))
                                    }"""

new_block = """                                    if (mirrorLinks.isNotEmpty()) {
                                        val cleanText = msgHtml.replace(Regex("(?i)<br[^>]*>"), "\\n").replace(Regex("<[^>]+>"), "").trim()
                                        val isRomPost = cleanText.contains("Ported", ignoreCase = true) || cleanText.contains("GSI", ignoreCase = true) || cleanText.contains("ROM", ignoreCase = true) || cleanText.contains("Treble", ignoreCase = true)
                                        if (isRomPost) {
                                            val lines = cleanText.split("\\n").map { it.trim() }.filter { it.isNotBlank() }
                                            val title = lines.firstOrNull()?.take(50) ?: "TG Update"
                                            val author = link.name + " " + (lines.drop(1).firstOrNull()?.take(30) ?: "")
                                            pageRoms.add(GsiRom(title, author.trim(), mirrorLinks, "arm64-v8a"))
                                        }
                                    }"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open("app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt", "w") as f:
        f.write(content)
    print("Patched successfully")
else:
    print("Block not found!")
