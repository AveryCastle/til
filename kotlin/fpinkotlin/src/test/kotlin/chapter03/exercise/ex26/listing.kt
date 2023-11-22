package chapter03.exercise.ex26

import chapter03.Branch
import chapter03.Leaf
import chapter03.Tree
import io.kotest.core.spec.style.WordSpec
import io.kotest.matchers.shouldBe

fun <A> depth(root: Tree<A>): Int =
    when (root) {
        is Leaf -> 0
        is Branch -> 1 + maxOf(depth(root.left), depth(root.right))
    }

class Exercise26 : WordSpec({
    "tree depth" should {
        "determine the maximum depth from the root to any leaf" {
            val tree = Branch(
                Branch(Leaf(1), Leaf(2)),
                Branch(
                    Leaf(3),
                    Branch(
                        Branch(
                            Leaf(4),
                            Leaf(5)
                        ),
                        Branch(
                            Leaf(6),
                            Branch(
                                Branch(
                                    Leaf(7),
                                    Branch(
                                        Leaf(8),
                                        Leaf(9)
                                    )
                                ),
                                Leaf(10)
                            )
                        )
                    )
                )
            )
            depth(tree) shouldBe 7
        }
    }
})
