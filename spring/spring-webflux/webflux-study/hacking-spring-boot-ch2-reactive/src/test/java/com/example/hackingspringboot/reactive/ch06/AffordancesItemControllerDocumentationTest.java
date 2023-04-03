package com.example.hackingspringboot.reactive.ch06;

import static org.mockito.Mockito.when;
import static org.springframework.restdocs.operation.preprocess.Preprocessors.preprocessResponse;
import static org.springframework.restdocs.operation.preprocess.Preprocessors.prettyPrint;
import static org.springframework.restdocs.webtestclient.WebTestClientRestDocumentation.document;
import com.example.hackingspringboot.reactive.InventoryService;
import com.example.hackingspringboot.reactive.Item;
import com.example.hackingspringboot.reactive.ItemRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.restdocs.AutoConfigureRestDocs;
import org.springframework.boot.test.autoconfigure.web.reactive.WebFluxTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.hateoas.MediaTypes;
import org.springframework.test.web.reactive.server.WebTestClient;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * @author Greg Turnquist
 */
// tag::intro[]
@WebFluxTest(controllers = AffordancesItemController.class) // <1>
@AutoConfigureRestDocs // <2>
public class AffordancesItemControllerDocumentationTest {

    @Autowired
    private WebTestClient webTestClient; // <3>

    @MockBean
    InventoryService service; // <4>

    @MockBean
    ItemRepository repository; // <5>
    // end::intro[]

    // tag::affordances[]
    @Test
    void findSingleItemAffordances() {
        when(repository.findById("item-1")).thenReturn(Mono.just( //
            new Item("item-1", "Alf alarm clock", "nothing I really need", 19.99)));

        this.webTestClient.get().uri("/affordances/items/item-1") // <1>
            .accept(MediaTypes.HAL_FORMS_JSON) // <2>
            .exchange() //
            .expectStatus().isOk() //
            .expectBody() //
            .consumeWith(document("single-item-affordances", //
                preprocessResponse(prettyPrint()))); // <3>
    }
    // end::affordances[]

    // tag::affordances2[]
    @Test
    void findAggregateRootItemAffordances() {
        when(repository.findAll()).thenReturn(Flux.just( //
            new Item("Alf alarm clock", "nothing I really need", 19.99)));
        when(repository.findById((String) null)).thenReturn(Mono.just( //
            new Item("item-1", "Alf alarm clock", "nothing I really need", 19.99)));

        this.webTestClient.get().uri("/affordances/items") // <1>
            .accept(MediaTypes.HAL_FORMS_JSON) // <2>
            .exchange() //
            .expectStatus().isOk() //
            .expectBody() //
            .consumeWith(document("aggregate-root-affordances", preprocessResponse(prettyPrint()))); // <3>
    }
    // end::affordances2[]

}
