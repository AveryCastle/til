package com.example.kotlinindepthbook.controller

import com.example.kotlinindepthbook.domain.User
import com.example.kotlinindepthbook.service.UserService
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/users")
class UserController(private val userService: UserService) {

    @GetMapping
    fun searchUser(username: String): User? {
        return userService.searchUserByUsername(username)
    }
}
