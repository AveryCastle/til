package algorithm;

public class Fibonacci2 {

    public static void main(String[] args) {

        for (int i = 1; i <= 10; i++) {
            int result = fibonacci(i);
            System.out.println(i + " => " + result);
        }
    }

    private static int fibonacci(int i) {
        int[] array = new int[i + 2];
        array[0] = 0;
        array[1] = 1;

        for (int j = 2; j <= i; j++) {
            array[j] = array[j - 1] + array[j - 2];
        }
        return array[i];
    }
}
