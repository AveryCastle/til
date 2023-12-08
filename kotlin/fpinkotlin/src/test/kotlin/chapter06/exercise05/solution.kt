package chapter06.exercise05

import chapter06.exercise01.nonNegativeInt
import chapter06.sec01.RNG
import chapter06.sec04.Rand
import chapter06.sec04.map
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

//fun double(rng: RNG): Pair<Double, RNG> {
//    val (i, rng2) = nonNegativeInt(rng)
//    return (i / (Int.MAX_VALUE.toDouble() + 1)) to rng2
//}

//fun <A, B> map(s: Rand<A>, f: (A) -> B): Rand<B> =
//    { rng ->
//        val (a, rng2) = s(rng)
//        f(a) to rng2
//    }

fun doubleR(): Rand<Double> =
    map(::nonNegativeInt) { i -> i / (Int.MAX_VALUE.toDouble() + 1) }

class Solution5 : WordSpec({

    "doubleR" should {

        val unusedRng = object : RNG {
            override fun nextInt(): Pair<Int, RNG> = TODO()
        }

        """generate a max value approaching 1 based on
            Int.MAX_VALUE using Rand""" {

            val rngMax = object : RNG {
                override fun nextInt(): Pair<Int, RNG> =
                    Int.MAX_VALUE to unusedRng
            }

            val doubleRand = doubleR()
            doubleRand(rngMax) shouldBe (0.9999999995343387 to unusedRng)
        }

        "generate a min value of 0 based on 0 using Rand" {
            val rngMin = object : RNG {
                override fun nextInt(): Pair<Int, RNG> =
                    0 to unusedRng
            }

            val doubleRand = doubleR()
            doubleRand(rngMin) shouldBe (0.0 to unusedRng)
        }
    }
})
