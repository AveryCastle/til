package chapter04.exercise.ex05

import chapter03.Cons
import chapter03.List
import chapter03.Nil
import chapter04.None
import chapter04.Option
import chapter04.Some
import chapter04.exercise.ex03.map2
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

fun <A, B> traverse(xa: List<A>, f: (A) -> Option<B>): Option<List<B>> =
    when (xa) {
        is Nil -> Some(Nil)
        is Cons -> map2(f(xa.head), traverse(xa.tail, f)) { b, xb ->
            Cons(b, xb)
        }
    }


class Solution5 : WordSpec({

    fun <A> sequence(xs: List<Option<A>>): Option<List<A>> =
        traverse(xs) { it }
    //end::init[]

    fun <A> catches(a: () -> A): Option<A> =
        try {
            Some(a())
        } catch (e: Throwable) {
            None
        }

    "traverse" should {
        """return some option of a transformed list if all
            transformations succeed""" {
            val xa = List.of(1, 2, 3, 4, 5)
            traverse(xa) { a: Int ->
                catches { a.toString() }
            } shouldBe Some(List.of("1", "2", "3", "4", "5"))
        }

        "return a none option if any transformations fail" {
            val xa = List.of("1", "2", "x", "4")
            traverse(xa) { a ->
                catches { a.toInt() }
            } shouldBe None
        }
    }

    "sequence" should {
        "turn a list of some options into an option of list" {
            val lo =
                List.of(Some(10), Some(20), Some(30))
            sequence(lo) shouldBe Some(List.of(10, 20, 30))
        }

        "turn a list of options containing a none into a none" {
            val lo =
                List.of(Some(10), None, Some(30))
            sequence(lo) shouldBe None
        }
    }
})
