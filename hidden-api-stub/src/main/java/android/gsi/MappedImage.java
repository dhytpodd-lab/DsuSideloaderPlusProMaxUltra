package android.gsi;

import android.os.Parcel;
import android.os.Parcelable;

public class MappedImage implements Parcelable {
    public String path;

    public MappedImage() {}

    protected MappedImage(Parcel in) {
        path = in.readString();
    }

    public static final Creator<MappedImage> CREATOR = new Creator<MappedImage>() {
        @Override
        public MappedImage createFromParcel(Parcel in) {
            return new MappedImage(in);
        }

        @Override
        public MappedImage[] newArray(int size) {
            return new MappedImage[size];
        }
    };

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeString(path);
    }
}
