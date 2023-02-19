package com.example.hackingspringboot.reactive;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.data.mongodb.core.MongoOperations;
import org.springframework.stereotype.Component;

@Component
public class TemplateDatabaseLoader {

    @Bean
    CommandLineRunner initialize(MongoOperations mongo) {
        return args -> {
            mongo.save(new Item("RM Indigo", "BTS RM 2nd Single Album", 45000));
            mongo.save(new Item("J-Hope In the Box", "BTS J-Hope 2nd Single Album", 55000));
        };
    }
}
