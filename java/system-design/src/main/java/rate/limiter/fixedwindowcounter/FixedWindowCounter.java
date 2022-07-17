package rate.limiter.fixedwindowcounter;

import rate.limiter.RateLimiter;

import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;

public class FixedWindowCounter implements RateLimiter {

    private final int windowSize;
    private final int threshold;
    private final AtomicInteger counter;
    private final AtomicLong lastUpdatedTime;

    public FixedWindowCounter(int windowSize, int threshold) {
        this.windowSize = windowSize;
        this.threshold = threshold;
        this.counter = new AtomicInteger(0);
        this.lastUpdatedTime = new AtomicLong(System.currentTimeMillis());
    }

    @Override
    public boolean grantAccess() {
        long currentTime = System.currentTimeMillis();
        refreshBucket(currentTime);
        if (counter.get() <= threshold) {
            return true;
        }
        return false;
    }

    private void refreshBucket(long currentTime) {
        int duration = (int) ((currentTime - lastUpdatedTime.get()) / windowSize / 1000);
//        System.out.println(String.format("%s -> timeline = %d, counter = %d", Thread.currentThread().getName(), duration, counter.get()));
        if (duration < 1) {
            counter.incrementAndGet();
        } else {
            counter.set(1);
            lastUpdatedTime.set(currentTime);
        }
    }
}
