package com.example.springwebfluxstudy.configurations;

import static org.springframework.web.reactive.function.server.RequestPredicates.DELETE;
import static org.springframework.web.reactive.function.server.RequestPredicates.GET;
import static org.springframework.web.reactive.function.server.RequestPredicates.POST;
import static org.springframework.web.reactive.function.server.RequestPredicates.PUT;
import static org.springframework.web.reactive.function.server.RequestPredicates.accept;
import static org.springframework.web.reactive.function.server.RequestPredicates.contentType;
import static org.springframework.web.reactive.function.server.RouterFunctions.route;
import com.example.springwebfluxstudy.handlers.UserHandler;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.MediaType;
import org.springframework.web.reactive.function.server.RouterFunction;
import org.springframework.web.reactive.function.server.ServerResponse;

@Configuration
public class RouterConfiguration {

    @Bean
    RouterFunction<ServerResponse> routes(UserHandler handler) {
        return route(GET("/handler/users").and(accept(MediaType.APPLICATION_JSON)), handler::getAllUsers)
            .andRoute(GET("/handler/users/stream").and(contentType(MediaType.TEXT_EVENT_STREAM)), handler::getAllUsers)
            .andRoute(GET("/handler/users/{userId}").and(accept(MediaType.APPLICATION_JSON)), handler::getUserById)
            .andRoute(POST("/handler/users").and(accept(MediaType.APPLICATION_JSON)), handler::create)
            .andRoute(PUT("/handler/users/{userId}").and(contentType(MediaType.APPLICATION_JSON)), handler::updateUserById)
            .andRoute(DELETE("/handler/users/{userId}").and(accept(MediaType.APPLICATION_JSON)), handler::deleteUserById);
    }
}
