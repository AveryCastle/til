package com.example.kotlinindepthbook

import org.springframework.boot.fromApplication
import org.springframework.boot.with

fun main(args: Array<String>) {
    fromApplication<KotlinInDepthBookApplication>().with(TestcontainersConfiguration::class).run(*args)
}
