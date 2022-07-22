package rate.limiter.slidingwindowlog;

import rate.limiter.RateLimiter;

import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicLong;

public class SlidingWindowLog implements RateLimiter {

    private final int windowSize;
    private final int threshold;
    private final Queue<Long> bucket;
    private final AtomicLong currentBasisTime;

    public SlidingWindowLog(int windowSize, int threshold) {
        this.windowSize = windowSize;
        this.threshold = threshold;
        this.bucket = new ConcurrentLinkedQueue<>();
        this.currentBasisTime = new AtomicLong(System.currentTimeMillis());
    }

    @Override
    public boolean grantAccess() {
        long currentTime = System.currentTimeMillis();
        refreshBucket(currentTime);
        if (bucket.size() < threshold) {
            bucket.offer(currentTime);
            return true;
        }
        return false;
    }

    private void refreshBucket(long currentTime) {
        if (bucket.isEmpty()) return;

        Long lastRequestLog = bucket.peek();
        long duration = currentTime - (lastRequestLog == null ? currentTime : lastRequestLog);
        while (duration >= windowSize) {
            if (bucket.isEmpty()) break;
            bucket.poll();
            lastRequestLog = bucket.peek();
            duration = currentTime - (lastRequestLog == null ? currentTime : lastRequestLog);
        }

        currentBasisTime.set(currentTime);
    }
}
