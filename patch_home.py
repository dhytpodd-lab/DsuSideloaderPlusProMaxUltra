import sys

with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/home/HomeViewModel.kt', 'r') as f:
    content = f.read()

target = """            updateAdditionalCardState(AdditionalCardState.NONE)
            _uiState.update { it.copy(passedInitialChecks = true) }
        }
    }"""

replacement = """            updateAdditionalCardState(AdditionalCardState.NONE)
            _uiState.update { it.copy(passedInitialChecks = true) }

            if (session.autoInstallUri != null) {
                val uri = session.autoInstallUri!!
                session.autoInstallUri = null
                onFileSelectionResult(uri)
            }
        }
    }"""

if target in content:
    content = content.replace(target, replacement)
    with open('app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/home/HomeViewModel.kt', 'w') as f:
        f.write(content)
    print("Patched successfully")
else:
    print("Target not found")
