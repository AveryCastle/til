package rate.limiter.slidingwindowcounter;

import java.util.HashMap;
import java.util.Map;

public class SlidingWindowCounterCreator {

    private final Map<String, SlidingWindowCounter> bucket = new HashMap<>();

    public SlidingWindowCounterCreator(String id, int windowSize, int threshold) {
        bucket.put(id, new SlidingWindowCounter(windowSize, threshold));
    }

    public void applicationAccess(String id) {
        if (bucket.get(id).grantAccess()) {
            System.out.println(Thread.currentThread().getName() + " -> able to access the application");
        } else {
            System.out.println(Thread.currentThread().getName() + " -> Too many request, Please try after some time");
        }
    }
}
