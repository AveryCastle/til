package chapter05.exercise14

import chapter04.Option
import chapter05.Stream
import chapter05.exercise04.forAll
import chapter05.exercise13.takeWhile
import chapter05.exercise13.zipAll
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

// (1,2,3,4):  (3,4)
// (1), (2), (3), (4)
// (1,2), (2,3), (3,4)
// (1,2,3), (2,3,4)
// (1,2,3,4)
fun <A> Stream<A>.startsWith(that: Stream<A>): Boolean =
    this.zipAll(that)
        .takeWhile { (_: Option<A>, second: Option<A>) ->
            !second.isEmpty()
        }.forAll { (first, second) ->
            first == second
        }

class Solution14 : WordSpec({

    "Stream.startsWith" should {
        "detect if one stream is a prefix of another" {
            Stream.of(1, 2, 3)
                .startsWith(Stream.of(1, 2)) shouldBe true
        }
        "detect if one stream is not a prefix of another" {
            Stream.of(1, 2, 3)
                .startsWith(Stream.of(2, 3)) shouldBe false
        }
    }
})
