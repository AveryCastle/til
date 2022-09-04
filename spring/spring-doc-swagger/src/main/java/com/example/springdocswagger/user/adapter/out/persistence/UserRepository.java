package com.example.springdocswagger.user.adapter.out.persistence;

import com.example.springdocswagger.user.domain.User;
import org.springframework.data.jpa.repository.JpaRepository;

interface UserRepository extends JpaRepository<User, Long> {
}
