package com.example.springdocswagger.user.application.service;

import com.example.springdocswagger.user.application.port.in.UserCreateUseCase;
import com.example.springdocswagger.user.application.port.in.UserResponse;
import com.example.springdocswagger.user.application.port.out.UserCreatePort;
import com.example.springdocswagger.user.domain.User;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
class UserCreateService implements UserCreateUseCase {

    private final UserCreatePort userCreatePort;

    @Override
    public UserResponse create(String account, String email, String phoneNumber) {
        User createdOne = userCreatePort.create(account, email, phoneNumber);
        return UserResponse.of(createdOne);
    }
}
