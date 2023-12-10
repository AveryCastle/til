package chapter06.exercise06

import chapter06.rng1
import chapter06.sec04.Rand
import chapter06.sec04.unit
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

//typealias Rand<A> = (RNG) -> Pair<A, RNG>

//fun <A, B> map(s: Rand<A>, f: (A) -> B): Rand<B> =
//    { rng ->
//        val (a, rng2) = s(rng)
//        f(a) to rng2
//    }

class Solution6 : WordSpec({

    fun <A, B, C> map2(
        ra: Rand<A>,
        rb: Rand<B>,
        f: (A, B) -> C
    ): Rand<C> = { rng ->
        val (a, rng2) = ra(rng)
        val (b, rng3) = rb(rng2)
        f(a, b) to rng3
    }

    "map2" should {
        "combine the results of two actions" {

            val combined: Rand<String> =
                map2(unit(1.0), unit(1)) { d, i ->
                    ">>> $d double; $i int"
                }

            combined(rng1).first shouldBe ">>> 1.0 double; 1 int"
        }
    }
})
