package chapter04.sec04

import chapter04.Either
import chapter04.Left
import chapter04.Right

fun mean(xs: List<Double>): Either<String, Double> =
    if (xs.isEmpty()) Left("mean of empty list")
    else Right(xs.sum() / xs.size)

fun safeDiv(x: Int, y: Int): Either<Exception, Int> =
    try {
        Right(x / y)
    } catch (e: Exception) {
        Left(e)
    }

fun <A> catches(a: () -> A): Either<Exception, A> =
    try {
        Right(a())
    } catch (e: Exception) {
        Left(e)
    }

fun main() {
    val list = listOf(0.0, 1.1, 3.23, 7.765)
    println("result = ${mean(list)}")

    val empty = listOf<Double>()
    println("${mean(empty)}")

    println("10/0 = ${safeDiv(10, 0)}")
    println("10/2 = ${safeDiv(10, 2)}")
}
