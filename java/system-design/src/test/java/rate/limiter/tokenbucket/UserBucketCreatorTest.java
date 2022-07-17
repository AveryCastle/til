package rate.limiter.tokenbucket;

import org.junit.jupiter.api.Test;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

class UserBucketCreatorTest {

    @Test
    void test() {
        UserBucketCreator userBucketCreator = new UserBucketCreator(1, 3, 10);
        ExecutorService executorService = Executors.newFixedThreadPool(10);
        for (int i = 0; i < 15; i++) {
            executorService.execute(() -> userBucketCreator.accessApplication(1));
        }

        try {
            Thread.sleep(2000L);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        for (int i = 0; i < 15; i++) {
            executorService.execute(() -> userBucketCreator.accessApplication(1));
        }
        executorService.shutdown();
    }
}
