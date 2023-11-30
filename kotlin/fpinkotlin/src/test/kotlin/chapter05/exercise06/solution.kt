package chapter05.exercise06

import chapter05.Cons
import chapter05.Empty
import chapter05.Stream
import chapter05.Stream.Companion.cons
import io.kotest.core.spec.style.WordSpec

// map,filter, append
fun <A, B> Stream<A>.map(f: (A) -> B): Stream<B> = when (this) {
    is Empty -> Stream.empty()
    is Cons -> cons({ f(this.head()) }, { this.tail().map(f) })
}

class Solution6: WordSpec({

    "Stream.map" should {

    }
})
