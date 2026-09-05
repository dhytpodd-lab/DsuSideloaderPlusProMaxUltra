with open('app/src/main/java/yangfentuozi/dsusideloaderplus/model/Session.kt', 'r') as f:
    content = f.read()

import re
content = re.sub(r'val autoInstallEvent = .*', 'var autoInstallUri: Uri? = null', content)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/model/Session.kt', 'w') as f:
    f.write(content)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/home/HomeViewModel.kt', 'r') as f:
    hvm = f.read()

old_hvm = """        viewModelScope.launch {
            session.autoInstallEvent.collect { uri ->
                onFileSelectionResult(uri)
            }
        }"""
new_hvm = """        if (session.autoInstallUri != null) {
            onFileSelectionResult(session.autoInstallUri!!)
            session.autoInstallUri = null
        }"""
hvm = hvm.replace(old_hvm, new_hvm)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/home/HomeViewModel.kt', 'w') as f:
    f.write(hvm)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt', 'r') as f:
    gvm = f.read()

gvm = gvm.replace("session.autoInstallEvent.tryEmit(documentFile.uri)", "session.autoInstallUri = documentFile.uri")

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt', 'w') as f:
    f.write(gvm)
