import re

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt', 'r') as f:
    content = f.read()

# 1. Add Google Drive to mirror links
old_mirror = """                            val mirrorLinks = mutableMapOf<String, String>()
                            extractedLinks.forEach { dlUrl ->
                                if (dlUrl.contains("sourceforge.net")) mirrorLinks["SourceForge"] = dlUrl
                                else if (dlUrl.contains("github.com")) mirrorLinks["GitHub"] = dlUrl
                                else if (dlUrl.contains("pixeldrain.com/u/")) mirrorLinks["Pixeldrain"] = dlUrl
                                else if (dlUrl.contains("pling.com")) mirrorLinks["Pling"] = dlUrl
                                else if (dlUrl.contains("axisgsiru.dolbaeb.me")) mirrorLinks["AxisCloud"] = dlUrl
                            }"""

new_mirror = """                            val mirrorLinks = mutableMapOf<String, String>()
                            extractedLinks.forEach { dlUrl ->
                                if (dlUrl.contains("sourceforge.net")) mirrorLinks["SourceForge"] = dlUrl
                                else if (dlUrl.contains("github.com")) mirrorLinks["GitHub"] = dlUrl
                                else if (dlUrl.contains("pixeldrain.com/u/")) mirrorLinks["Pixeldrain"] = dlUrl
                                else if (dlUrl.contains("pling.com")) mirrorLinks["Pling"] = dlUrl
                                else if (dlUrl.contains("axisgsiru.dolbaeb.me")) mirrorLinks["AxisCloud"] = dlUrl
                                else if (dlUrl.contains("drive.google.com")) mirrorLinks["Google Drive"] = dlUrl
                            }"""

content = content.replace(old_mirror, new_mirror)

# 2. Add Google Drive to the browser intent fallback in startDownload
old_start = """    fun startDownload(url: String, title: String) {
        if (url.contains("sourceforge.net")) {"""

new_start = """    fun startDownload(url: String, title: String) {
        if (url.contains("sourceforge.net") || url.contains("drive.google.com")) {"""

content = content.replace(old_start, new_start)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt', 'w') as f:
    f.write(content)
