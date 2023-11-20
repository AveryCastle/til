package chapter03.sec4

sealed class List<out A> {
    companion object {
        fun <A> of(vararg aa: A): List<A> {
            val tail = aa.sliceArray(1..<aa.size)
            return if (aa.isEmpty()) Nil else Cons(aa[0], of(*tail))
        }

        fun sum(ints: List<Int>): Int =
            foldRight(ints, 0) { a, b -> a + b }

        // 연습문제 3.6
        fun product(doubles: List<Double>): Double =
            foldRight(doubles, 1.0) { a, b ->
                when {
                    a == 0.0 || b == 0.0 -> 0.0
                    else -> a * b
                }
            }

        fun <A> empty(): List<A> = Nil

        fun <A, B> foldRight(xs: List<A>, z: B, f: (A, B) -> B): B =
            when (xs) {
                is Nil -> z
                is Cons -> f(xs.head, foldRight(xs.tail, z, f))
            }

        tailrec fun <A, B> foldLeft(xs: List<A>, z: B, f: (B, A) -> B): B =
            when (xs) {
                is Nil -> z
                is Cons -> foldLeft(xs.tail, f(z, xs.head), f)
            }

        // 연슴문제3.8
        fun <A> length(xs: List<A>): Int = foldRight(xs, 0) { _, z -> z + 1 }

        // 연습문제 3.14
        fun <A> concat(xxs: List<List<A>>): List<A> =
            foldRight(
                xxs,
                empty()
            ) { xs1: List<A>, xs2: List<A> ->
                foldRight(xs1, xs2) { head, x2 -> Cons(head, x2) }
            }

        // 연습문제 3.17
        fun <A, B> map(xs: List<A>, f: (A) -> B): List<B> =
            foldRight(xs, empty()) { h: A, t: List<B> -> Cons(f(h), t) }
    }
}

fun increment(xs: List<Int>): List<Int> =
    List.foldRight(xs, List.empty()) { h, t -> Cons(h + 1, t) }

fun doubleToString(xs: List<Double>): List<String> =
    List.foldRight(xs, List.empty()) { h, t -> Cons(h.toString(), t) }

data object Nil : List<Nothing>()

data class Cons<out A>(val head: A, val tail: List<A>) : List<A>()

fun main() {
    println("sum = ${List.sum(List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))}")
    println("product = ${List.product(List.of(1.0, 2.0, 3.0, 7.7, 4.0, 5.0))}")

    println(
        List.foldRight(
            Cons(1, Cons(2, Cons(3, Nil))),
            Nil as List<Int>
        ) { x, y -> Cons(x, y) }
    )

    val members = List.of("RM", "JIN", "SUGA", "J-HOPE", "JIMIN", "V", "JK")
    println("length = ${List.length(members)}")

    val bts = List.of(List.of("JK", "V", "JIMIN"), List.of("RM", "J-HOPE"), List.of("SUGA", "Jin"))
    println("concat = ${List.concat(bts)}")

    val integers = List.of(1, 2, 3, 4, 5, 6, 7)
    println("increment = ${increment(integers)}")

    val doubles = List.of(1.1, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0)
    println("doubleToString = ${doubleToString(doubles)}")

    println("map = ${List.map(members) { x -> x.length }}")
}
