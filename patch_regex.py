with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt', 'r') as f:
    content = f.read()

content = content.replace('val linkRegex = Regex("<a[^>]+href=\\"([^"]+)\\"")', 'val linkRegex = Regex("""<a[^>]+href="([^"]+)"""")')
content = content.replace('val msgRegex = Regex("<div class=\\"tgme_widget_message_text[^>]*>(.*?)</div>", RegexOption.DOT_MATCHES_ALL)', 'val msgRegex = Regex("""<div class="tgme_widget_message_text[^>]*>(.*?)</div>""", RegexOption.DOT_MATCHES_ALL)')

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt', 'w') as f:
    f.write(content)

