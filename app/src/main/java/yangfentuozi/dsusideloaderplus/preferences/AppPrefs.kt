package yangfentuozi.dsusideloaderplus.preferences

object AppPrefs {
    /**
     * Update feature only works if AUTHOR_SIGN_DIGEST is set
     * with same SHA-512 digest from signed apk OR is a DEBUG build
     * if AUTHOR_SIGN_DIGEST doesn't match, also no problem
     * app will work as expected, just without update feature.
     * check AboutViewModel init
     */
    const val UPDATE_CHECK_URL =
        "https://raw.githubusercontent.com/dhytpodd-lab/dsusideloaderpluspromaxultra/main/other/updater.json"
    const val AUTHOR_SIGN_DIGEST = "6b22aa49b98175b1611a6686185e50ac4bc40c1b23895d341fc0647c0f4ee36f09cc3cee5dc01130d40c383de6145c4f69ae6cadbb6c84a4113668ebab092dec"
    const val USER_PREFERENCES = "user_preferences"
    const val BOOTLOADER_UNLOCKED_WARNING = "bootloader_unlocked_warning"
    const val SAF_PATH = "writable_path"
    const val DEVELOPER_OPTIONS = "developer_options"
    const val USE_BUILTIN_INSTALLER = "builtin_installer"
    const val KEEP_SCREEN_ON = "keep_screen_on"
    const val UMOUNT_SD = "umount_sd"
    const val DISABLE_STORAGE_CHECK = "disable_storage_check"
    const val FULL_LOGCAT_LOGGING = "full_logcat_logging"
}
