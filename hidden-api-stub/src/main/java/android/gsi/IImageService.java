package android.gsi;

import android.os.Binder;
import android.os.IBinder;
import android.os.IInterface;
import java.util.List;

public interface IImageService extends IInterface {
    int CREATE_IMAGE_DEFAULT = 0;
    int CREATE_IMAGE_READONLY = 1;

    void createBackingImage(String name, long size, int flags, IProgressCallback onProgress);

    void deleteBackingImage(String name);

    void mapImageDevice(String name, int timeoutMs, MappedImage mapping);

    void unmapImageDevice(String name);

    boolean backingImageExists(String name);

    boolean isImageMapped(String name);

    List<String> getAllBackingImages();

    abstract class Stub extends Binder implements IImageService {

        public static IImageService asInterface(IBinder obj) {
            throw new UnsupportedOperationException();
        }
    }
}
