@file: JvmName("KotlinUtil")

package intro

// Top Level에 function 정의를 함.
fun main(args: Array<String>) {
    // if: expression
    val name = if (args.isNotEmpty()) args[0] else "Kotlin"
    println("Hello, $name!")
    println("Hello, ${args.getOrElse(0) { "Anonymous" }}")

    println("First ${foo()} - Second ${foo()}")

    println(listOf('a', 'b', 'c').joinToString(separator = "", prefix = "(", postfix = ")"))

    displaySeparator(size = 3)
}

fun foo(): String {
    println("Calculating foo")
    return "foo"
}

fun max(a: Int, b: Int): Int = if (a > b) a else b

@JvmOverloads
fun displaySeparator(character: Char = '*', size: Int = 10): Unit {
    repeat(size) {
        print(character)
    }
}
