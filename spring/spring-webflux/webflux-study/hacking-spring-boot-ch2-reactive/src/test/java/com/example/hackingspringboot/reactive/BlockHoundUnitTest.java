package com.example.hackingspringboot.reactive;

import static org.assertj.core.api.Assertions.assertThat;
import java.time.Duration;
import org.junit.jupiter.api.Test;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

class BlockHoundUnitTest {

    @Test
    void threadSleepIsABlockingCall() {
        Mono.delay(Duration.ofSeconds(1)) // <1>
            .flatMap(tick -> {
                try {
                    Thread.sleep(10); // <2>
                    return Mono.just(true);
                } catch (InterruptedException e) {
                    return Mono.error(e);
                }
            }) //
            .as(StepVerifier::create) //
//            .verifyComplete();
            .verifyErrorMatches(throwable -> {
                assertThat(throwable.getMessage()) //
                    .contains("Blocking call! java.lang.Thread.sleep");
                return true;
            });
    }
}
