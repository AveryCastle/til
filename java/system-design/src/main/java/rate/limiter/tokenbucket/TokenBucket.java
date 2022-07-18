package rate.limiter.tokenbucket;

import rate.limiter.RateLimiter;

import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;

public class TokenBucket implements RateLimiter {

    private final int refillCountInSecond;
    private final int bucketSize;
    private final AtomicInteger currentCount;
    private final AtomicLong lastRefilledTime;

    public TokenBucket(int refillCountInSecond, int bucketSize) {
        this.refillCountInSecond = refillCountInSecond;
        this.bucketSize = bucketSize;
        this.currentCount = new AtomicInteger(refillCountInSecond);
        this.lastRefilledTime = new AtomicLong(System.currentTimeMillis() / 1000 * 1000);
    }

    @Override
    public boolean grantAccess() {
        refreshToken();

        if (currentCount.get() > 0) {
            currentCount.decrementAndGet();
            return true;
        }
        return false;
    }

    private void refreshToken() {
        long currentTime = System.currentTimeMillis();
        long duration = (currentTime - lastRefilledTime.get()) / 1000;
        if (duration >= 1) {
            lastRefilledTime.set(currentTime / 1000 * 1000);
        }

        int additionalToken = (int) (duration * refillCountInSecond);
        int currentCapacity = Math.min(currentCount.get() + additionalToken, bucketSize);
        currentCount.set(currentCapacity);
    }
}
