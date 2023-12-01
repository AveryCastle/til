package chapter05.exercise12

import chapter03.List
import chapter04.Some
import chapter05.Stream
import chapter05.exercise02.take
import chapter05.exercise11.unfold
import chapter05.toList
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

class Solution12 : WordSpec({

    fun fibs(): Stream<Int> =
        unfold(Pair(0, 1)) { pair -> Some(Pair(pair.first, Pair(pair.second, pair.first + pair.second))) }

    fun from(n: Int): Stream<Int> =
        unfold(n) { i -> Some(Pair(i, i + 1)) }

    fun <A> constant(a: A): Stream<A> =
        unfold(a) { Some(Pair(a, a)) }

    fun ones(): Stream<Int> =
        unfold(1) { Some(Pair(1, 1)) }

    "fibs" should {
        "return a Stream of fibonacci sequence numbers" {
            fibs().take(10).toList() shouldBe
                    List.of(0, 1, 1, 2, 3, 5, 8, 13, 21, 34)
        }
    }

    "from" should {
        "return a Stream of ever incrementing numbers" {
            from(1).take(7).toList() shouldBe List.of(1, 2, 3, 4, 5, 6, 7)
            from(100).take(7).toList() shouldBe List.of(100, 101, 102, 103, 104, 105, 106)
        }
    }

    "constant" should {
        "return an infinite stream of a given value" {
            constant("bts").take(10).toList() shouldBe
                    Stream.of("bts", "bts", "bts", "bts", "bts", "bts", "bts", "bts", "bts", "bts").toList()
        }
    }

    "ones" should {
        "return an infinite stream of 1s" {
            ones().take(5).toList() shouldBe
                    List.of(1, 1, 1, 1, 1)
        }
    }
})
