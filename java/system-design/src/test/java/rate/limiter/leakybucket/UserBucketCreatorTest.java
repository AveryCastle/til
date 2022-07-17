package rate.limiter.leakybucket;

import org.junit.jupiter.api.Test;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

class UserBucketCreatorTest {

    @Test
    void test() {
        UserBucketCreator userBucketCreator = new UserBucketCreator("order", 10, 5);
        ExecutorService executorService = Executors.newFixedThreadPool(15);

        for (int i = 0; i < 15; i++) {
            executorService.execute(() -> userBucketCreator.applicationAccess("order"));
        }

//        try {
//            Thread.sleep(1000);
//        } catch (InterruptedException e) {
//            e.printStackTrace();
//        }
//
//        for (int i = 0; i < 15; i++) {
//            executorService.execute(() -> userBucketCreator.applicationAccess("order"));
//        }

        executorService.shutdown();
    }
}
