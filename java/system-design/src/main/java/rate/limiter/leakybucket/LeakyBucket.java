package rate.limiter.leakybucket;

import rate.limiter.RateLimiter;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;

public class LeakyBucket implements RateLimiter {

    private final int bucketCapacity;
    private final int outflowRateInSecond;
    private final BlockingQueue<Integer> queue;
    private final AtomicLong lastLeakTime;
    private final AtomicInteger processedCount;

    public LeakyBucket(int bucketCapacity, int outflowRateInSecond) {
        this.bucketCapacity = bucketCapacity;
        this.outflowRateInSecond = outflowRateInSecond;
        queue = new LinkedBlockingQueue<>(bucketCapacity);
        lastLeakTime = new AtomicLong(System.currentTimeMillis());
        processedCount = new AtomicInteger(0);
    }

    @Override
    public boolean grantAccess() {
        refreshBucket();
        if (queue.remainingCapacity() > 0) {
            queue.add(1);
            return true;
        }
        return false;
    }

    private void refreshBucket() {
        long currentTime = System.currentTimeMillis();
        int processCapacity = (int) ((currentTime - lastLeakTime.get()) / 1000) * outflowRateInSecond;

        if (currentTime - lastLeakTime.get() >= 1000) {
//            System.out.println(String.format("over. %s -> processCapacity = %d, queue remain Size = %d", Thread.currentThread().getName(), processCapacity, queue.remainingCapacity()));
            processedCount.set(0);
        }

        while (processedCount.get() < processCapacity) {
            queue.poll();
            int count = processedCount.incrementAndGet();
            lastLeakTime.set(currentTime);
//            System.out.println(String.format("%s -> processCapacity = %d, queue size = %d", Thread.currentThread().getName(), count, queue.remainingCapacity()));
        }
    }
}
