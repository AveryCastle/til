package pattern.circuitbreaker;

public class RemoteServiceException extends Exception {

    public RemoteServiceException(String message) {
        super(message);
    }
}
