package com.example.springwebfluxstudy.controllers;

import static org.mockito.Mockito.when;

import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.test.web.reactive.server.WebTestClient;

import com.example.springwebfluxstudy.models.User;
import com.example.springwebfluxstudy.services.UserService;

import reactor.core.publisher.Flux;

class UserControllerTest {

    @Test
    void shouldReturnUsers() {
        User[] users = {
            new User("user-1", "Jimin", 28, Integer.MAX_VALUE, "BTS"),
            new User("user-2", "V", 28, Integer.MAX_VALUE, "BTS")
        };
        Flux<User> userFlux = Flux.just(users);

        UserService service = Mockito.mock(UserService.class);
        when(service.getAllUsers()).thenReturn(userFlux);

        WebTestClient testClient = WebTestClient.bindToController(new UserController(service)).build();

        testClient.get().uri("/users")
            .exchange()
            .expectStatus().isOk()
            .expectBody()
            .jsonPath("$").isArray()
            .jsonPath("$").isNotEmpty()
            .jsonPath("$[0].id").isEqualTo(users[0].getId())
            .jsonPath("$[0].name").isEqualTo(users[0].getName())
            .jsonPath("$[1].id").isEqualTo(users[1].getId())
            .jsonPath("$[1].name").isEqualTo(users[1].getName());
    }
}
