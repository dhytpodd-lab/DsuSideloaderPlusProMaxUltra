with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubScreen.kt', 'r') as f:
    content = f.read()

content = content.replace("import kotlinx.coroutines.Dispatchers", "import kotlinx.coroutines.Dispatchers\nimport yangfentuozi.dsusideloaderplus.ui.screen.Destinations")

old_effect = """    LaunchedEffect(Unit) {
        viewModel.fetchCustomLinks(prefs)
        viewModel.fetchTelegramChannels(customLinks)
    }"""

new_effect = """    LaunchedEffect(Unit) {
        viewModel.fetchCustomLinks(prefs)
        viewModel.fetchTelegramChannels(customLinks)
    }
    
    LaunchedEffect(viewModel) {
        viewModel.navigateToHome.collect {
            navigate(Destinations.Home)
        }
    }"""

content = content.replace(old_effect, new_effect)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubScreen.kt', 'w') as f:
    f.write(content)
