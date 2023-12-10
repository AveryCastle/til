package chapter06.exercise08

import chapter06.rng1
import chapter06.sec01.RNG
import chapter06.sec04.Rand
import chapter06.sec04.nonNegativeInt
import chapter06.sec04.unit
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

fun <A, B> flatMap(f: Rand<A>, g: (A) -> Rand<B>): Rand<B> =
    { rng: RNG ->
        val (a, rng2) = f(rng)
        g(a)(rng2)
    }


fun nonNegativeIntLessThan(n: Int): Rand<Int> =
    flatMap(::nonNegativeInt) { i: Int ->
        val mod = i % n
        if (i + (n - 1) - mod >= 0)
            unit(mod)
        else nonNegativeIntLessThan(i)
    }

class Solution8 : WordSpec({

    "flatMap" should {
        "pass along an RNG" {

            val result =
                (flatMap(unit(1)) { i ->
                    unit(i.toString())
                })(rng1)

            result.first shouldBe "1"
            result.second shouldBe rng1
        }
    }

    "nonNegativeIntLessThan" should {
        "return a non negative int less than n" {

            val result =
                (nonNegativeIntLessThan(10))(rng1)

            result.first shouldBe 1
        }
    }
})
