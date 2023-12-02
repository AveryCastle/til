package chapter05.exercise15

import chapter03.List
import chapter03.Nil.map
import chapter04.None
import chapter04.Some
import chapter05.Cons
import chapter05.Stream
import chapter05.exercise11.unfold
import chapter05.toList
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

fun <A> Stream<A>.tails(): Stream<Stream<A>> =
    unfold(this) { it: Stream<A> ->
        when (it) {
            is Cons ->
                Some(it to it.tail())

            else -> None
        }
    }

class Solution15 : WordSpec({

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
})
