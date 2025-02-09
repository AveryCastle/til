package com.example.kotlinindepthbook.domain

import jakarta.persistence.Column
import jakarta.persistence.Entity
import jakarta.persistence.Id
import java.time.LocalDateTime

@Entity(name = "users")
class User(
    @Id
    val id: Long,

    @Column(nullable = false)
    var username: String,

    @Column(nullable = false)
    var age: Int,

    @Column(nullable = false)
    var gender: Gender,

    @Column(nullable = false)
    val createdAt: LocalDateTime = LocalDateTime.now()
)

enum class Gender(val code: Int) {
    MALE(1), FEMALE(2);

    companion object {
        fun fromCode(code: Int): Gender {
            return entries.first { it.code == code }
        }
    }
}
