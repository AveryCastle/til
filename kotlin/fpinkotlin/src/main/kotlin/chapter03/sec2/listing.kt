package chapter03.sec2

import kotlin.random.Random

sealed class List<out A> {
    companion object {
        fun <A> of(vararg aa: A): List<A> {
            val tail = aa.sliceArray(1..<aa.size)
            return if (aa.isEmpty()) Nil else Cons(aa[0], of(*tail))
        }

        // 연습문제 3.1
        fun <A> tail(xs: List<A>): List<A> =
            when (xs) {
                is Cons -> xs.tail
                is Nil -> throw IllegalStateException("Nil cannot have a `tail`")
            }

        // 연습문제 3.2
        fun <A> setHead(xs: List<A>, x: A): List<A> =
            when (xs) {
                is Nil -> throw IllegalStateException("Cannot replace `head` of a Nil list")
                is Cons -> Cons(x, xs.tail)
            }

        fun sum(ints: List<Int>): Int =
            when (ints) {
                is Nil -> 0
                is Cons -> ints.head + sum(ints.tail)
            }

        fun product(doubles: List<Double>): Double =
            when (doubles) {
                is Nil -> 1.0
                is Cons ->
                    if (doubles.head == 0.0) 0.0
                    else doubles.head * product(doubles.tail)
            }
    }
}

object Nil : List<Nothing>() {
    override fun toString(): String = "Nil"
}

//tag::init7[]
data class Cons<out A>(val head: A, val tail: List<A>) : List<A>()
//end::init7[]

//tag::init2[]
fun <A> of(vararg aa: A): List<A> {
    val tail = aa.sliceArray(1 until aa.size)
    return if (aa.isEmpty()) Nil else Cons(aa[0], List.of(*tail))
}
//end::init2[]


// 연습문제 3.1.
fun <A> List<A>.tail(): List<A> = when (this) {
    is Nil -> throw IllegalStateException("Nil cannot have a `tail`")
    is Cons -> this.tail
}

val ints = List.of(1, 2, 3, 4, 5)

val x = Random.nextInt(-10, 10)
val y: String =
    if (x == 0) {
        "x is zero"
    } else if (x < 0) {
        "x is negative"
    } else {
        "x is positive"
    }
val z: String =
    when {
        x == 0 -> "x is zero"
        x < 0 -> "x is negative"
        else -> "x is positive"
    }

fun main() {
    val members = List.of("Jimin", "JK")
    println(members)

    println(List.sum(ints))

    println(y)
    println(z)

    println(ints.tail())

    println(List.setHead(members, "V"))
}
