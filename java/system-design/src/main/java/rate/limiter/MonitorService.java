package rate.limiter;

public class MonitorService {

    private final RemoteService remoteService;
    private final RateLimiterCreator rateLimiterCreator;

    public MonitorService(RemoteService remoteService, RateLimiterCreator rateLimiterCreator) {
        this.remoteService = remoteService;
        this.rateLimiterCreator = rateLimiterCreator;
        this.rateLimiterCreator.register(remoteService);
    }

    public String greet(String name) {
        System.out.println(rateLimiterCreator.request(name));
        return "ok";
    }
}
