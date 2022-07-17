package rate.limiter.fixedwindowcounter;

import java.util.HashMap;
import java.util.Map;

public class UserBucketCreator {

    private final Map<String, FixedWindowCounter> bucket = new HashMap<>();

    public UserBucketCreator(String id, int timeline, int threshold) {
        bucket.put(id, new FixedWindowCounter(timeline, threshold));
    }

    public void applicationAccess(String id) {
        FixedWindowCounter fixedWindowCounter = bucket.get(id);
        if (fixedWindowCounter.grantAccess()) {
            System.out.println(Thread.currentThread().getName() + " -> able to access the application");
        } else {
            System.out.println(Thread.currentThread().getName() + " -> Too many request, Please try after some time");
        }
    }
}
