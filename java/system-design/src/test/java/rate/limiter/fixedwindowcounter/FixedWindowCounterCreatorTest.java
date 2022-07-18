package rate.limiter.fixedwindowcounter;

import org.junit.jupiter.api.Test;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

class FixedWindowCounterCreatorTest {

    @Test
    void test() {
        ExecutorService executorService = Executors.newFixedThreadPool(20);

        UserBucketCreator userBucketCreator = new UserBucketCreator("push", 1, 5);
        for (int i = 0; i < 15; i++) {
            executorService.execute(() -> userBucketCreator.applicationAccess("push"));
        }

//        try {
//            Thread.sleep(500);
//        } catch (InterruptedException e) {
//            e.printStackTrace();
//        }
//        System.out.println("===========================================");
//        for (int i = 0; i < 15; i++) {
//            executorService.execute(() -> userBucketCreator.applicationAccess("push"));
//        }

        executorService.shutdown();
    }
}
