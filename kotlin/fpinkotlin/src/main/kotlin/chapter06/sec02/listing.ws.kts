import chapter06.sec02.SimpleRNG

val rng = SimpleRNG(42)

val (n1, rng2) = rng.nextInt()

n1

rng2

val (n2, rng3) = rng2.nextInt()

n2

rng3
