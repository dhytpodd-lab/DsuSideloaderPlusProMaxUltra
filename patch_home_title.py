with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/home/HomeScreen.kt', 'r') as f:
    content = f.read()

target = "barTitle = stringResource(id = R.string.app_name),"
replacement = """barTitle = if (uiState.additionalCard == AdditionalCardState.SETUP_STORAGE) "DSU Sideloader Plus" else stringResource(id = R.string.app_name),"""

content = content.replace(target, replacement)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/home/HomeScreen.kt', 'w') as f:
    f.write(content)
