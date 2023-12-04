import chapter06.sec02.SimpleRNG
import chapter06.sec03.randomPair
import chapter06.sec03.randomPair2

val rng1 = SimpleRNG(10)

val (n1, n2) = randomPair(rng1)
n1
n2


val (i1, i2) = randomPair2(rng1)
i1
i2
