package rate.limiter.slidingwindowcounter;

import rate.limiter.RateLimiter;

import java.text.SimpleDateFormat;
import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;

public class SlidingWindowCounter implements RateLimiter {

    private final SimpleDateFormat simpleDateFormat = new SimpleDateFormat("HH:mm:ss");

    private final int windowSize;
    private final int threshold;
    private final Queue<Long> slidingWindow;
    private final AtomicLong currentBasisTime;
    private final AtomicInteger currentCounter;

    public SlidingWindowCounter(int windowSize, int threshold) {
        this.windowSize = windowSize;
        this.threshold = threshold;
        this.slidingWindow = new ConcurrentLinkedQueue<>();
        this.currentBasisTime = new AtomicLong((System.currentTimeMillis() / windowSize) * windowSize);
        this.currentCounter = new AtomicInteger(0);
    }

    @Override
    public boolean grantAccess() {
        long currentTime = System.currentTimeMillis();
        synchronized (this) {
            refreshSlidingWindow(currentTime);
            if (calculatePreviousWindowCounter(currentTime) + currentCounter.get() < threshold) {
                slidingWindow.offer(currentTime);
                currentCounter.incrementAndGet();
                return true;
            }
        }

        return false;
    }

    private void refreshSlidingWindow(long currentTime) {
        Long oldestTimestamp = slidingWindow.peek();
        if (oldestTimestamp == null) return;

        long duration = (currentTime - oldestTimestamp) / windowSize;
        if (duration >= 1) {
            currentCounter.set(0);
            currentBasisTime.set((currentTime / windowSize) * windowSize);
        }

        while (duration >= 1) {
            slidingWindow.poll();
            if (slidingWindow.isEmpty()) break;
            duration = (currentTime - oldestTimestamp) / windowSize;
        }
    }

    // 직전 window counter 계산
    private int calculatePreviousWindowCounter(long currentTime) {
        return (int) (calculatePreviousTotalCount() * (1 - (currentTime - currentBasisTime.get()) / windowSize));
    }

    private int calculatePreviousTotalCount() {
        return (int) slidingWindow.stream()
                .filter(timestamp -> timestamp < currentBasisTime.get())
                .count();
    }
}
