package chapter06.sec01

import kotlin.random.Random

fun rollDie(): Int {
    val rng = Random
    return rng.nextInt(6)
}

interface RNG {
    fun nextInt(): Pair<Int, RNG>
}
