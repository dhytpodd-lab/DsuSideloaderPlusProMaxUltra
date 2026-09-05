with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt', 'r') as f:
    content = f.read()

content = content.replace("import yangfentuozi.dsusideloaderplus.core.StorageManager", "import yangfentuozi.dsusideloaderplus.core.StorageManager\nimport yangfentuozi.dsusideloaderplus.model.Session\nimport kotlinx.coroutines.flow.MutableSharedFlow\nimport kotlinx.coroutines.flow.asSharedFlow")

old_constructor = """class GsiHubViewModel @Inject constructor(
    @ApplicationContext private val context: Context,
    private val storageManager: StorageManager
) : ViewModel() {"""

new_constructor = """class GsiHubViewModel @Inject constructor(
    @ApplicationContext private val context: Context,
    private val storageManager: StorageManager,
    private val session: Session
) : ViewModel() {
    private val _navigateToHome = MutableSharedFlow<Unit>(extraBufferCapacity = 1)
    val navigateToHome = _navigateToHome.asSharedFlow()"""

content = content.replace(old_constructor, new_constructor)

old_finish = """                if (!isActive) {
                    try { documentFile.delete() } catch (e: Exception) {}
                } else {
                    downloadProgress.remove(url)
                }"""

new_finish = """                if (!isActive) {
                    try { documentFile.delete() } catch (e: Exception) {}
                } else {
                    downloadProgress.remove(url)
                    session.autoInstallEvent.tryEmit(documentFile.uri)
                    _navigateToHome.tryEmit(Unit)
                }"""

content = content.replace(old_finish, new_finish)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt', 'w') as f:
    f.write(content)
