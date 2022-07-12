package pattern.circuitbreaker;

public class DefaultCircuitBreaker implements CircuitBreaker {

    private final RemoteService remoteService;
    private final long timeout; // millisecond
    private final int threshold; // 횟수
    private final long retryTimePeriod; // millisecond
    private int failCount;
    private State state;
    private long lastFailTime;
    private String lastFailureResponse;
    private final long FUTURE_TIME = 1000 * 1000 * 1000 * 1000;

    public DefaultCircuitBreaker(RemoteService RemoteService, long timeout, int failThreshold, long retryTimePeriod) {
        this.remoteService = RemoteService;
        this.timeout = timeout;
        this.threshold = failThreshold;
        this.retryTimePeriod = retryTimePeriod * 1000 * 1000;
        this.failCount = 0;
        this.state = State.CLOSED;
        this.lastFailTime = System.nanoTime() + FUTURE_TIME;
    }

    @Override
    public void recordSuccess() {
        this.failCount = 0;
        this.state = State.CLOSED;
        this.lastFailTime = System.nanoTime() + FUTURE_TIME;
    }

    @Override
    public void recordFail(String response) {
        this.failCount += 1;
        this.state = State.OPEN;
        this.lastFailTime = System.nanoTime();
        this.lastFailureResponse = response;
        System.out.println(String.format("failCount = %d, state = %s, lastFailureResponse = %s", failCount, state, lastFailureResponse));
    }

    @Override
    public State getState() {
        evaluateState();
        return this.state;
    }

    @Override
    public String attemptRequest() {
        evaluateState();
        if (state == State.OPEN) {
            return this.lastFailureResponse;
        } else {
            try {
                long startTime = System.nanoTime();
                var result = remoteService.process();
                long finishTime = System.nanoTime();

                if ((finishTime - startTime) / 1000 * 1000 > timeout) {
                    var errorMessage = "takes long...";
                    recordFail(errorMessage);
                } else {
                    recordSuccess();
                }
                return result;
            } catch (Exception e) {
                recordFail(e.getMessage());
                throw e;
            }
        }
    }

    private void evaluateState() {
        // 실패
        if (failCount >= threshold) {
            if ((System.nanoTime() - lastFailTime) > retryTimePeriod) {
                this.state = State.HALF_OPEN;
            } else {
                this.state = State.OPEN;
            }
        } else {
            this.state = State.CLOSED;
        }
    }
}
