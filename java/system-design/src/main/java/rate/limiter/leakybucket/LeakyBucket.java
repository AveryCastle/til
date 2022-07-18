package rate.limiter.leakybucket;

import rate.limiter.RateLimiter;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;

public class LeakyBucket implements RateLimiter {

    private final int bucketCapacity;
    private final int outflowRateInSecond;
    private final AtomicLong lastOutflowTime;
    private final BlockingQueue<Integer> bucket;
    private final AtomicInteger processedCount;

    public LeakyBucket(int bucketCapacity, int outflowRateInSecond) {
        this.bucketCapacity = bucketCapacity;
        this.outflowRateInSecond = outflowRateInSecond;
        this.lastOutflowTime = new AtomicLong(System.currentTimeMillis());
        this.bucket = new LinkedBlockingQueue<>(bucketCapacity);
        this.processedCount = new AtomicInteger(0);
    }

    @Override
    public boolean grantAccess() {
        refreshBucket();

        if (bucket.remainingCapacity() > 0) {
            bucket.offer(1);
            return true;
        }
        return false;
    }

    private void refreshBucket() {
        long currentTime = System.currentTimeMillis();
        long durationInSecond = (currentTime - lastOutflowTime.get()) / 1000;
        if (durationInSecond >= 1) {
            processedCount.set(0);
        }

        int currentCapacity = (int) ((currentTime - lastOutflowTime.get()) * outflowRateInSecond);
        while (processedCount.get() < currentCapacity) {
            processedCount.incrementAndGet();
            bucket.poll();
            lastOutflowTime.set(currentTime);
        }
    }
}
