package com.example.springdocswagger.user.adapter.out.persistence;

import com.example.springdocswagger.user.application.port.out.UserSearchPort;
import com.example.springdocswagger.user.domain.User;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
@RequiredArgsConstructor
class UserSearchPersistentAdapter implements UserSearchPort {

    private final UserRepository userRepository;

    @Override
    public List<User> searchAll(String orderProperty) {
        return userRepository.findAll(Sort.by(Sort.Order.asc(orderProperty)));
    }
}
