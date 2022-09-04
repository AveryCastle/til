package com.example.springdocswagger.user.application.port.in;

public interface UserCreateUseCase {
    UserResponse create(String account, String email, String phoneNumber);
}
