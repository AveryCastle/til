package rate.limiter;

import java.util.HashMap;
import java.util.Map;

public abstract class RateLimiterCreator {

    protected RemoteService remoteService;

    protected final Map<String, RateLimiter> BUCKET = new HashMap<>();

    protected final String id;
    protected final int windowSize;
    protected final int threshold;

    protected RateLimiterCreator(String id, int windowSize, int threshold) {
        this.id = id;
        this.windowSize = windowSize;
        this.threshold = threshold;
    }

    public abstract String request(String name);

    public abstract void register(RemoteService remoteService);
}
