package rate.limiter.tokenbucket;

import org.junit.jupiter.api.Test;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

class TokenBucketCreatorTest {

    @Test
    void test() {
        TokenBucketCreator userBucketCreator = new TokenBucketCreator(1, 5, 20);
        ExecutorService executorService = Executors.newFixedThreadPool(10);
        for (int i = 0; i < 20; i++) {
            executorService.execute(() -> userBucketCreator.accessApplication(1));
        }

        try {
            Thread.sleep(2001L);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("======================================================");
        for (int i = 0; i < 15; i++) {
            executorService.execute(() -> userBucketCreator.accessApplication(1));
        }

        try {
            Thread.sleep(1000L);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("======================================================");
        for (int i = 0; i < 15; i++) {
            executorService.execute(() -> userBucketCreator.accessApplication(1));
        }
        executorService.shutdown();
    }
}
