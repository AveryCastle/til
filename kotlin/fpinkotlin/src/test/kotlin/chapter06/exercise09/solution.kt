package chapter06.exercise09

import chapter06.exercise08.flatMap
import chapter06.rng1
import chapter06.sec04.Rand
import chapter06.sec04.unit
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

fun <A, B> map(s: Rand<A>, f: (A) -> B): Rand<B> =
    flatMap(s) { it: A -> unit(f(it)) }


fun <A, B, C> map2(
    ra: Rand<A>,
    rb: Rand<B>,
    f: (A, B) -> C
): Rand<C> =
    flatMap(ra) { a: A ->
        map(rb) { b: B ->
            f(a, b)
        }
    }


class Solution9 : WordSpec({

    "map" should {
        "combine the results of two actions" {

            val combined: Rand<String> =
                map(unit(1)) { i ->
                    ">>> $i int"
                }

            combined(rng1).first shouldBe ">>> 1 int"
        }
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
