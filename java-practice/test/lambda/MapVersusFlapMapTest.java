package lambda;


import static java.util.Arrays.asList;
import static org.junit.Assert.assertEquals;

import org.junit.Test;

import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import static java.util.Arrays.asList;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class MapVersusFlapMapTest {

    @Test
    public void compare() {
        List<String> stringList = Stream.of("abc", "lmn", "xyz").map(String::toUpperCase).collect(Collectors.toList());
        assertEquals(asList("ABC", "LMN", "XYZ"), stringList);

        List<String> collect = Stream.of(asList("abc"), asList("lmn"), asList("xyz"))
                .flatMap(List::stream).map(String::toUpperCase)
                .collect(Collectors.toList());
        assertEquals(asList("ABC", "LMN", "XYZ"), collect);
    }
}
