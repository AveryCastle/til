package pattern.circuitbreaker;

public enum State {
    CLOSED,
    HALF_OPEN,
    OPEN;
}
