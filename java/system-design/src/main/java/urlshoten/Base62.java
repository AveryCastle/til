package urlshoten;

public class Base62 {

    private static final char[] BASE62 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789".toCharArray();

    public static String encoding(int value) {
        final StringBuilder sb = new StringBuilder();

        do {
            int remain = value % 62;
            sb.append(BASE62[remain]);
            value /= 62;
        } while (value > 0);

        return sb.toString();
    }
}
