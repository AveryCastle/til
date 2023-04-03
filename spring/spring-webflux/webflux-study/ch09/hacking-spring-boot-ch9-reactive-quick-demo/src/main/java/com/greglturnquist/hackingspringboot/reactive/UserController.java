package com.greglturnquist.hackingspringboot.reactive;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

@RestController
@RequiredArgsConstructor
public class UserController {

    private final UserRepository repository;

    @GetMapping("/users/{name}")
    Mono<User> findUser(@PathVariable String name) {
        return repository.findByName(name);
    }
}
