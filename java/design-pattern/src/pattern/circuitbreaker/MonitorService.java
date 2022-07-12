package pattern.circuitbreaker;

public class MonitorService {

    private CircuitBreaker circuitBreaker;

    public void register(CircuitBreaker circuitBreaker) {
        this.circuitBreaker = circuitBreaker;
    }

    public String request() {
        try {
            return circuitBreaker.attemptRequest();
        } catch (Exception e) {
            return e.getMessage();
        }
    }
}
