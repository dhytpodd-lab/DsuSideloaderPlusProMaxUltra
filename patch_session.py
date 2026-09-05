with open('app/src/main/java/yangfentuozi/dsusideloaderplus/model/Session.kt', 'r') as f:
    content = f.read()

content = content.replace("import kotlinx.coroutines.flow.MutableStateFlow", "import kotlinx.coroutines.flow.MutableStateFlow\nimport kotlinx.coroutines.flow.MutableSharedFlow")

old_session_class = """class Session(
    var userSelection: UserSelection = UserSelection(),
    var dsuInstallation: DSUInstallationSource = DSUInstallationSource(),
    var preferences: InstallationPreferences = InstallationPreferences(),
    var operationMode: MutableStateFlow<OperationMode> = MutableStateFlow(OperationMode.ADB),
) {"""

new_session_class = """class Session(
    var userSelection: UserSelection = UserSelection(),
    var dsuInstallation: DSUInstallationSource = DSUInstallationSource(),
    var preferences: InstallationPreferences = InstallationPreferences(),
    var operationMode: MutableStateFlow<OperationMode> = MutableStateFlow(OperationMode.ADB),
) {
    val autoInstallEvent = MutableSharedFlow<Uri>(extraBufferCapacity = 1)"""

content = content.replace(old_session_class, new_session_class)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/model/Session.kt', 'w') as f:
    f.write(content)
