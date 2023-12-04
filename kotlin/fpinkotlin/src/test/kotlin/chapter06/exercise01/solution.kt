package chapter06.exercise01

import chapter06.sec01.RNG
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

// 내가 푼 것(틀림)
// i가 Int.MIN_VALUE 일 때, Int.MIN_VALUE + Int.MAX_VALUE 는 -1 이다.
//fun nonNegativeInt(rng: RNG): Pair<Int, RNG> {
//    val (i, newRng) = rng.nextInt()
//    val num = if (i < 0) i + Int.MAX_VALUE else i
//    return num to newRng
//}

fun nonNegativeInt(rng: RNG): Pair<Int, RNG> {
    val (i1, rng2) = rng.nextInt()
    return (if (i1 < 0) -(i1 + 1) else i1) to rng2
}

class Solution : WordSpec({

    "nonNegativeInt" should {

        val unusedRng = object : RNG {
            override fun nextInt(): Pair<Int, RNG> = TODO()
        }

        "return 0 if nextInt() yields 0" {

            val rng0 = object : RNG {
                override fun nextInt(): Pair<Int, RNG> =
                    0 to unusedRng
            }

            nonNegativeInt(rng0) shouldBe (0 to unusedRng)
        }

        "return Int.MAX_VALUE when nextInt() yields Int.MAX_VALUE" {

            val rngMax = object : RNG {
                override fun nextInt(): Pair<Int, RNG> =
                    Int.MAX_VALUE to unusedRng
            }

            nonNegativeInt(rngMax) shouldBe (Int.MAX_VALUE to unusedRng)
        }

        "return Int.MAX_VALUE when nextInt() yields Int.MIN_VALUE" {

            val rngMin = object : RNG {
                override fun nextInt(): Pair<Int, RNG> =
                    Int.MIN_VALUE to unusedRng
            }

            nonNegativeInt(rngMin) shouldBe (Int.MAX_VALUE to unusedRng)
        }

        "return 0 when nextInt() yields -1" {

            val rngNeg = object : RNG {
                override fun nextInt(): Pair<Int, RNG> =
                    -1 to unusedRng
            }

            nonNegativeInt(rngNeg) shouldBe (0 to unusedRng)
        }
    }
})
