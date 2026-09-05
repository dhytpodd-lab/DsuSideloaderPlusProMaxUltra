sed -i '/object Destinations {/a \    const val GsiHub = "gsi_hub"' app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/Navigation.kt
sed -i '/composable(Destinations.Libraries)/a \        composable(Destinations.GsiHub) { yangfentuozi.dsusideloaderplus.ui.screen.gsihub.GsiHubScreen(navigate = { navigate(it) }) }' app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/Navigation.kt
