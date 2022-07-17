package rate.limiter.slidingwindowlog;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

public class UserBucketCreator {

    private final Map<Integer, SlidingWindowLog> bucket;

    public UserBucketCreator(int id, int timeWindowInSecond, int bucketCapacity) {
        bucket = new HashMap<>();
        bucket.put(id, new SlidingWindowLog(timeWindowInSecond, bucketCapacity));
    }

    public void accessApplication(int id) {
        if (bucket.get(id).grantAccess()) {
            System.out.println(LocalDateTime.now() + ", " + Thread.currentThread().getName() + " -> able to access the application");
        } else {
            System.out.println(LocalDateTime.now() + ", " + Thread.currentThread().getName() + " -> Too many request, Please try after some time");
        }
    }
}
