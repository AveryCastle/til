package com.example.springwebfluxstudy.repositories;

import com.example.springwebfluxstudy.models.User;
import org.springframework.data.mongodb.repository.ReactiveMongoRepository;

public interface UserRepository extends ReactiveMongoRepository<User, String> {

}
