package chapter05.exercise11

import chapter03.List
import chapter04.None.getOrElse
import chapter04.None.map
import chapter04.Option
import chapter04.Some
import chapter05.Stream
import chapter05.Stream.Companion.cons
import chapter05.Stream.Companion.empty
import chapter05.exercise02.take
import chapter05.toList
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe


fun <A, S> unfold(z: S, f: (S) -> Option<Pair<A, S>>): Stream<A> =
    f(z).map { pair ->
        cons({ pair.first }, { unfold(pair.second, f) })
    }.getOrElse { empty() }

class Solution11 : WordSpec({

    "unfold" should {
        """return a stream based on an initial state and a function
            applied to each subsequent element""" {
            unfold(0) { s: Int -> Some(s to (s + 1)) }
                .take(5).toList() shouldBe
                    List.of(0, 1, 2, 3, 4)
        }
    }
})
