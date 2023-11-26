package chapter04.exercise.ex08

import chapter04.Either
import chapter04.Left
import chapter04.Right
import chapter04.sec04.*
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

class Solution82 : WordSpec({

    ////////////////////// 공통 ///////////////////////////////
    fun mkName(name: String): Either<List<String>, Name> =
        if (name.isBlank()) Left(listOf("Name is empty"))
        else Right(Name(name))

    fun mkAge(age: Int): Either<List<String>, Age> =
        if (age < 0) Left(listOf("Age is out of range"))
        else Right(Age(age))
    /////////////////////////////////////////////////////////

    fun <E, A, B> Either<E, A>.mapLeft(f: (E) -> B): Either<B, A> =
        when (this) {
            is Left -> Left(f(this.value))
            is Right -> this
        }

    fun <E, A, B, C> map2(
        ae: Either<E, A>,
        be: Either<E, B>,
        f: (A, B) -> C
    ): Either<List<E>, C> =
        when (ae) {
            is Left -> when (be) {
                is Left -> Left(listOf(ae.value, be.value))
                is Right -> Left(listOf(ae.value))
            }

            is Right -> be.mapLeft { listOf(it) }.map { b: B -> f(ae.value, b) }
        }

    fun mkPerson2(name: String, age: Int): Either<List<String>, Person> =
        map2(
            mkName(name),
            mkAge(age)
        ) { n, a ->
            Person(n, a)
        }.mapLeft { it.flatten() }

    "mkPerson2" should {
        """return a successful mkPerson if all
            mkPerson succeed""" {

            mkPerson2("Jimin", 19) shouldBe
                    Right(Person(Name("Jimin"), Age(19)))
        }

        "return a failures if any mkPerson fail" {
            mkPerson2("", -1) shouldBe
                    Left(listOf("Name is empty", "Age is out of range"))
        }
    }

    fun <E, A> Either<E, A>.getAllLefts(): List<E> =
        when (this) {
            is Left -> listOf(this.value)
            is Right -> emptyList()
        }

    fun <E, A, B, C> map3(
        ae: Either<E, A>,
        be: Either<E, B>,
        f: (A, B) -> C
    ): Either<List<E>, C> =
        ae.flatMap { a ->
            be.map { b ->
                f(a, b)
            }
        }.mapLeft { listOf(it) + be.getAllLefts() }


    fun mkPerson3(name: String, age: Int): Either<List<String>, Person> =
        map3(
            mkName(name),
            mkAge(age)
        ) { n, a ->
            Person(n, a)
        }.mapLeft { it.flatten() }

    "mkPerson3" should {
        """return a successful mkPerson if all
            mkPerson succeed""" {

            mkPerson3("Jimin", 19) shouldBe
                    Right(Person(Name("Jimin"), Age(19)))
        }

        "return a failures if any mkPerson fail" {
            mkPerson3("", -1) shouldBe
                    Left(listOf("Name is empty", "Age is out of range"))
        }
    }
})
