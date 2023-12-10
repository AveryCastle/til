package chapter06.sec04

import chapter06.sec01.RNG

typealias Rand<A> = (RNG) -> Pair<A, RNG>

fun <A> unit(a: A): Rand<A> = { rng -> a to rng }

fun <A, B> map(s: Rand<A>, f: (A) -> B): Rand<B> =
    { rng ->
        val (a, rng2) = s(rng)
        f(a) to rng2
    }

fun nonNegativeInt(rng: RNG): Pair<Int, RNG> {
    val (i1, rng2) = rng.nextInt()
    return (if (i1 < 0) -(i1 + 1) else i1) to rng2
}

fun noneNegativeEven(): Rand<Int> =
    map(::nonNegativeInt) { it - (it % 2) }

fun <A, B, C> map2(
    ra: Rand<A>,
    rb: Rand<B>,
    f: (A, B) -> C
): Rand<C> = { rng ->
    val (a, rng2) = ra(rng)
    val (b, rng3) = rb(rng2)
    f(a, b) to rng3
}

fun <A, B> both(ra: Rand<A>, rb: Rand<B>): Rand<Pair<A, B>> =
    map2(ra, rb) { a: A, b: B -> a to b }

val intR: Rand<Int> = { rng: RNG -> rng.nextInt() }

val doubleR: Rand<Double> = map(::nonNegativeInt) { i: Int ->
    i / (Int.MAX_VALUE.toDouble() + 1)
}

val intDoubleR: Rand<Pair<Int, Double>> = both(intR, doubleR)

val doubleIntR: Rand<Pair<Double, Int>> = both(doubleR, intR)

fun nonNegativeLessThan(n: Int): Rand<Int> =
    map(::nonNegativeInt) { it % n }

fun nonNegativeLessThan2(n: Int): Rand<Int> =
    { rng: RNG ->
        val (i, rng2) = nonNegativeInt(rng)
        val mod = i % n
        if (i + (n - 1) - mod >= 0)
            mod to rng2
        else nonNegativeLessThan(n)(rng2)
    }
