package com.example.aoppractice2.controller;

import com.example.aoppractice2.domain.User;
import com.example.aoppractice2.service.UserService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/users")
public class UserController {

    @Autowired
    private UserService userService;

    @PostMapping("")
    public User create(@RequestBody User user) {
        return userService.create(user);
    }

    @GetMapping("")
    public User login(@RequestParam String loginId, @RequestParam String password) throws Exception {
        return userService.login(loginId, password);
    }

}
