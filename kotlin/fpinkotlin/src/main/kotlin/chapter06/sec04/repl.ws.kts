import chapter06.sec02.SimpleRNG
import chapter06.sec04.rollDie
import chapter06.sec04.rollDieFix

val rng = SimpleRNG(5)
val result = rollDie()(rng)
result

val result2 = rollDieFix()(rng)
result2
