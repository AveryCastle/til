package com.example.kotlinindepthbook.service

import com.example.kotlinindepthbook.domain.User
import com.example.kotlinindepthbook.repository.UserRepository
import lombok.extern.slf4j.Slf4j
import org.slf4j.Logger
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Service

@Slf4j
@Service
class UserService(
    private val userRepository: UserRepository,
) {
    companion object {
        private val log: Logger = LoggerFactory.getLogger(UserService::class.java)
    }

    fun searchUserByUsername(username: String): User? {
        val findOne = userRepository.findByUsername(username)
        log.info("user = $findOne")
        return findOne
    }
}
