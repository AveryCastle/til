package rate.limiter.leakybucket;

import rate.limiter.RateLimiter;

import java.util.Queue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;

public class LeakyBucket implements RateLimiter {

    private final int bucketSize;
    private final int processCountInSecond;
    private final Queue<Integer> bucket;
    private final AtomicInteger currentProcessedCount;
    private final AtomicLong lastProcessedTime;

    public LeakyBucket(int bucketSize, int processCountInSecond) {
        this.bucketSize = bucketSize;
        this.processCountInSecond = processCountInSecond;
        this.bucket = new LinkedBlockingQueue<>(bucketSize);
        this.currentProcessedCount = new AtomicInteger(0);
        this.lastProcessedTime = new AtomicLong(System.currentTimeMillis());
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
        double duration = (double) (currentTime - lastProcessedTime.get()) / 1000;

        if (duration >= 1) {
            currentProcessedCount.set(0);
        }

        double currentCapacity = processCountInSecond * duration;
        while (currentProcessedCount.get() < currentCapacity) {
            currentProcessedCount.incrementAndGet();
            bucket.poll();
            lastProcessedTime.set(currentTime);
        }
    }
}
