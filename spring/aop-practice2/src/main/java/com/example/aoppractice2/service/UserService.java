package com.example.aoppractice2.service;

import com.example.aoppractice2.domain.User;
import com.example.aoppractice2.repository.UserRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    public User login(String loginId, String password) throws Exception {
        User foundOne = userRepository.findByLoginId(loginId);

        if (!foundOne.getPassword().equals(password)) {
            throw new Exception("wrong password");
        }

        return foundOne;
    }

    public User create(User user) {
        return userRepository.save(user);
    }
}
