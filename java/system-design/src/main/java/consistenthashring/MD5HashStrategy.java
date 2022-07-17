package consistenthashring;

import java.security.MessageDigest;

public class MD5HashStrategy implements HashStrategy {

    @Override
    public Integer hashCode(String key) {
        return MD5.md5(key).hashCode();
    }

    // MD5 암호화. 32비트
    private static class MD5 {

        public static String md5(String key) {
            MessageDigest md5 = null;
            try {
                md5 = MessageDigest.getInstance("MD5");
            } catch (Exception e) {
                e.printStackTrace();
                return "";
            }

            byte[] md5Bytes = md5.digest(key.getBytes());

            StringBuffer hexValue = new StringBuffer();

            for (int i = 0; i < md5Bytes.length; i++) {
                int val = ((int) md5Bytes[i]) & 0xff;
                if (val < 16)
                    hexValue.append("0");
                hexValue.append(Integer.toHexString(val));
            }

            return hexValue.toString();
        }
    }
}
