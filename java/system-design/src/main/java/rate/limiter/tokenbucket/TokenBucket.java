package rate.limiter.tokenbucket;

import rate.limiter.RateLimiter;

import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;

public class TokenBucket implements RateLimiter {

    private final int refillCountInSeconds;
    private final int bucketCapacity;
    private final AtomicInteger currentCapacity;
    private final AtomicLong lastUpdatedTime;

    public TokenBucket(int refillCountInSeconds, int bucketCapacity) {
        this.refillCountInSeconds = refillCountInSeconds;
        this.bucketCapacity = bucketCapacity;
        currentCapacity = new AtomicInteger(bucketCapacity);
        lastUpdatedTime = new AtomicLong(System.currentTimeMillis());
    }

    @Override
    public boolean grantAccess() {
        refreshBucket();
        if (currentCapacity.get() > 0) {
            currentCapacity.decrementAndGet();
            return true;
        }

        return false;
    }

    private void refreshBucket() {
        long currentTime = System.currentTimeMillis();
        int additionalToken = (int) Math.ceil((currentTime - lastUpdatedTime.get()) / 1000) * refillCountInSeconds;
        int currCapacity = Math.min(currentCapacity.get() + additionalToken, bucketCapacity);
        currentCapacity.set(currCapacity);
        lastUpdatedTime.set(currentTime);
    }
}
