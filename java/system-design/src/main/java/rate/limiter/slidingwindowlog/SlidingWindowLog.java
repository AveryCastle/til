package rate.limiter.slidingwindowlog;

import rate.limiter.RateLimiter;

import java.text.SimpleDateFormat;
import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;

public class SlidingWindowLog implements RateLimiter {

    private final SimpleDateFormat simpleDateFormat = new SimpleDateFormat("HH:mm:ss");

    private final Queue<Long> slidingWindow;
    private final int timeWindowInSeconds;
    private final int bucketCapacity;

    public SlidingWindowLog(int timeWindowInSeconds, int bucketCapacity) {
        this.timeWindowInSeconds = timeWindowInSeconds;
        this.bucketCapacity = bucketCapacity;
        this.slidingWindow = new ConcurrentLinkedQueue<>();
    }

    @Override
    public boolean grantAccess() {
        long currentTime = System.currentTimeMillis();
        checkAndUpdateSlidingWindow(currentTime);
        if (slidingWindow.size() < bucketCapacity) {
            this.slidingWindow.offer(currentTime);
            return true;
        }
        return false;
    }

    private void checkAndUpdateSlidingWindow(long currentTime) {
        if (slidingWindow.isEmpty()) return;

        long calculatedTime = (currentTime - slidingWindow.peek()) / 1000;
//        System.out.println(String.format("%s -> calculatedTime = %d, slidingWindow size = %d", simpleDateFormat.format(new Date(currentTime)), calculatedTime, slidingWindow.size()));
        while (calculatedTime >= timeWindowInSeconds) {
            slidingWindow.poll();
            if (slidingWindow.isEmpty()) break;
            calculatedTime = (currentTime - slidingWindow.peek()) / 1000;
//            System.out.println(String.format("%s -> calculatedTime = %d, slidingWindow size = %d", simpleDateFormat.format(new Date(currentTime)), calculatedTime, slidingWindow.size()));
        }
    }
}
