package chapter05.sec01

fun maybeTwice(b: Boolean, i: () -> Int) =
    if (b) i() + i() else 0

fun maybeTwice2(b: Boolean, i: () -> Int) {
    val j: Int by lazy(i)
    if (b) j + j else 0
}

fun main() {
    maybeTwice(true) { println("hi"); 7 }
    maybeTwice2(true) { println("hi2"); 7 }
}
