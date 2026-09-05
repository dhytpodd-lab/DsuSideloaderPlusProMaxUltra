import re

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/home/HomeScreen.kt', 'r') as f:
    content = f.read()

pattern = r'\s*item \{\s*yangfentuozi\.dsusideloaderplus\.ui\.components\.SettingsItem\(\s*title = stringResource\(id = R\.string\.gsi_hub_title\),\s*summary = stringResource\(id = R\.string\.gsi_hub_summary\),\s*onClick = \{ navigate\(Destinations\.GsiHub\) \},\s*\)\s*\}'

content = re.sub(pattern, '', content)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/home/HomeScreen.kt', 'w') as f:
    f.write(content)

