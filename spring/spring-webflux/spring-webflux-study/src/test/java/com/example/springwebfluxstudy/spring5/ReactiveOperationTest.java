package com.example.springwebfluxstudy.spring5;

import java.time.Duration;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Objects;
import org.junit.jupiter.api.Test;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;
import reactor.test.StepVerifier;

class ReactiveOperationTest {

    @Test
    void zipFluxesToObject() {
        Flux<String> youngerFlux = Flux.just("Jimin", "V", "JK");
        Flux<String> olderFlux = Flux.just("J-Hope", "RM", "SUGA", "Jin");

        Flux<String> zippedFlux = Flux.zip(youngerFlux, olderFlux, (y, o) -> y + " is younger than " + o);

        StepVerifier.create(zippedFlux)
            .expectNext("Jimin is younger than J-Hope")
            .expectNext("V is younger than RM")
            .expectNext("JK is younger than SUGA")
            .verifyComplete();
    }

    @Test
    void firstFlux() {
        Flux<String> slowFlux = Flux.just("Jimin", "V", "JK")
            .delaySubscription(Duration.ofMillis(100));
        Flux<String> fastFlux = Flux.just("J-Hope", "RM", "SUGA", "Jin");

        Flux<String> fistFlux = Flux.firstWithSignal(slowFlux, fastFlux);

        StepVerifier.create(fistFlux)
            .expectNext("J-Hope")
            .expectNext("RM")
            .expectNext("SUGA")
            .expectNext("Jin")
            .verifyComplete();
    }

    @Test
    void skipAFew() {
        Flux<String> skipFlux = Flux.just(
                "Jimin", "V", "JK", "J-Hope", "RM", "SUGA", "Jin")
            .skip(3);

        StepVerifier.create(skipFlux)
            .expectNext("J-Hope")
            .expectNext("RM")
            .expectNext("SUGA")
            .expectNext("Jin")
            .verifyComplete();
    }

    @Test
    void skipAFewSeconds() {
        Flux<String> skipFlux = Flux.just(
                "Jimin", "V", "JK", "J-Hope", "RM", "SUGA", "Jin")
            .delayElements(Duration.ofMillis(300))
            .skip(Duration.ofSeconds(1));

        StepVerifier.create(skipFlux)
            .expectNext("J-Hope", "RM", "SUGA", "Jin")
            .verifyComplete();
    }

    @Test
    void take() {
        Flux<String> takeFlux = Flux.just(
                "Jimin", "V", "JK", "J-Hope", "RM", "SUGA", "Jin")
            .take(3);

        StepVerifier.create(takeFlux)
            .expectNext("Jimin", "V", "JK")
            .verifyComplete();
    }

    @Test
    void takeDuration() {
        Flux<String> takeFlux = Flux.just(
                "Jimin", "V", "JK", "J-Hope", "RM", "SUGA", "Jin")
            .delayElements(Duration.ofMillis(200))
            .take(Duration.ofMillis(1000));

        StepVerifier.create(takeFlux)
            .expectNext("Jimin", "V", "JK", "J-Hope")
            .verifyComplete();
    }

    @Test
    void filter() {
        Flux<String> flux = Flux.just(
                "Jimin", "V", "JK", "J-Hope", "RM", "SUGA", "Jin")
            .filter(member -> member.startsWith("J"));

        StepVerifier.create(flux)
            .expectNext("Jimin", "JK", "J-Hope", "Jin")
            .verifyComplete();
    }

    @Test
    void distinct() {
        Flux<String> distinctFlux = Flux.just(
                "Jimin", "V", "JK", "V", "RM", "JK", "Jimin")
            .distinct();

        StepVerifier.create(distinctFlux)
            .expectNext("Jimin", "V", "JK", "RM")
            .verifyComplete();
    }

    @Test
    void map() {
        Flux<String> mapFlux = Flux.just(
                "Jimin", "V", "JK", "J-Hope", "RM", "SUGA", "Jin")
            .map(member -> member + " of BTS");

        StepVerifier.create(mapFlux)
            .expectNext("Jimin of BTS")
            .expectNext("V of BTS")
            .expectNext("JK of BTS")
            .expectNext("J-Hope of BTS")
            .expectNext("RM of BTS")
            .expectNext("SUGA of BTS")
            .expectNext("Jin of BTS")
            .verifyComplete();
    }

