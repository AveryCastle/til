package chapter04.exercise.ex08

import chapter04.sec04.Age
import chapter04.sec04.Name
import chapter04.sec04.Person
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

sealed class Partial<out A, out B>

data class Failures<out A>(val get: List<A>) : Partial<A, Nothing>()
data class Success<out B>(val get: B) : Partial<Nothing, B>()

fun <E, A, B> Partial<E, A>.map(f: (A) -> B): Partial<E, B> =
    when (this) {
        is Failures -> this
        is Success -> Success(f(this.get))
    }

fun <E, A, B> Partial<E, A>.flatMap(f: (A) -> Partial<E, B>): Partial<E, B> =
    when (this) {
        is Failures -> this
        is Success -> f(this.get)
    }

fun <E, A, B, C> map2(
    ae: Partial<E, A>,
    be: Partial<E, B>,
    f: (A, B) -> C
): Partial<E, C> =
    when {
        ae is Failures && be is Failures -> Failures(ae.get + be.get)
        ae is Failures -> ae
        be is Failures -> be
        else -> ae.flatMap { a ->
            be.map { b ->
                f(a, b)
            }
        }
    }

class Solution8 : WordSpec({

    fun mkName(name: String): Partial<String, Name> =
        if (name.isBlank()) Failures(listOf("Name is empty"))
        else Success(Name((name)))

    fun mkAge(age: Int): Partial<String, Age> =
        if (age < 0) Failures(listOf("Age is out of range"))
        else Success(Age(age))

    fun mkPerson(name: String, age: Int): Partial<String, Person> =
        map2(mkName(name), mkAge(age)) { n: Name, ageE: Age ->
            Person(n, ageE)
        }

    "mkPerson" should {
        """return a successful mkPerson if all
            mkPerson succeed""" {

            mkPerson("Jimin", 19) shouldBe
                    Success(Person(Name("Jimin"), Age(19)))
        }

        "return a failures if any mkPerson fail" {
            mkPerson("", -1) shouldBe
                    Failures(listOf("Name is empty", "Age is out of range"))
        }
    }
})
