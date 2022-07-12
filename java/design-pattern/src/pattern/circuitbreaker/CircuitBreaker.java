package pattern.circuitbreaker;

public interface CircuitBreaker {

    State getState();

    void recordSuccess();

    void recordFail(String response);

    String attemptRequest();
}
