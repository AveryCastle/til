package chapter04.exercise.ex01

import chapter04.None
import chapter04.None.filter
import chapter04.None.flatMap
import chapter04.None.getOrElse
import chapter04.None.map
import chapter04.None.orElse
import chapter04.Option
import chapter04.Some
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

class Solution1 : WordSpec({

    val none = Option.empty<Int>()

    val some = Some(10)

    "Option.map" should {
        "transform an option of some value" {
            some.map { it * 2 } shouldBe Some(20)
        }
        "pass over an option of none" {
            none.map { it * 10 } shouldBe None
        }
    }

    "Option.flatMap" should {
        "apply a function yielding an option to an option of some value" {
            some.flatMap { a ->
                Some(a.toString())
            } shouldBe Some("10")
        }
        "pass over an option of none" {
            none.flatMap { a ->
                Some(a.toString())
            } shouldBe None
        }
    }

    "Option.getOrElse" should {
        "extract the value of some option" {
            some.getOrElse { 0 } shouldBe 10
        }
        "return a default value if the option is none" {
            none.getOrElse { 0 } shouldBe 0
        }
    }

    "Option.orElse" should {
        "return the option if the option is some" {
            some.orElse { Some(20) } shouldBe some
        }
        "return a default option if the option is none" {
            none.orElse { Some(20) } shouldBe Some(20)
        }
    }

    "Option.filter" should {
        "return some option if the predicate is met" {
            some.filter { it > 0 } shouldBe some
        }
        "return a none option if the predicate is not met" {
            some.filter { it < 0 } shouldBe None
            none.filter { it < 0 } shouldBe None
        }
    }
})
