package chap6;

import static org.junit.Assert.*;

import org.junit.Test;

public class PartitionPrimeTest {

    @Test
    public void test() {
        long fastest = Long.MAX_VALUE;
        for (int i = 0; i < 10; i++) {
            long start = System.nanoTime();
            PartitionPrime.isPrime(1_000_000);
            long duration = (System.nanoTime() - start) / 1_000_000;
            if (duration < fastest) {
                fastest = duration;
            }
        }
        System.out.println("Fastest execution done in " + fastest + " msecs.");
    }
}
