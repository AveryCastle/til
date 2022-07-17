package rate.limiter.leakybucket;

import java.util.HashMap;
import java.util.Map;

public class UserBucketCreator {

    private final Map<String, LeakyBucket> bucket = new HashMap<>();
    private final int bucketCapacity;
    private final int outflowRateInSecond;

    public UserBucketCreator(String id, int bucketCapacity, int outflowRateInSecond) {
        this.bucketCapacity = bucketCapacity;
        this.outflowRateInSecond = outflowRateInSecond;
        this.bucket.put(id, new LeakyBucket(bucketCapacity, outflowRateInSecond));
    }

    public void applicationAccess(String id) {
        LeakyBucket leakyBucket = bucket.get(id);
        if (leakyBucket.grantAccess()) {
            System.out.println(Thread.currentThread().getName() + " -> able to access the application");
        } else {
            System.out.println(Thread.currentThread().getName() + " -> Too many request, Please try after some time");
        }
    }
}
