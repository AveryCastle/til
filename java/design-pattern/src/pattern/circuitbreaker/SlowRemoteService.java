package pattern.circuitbreaker;

public class SlowRemoteService implements RemoteService {

    private static int callCount = 0;

    @Override
    public String process() {
        callCount++;
        if (callCount < 3) {
            try {
                Thread.sleep(2000);
                System.out.println("SlowRemoteService is slowing...");
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        return "Hello, I'm A. I'm processing something.";
    }
}
