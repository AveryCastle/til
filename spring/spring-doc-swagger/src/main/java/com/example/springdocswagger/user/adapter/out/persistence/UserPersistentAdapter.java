package com.example.springdocswagger.user.adapter.out.persistence;

import com.example.springdocswagger.user.application.port.out.UserCreatePort;
import com.example.springdocswagger.user.application.port.out.UserSearchPort;
import com.example.springdocswagger.user.domain.User;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
@RequiredArgsConstructor
class UserPersistentAdapter implements UserCreatePort {

    private final UserRepository userRepository;

    @Override
    public User create(String account, String email, String phoneNumber) {
        User user = new User(account, email, phoneNumber);
        return userRepository.save(user);
    }
}
