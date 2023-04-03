package com.example.springwebfluxstudy.configurations;

import static org.springframework.web.reactive.function.server.RequestPredicates.DELETE;
import static org.springframework.web.reactive.function.server.RequestPredicates.GET;
import static org.springframework.web.reactive.function.server.RequestPredicates.POST;
import static org.springframework.web.reactive.function.server.RequestPredicates.PUT;
import static org.springframework.web.reactive.function.server.RequestPredicates.accept;
import static org.springframework.web.reactive.function.server.RequestPredicates.contentType;
import static org.springframework.web.reactive.function.server.RouterFunctions.route;
import static org.springframework.web.reactive.function.server.ServerResponse.ok;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.MediaType;
import org.springframework.web.reactive.function.server.RouterFunction;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;

import com.example.springwebfluxstudy.handlers.UserHandler;
import com.example.springwebfluxstudy.models.User;
import com.example.springwebfluxstudy.services.UserService;

import lombok.RequiredArgsConstructor;
import reactor.core.publisher.Mono;

@Configuration
@RequiredArgsConstructor
public class RouterConfiguration {

    private final UserService userService;

    @Bean
    RouterFunction<ServerResponse> routes(UserHandler handler) {
        return route(GET("/handler/users").and(accept(MediaType.APPLICATION_JSON)), handler::getAllUsers)
            .andRoute(GET("/handler/users/stream").and(contentType(MediaType.TEXT_EVENT_STREAM)), handler::getAllUsers)
            .andRoute(GET("/handler/users/{userId}").and(accept(MediaType.APPLICATION_JSON)), handler::getUserById)
            .andRoute(POST("/handler/users").and(accept(MediaType.APPLICATION_JSON)), handler::create)
            .andRoute(PUT("/handler/users/{userId}").and(contentType(MediaType.APPLICATION_JSON)), handler::updateUserById)
            .andRoute(DELETE("/handler/users/{userId}").and(accept(MediaType.APPLICATION_JSON)), handler::deleteUserById)
            .andRoute(GET("/recents"), this::recents);
    }

    Mono<ServerResponse> recents(ServerRequest request) {
        return ServerResponse.ok().body(userService.getAllUsers().take(3), User.class);
    }

    @Bean
    public RouterFunction<?> helloRouterFunction() {
        return route(GET("/hello"),
            request -> ok().body(Mono.just("Hello, World!"), String.class))
            .andRoute(GET("/bye"),
                request -> ok().body(Mono.just("See ya!"), String.class));
    }
}
