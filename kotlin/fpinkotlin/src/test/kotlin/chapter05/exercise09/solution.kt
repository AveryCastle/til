package chapter05.exercise09

import chapter03.List
import chapter05.Stream
import chapter05.Stream.Companion.cons
import chapter05.exercise02.take
import chapter05.toList
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

class Solution9 : WordSpec({

    fun from(n: Int): Stream<Int> =
        cons({ n }) { from(n + 1) }

    "from" should {
        "return a Stream of ever incrementing numbers" {
            from(1).take(7).toList() shouldBe List.of(1, 2, 3, 4, 5, 6, 7)
        }
    }
})
