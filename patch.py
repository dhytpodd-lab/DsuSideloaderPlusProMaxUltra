import sys

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/core/StorageManager.kt', 'r') as f:
    content = f.read()

get_workspace_code = """    private fun getWorkspaceFolder(): DocumentFile {
        if (this::workspaceFolder.isInitialized && workspaceFolder.canRead()) {
            return workspaceFolder
        }

        if (rwPathAllowedByUser.isEmpty()) {
            throw Exception("Allowed path by user is empty, ask user to allow storage permission again.")
        }

        val writeableDir =
            DocumentFile.fromTreeUri(appContext, rwPathAllowedByUser.toUri())
                ?: throw Exception("Workspace folder cannot be null.")

        workspaceFolder = writeableDir.findFile(Constants.WORKSPACE_FOLDER)
            ?: writeableDir.createDirectory(Constants.WORKSPACE_FOLDER)!!

        return workspaceFolder
    }

    private fun getDownloadsFolder(): DocumentFile {
        if (rwPathAllowedByUser.isEmpty()) {
            throw Exception("Allowed path by user is empty, ask user to allow storage permission again.")
        }

        val writeableDir =
            DocumentFile.fromTreeUri(appContext, rwPathAllowedByUser.toUri())
                ?: throw Exception("Downloads folder cannot be null.")

        val downloadsFolder = writeableDir.findFile(Constants.DOWNLOADS_FOLDER)
            ?: writeableDir.createDirectory(Constants.DOWNLOADS_FOLDER)!!

        return downloadsFolder
    }"""

content = content.replace(
"""    private fun getWorkspaceFolder(): DocumentFile {
        if (this::workspaceFolder.isInitialized && workspaceFolder.canRead()) {
            return workspaceFolder
        }

        if (rwPathAllowedByUser.isEmpty()) {
            throw Exception("Allowed path by user is empty, ask user to allow storage permission again.")
        }

        val writeableDir =
            DocumentFile.fromTreeUri(appContext, rwPathAllowedByUser.toUri())
                ?: throw Exception("Workspace folder cannot be null.")

        workspaceFolder = writeableDir.findFile(Constants.WORKSPACE_FOLDER)
            ?: writeableDir.createDirectory(Constants.WORKSPACE_FOLDER)!!

        return workspaceFolder
    }""", get_workspace_code)

create_doc_file_code = """    fun createDocumentFile(filename: String): DocumentFile {
        return getWorkspaceFolder().createFile("application/octet-stream", filename)!!
    }

    fun createDownloadFile(filename: String): DocumentFile {
        return getDownloadsFolder().createFile("application/octet-stream", filename)!!
    }"""

content = content.replace("""    fun createDocumentFile(filename: String): DocumentFile {
        return getWorkspaceFolder().createFile("application/octet-stream", filename)!!
    }""", create_doc_file_code)

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/core/StorageManager.kt', 'w') as f:
    f.write(content)
