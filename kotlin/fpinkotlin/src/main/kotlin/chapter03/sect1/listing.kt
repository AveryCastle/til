package chapter03.sect1

// out: generic variant
// 참고: https://kotlinlang.org/docs/generics.html
sealed class List<out A>

data object Nil : List<Nothing>()

data class Cons<out A>(val head: A, val tail: List<A>) : List<A>()

fun main() {
    val ex1: List<Double> = Nil
    val ex2: List<Int> = Cons(1, Nil)
    val ex3: List<String> = Cons("Jimin", Cons("JK", Nil))
}
