package rate.limiter.tokenbucket;

import java.util.HashMap;
import java.util.Map;

public class TokenBucketCreator {

    private final Map<Integer, TokenBucket> bucket = new HashMap<>();

    public TokenBucketCreator(int id, int refillCount, int bucketCapacity) {
        this.bucket.put(id, new TokenBucket(refillCount, bucketCapacity));
    }

    public void accessApplication(int id) {
        TokenBucket tokenBucket = bucket.get(id);
        if (tokenBucket.grantAccess()) {
            System.out.println(Thread.currentThread().getName() + " -> able to access the application");
        } else {
            System.out.println(Thread.currentThread().getName() + " -> Too many request, Please try after some time");
        }
    }
}
