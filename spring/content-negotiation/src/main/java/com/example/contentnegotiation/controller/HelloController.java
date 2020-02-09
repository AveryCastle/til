package com.example.contentnegotiation.controller;

import com.example.contentnegotiation.model.User;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class HelloController {

    @GetMapping("/")
    public @ResponseBody
    User user() {
        return new User("성주현", 35);
    }
}
