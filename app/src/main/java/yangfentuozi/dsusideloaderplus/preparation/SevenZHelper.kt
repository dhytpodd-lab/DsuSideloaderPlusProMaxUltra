package yangfentuozi.dsusideloaderplus.preparation

import android.net.Uri
import android.os.ParcelFileDescriptor
import org.apache.commons.compress.archivers.sevenz.SevenZFile
import yangfentuozi.dsusideloaderplus.core.StorageManager
import java.io.BufferedOutputStream
import java.util.zip.ZipEntry
import java.util.zip.ZipOutputStream
import java.util.zip.Deflater
import kotlinx.coroutines.Job

class SevenZHelper(
    private val storageManager: StorageManager,
    private val inputFile: Uri,
    private val outputFileUri: Uri,
    private val installationJob: Job,
    private val onProgressChange: (Float) -> Unit,
) {
    fun extractToZip(): Pair<Uri, Long> {
        var pfd: ParcelFileDescriptor? = null
        var sevenZFile: SevenZFile? = null
        var zipOut: ZipOutputStream? = null
        try {
            pfd = storageManager.openFileDescriptor(inputFile, "r")
            val fileChannel = FileChannelFromFd(pfd.fileDescriptor)
            sevenZFile = SevenZFile(fileChannel)

            var entry = sevenZFile.nextEntry
            var targetEntry = entry
            while (entry != null) {
                if (!entry.isDirectory && entry.name.endsWith(".img")) {
                    targetEntry = entry
                    break
                }
                entry = sevenZFile.nextEntry
            }

            if (targetEntry == null) {
                throw Exception("No .img file found inside the .7z archive")
            }

            val outputStream = storageManager.openOutputStream(outputFileUri)
            // Use a large buffer for output stream (1MB)
            zipOut = ZipOutputStream(BufferedOutputStream(outputStream, 1024 * 1024))
            
            // VERY IMPORTANT for speed: DO NOT COMPRESS AT ALL.
            zipOut.setLevel(Deflater.NO_COMPRESSION)
            
            // Put it into a zip
            val zipEntry = ZipEntry("system.img")
            zipOut.putNextEntry(zipEntry)

            // Huge buffer for reading 7z (512KB)
            val buffer = ByteArray(512 * 1024)
            var bytesRead: Int
            var totalRead: Long = 0
            val size = targetEntry.size
            var lastUpdate = System.currentTimeMillis()

            while (sevenZFile.read(buffer).also { bytesRead = it } != -1 && !installationJob.isCancelled) {
                zipOut.write(buffer, 0, bytesRead)
                totalRead += bytesRead
                
                val now = System.currentTimeMillis()
                // Update UI only every 250ms to prevent flooding and CPU waste
                if (size > 0 && now - lastUpdate > 250) {
                    onProgressChange(totalRead.toFloat() / size.toFloat())
                    lastUpdate = now
                }
            }
            
            // Push final progress
            if (size > 0) {
                onProgressChange(1f)
            }

            zipOut.closeEntry()
            zipOut.flush()
            zipOut.close()

            val fileLength = storageManager.getFilesizeFromUri(outputFileUri)
            return Pair(outputFileUri, fileLength)
        } finally {
            try { zipOut?.close() } catch (e: Exception) {}
            try { sevenZFile?.close() } catch (e: Exception) {}
            try { pfd?.close() } catch (e: Exception) {}
        }
    }
}
