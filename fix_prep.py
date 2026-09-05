import re

with open("app/src/main/java/yangfentuozi/dsusideloaderplus/preparation/Preparation.kt", "r") as f:
    content = f.read()

# Let's just find `private fun prepareRooted() {` to `if (!job.isCancelled) {` and replace it
replacement = """    private fun prepareRooted() {
        val source: DSUInstallationSource = when (getExtension(userSelectedFileUri)) {
            "img" -> {
                DSUInstallationSource.SingleSystemImage(
                    userSelectedFileUri,
                    storageManager.getFilesizeFromUri(userSelectedFileUri),
                )
            }
            "xz", "gz", "gzip" -> {
                val result = extractFile(userSelectedFileUri)
                DSUInstallationSource.SingleSystemImage(result.first, result.second)
            }
            "zip" -> {
                DSUInstallationSource.DsuPackage(userSelectedFileUri)
            }
            "7z" -> {
                val result = prepare7z(userSelectedFileUri)
                DSUInstallationSource.DsuPackage(result.first)
            }
            else -> {
                throw Exception("Unsupported filetype")
            }
        }
"""

start_str = "    private fun prepareRooted() {"
end_str = "        if (!job.isCancelled) {"
start_idx = content.find(start_str)
end_idx = content.find(end_str)

new_content = content[:start_idx] + replacement + content[end_idx:]

with open("app/src/main/java/yangfentuozi/dsusideloaderplus/preparation/Preparation.kt", "w") as f:
    f.write(new_content)
