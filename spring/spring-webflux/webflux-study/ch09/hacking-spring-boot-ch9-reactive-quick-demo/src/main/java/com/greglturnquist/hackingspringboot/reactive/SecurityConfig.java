package com.greglturnquist.hackingspringboot.reactive;

import java.util.Arrays;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.mongodb.core.MongoOperations;
import org.springframework.security.config.annotation.method.configuration.EnableReactiveMethodSecurity;
import org.springframework.security.config.web.server.ServerHttpSecurity;
import org.springframework.security.core.userdetails.ReactiveUserDetailsService;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.web.server.SecurityWebFilterChain;

@Configuration
@EnableReactiveMethodSecurity
public class SecurityConfig {

    @Bean
    public ReactiveUserDetailsService userDetailsService(UserRepository repository) { // <1>
        return username -> repository.findByName(username) // <2>
            .map(user -> User.withDefaultPasswordEncoder() // <3>
                .username(user.getName()) //
                .password(user.getPassword()) //
                .authorities(user.getRoles().toArray(new String[0])) //
                .build()); // <4>
    }

    // tag::custom-policy[]
    static final String USER = "USER";
    static final String INVENTORY = "INVENTORY";

    @Bean
    SecurityWebFilterChain myCustomSecurityPolicy(ServerHttpSecurity http) { // <1>
        return http //
            .authorizeExchange(exchanges -> exchanges //
//                .pathMatchers(HttpMethod.POST, "/").hasRole(INVENTORY) // @EnableReactiveMethodSecurity 추가로 필요 없어짐.
//                .pathMatchers(HttpMethod.DELETE, "/**").hasRole(INVENTORY)
                .anyExchange().authenticated() // <3>
                .and() //
                .httpBasic() // <4>
                .and() //
                .formLogin()) // <5>
            .csrf().disable() //
            .build();
    }

    @Bean
    CommandLineRunner initialize(MongoOperations operations) { // org.mongodb:mongodb-driver-sync 용
//    CommandLineRunner initialize(ReactiveMongoOperations operations) { // org.mongodb:mongodb-driver-reactivestreams 용
        return args -> {
            operations.save(new com.greglturnquist.hackingspringboot.reactive.User( //
                "tester", "password", Arrays.asList(role(USER))));

            operations.save(new com.greglturnquist.hackingspringboot.reactive.User( //
                "manager", "password", Arrays.asList(role(USER), role(INVENTORY))));
        };
    }

    static String role(String auth) {
        return "ROLE_" + auth;
    }
}
