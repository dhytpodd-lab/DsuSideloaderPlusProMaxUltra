with open("app/src/main/java/yangfentuozi/dsusideloaderplus/preparation/SevenZHelper.kt", "r") as f:
    content = f.read()

old_block = """            // VERY IMPORTANT for speed: do not try to compress an already huge image, just pack it quickly
            zipOut.setMethod(ZipOutputStream.STORED)
            zipEntry.size = size
            zipEntry.compressedSize = size
            val crc32 = java.util.zip.CRC32()
            // Oh wait, for STORED we need CRC32 ahead of time, which is impossible without reading the whole file twice. Let us use Deflater.NO_COMPRESSION instead."""

new_block = """            // VERY IMPORTANT for speed: DO NOT COMPRESS AT ALL.
            zipOut.setLevel(Deflater.NO_COMPRESSION)"""

content = content.replace(old_block, new_block)

with open("app/src/main/java/yangfentuozi/dsusideloaderplus/preparation/SevenZHelper.kt", "w") as f:
    f.write(content)

