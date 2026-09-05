with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/home/HomeViewModel.kt', 'r') as f:
    content = f.read()

old_init = """    init {
        checkUnsupportedCard()
        viewModelScope.launch(Dispatchers.IO) {
            checkStorage()
        }"""

new_init = """    init {
        checkUnsupportedCard()
        viewModelScope.launch(Dispatchers.IO) {
            checkStorage()
        }
        viewModelScope.launch {
            session.autoInstallEvent.collect { uri ->
                onFileSelectionResult(uri)
            }
        }"""

content = content.replace(old_init, new_init)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/home/HomeViewModel.kt', 'w') as f:
    f.write(content)
