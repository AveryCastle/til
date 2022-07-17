package rate.limiter.slidingwindowcounter;

import org.junit.jupiter.api.Test;

import java.util.stream.IntStream;

class SlidingWindowCounterCreatorTest {

    @Test
    void slidingWindowCounter() {
        SlidingWindowCounterCreator slidingWindowCounterCreator = new SlidingWindowCounterCreator("push", 1000, 7);

        IntStream.rangeClosed(0, 100).parallel().forEach(el -> {
//            try {
//                Thread.sleep(10);
//            } catch (InterruptedException e) {
//                e.printStackTrace();
//            }
            slidingWindowCounterCreator.applicationAccess("push");
        });
//        ExecutorService executorService = Executors.newFixedThreadPool(20);
//        for (int i = 0; i < 20; i++) {
//            try {
//                Thread.sleep(100);
//            } catch (InterruptedException e) {
//                e.printStackTrace();
//            }
//            executorService.execute(() -> {
//                slidingWindowCounterCreator.applicationAccess("push");
//            });
//        }

//        System.out.println("==================================================");
//        try {
//            Thread.sleep(1000);
//        } catch (InterruptedException e) {
//            e.printStackTrace();
//        }
//
//        for (int i = 0; i < 15; i++) {
//            executorService.execute(() -> slidingWindowCounterCreator.applicationAccess("push"));
//        }

//        executorService.shutdown();
    }
}
