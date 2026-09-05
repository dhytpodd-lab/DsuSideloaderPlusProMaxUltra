with open("app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt", "r") as f:
    content = f.read()

old_line = 'val isRomPost = cleanText.contains("Ported", ignoreCase = true) || cleanText.contains("GSI", ignoreCase = true) || cleanText.contains("ROM", ignoreCase = true) || cleanText.contains("Treble", ignoreCase = true)'
new_line = 'val isRomPost = Regex("(?i)\\\\b(ported|port|gsi|rom|treble|erfs)\\\\b").containsMatchIn(cleanText) && lines.size > 1'

# Wait, `lines` is defined AFTER `isRomPost` in the current code! Let's re-arrange slightly.
old_block = """                                        val isRomPost = cleanText.contains("Ported", ignoreCase = true) || cleanText.contains("GSI", ignoreCase = true) || cleanText.contains("ROM", ignoreCase = true) || cleanText.contains("Treble", ignoreCase = true)
                                        if (isRomPost) {
                                            val lines = cleanText.split("\\n").map { it.trim() }.filter { it.isNotBlank() }
                                            val title = lines.firstOrNull()?.take(50) ?: "TG Update"
                                            val author = link.name + " " + (lines.drop(1).firstOrNull()?.take(30) ?: "")
                                            pageRoms.add(GsiRom(title, author.trim(), mirrorLinks, "arm64-v8a"))
                                        }"""

new_block = """                                        val lines = cleanText.split("\\n").map { it.trim() }.filter { it.isNotBlank() }
                                        val isRomPost = Regex("(?i)\\\\b(ported|port|gsi|rom|treble|erfs)\\\\b").containsMatchIn(cleanText)
                                        val isNotReview = !Regex("(?i)\\\\b(review|reviews|chat|group)\\\\b").containsMatchIn(cleanText)
                                        if (isRomPost && isNotReview && lines.size >= 2) {
                                            val title = lines.firstOrNull()?.take(50) ?: "TG Update"
                                            val author = link.name + " " + (lines.drop(1).firstOrNull()?.take(30) ?: "")
                                            pageRoms.add(GsiRom(title, author.trim(), mirrorLinks, "arm64-v8a"))
                                        }"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open("app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt", "w") as f:
        f.write(content)
    print("Patched successfully")
else:
    print("Block not found!")
