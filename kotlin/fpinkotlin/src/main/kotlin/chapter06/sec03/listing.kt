package chapter06.sec03

import chapter06.sec01.RNG

fun randomPair(rng: RNG): Pair<Int, Int> {
    val (i1, _) = rng.nextInt()
    val (i2, _) = rng.nextInt()
    return i1 to i2
}

fun randomPair2(rng: RNG): Pair<Int, Int> {
    val (i1, rng1) = rng.nextInt()
    val (i2, _) = rng1.nextInt()
    return i1 to i2
}
