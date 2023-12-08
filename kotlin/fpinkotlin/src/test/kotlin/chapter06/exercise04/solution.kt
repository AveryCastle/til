package chapter06.exercise04

import chapter03.Cons
import chapter03.List
import chapter03.Nil
import chapter06.rng1
import chapter06.sec01.RNG
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

fun ints(count: Int, rng: RNG): Pair<List<Int>, RNG> =
    if (count > 0) {
        val (i1, rng1) = rng.nextInt()
        val (xs, rng2) = ints(count - 1, rng1)
        Cons(i1, xs) to rng2
    } else {
        Nil to rng
    }


class Solution : WordSpec({

    "ints" should {
        "generate a list of ints of a specified length" {

            ints(5, rng1) shouldBe (List.of(1, 1, 1, 1, 1) to rng1)
        }
    }
})
