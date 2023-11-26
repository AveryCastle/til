package chapter04.exercise.ex07

import chapter03.Cons
import chapter03.List
import chapter03.Nil
import chapter04.Either
import chapter04.Left
import chapter04.Right
import chapter04.sec04.map2
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe


class Solution7 : WordSpec({

    fun <E, A, B> traverse(
        xa: List<A>,
        f: (A) -> Either<E, B>
    ): Either<E, List<B>> =
        when (xa) {
            is Nil -> Right(Nil)
            is Cons ->
                map2(f(xa.head), traverse(xa.tail, f)) { b: B, xb: List<B> ->
                    Cons(b, xb)
                }
        }

    fun <E, A> sequence(xs: List<Either<E, A>>): Either<E, List<A>> =
        traverse(xs) { it }

    fun <A> catches(a: () -> A): Either<String, A> =
        try {
            Right(a())
        } catch (e: Exception) {
            Left(e.message!!)
        }

    "traverse" should {
        """return a right either of a transformed list if all
            transformations succeed""" {
            val xa =
                List.of("1", "2", "3", "4", "5")

            traverse(xa) { a ->
                catches { Integer.parseInt(a) }
            } shouldBe Right(
                List.of(1, 2, 3, 4, 5)
            )
        }

        "return a left either if any transformations fail" {
            val xa =
                List.of("1", "2", "x", "4", "5")

            traverse(xa) { a ->
                catches { Integer.parseInt(a) }
            } shouldBe Left(
                """For input string: "x""""
            )
        }
    }

    "sequence" should {
        "turn a list of right eithers into a right either of list" {
            val xe: List<Either<String, Int>> =
                List.of(Right(1), Right(2), Right(3))

            sequence(xe) shouldBe Right(List.of(1, 2, 3))
        }

        """convert a list containing any left eithers into a
            left either""" {
            val xe: List<Either<String, Int>> =
                List.of(Right(1), Left("boom"), Right(3))

            sequence(xe) shouldBe Left("boom")
        }
    }
})
