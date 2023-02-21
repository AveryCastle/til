package com.example.hackingspringboot.reactive;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.when;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.reactive.WebFluxTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.reactive.server.WebTestClient;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@WebFluxTest(HomeController.class)
class HomeControllerSliceTest {

    @Autowired
    private WebTestClient client;

    @MockBean
    private InventoryService inventoryService;

    @MockBean
    private CartService cartService;

    @Test
    void homePage() {
        when(inventoryService.getInventory()).thenReturn(Flux.just( //
            new Item("id1", "name1", "desc1", 1.99), //
            new Item("id2", "name2", "desc2", 9.99) //
        ));
        when(inventoryService.getCart("My Cart")) //
            .thenReturn(Mono.just(new Cart("My Cart")));

        client.get().uri("/").exchange() //
            .expectStatus().isOk() //
            .expectBody(String.class) //
            .consumeWith(exchangeResult -> {
                assertThat( //
                    exchangeResult.getResponseBody()).contains("My Cart");
//                assertThat( //
//                    exchangeResult.getResponseBody()).contains("action=\"/add/id2\"");
            });
    }
}
