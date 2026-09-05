sed -i 's/"application\/zip",/"application\/zip",\n        "application\/x-7z-compressed",/g' app/src/main/java/yangfentuozi/dsusideloaderplus/ui/cards/installation/InstallationCard.kt
sed -i 's/"gz", "xz", "img", "gzip"/"gz", "xz", "img", "gzip", "7z"/g' app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/home/HomeViewModel.kt

sed -i 's/"zip" -> prepareZip(userSelectedFileUri)/"zip" -> prepareZip(userSelectedFileUri)\n                "7z" -> prepare7z(userSelectedFileUri)/g' app/src/main/java/yangfentuozi/dsusideloaderplus/preparation/Preparation.kt

cat << 'EOF2' >> app/src/main/java/yangfentuozi/dsusideloaderplus/preparation/Preparation.kt

    private fun prepare7z(sevenZFile: Uri): Pair<Uri, Long> {
        val outputFile = getFileName(sevenZFile)
        onStepUpdate(InstallationStep.DECOMPRESSING_XZ)
        
        val uri = getSafeUri(sevenZFile)
        val finalFile = storageManager.createDocumentFile(outputFile)
        
        val imgFilePair = SevenZHelper(
            storageManager,
            uri,
            finalFile.uri,
            job,
            onPreparationProgressUpdate
        ).extract()
        
        return prepareImage(imgFilePair.first)
    }
EOF2
