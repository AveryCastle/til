package chapter03.sec4

sealed class List<out A> {
    companion object {
        fun <A> of(vararg aa: A): List<A> {
            val tail = aa.sliceArray(1..<aa.size)
            return if (aa.isEmpty()) Nil else Cons(aa[0], of(*tail))
        }

        fun sum(ints: List<Int>): Int =
            foldRight(ints, 0) { a, b -> a + b }

        fun sumL(ints: List<Int>): Int =
            foldLeft(ints, 0) { acc, num -> acc + num }

        // 연습문제 3.6
        fun product(doubles: List<Double>): Double =
            foldRight(doubles, 1.0) { a, b ->
                when {
                    a == 0.0 || b == 0.0 -> 0.0
                    else -> a * b
                }
            }

        fun productL(doubles: List<Double>): Double =
            foldLeft(doubles, 1.0) { a, b -> a * b }

        fun <A> empty(): List<A> = Nil

        fun <A, B> foldRight(xs: List<A>, z: B, f: (A, B) -> B): B =
            when (xs) {
                is Nil -> z
                is Cons -> f(xs.head, foldRight(xs.tail, z, f))
            }

        // 연습문제 3.9
        tailrec fun <A, B> foldLeft(xs: List<A>, z: B, f: (B, A) -> B): B =
            when (xs) {
                is Nil -> z
                is Cons -> foldLeft(xs.tail, f(z, xs.head), f)
            }

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

        // 연슴문제 3.8
        fun <A> length(xs: List<A>): Int = foldRight(xs, 0) { _, acc -> acc + 1 }

        fun <A> lengthL(xs: List<A>): Int = foldLeft(xs, 0) { acc, _ -> acc + 1 }

        // 연습문제 3.11
        fun <A> reverse(xs: List<A>): List<A> =
            foldLeft(xs, empty()) { tail: List<A>, head: A -> Cons(head, tail) }

        // 연습문제 3.13
        fun <A> append(a1: List<A>, a2: List<A>): List<A> =
            foldRight(a1, a2) { h, t -> Cons(h, t) }

        // 연습문제 3.18
        fun <A> filter(xs: List<A>, f: (A) -> Boolean): List<A> =
            foldRight(xs, empty()) { h: A, t: List<A> -> if (f(h)) Cons(h, t) else t }

        // 연습문제 3.19
        fun <A, B> flatMap(xs: List<A>, f: (A) -> List<B>): List<B> =
            foldRight(xs, empty()) { h: A, t: List<B> -> append(f(h), t) }

        fun <A> filterM(xs: List<A>, f: (A) -> Boolean): List<A> =
            flatMap(xs) { a ->
                if (f(a)) of(a) else empty()
            }

        // 연습문제 3.20
        fun add(xs1: List<Int>, xs2: List<Int>): List<Int> =
            when (xs1) {
                is Nil -> Nil
                is Cons ->
                    when (xs2) {
                        is Nil -> Nil
                        is Cons -> Cons(xs1.head + xs2.head, add(xs1.tail, xs2.tail))
                    }
            }

        // 연습문제 3.22
        fun <A> zipWith(xs1: List<A>, xs2: List<A>, f: (A, A) -> A): List<A> =
            when (xs1) {
                is Nil -> Nil
                is Cons ->
                    when (xs2) {
                        is Nil -> Nil
                        is Cons -> Cons(f(xs1.head, xs2.head), zipWith(xs1.tail, xs2.tail, f))
                    }
            }

        // 연습문제 3.23
        tailrec fun <A> startsWith(l1: List<A>, l2: List<A>): Boolean =
            when (l1) {
                is Nil -> l2 == Nil
                is Cons -> when (l2) {
                    is Nil -> true
                    is Cons -> if (l1.head == l2.head) startsWith(l1.tail, l2.tail) else false
                }
            }

        tailrec fun <A> hasSubsequence(xs: List<A>, sub: List<A>): Boolean =
            when (xs) {
                is Nil -> false
                is Cons ->
                    if (startsWith(xs, sub)) true
                    else hasSubsequence(xs.tail, sub)
            }
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


    println("reverse = ${List.reverse(members)}")

    println("appendR = ${List.append(members, List.of("BTS", "ARMY"))}")

    // 연습문제 3.9
    try {
        val largeList = List.of(*Array(9000) { it })
        val result = List.length(largeList)
        println("Length of the list: $result")

        println("sum using foldLeft = ${List.sum(largeList)}")
    } catch (e: StackOverflowError) {
        println("Stack overflow occurred. The function is not stack-safe.")
    }

    val numbers = List.of(1, 2, 3, 4, 5)
    val sumOfResult = List.foldLeft(numbers, 0) { acc, num -> acc + num }
    println("$sumOfResult")

    println("lengthL = ${List.lengthL(members)}")

    println("${List.reverse(members)}")

    println("filter = ${List.filter(numbers) { x -> x > 3 }}")
    println("filter = ${List.filter(members) { name -> name.contains("J") }}")

    println("flatMap = ${List.flatMap(List.of(1, 2, 3)) { i -> List.of(i, i) }}")

    println("filterM = ${List.filterM(numbers) { x -> x > 3 }}")
    println("filterM = ${List.filterM(members) { name -> name.contains("J") }}")

    println("add = ${List.add(List.of(1, 2, 3), List.of(4, 5, 6))}")
    println("zipWith(add)= ${List.zipWith(List.of(1, 2, 3), List.of(4, 5, 6)) { a, b -> a + b }}")

    println("zipWith(minus)= ${List.zipWith(List.of(1, 2, 3), List.of(10, 25, 36)) { a, b -> a - b }}")
    println("zipWith(plus)= ${List.zipWith(List.of("Jimin", "V", "JK"), List.of("JIN", "SUGA", "J-HOPE")) { a, b -> "$a+$b" }}")

    println("hasSubsequence = ${List.hasSubsequence(members, List.of("V"))}")
    println("hasSubsequence = ${List.hasSubsequence(List.empty(), List.of("V"))}")
    println("hasSubsequence = ${List.hasSubsequence(members, List.empty())}")
    println("hasSubsequence = ${List.hasSubsequence(members, List.of("JIMIN", "V"))}")
    println("hasSubsequence = ${List.hasSubsequence(members, List.of("SUGA", "JIMIN", "V"))}")
    println("hasSubsequence = ${List.hasSubsequence(members, List.of("RM", "JIN", "SUGA", "J-HOPE"))}")
}
