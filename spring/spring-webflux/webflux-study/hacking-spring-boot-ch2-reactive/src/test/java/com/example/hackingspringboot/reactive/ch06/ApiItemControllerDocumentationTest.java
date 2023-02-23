package com.example.hackingspringboot.reactive.ch06;

import static org.mockito.ArgumentMatchers.any;
import static org.springframework.restdocs.operation.preprocess.Preprocessors.preprocessResponse;
import static org.springframework.restdocs.operation.preprocess.Preprocessors.prettyPrint;
import static org.springframework.restdocs.webtestclient.WebTestClientRestDocumentation.document;
import static reactor.core.publisher.Mono.when;
import com.example.hackingspringboot.reactive.InventoryService;
import com.example.hackingspringboot.reactive.Item;
import com.example.hackingspringboot.reactive.ItemRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.restdocs.AutoConfigureRestDocs;
import org.springframework.boot.test.autoconfigure.web.reactive.WebFluxTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.web.reactive.server.WebTestClient;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@ExtendWith(SpringExtension.class)
@WebFluxTest(controllers = ApiItemController.class)
@AutoConfigureRestDocs
class ApiItemControllerDocumentationTest {

    @Autowired
    private WebTestClient webTestClient;

    @MockBean
    private InventoryService inventoryService;

    @MockBean
    private ItemRepository repository;

    @Test
    void findingAllItems() {
        when(repository.findAll()).thenReturn( // <1>
            Flux.just(new Item("item-1", "Alf alarm clock", //
                "nothing I really need", 19.99)));

        this.webTestClient.get().uri("/api/items") //
            .exchange() //
            .expectStatus().isOk() //
            .expectBody() //
            .consumeWith(document("findAll", preprocessResponse(prettyPrint()))); // <2>
    }
    // end::test1[]

    // tag::test2[]
    @Test
    void postNewItem() {
        when(repository.save(any())).thenReturn( //
            Mono.just(new Item("1", "Alf alarm clock", "nothing important", 19.99)));

        this.webTestClient.post().uri("/api/items") // <1>
            .bodyValue(new Item("Alf alarm clock", "nothing important", 19.99)) // <2>
            .exchange() //
            .expectStatus().isCreated() // <3>
            .expectBody() //
            .consumeWith(document("post-new-item", preprocessResponse(prettyPrint()))); // <4>
    }
    // end::test2[]

    // tag::test3[]
    @Test
    void findOneItem() {
        when(repository.findById("item-1")).thenReturn( //
            Mono.just(new Item("item-1", "Alf alarm clock", "nothing I really need", 19.99))); // <1>

        this.webTestClient.get().uri("/api/items/item-1") //
            .exchange() //
            .expectStatus().isOk() //
            .expectBody() //
            .consumeWith(document("findOne", preprocessResponse(prettyPrint()))); // <2>
    }
    // end::test3[]

    @Test
    void updateItem() {
        when(repository.save(any())).thenReturn( //
            Mono.just(new Item("1", "Alf alarm clock", "updated", 19.99)));

        this.webTestClient.put().uri("/api/items/1") // <1>
            .bodyValue(new Item("Alf alarm clock", "updated", 19.99)) // <2>
            .exchange() //
            .expectStatus().isOk() // <3>
            .expectBody() //
            .consumeWith(document("update-item", preprocessResponse(prettyPrint()))); // <4>
    }
}
