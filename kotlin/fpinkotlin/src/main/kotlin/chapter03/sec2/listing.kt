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

        // 연습문제 3.3
        fun <A> drop(l: List<A>, n: Int): List<A> =
            if (n == 0) l
            else when (l) {
                is Nil -> throw IllegalStateException("Cannot drop more elements than in list")
                is Cons -> drop(l.tail, n - 1)
            }

        // 연습문제 3.4
        fun <A> dropWhile(l: List<A>, f: (A) -> Boolean): List<A> =
            when (l) {
                is Nil -> l
                is Cons ->
                    if (f(l.head)) dropWhile(l.tail, f) else l
            }

        fun <A> append(a1: List<A>, a2: List<A>): List<A> =
            when (a1) {
                is Nil -> a2
                is Cons -> Cons(a1.head, append(a1.tail, a2))
            }

        // 연습문제 3.5
        fun <A> init(l: List<A>): List<A> =
            when (l) {
                is Nil -> throw IllegalStateException("Cannot init Nil list")
                is Cons ->
                    if (l.tail == Nil) Nil
                    else Cons(l.head, init(l.tail))
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
    val members = List.of("Jimin", "JK", "V", "J-HOPE", "SUGA", "JIN", "RM")
    println(members)

    println(List.sum(ints))

    println(y)
    println(z)

    println(ints.tail())

    println(List.setHead(members, "V"))

    println("after drop 2 = ${List.drop(members, 2)}")

    val numbers = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    println("dropWhile result => ${List.dropWhile(numbers) { it < 5 }}")
    println("after dropWhile => ${numbers}")

    println(List.append(members, List.of("BTS", "V", "ARMY")))

    println(List.init(members))

}
