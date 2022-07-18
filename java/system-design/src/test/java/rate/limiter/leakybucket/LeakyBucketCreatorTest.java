package rate.limiter.leakybucket;

import org.junit.jupiter.api.Test;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

class LeakyBucketCreatorTest {

    @Test
    void test() {
        LeakyBucketCreator leakyBucketCreator = new LeakyBucketCreator("order", 10, 10);
        ExecutorService executorService = Executors.newFixedThreadPool(20);

        for (int i = 0; i < 30; i++) {
            executorService.execute(() -> leakyBucketCreator.applicationAccess("order"));
        }

        try {
            Thread.sleep(1001);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("==============================================================");
        for (int i = 0; i < 30; i++) {
            executorService.execute(() -> leakyBucketCreator.applicationAccess("order"));
        }

        executorService.shutdown();
    }
}
