package android.gsi;

import android.os.Binder;
import android.os.IBinder;
import android.os.IInterface;
import java.util.List;

public interface IGsiService extends IInterface {
    int INSTALL_OK = 0;
    int INSTALL_ERROR_GENERIC = 1;
    int INSTALL_ERROR_NO_SPACE = 2;

    boolean isGsiInstalled();

    boolean isGsiEnabled();

    boolean isGsiRunning();

    String getActiveDsuSlot();

    String getInstalledGsiImageDir();

    List<String> getInstalledDsuSlots();

    IImageService openImageService(String prefix);

    abstract class Stub extends Binder implements IGsiService {

        public static IGsiService asInterface(IBinder obj) {
            throw new UnsupportedOperationException();
        }
    }
}