    @Test
    void flapMap() {
        Flux<BTS> flatMapFlux = Flux.just(
                "Park Jimin", "Kim V", "Jeon JK", "Jeong J-Hope", "Kim RM", "Min SUGA", "Kim Jin")
            .flatMap(member -> Mono.just(member)
                .map(p -> {
                    String[] split = p.split("\\s");
                    return new BTS(split[0], split[1]);
                }))
            .subscribeOn(Schedulers.parallel());

        List<BTS> bts = Arrays.asList(
            new BTS("Park", "Jimin"),
            new BTS("Kim", "V"),
            new BTS("Jeon", "JK"),
            new BTS("Jeong", "J-Hope"),
            new BTS("Kim", "RM"),
            new BTS("Min", "SUGA"),
            new BTS("Kim", "Jin")
        );
        StepVerifier.create(flatMapFlux)
            .expectNextMatches(p -> bts.contains(p))
            .expectNextMatches(p -> bts.contains(p))
            .expectNextMatches(p -> bts.contains(p))
            .expectNextMatches(p -> bts.contains(p))
            .expectNextMatches(p -> bts.contains(p))
            .expectNextMatches(p -> bts.contains(p))
            .expectNextMatches(p -> bts.contains(p))
            .verifyComplete();
    }

    @Test
    void buffer() {
        Flux<String> stringFlux = Flux.just(
            "Jimin", "V", "JK", "J-Hope", "RM", "SUGA", "Jin");
        Flux<List<String>> bufferedFlux = stringFlux.buffer(3);

        StepVerifier.create(bufferedFlux)
            .expectNext(Arrays.asList("Jimin", "V", "JK"))
            .expectNext(Arrays.asList("J-Hope", "RM", "SUGA"))
            .expectNext(Arrays.asList("Jin"))
            .verifyComplete();
    }

    @Test
    void bufferWithFlatMap() {
        Flux<String> stringFlux = Flux.just(
            "Jimin", "v", "jk", "Jin", "j-hop", "rm", "suga");
        stringFlux.buffer(3)
            .flatMap(member ->
                Flux.fromIterable(member)
                    .map(name -> name.toUpperCase(Locale.ROOT))
                    .subscribeOn(Schedulers.parallel())
                    .log()
            ).subscribe();
    }

    @Test
    void collectList() {
        Flux<String> stringFlux = Flux.just("Jimin", "V", "JK", "J-Hope", "RM", "SUGA", "Jin");

        Mono<List<String>> listMono = stringFlux.collectList();

        StepVerifier.create(listMono)
            .expectNext(Arrays.asList("Jimin", "V", "JK", "J-Hope", "RM", "SUGA", "Jin"))
            .verifyComplete();
    }

    @Test
    void collectMap() {
        Flux<String> stringFlux = Flux.just("Jimin", "V", "JK", "J-Hope", "RM", "SUGA", "Jin");

        Mono<Map<Character, String>> mapMono = stringFlux.collectMap(a -> a.charAt(0));

        StepVerifier.create(mapMono)
            .expectNextMatches(map -> {
                boolean result = true;
                Iterator<String> iterator = map.values().iterator();
                List<String> values = Arrays.asList("V", "RM", "SUGA", "Jin");
                while (iterator.hasNext()) {
                    if (!values.contains(iterator.next())) {
                        result = false;
                        break;
                    }
                }
                return map.size() == 4 && result;
            })
            .verifyComplete();
    }

    class BTS {

        private String seong;
        private String name;

        public BTS(String seong, String name) {
            this.seong = seong;
            this.name = name;
        }

        public BTS(String name) {
            this.name = name;
        }

        public String getSeong() {
            return seong;
        }

        public String getName() {
            return name;
        }

        @Override
        public String toString() {
            return "BTS{" +
                "seong='" + seong + '\'' +
                ", name='" + name + '\'' +
                '}';
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) {
                return true;
            }
            if (o == null || getClass() != o.getClass()) {
                return false;
            }

            BTS bts = (BTS) o;

            if (!Objects.equals(seong, bts.seong)) {
                return false;
            }
            return name.equals(bts.name);
        }

        @Override
        public int hashCode() {
            int result = seong != null ? seong.hashCode() : 0;
            result = 31 * result + name.hashCode();
            return result;
        }
    }
}
