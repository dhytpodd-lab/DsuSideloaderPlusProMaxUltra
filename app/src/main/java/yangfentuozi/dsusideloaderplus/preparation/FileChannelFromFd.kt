package yangfentuozi.dsusideloaderplus.preparation

import java.io.FileDescriptor
import java.nio.ByteBuffer
import java.nio.channels.SeekableByteChannel
import android.system.Os
import android.system.OsConstants

class FileChannelFromFd(private val fd: FileDescriptor) : SeekableByteChannel {
    private var currentPosition: Long = 0
    private var isOpen = true
    
    override fun close() {
        isOpen = false
    }

    override fun isOpen(): Boolean = isOpen

    override fun read(dst: ByteBuffer?): Int {
        if (dst == null) return -1
        val startPos = dst.position()
        val readCount = Os.pread(fd, dst, currentPosition)
        if (readCount > 0) {
            currentPosition += readCount
            dst.position(startPos + readCount)
        }
        return if (readCount == 0) -1 else readCount
    }

    override fun write(src: ByteBuffer?): Int {
        throw UnsupportedOperationException("Read-only channel")
    }

    override fun position(): Long = currentPosition

    override fun position(newPosition: Long): SeekableByteChannel {
        currentPosition = newPosition
        return this
    }

    override fun size(): Long {
        return Os.fstat(fd).st_size
    }

    override fun truncate(size: Long): SeekableByteChannel {
        throw UnsupportedOperationException("Read-only channel")
    }
}
