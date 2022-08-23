package intro

// this가 Receiver가 된다.
//fun String.lastChar(): Char = this.get(this.length - 1)
// Receiver this를 생략할 수 있다.
fun String.lastChar(): Char = get(this.length - 1)

fun String.repeat(n: Int): String {
    val sb = StringBuilder(n * length)
    for (i in 1..n) {
        sb.append(this)
    }
    return sb.toString()
}


fun main() {
    val to: Pair<String, Int> = "Jimin".to(27)
    println(to)

    val infixForm: Pair<String, Int> = "V" to 27
    println(infixForm)

    val q1 = """To code,
        #or not to code?..""".trimMargin(marginPrefix = "#")
    println(q1)

    val q2 = """
        To code,
        or not to code?..
    """.trimIndent()
    println(q2)

    val regex = """\d{3}.\d{3}.\d{3}""".toRegex()
    println(regex.matches("127.0.1"))
    println(regex.matches("127.111.123"))

    // Conversion to Numbers
    println("123".toInt())
    println("1e-10".toDouble())

    println("Jimin".toIntOrNull())

    getNumber() eq 27
    getNumber() eq 28


    val sum = listOf(1, 2, 3).sum()
    println(sum)    // 6

    val a = A()
    println(a.foo()) // signature가 동일할 때는 member가 우선한다.
    println(a.foo(1))
}

fun getNumber() = 27

infix fun <T> T.eq(other: T) {
    if (this == other) println("OK")
    else println("Error: $this != $other")
}

fun List<Int>.sum(): Int {
    var result = 0
    for (i in this) {
        result += i
    }
    return result
}

class A {
    fun foo() = "abcd"
}

fun A.foo() = "changed!"

fun A.foo(index: Int) = "$index"
