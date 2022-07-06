package com.example.aoppractice2.repository;

import com.example.aoppractice2.domain.User;

import org.springframework.data.repository.Repository;

public interface UserRepository extends Repository<User, Long> {

    User findByLoginId(String loginId);

    User save(User user);
}
