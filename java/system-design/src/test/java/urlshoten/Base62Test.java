package urlshoten;

import org.junit.jupiter.api.Test;

import java.util.stream.IntStream;

class Base62Test {

    @Test
    void encoding() {
        IntStream.rangeClosed(0, 100).forEach(el -> {
            System.out.println(Base62.encoding(el));
        });
    }
}
