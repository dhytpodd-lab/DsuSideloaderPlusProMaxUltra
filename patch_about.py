with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/about/AboutScreen.kt', 'r') as f:
    content = f.read()

old_item = """            item {
                SettingsItem(
                    title = "daniil_qq",
                    summary = "Pro Max Ultra Mod Developer",
                    onClick = { /* no-op */ },
                )
            }"""

new_item = """            item {
                SettingsItem(
                    title = "daniil_qq",
                    summary = "Pro Max Ultra Mod Developer",
                    onClick = { uriHandler.openUri("https://t.me/autismbtw") },
                )
            }"""

content = content.replace(old_item, new_item)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/about/AboutScreen.kt', 'w') as f:
    f.write(content)
