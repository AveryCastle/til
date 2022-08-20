package intro

fun main(args: Array<String>) {
//    val f1: () -> Int? = null
    val f2: () -> Int? = { null }
    val f3: (() -> Int)? = null
//    val f4: (() -> Int)? = { null }

//    f3() // error
    if (f3 != null) { // # way1
        f3()
    }
    println(f3?.invoke()) // # way2
}