package com.example.springdocswagger.user.application.port.out;

import com.example.springdocswagger.user.domain.User;

public interface UserCreatePort {

    User create(String account, String email, String phoneNumber);
}
