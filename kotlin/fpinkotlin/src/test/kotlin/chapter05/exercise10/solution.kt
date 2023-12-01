package chapter05.exercise10

import chapter03.List
import chapter05.Stream
import chapter05.Stream.Companion.cons
import chapter05.exercise02.take
import chapter05.toList
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

class Solution10 : WordSpec({

    fun fibs(): Stream<Int> {
        fun go(curr: Int, next: Int): Stream<Int> = cons({ curr }, { go(next, curr + next) })

        return go(0, 1)
    }

    "fibs" should {
        "return a Stream of fibonacci sequence numbers" {
            fibs().take(10).toList() shouldBe
                    List.of(0, 1, 1, 2, 3, 5, 8, 13, 21, 34)
        }
    }
})
