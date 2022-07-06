package algorithm;

public class FizzBuzz {

    public static void main(String[] args) {

        for (int i = 1; i <= 30; i++) {
            String result = fizzBuzz(i);
            System.out.println(i + " => " + result);
        }
    }

    private static String fizzBuzz(int num) {
        StringBuilder sb = new StringBuilder();

        for (int i = 1; i <= num; i++) {
            if (i % 3 == 0)
                sb.append("Fizz");
            if (i % 5 == 0)
                sb.append("Buzz");
            if (i % 3 != 0 && i % 5 != 0)
                sb.append(i);
        }
        return sb.toString();
    }
}
