package javaeleven;

public class JavaEleven {

    public static void main(String[] args) {
        System.out.println("원본 문자열 => ");
        String s1 = " 공백 앞 뒤에 있는데 공백 없애나요? ";
        System.out.println(s1);

        System.out.println(s1.isBlank());

        System.out.println("strip() => ");
        System.out.println(s1.strip());

        System.out.println(s1.stripTrailing());
        System.out.println(s1.stripLeading());

        System.out.println(s1.repeat(3));

        var x = "abcdefg";
        System.out.println(x);
    }
}
