package pattern.circuitbreaker;

public class EndUserApp {

    /**
     * Program entry point.
     *
     * @param args command line args
     */
    public static void main(String[] args) {
        System.out.println(System.currentTimeMillis());
        SlowRemoteService slowRemoteService = new SlowRemoteService();

        DefaultCircuitBreaker slowServiceCircuitBreaker = new DefaultCircuitBreaker(slowRemoteService, 1000, 2, 3000);

        MonitorService monitorService = new MonitorService();
        monitorService.register(slowServiceCircuitBreaker);

        System.out.println("1. " + monitorService.request());
        System.out.println("2. " + monitorService.request());
        System.out.println(slowServiceCircuitBreaker.getState());

        System.out.println("3. " + monitorService.request());
        System.out.println(slowServiceCircuitBreaker.getState());

        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println(slowServiceCircuitBreaker.getState());

        System.out.println("4. " + monitorService.request());

        System.out.println(slowServiceCircuitBreaker.getState());
    }
}
