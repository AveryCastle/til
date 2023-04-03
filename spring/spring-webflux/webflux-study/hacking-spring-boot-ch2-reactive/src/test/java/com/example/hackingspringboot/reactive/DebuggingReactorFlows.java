package com.example.hackingspringboot.reactive;

import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Hooks;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

@Slf4j
class DebuggingReactorFlows {

    static class SimpleExample {

        @Test
        void reactorFlows() {
            ExecutorService executor = Executors.newSingleThreadExecutor();

            List<Integer> source;
            if (new Random().nextBoolean()) {
                source = IntStream.range(1, 11).boxed().collect(Collectors.toList());
            } else {
                source = Arrays.asList(1, 2, 3, 4);
            }

            try {
                executor.submit(() -> source.get(5)).get();
            } catch (ExecutionException | InterruptedException e) {
                log.error("{}", e);
            } finally {
                executor.shutdown();
            }
        }
    }

    static class ReactorExample {

        @Test
        void reactorFlows() {
            Mono<Integer> source;
            if (new Random().nextBoolean()) {
                source = Flux.range(1, 10).elementAt(5);
            } else {
                source = Flux.just(1, 2, 3, 4).elementAt(5);
            }

            source.subscribeOn(Schedulers.parallel()).block();
        }
    }

    static class ReactorDebuggingExample {

        @Test
        void reactorFlows() {
            Hooks.onOperatorDebug();

            Mono<Integer> source;
            if (new Random().nextBoolean()) {
                source = Flux.range(1, 10).elementAt(5);
            } else {
                source = Flux.just(1, 2, 3, 4).elementAt(5);
            }

            source.subscribeOn(Schedulers.parallel()).block();
        }
    }
}
