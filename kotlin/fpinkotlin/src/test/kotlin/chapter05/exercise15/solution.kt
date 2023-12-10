package chapter05.exercise15

import chapter03.List
import chapter03.Nil.map
import chapter04.None
import chapter04.Some
import chapter05.Cons
import chapter05.Stream
import chapter05.exercise11.unfold
import chapter05.exercise14.startsWith
import chapter05.toList
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe


class Solution15 : WordSpec({

    fun <A> Stream<A>.tails(): Stream<Stream<A>> =
        unfold(this) { it: Stream<A> ->
            when (it) {
                is Cons ->
                    Some(it to it.tail())

                else -> None
            }
        }

    fun <A> Stream<A>.hasSequence(s: Stream<A>): Boolean =
        tails().exists2 { it.startsWith(s) }

    "Stream.tails()" should {
        "returns " {
            map(
                Stream.of("jimin", "v", "jk")
                    .tails().toList()
            ) { it.toList() } shouldBe
                    List.of(
                        List.of("jimin", "v", "jk"),
                        List.of("v", "jk"),
                        List.of("jk")
                    )
        }
    }

    "Stream.hasSequence" should {
        "returns true if exists" {
            Stream.of("jimin", "v", "jk").hasSequence(Stream.of("jk")) shouldBe true
        }
    }
})
