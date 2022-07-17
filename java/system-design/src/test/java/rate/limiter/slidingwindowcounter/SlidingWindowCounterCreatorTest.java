package rate.limiter.slidingwindowcounter;

import org.junit.jupiter.api.Test;
import rate.limiter.MonitorService;
import rate.limiter.SlowRemoteService;

import java.util.stream.IntStream;

class SlidingWindowCounterCreatorTest {

    @Test
    void slidingWindowCounter() {
        MonitorService monitorService = new MonitorService(new SlowRemoteService(), new SlidingWindowCounterCreator("greet", 1000, 5));

        IntStream.rangeClosed(0, 20).parallel().forEach(el -> {
            monitorService.greet(el + "");
        });
    }
}
