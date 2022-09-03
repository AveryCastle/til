package com.example.springdocswagger.user.application.service;

import com.example.springdocswagger.user.application.port.in.UserResponse;
import com.example.springdocswagger.user.application.port.in.UserSearchUseCase;
import com.example.springdocswagger.user.application.port.out.UserSearchPort;
import com.example.springdocswagger.user.domain.User;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
class UserSearchService implements UserSearchUseCase {

    private final UserSearchPort userSearchPort;

    @Override
    public List<UserResponse> searchAll(final String ordering) {
        List<User> users = userSearchPort.searchAll(ordering);
        return users.stream()
                .map(user -> UserResponse.of(user))
                .toList();
    }
}
