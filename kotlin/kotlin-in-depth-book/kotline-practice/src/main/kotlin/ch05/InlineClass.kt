package ch05

inline class Dollar(val amount: Int) {
    fun add(d: Dollar) = Dollar(amount + d.amount)
    val isDept get() = amount < 0
}

fun main() {
    println(Dollar(15).add(Dollar(100)).amount)
    println(Dollar(-10).isDept)
}
