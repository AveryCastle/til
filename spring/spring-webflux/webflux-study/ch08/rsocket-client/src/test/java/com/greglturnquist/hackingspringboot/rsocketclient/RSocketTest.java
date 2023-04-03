package com.greglturnquist.hackingspringboot.rsocketclient;

import static org.assertj.core.api.Assertions.assertThat;
import java.util.List;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.reactive.AutoConfigureWebTestClient;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.reactive.server.WebTestClient;
import reactor.test.StepVerifier;

@SpringBootTest
@AutoConfigureWebTestClient
class RSocketTest {

    @Autowired
    WebTestClient webTestClient;

    @Autowired
    ItemRepository repository;

    @Test
    void verifyRemoteOperationsThroughRSocketRequestResponse() throws InterruptedException {
        // 데이터 초기화
        repository.deleteAll()
            .as(StepVerifier::create)
            .verifyComplete();

        // 새 Item 생성
        webTestClient.post().uri("/items/request-response")
            .bodyValue(new Item("Jimin Face", "Jimin Single Album", 45000))
            .exchange()
            .expectStatus().isCreated()
            .expectBody(Item.class)
            .value(item -> {
                assertThat(item.getId()).isNotNull();
                assertThat(item.getName()).isEqualTo("Jimin Face");
                assertThat(item.getDescription()).isEqualTo("Jimin Single Album");
                assertThat(item.getPrice()).isEqualTo(45000);
            });

        Thread.sleep(500);

        repository.findAll()
            .as(StepVerifier::create)
            .expectNextMatches(item -> {
                assertThat(item.getId()).isNotNull();
                assertThat(item.getName()).isEqualTo("Jimin Face");
                assertThat(item.getDescription()).isEqualTo("Jimin Single Album");
                assertThat(item.getPrice()).isEqualTo(45000);

                return true;
            })
            .verifyComplete();
    }

    @Test
    void verifyRemoteOperationsThroughRSocketRequestStream() {
        repository.deleteAll().block();

        List<Item> items = IntStream.rangeClosed(1, 3)
            .mapToObj(i -> new Item("name-" + i, "description-" + i, i))
            .collect(Collectors.toList());

        repository.saveAll(items).blockLast();

        webTestClient.get().uri("/items/request-stream")
            .accept(MediaType.APPLICATION_NDJSON)
            .exchange()
            .expectStatus().isOk()
            .returnResult(Item.class)
            .getResponseBody()
            .as(StepVerifier::create)
            .expectNextMatches(itemPredicate("1"))
            .expectNextMatches(itemPredicate("2"))
            .expectNextMatches(itemPredicate("3"))
            .verifyComplete();
    }

    @Test
    void verifyRemoteOperationsThroughRSocketFireAndForget() throws InterruptedException {
        repository.deleteAll()
            .as(StepVerifier::create)
            .verifyComplete();

        webTestClient.post().uri("/items/fire-and-forget")
            .bodyValue(new Item("JIMIN Face", "JIMIN FIRST SINGLE", 45000))
            .exchange()
            .expectStatus().isCreated()
            .expectBody().isEmpty();
        
        Thread.sleep(500);

        repository.findAll()
            .as(StepVerifier::create)
            .expectNextMatches(item -> {
                assertThat(item.getId()).isNotNull();
                assertThat(item.getName()).isEqualTo("JIMIN Face");
                assertThat(item.getDescription()).isEqualTo("JIMIN FIRST SINGLE");
                assertThat(item.getPrice()).isEqualTo(45000);

                return true;
            })
            .verifyComplete();
    }

    private Predicate<Item> itemPredicate(String num) {
        return item -> {
            assertThat(item.getName()).startsWith("name");
            assertThat(item.getName()).endsWith(num);
            assertThat(item.getDescription()).startsWith("description");
            assertThat(item.getDescription()).endsWith(num);
            assertThat(item.getPrice()).isPositive();

            return true;
        };
    }
}
