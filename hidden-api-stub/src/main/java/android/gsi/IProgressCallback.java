package android.gsi;

import android.os.Binder;
import android.os.IBinder;
import android.os.IInterface;

public interface IProgressCallback extends IInterface {

    void onProgress(long current, long total);

    abstract class Stub extends Binder implements IProgressCallback {

        public static IProgressCallback asInterface(IBinder obj) {
            throw new UnsupportedOperationException();
        }
    }
}
