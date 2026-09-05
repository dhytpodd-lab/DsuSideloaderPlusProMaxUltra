sed -i 's/pagesFetched < 10/pagesFetched < 50/g' app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt

sed -i '/else if (dlUrl.contains("drive.google.com")) mirrorLinks\["Google Drive"\] = dlUrl/a \
                                        else if (dlUrl.contains("mega.nz")) mirrorLinks["MEGA"] = dlUrl\
                                        else if (dlUrl.contains("mediafire.com")) mirrorLinks["MediaFire"] = dlUrl\
                                        else if (dlUrl.contains("t.me/")) mirrorLinks["Telegram"] = dlUrl\
                                        else if (dlUrl.contains("yadi.sk") || dlUrl.contains("disk.yandex")) mirrorLinks["Yandex Disk"] = dlUrl\
                                        else if (dlUrl.contains("androidfilehost.com")) mirrorLinks["AndroidFileHost"] = dlUrl\
                                        else if (dlUrl.contains("terabox.com")) mirrorLinks["TeraBox"] = dlUrl' app/src/main/java/yangfentuozi/dsusideloaderplus/ui/screen/gsihub/GsiHubViewModel.kt
