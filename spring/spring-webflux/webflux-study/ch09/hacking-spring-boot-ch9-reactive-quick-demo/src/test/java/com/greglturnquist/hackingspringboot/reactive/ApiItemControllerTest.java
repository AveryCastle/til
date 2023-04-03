package com.greglturnquist.hackingspringboot.reactive;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.hateoas.config.EnableHypermediaSupport.HypermediaType.HAL;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.reactive.AutoConfigureWebTestClient;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.hateoas.CollectionModel;
import org.springframework.hateoas.EntityModel;
import org.springframework.hateoas.IanaLinkRelations;
import org.springframework.hateoas.RepresentationModel;
import org.springframework.hateoas.config.EnableHypermediaSupport;
import org.springframework.hateoas.config.HypermediaWebTestClientConfigurer;
import org.springframework.hateoas.server.core.TypeReferences.CollectionModelType;
import org.springframework.hateoas.server.core.TypeReferences.EntityModelType;
import org.springframework.http.MediaType;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.web.reactive.server.WebTestClient;
import reactor.test.StepVerifier;

@SpringBootTest()
@EnableHypermediaSupport(type = HAL)
@AutoConfigureWebTestClient
class ApiItemControllerTest {

    @Autowired
    WebTestClient webTestClient;

    @Autowired
    ItemRepository repository;

    @Autowired
    HypermediaWebTestClientConfigurer webClientConfigurer;

    @BeforeEach
    void setUp() {
        this.webTestClient = this.webTestClient.mutateWith(webClientConfigurer);
    }

    @Test
    void noCredentialsFailsAtRoot() {
        webTestClient.get().uri("/api")
            .exchange()
            .expectStatus().isUnauthorized();
    }

    @Test
    @WithMockUser(username = "ada")
    void credentialsWorksOnRoot() {
        webTestClient.get().uri("/api")
            .exchange()
            .expectStatus().isOk()
            .expectBody(String.class)
            .isEqualTo("{\"_links\":{\"self\":{\"href\":\"/api\"},\"item\":{\"href\":\"/api/items\"}}}");
    }

    @Test
    @WithMockUser(username = "alice", roles = {"SOME_OTHER_ROLE"})
    void addingInventoryWithoutProperRoleFails() {
        webTestClient
            .post().uri("/api/items/add")
            .contentType(MediaType.APPLICATION_JSON)
            .bodyValue("{" +
                "\"name\": \"Jimin Face\", " +
                "\"description\": \"Jimin's New Album\", " +
                "\"price\": 39000" + //
                "}")
            .exchange()
            .expectStatus().isForbidden();
    }

    @Test
    @WithMockUser(username = "bob", roles = {"INVENTORY"})
    void addingInventoryWithProperRoleSucceeds() {
        webTestClient
            .post().uri("/api/items/add")
            .contentType(MediaType.APPLICATION_JSON)
            .bodyValue("{" +
                "\"name\": \"Jimin Face\", " +
                "\"description\": \"Jimin's New Album\", " +
                "\"price\": 39000" + //
                "}")
            .exchange()
            .expectStatus().isCreated();

        repository.findByName("Jimin Face")
            .as(StepVerifier::create)
            .expectNextMatches(item -> {
                assertThat(item.getDescription()).isEqualTo("Jimin's New Album");
                assertThat(item.getPrice()).isEqualTo(39000);

                return true;
            })
            .verifyComplete();
    }

    @Test
    @WithMockUser(username = "alice", roles = {"INVENTORY"})
    void navigateToItemWithInventoryAuthority() {
        // api 에 GET 요청.
        RepresentationModel<?> root = webTestClient.get().uri("/api")
            .exchange()
            .expectBody(RepresentationModel.class)
            .returnResult().getResponseBody();

        CollectionModel<EntityModel<Item>> items = webTestClient.get()
            .uri(root.getRequiredLink(IanaLinkRelations.ITEM).toUri())
            .exchange()
            .expectBody(new CollectionModelType<EntityModel<Item>>() {
            })
            .returnResult().getResponseBody();

        assertThat(items.getLinks()).hasSize(2);
        assertThat(items.hasLink(IanaLinkRelations.SELF)).isTrue();
        assertThat(items.hasLink("add")).isTrue();

        // Find the first Item...
        EntityModel<Item> first = items.getContent().iterator().next();

        // 첫 번째 ITEM의 EntityModel 에서 SELF 링크를 통해 첫 번째 Item 획득.
        EntityModel<Item> item = this.webTestClient.get()
            .uri(first.getRequiredLink(IanaLinkRelations.SELF).toUri())
            .exchange()
            .expectBody(new EntityModelType<Item>() {
            })
            .returnResult().getResponseBody();

        assertThat(item.getLinks()).hasSize(3);
        assertThat(item.hasLink(IanaLinkRelations.SELF)).isTrue();
        assertThat(item.hasLink(IanaLinkRelations.ITEM)).isTrue();
        assertThat(item.hasLink("delete")).isTrue();
    }
}
