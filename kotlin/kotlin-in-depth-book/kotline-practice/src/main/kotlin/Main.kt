import ch03.circleArea
import ch03.divide

fun main() {
    println("Hello World!")

//    val a = readLine()!!.toInt()
//    val b = readLine()!!.toInt()
//
//    println(a + b)

    println(circleArea(10.5))

    println(divide("1234567789011", 10))

    println("def" in "abc".."xyz")
    println("def" in "aaa".."zzz")
    println(10 in 1..10)
    println(5 in 10 downTo 1)
    println(5 in 10 downTo 1 step 2)
    println(5 in 1 until 10 step 2)

    var sum = 0
    val a = IntArray(10) { it * it }
    for (x: Int in a) {
        sum += x
    }
    println(sum)

    for (n: Int in 1..100) {
        println(n)
    }
}
