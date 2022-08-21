package playground

fun main(args: Array<String>) {
    val s: String? = "a"
//    println(s as? Int) // null
    println(s as Int?) // exception
}