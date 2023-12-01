package chapter05.exercise08

import chapter05.Stream
import chapter05.exercise02.take
import chapter05.toList
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

class Solution8 : WordSpec({

    fun <A> constant(a: A): Stream<A> =
        Stream.cons({ a }) { constant(a) }

    "Stream.constant" should {
        "return an infinite stream of a given value" {
            constant("bts").take(10).toList() shouldBe
                    Stream.of("bts", "bts", "bts", "bts", "bts", "bts", "bts", "bts", "bts", "bts").toList()
        }
    }
})
