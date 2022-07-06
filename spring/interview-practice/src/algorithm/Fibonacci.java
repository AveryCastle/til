package algorithm;

public class Fibonacci {

    public static int fibonacchi(int number) {
        return fibonacchi_iter(0, 1, number);
    }

    private static int fibonacchi_iter(int product1, int product2, int number) {
        if (number <= 1) {
            return product1;
        } else {
            return fibonacchi_iter(product2, product1 + product2, --number);
        }
    }
}
