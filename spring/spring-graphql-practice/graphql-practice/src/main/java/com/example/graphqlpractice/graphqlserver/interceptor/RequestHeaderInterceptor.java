package com.example.graphqlpractice.graphqlserver.interceptor;

import java.util.Collections;
import org.springframework.context.annotation.Configuration;
import org.springframework.graphql.server.WebGraphQlInterceptor;
import org.springframework.graphql.server.WebGraphQlRequest;
import org.springframework.graphql.server.WebGraphQlResponse;
import org.springframework.http.HttpHeaders;
import reactor.core.publisher.Mono;

@Configuration
public class RequestHeaderInterceptor implements WebGraphQlInterceptor {

    @Override
    public Mono<WebGraphQlResponse> intercept(WebGraphQlRequest request, Chain chain) {
        String value = request.getHeaders().getFirst(HttpHeaders.AUTHORIZATION);
        request.configureExecutionInput((executionInput, builder) ->
            builder.graphQLContext(Collections.singletonMap("myAuthorization", value)).build());
        return chain.next(request);
    }
}
