package rate.limiter;

public class SlowRemoteService implements RemoteService {

    @Override
    public String hello(String name) {
//        try {
//            Thread.sleep(500);
//        } catch (InterruptedException e) {
//            e.printStackTrace();
//        }
        return "Hello, " + name;
    }
}
