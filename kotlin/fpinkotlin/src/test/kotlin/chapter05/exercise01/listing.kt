package chapter05.exercise01

import chapter03.List
import chapter03.Nil
import chapter05.Cons
import chapter05.Empty
import chapter05.Stream
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

fun <A> Stream<A>.toList(): List<A> {
    tailrec fun go(xs: Stream<A>, acc: List<A>): List<A> = when (xs) {
        is Empty -> acc
        is Cons -> go(xs.tail(), chapter03.Cons(xs.head(), acc))
    }

    return go(this, Nil).reverse()
}

class Solution1 : WordSpec({

    class Solution1 : WordSpec({
        "Stream.toList" should {
            "force the stream into an evaluated list" {
                val s = Stream.of(1, 2, 3, 4, 5)
                s.toList() shouldBe List.of(1, 2, 3, 4, 5)
            }
        }
    })
})
