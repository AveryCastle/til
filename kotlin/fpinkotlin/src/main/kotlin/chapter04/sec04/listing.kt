package chapter04.sec04

import chapter03.Nil
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

suspend fun String.parseToInt(): arrow.core.Either<Throwable, Int> =
    arrow.core.Either.catch { this.toInt() }


data class Name(val value: String)

data class Age(val value: Int)

data class Person(val name: Name, val age: Age)

fun mkName(name: String): Either<String, Name> =
    if (name.isBlank()) Left("Name is empty")
    else Right(Name((name)))

fun mkAge(age: Int): Either<String, Age> =
    if (age < 0) Left("Age is out of range")
    else Right(Age(age))

fun <E, A, B> Either<E, A>.map(f: (A) -> B): Either<E, B> =
    when (this) {
        is Left -> this
        is Right -> Right(f(this.value))
    }

fun <E, A, B> Either<E, A>.flatMap(f: (A) -> Either<E, B>): Either<E, B> =
    when (this) {
        is Left -> this
        is Right -> f(this.value)
    }

fun <E, A, B, C> map2(
    ae: Either<E, A>,
    be: Either<E, B>,
    f: (A, B) -> C
): Either<E, C> =
    ae.flatMap { a: A ->
        be.map { b: B ->
            f(a, b)
        }
    }

fun mkPerson(name: String, age: Int): Either<String, Person> =
    map2(mkName(name), mkAge(age)) { nameE: Name, ageE: Age ->
        Person(nameE, ageE)
    }

fun main() {
    val list = listOf(0.0, 1.1, 3.23, 7.765)
    println("result = ${mean(list)}")

    val empty = listOf<Double>()
    println("${mean(empty)}")

    println("10/0 = ${safeDiv(10, 0)}")
    println("10/2 = ${safeDiv(10, 2)}")

    println(mkName("Jimin"))
    println(mkAge(29))
    println(mkPerson("Jimin", 29))

    println(mkPerson("", -1))
}
