package chapter03.exercise.ex27

import chapter03.Branch
import chapter03.Leaf
import chapter03.Tree
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

fun <A, B> map(tree: Tree<A>, f: (A) -> B): Tree<B> =
    when (tree) {
        is Leaf -> Leaf(f(tree.value))
        is Branch -> Branch(map(tree.left, f), map(tree.right, f))
    }

class Solution27 : WordSpec({
    "tree map" should {
        "transform all leaves of a map" {
            val actual =
                Branch(
                    Branch(
                        Leaf(1),
                        Leaf(2)
                    ),
                    Branch(
                        Leaf(3),
                        Leaf(4)
                    )
                )
            val expected = Branch(
                Branch(
                    Leaf(10),
                    Leaf(20)
                ),
                Branch(
                    Leaf(30),
                    Leaf(40)
                )
            )
            map(actual) { it * 10 } shouldBe expected
        }
    }
})
