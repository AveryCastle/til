package chapter06.sec02

import chapter06.sec01.RNG


data class SimpleRNG(val seed: Long) : RNG {
    override fun nextInt(): Pair<Int, RNG> {
        val newSeed: Long =
            (seed * 0x5DEECE66DL + 0xBL) and
                    0xFFFFFFFFFFFFL // <1>
        val nextRNG: SimpleRNG = SimpleRNG(newSeed) // <2>
        val n: Int = (newSeed ushr 16).toInt() // <3>
        return n to nextRNG // <4>
    }
}
