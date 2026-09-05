with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubScreen.kt', 'r') as f:
    content = f.read()

old_linear = """                                            if (isThisDownloading && progress != null) {
                                                LinearProgressIndicator(
                                                    progress = { progress },
                                                    modifier = Modifier.fillMaxWidth().padding(top = 4.dp)
                                                )
                                            }"""

new_linear = """                                            if (isThisDownloading && progress != null) {
                                                if (progress < 0f) {
                                                    LinearProgressIndicator(
                                                        modifier = Modifier.fillMaxWidth().padding(top = 4.dp)
                                                    )
                                                } else {
                                                    LinearProgressIndicator(
                                                        progress = { progress },
                                                        modifier = Modifier.fillMaxWidth().padding(top = 4.dp)
                                                    )
                                                }
                                            }"""
content = content.replace(old_linear, new_linear)

old_circular = """                                        if (progress != null) {
                                            CircularProgressIndicator(
                                                progress = { progress },
                                                modifier = Modifier.size(24.dp)
                                            )
                                        }"""

new_circular = """                                        if (progress != null) {
                                            if (progress < 0f) {
                                                CircularProgressIndicator(
                                                    modifier = Modifier.size(24.dp)
                                                )
                                            } else {
                                                CircularProgressIndicator(
                                                    progress = { progress },
                                                    modifier = Modifier.size(24.dp)
                                                )
                                            }
                                        }"""

content = content.replace(old_circular, new_circular)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubScreen.kt', 'w') as f:
    f.write(content)
