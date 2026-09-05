sed -i 's/val imgFilePair = SevenZHelper(/val zipFilePair = SevenZHelper(/g' app/src/main/java/yangfentuozi/dsusideloaderplus/preparation/Preparation.kt
sed -i 's/).extract()/).extractToZip()/g' app/src/main/java/yangfentuozi/dsusideloaderplus/preparation/Preparation.kt
sed -i 's/return prepareImage(imgFilePair.first)/return Pair(zipFilePair.first, -1)/g' app/src/main/java/yangfentuozi/dsusideloaderplus/preparation/Preparation.kt
sed -i 's/val outputFile = getFileName(sevenZFile)/val outputFile = "${getFileName(sevenZFile)}.zip"/g' app/src/main/java/yangfentuozi/dsusideloaderplus/preparation/Preparation.kt
