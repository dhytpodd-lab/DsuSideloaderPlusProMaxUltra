with open('app/src/main/java/yangfentuozi/dsusideloaderplus/model/Session.kt', 'r') as f:
    content = f.read()

old_shared = "val autoInstallEvent = MutableSharedFlow<Uri>(extraBufferCapacity = 1)"
new_shared = "val autoInstallEvent = MutableSharedFlow<Uri>(replay = 1, extraBufferCapacity = 1, onBufferOverflow = kotlinx.coroutines.channels.BufferOverflow.DROP_OLDEST)"

content = content.replace(old_shared, new_shared)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/model/Session.kt', 'w') as f:
    f.write(content)
