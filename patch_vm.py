with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt', 'r') as f:
    content = f.read()

old_write = """                val downloadsDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS)
                if (!downloadsDir.exists()) downloadsDir.mkdirs()
                
                var extension = ".img.xz"
                if (currentUrl.endsWith(".gz")) extension = ".img.gz"
                if (currentUrl.endsWith(".zip")) extension = ".zip"
                if (currentUrl.endsWith(".7z")) extension = ".7z"
                
                val outputFile = File(downloadsDir, "${title.replace(" ", "_")}$extension")
                val outputStream = FileOutputStream(outputFile)"""

new_write = """                var extension = ".img.xz"
                if (currentUrl.endsWith(".gz")) extension = ".img.gz"
                if (currentUrl.endsWith(".zip")) extension = ".zip"
                if (currentUrl.endsWith(".7z")) extension = ".7z"
                
                val filename = "${title.replace(" ", "_")}$extension"
                val documentFile = storageManager.createDocumentFile(filename)
                val outputStream = storageManager.openOutputStream(documentFile.uri)"""

content = content.replace(old_write, new_write)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt', 'w') as f:
    f.write(content)

