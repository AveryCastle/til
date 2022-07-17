package rate.limiter.slidingwindowlog;

import org.junit.jupiter.api.Test;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

class UserBucketCreatorTest {

    @Test
    void test() {
        UserBucketCreator userBucketCreator = new UserBucketCreator(1, 1, 5);
        ExecutorService executors = Executors.newFixedThreadPool(12);
        for (int i = 0; i < 10; i++) {
//            try {
//                Thread.sleep(1);
//            } catch (InterruptedException e) {
//                e.printStackTrace();
//            }
            executors.execute(() -> userBucketCreator.accessApplication(1));
        }

        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        for (int i = 0; i < 12; i++) {
            executors.execute(() -> userBucketCreator.accessApplication(1));
        }

        executors.shutdown();
    }
}
