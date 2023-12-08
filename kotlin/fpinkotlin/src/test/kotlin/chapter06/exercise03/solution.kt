package chapter06.exercise03

import chapter06.exercise02.double
import chapter06.sec01.RNG
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

fun intDouble(rng: RNG): Pair<Pair<Int, Double>, RNG> {
    val (i, rng1) = rng.nextInt()
    val (d, rng2) = double(rng1)
    return Pair(i, d) to rng2
}

fun doubleInt(rng: RNG): Pair<Pair<Double, Int>, RNG> {
    val (pair, rng1) = intDouble(rng)
    val (i, d) = pair
    return Pair(d, i) to rng1
}

fun double3(rng: RNG): Pair<Triple<Double, Double, Double>, RNG> {
    val (d, rng1) = double(rng)
    val (d1, rng2) = double(rng1)
    val (d2, rng3) = double(rng2)
    return Triple(d, d1, d2) to rng3
}

class Solution : WordSpec({

    "intDouble" should {

        val doubleBelowOne =
            Int.MAX_VALUE.toDouble() / (Int.MAX_VALUE.toDouble() + 1)

        val unusedRng = object : RNG {
            override fun nextInt(): Pair<Int, RNG> = TODO()
        }

        val rng3 = object : RNG {
            override fun nextInt(): Pair<Int, RNG> =
                Int.MAX_VALUE to unusedRng
        }

        val rng2 = object : RNG {
            override fun nextInt(): Pair<Int, RNG> =
                Int.MAX_VALUE to rng3
        }

        val rng = object : RNG {
            override fun nextInt(): Pair<Int, RNG> =
                Int.MAX_VALUE to rng2
        }

        "generate a pair of int and double" {
            val (id, _) = intDouble(rng)
            val (i, d) = id
            i shouldBe Int.MAX_VALUE
            d shouldBe doubleBelowOne
        }

        "generate a pair of double and int" {
            val (di, _) = doubleInt(rng)
            val (d, i) = di
            d shouldBe doubleBelowOne
            i shouldBe Int.MAX_VALUE
        }

        "generate a triple of double, double, double" {
            val (ddd, _) = double3(rng)
            val (d1, d2, d3) = ddd
            d1 shouldBe doubleBelowOne
            d2 shouldBe doubleBelowOne
            d3 shouldBe doubleBelowOne
        }
    }
})
