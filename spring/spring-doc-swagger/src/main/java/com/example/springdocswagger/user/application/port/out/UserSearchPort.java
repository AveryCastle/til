package com.example.springdocswagger.user.application.port.out;

import com.example.springdocswagger.user.domain.User;

import java.util.List;

public interface UserSearchPort {
    List<User> searchAll(final String orderProperty);
}
