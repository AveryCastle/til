import org.junit.jupiter.api.Test;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.IntStream;

public class TestClass {

    private final AtomicInteger atomicInteger = new AtomicInteger();

    @Test
    void test() {
        ExecutorService executorService = Executors.newFixedThreadPool(3);

        IntStream.rangeClosed(1, 100).parallel().forEach(el -> {
            executorService.submit(() -> {
                System.out.println(String.format("thread = %s, timestamp = %d, seq = %d", Thread.currentThread().getName(), System.currentTimeMillis(), atomicInteger.getAndIncrement()));
            });
        });
    }
}
