package chapter06

import chapter06.sec01.RNG


val rng1 = object : RNG {
    override fun nextInt() = 1 to this
}
