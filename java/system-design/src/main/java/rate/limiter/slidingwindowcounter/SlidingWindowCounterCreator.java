package rate.limiter.slidingwindowcounter;

import rate.limiter.RateLimiterCreator;
import rate.limiter.RemoteService;

public class SlidingWindowCounterCreator extends RateLimiterCreator {

    public SlidingWindowCounterCreator(String id, int windowSize, int threshold) {
        super(id, windowSize, threshold);
        BUCKET.put(id, new SlidingWindowCounter(windowSize, threshold));
    }

    public void applicationAccess(String id) {
        if (BUCKET.get(id).grantAccess()) {
            System.out.println(Thread.currentThread().getName() + " -> able to access the application");
        } else {
            System.out.println(Thread.currentThread().getName() + " -> Too many request, Please try after some time");
        }
    }

    @Override
    public void register(RemoteService remoteService) {
        this.remoteService = remoteService;
    }

    @Override
    public String request(String name) {
        if (BUCKET.get(id).grantAccess()) {
            return remoteService.hello(name);
        } else {
            return "circuit breaker open!";
        }
    }
}
