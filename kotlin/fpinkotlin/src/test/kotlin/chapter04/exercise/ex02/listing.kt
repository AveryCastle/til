package chapter04.exercise.ex02

import chapter04.None.flatMap
import chapter04.None.getOrElse
import chapter04.Option
import chapter04.sec02.mean
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.doubles.plusOrMinus
import io.kotest.matchers.shouldBe
import kotlin.math.pow

fun variance(xs: List<Double>): Option<Double> =
    mean(xs).flatMap { m ->
        mean(xs.map { x ->
            (x - m).pow(2)
        })
    }

class Solution2 : WordSpec({

    "variance" should {
        "determine the variance of a list of numbers" {
            val ls = listOf(1.0, 1.1, 1.0, 3.0, 0.9, 0.4)

            variance(ls).getOrElse { 0.0 } shouldBe
                    (0.675).plusOrMinus(0.005)
        }
    }
})
