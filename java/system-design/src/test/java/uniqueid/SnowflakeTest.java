package uniqueid;

import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.stream.IntStream;

class SnowflakeTest {

    @Test
    void uniqueId() {
        ExecutorService executorService = Executors.newFixedThreadPool(20);
        IntStream.rangeClosed(0, 100).parallel().forEach(el -> {
            long uniqueId = Snowflake.nextValue(3, 12);
            System.out.println(uniqueId);
//            Arrays.stream(Snowflake.parse(uniqueId)).forEach(element -> System.out.print(element + " : "));
//            System.out.println("\n");
        });

        executorService.shutdown();
    }
}
