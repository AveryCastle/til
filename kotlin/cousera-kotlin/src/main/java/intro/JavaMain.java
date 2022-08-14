package intro;

import java.io.IOException;

public class JavaMain {

    public static void main(String[] args) {
//        try {
//            ExceptionsKt.fnBar();
//        } catch (IOException e) {
//            e.printStackTrace();
//        }
//
//        ExceptionsKt.fnFoo();

        char lastChar = ExtensionFunctionsKt.lastChar("Jimin");
        System.out.println(lastChar);

        String strings = ExtensionFunctionsKt.repeat("SUGA", 5);
        System.out.println(strings);
    }
}
