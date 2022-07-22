package rate.limiter.tokenbucket;

import rate.limiter.RateLimiter;

import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;

public class TokenBucket implements RateLimiter {

    private final int bucketSize;
    private final int refillRateInSecond;
    private final AtomicInteger count;
    private final AtomicLong lastRefillTime;

    public TokenBucket(int bucketSize, int refillRateInSecond) {
        this.bucketSize = bucketSize;
        this.refillRateInSecond = refillRateInSecond;
        this.count = new AtomicInteger(refillRateInSecond);
        this.lastRefillTime = new AtomicLong(System.currentTimeMillis());
    }

    @Override
    public boolean grantAccess() {
        refreshBucket();
        if (count.get() > 0) {
            count.decrementAndGet();
            return true;
        }
        return false;
    }

    private void refreshBucket() {
        long currentTime = System.currentTimeMillis();
        long duration = (currentTime - lastRefillTime.get()) / 1000;
        int additionalTokenCount = (int) duration * refillRateInSecond;
        int currentCapacity = Math.min(count.get() + additionalTokenCount, bucketSize);

        count.set(currentCapacity);

        if (duration >= 1) {
            lastRefillTime.set(currentTime);
        }
    }
}
