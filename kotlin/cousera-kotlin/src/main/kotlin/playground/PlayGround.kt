package playground

fun isValidChecking(str: String): Boolean {
    fun isValidNumberOrChar(ch: Char): Boolean = ch.isLetterOrDigit()

    if (str.isEmpty() || (!str[0].isLetter() && str[0] != '_')) {
        return false
    }


    for (ch in str.substring(1)) {
        if (!isValidNumberOrChar(ch)) return false
    }

    return true
}


fun List<Int>.summarize(): Int {
    var sum = 0
    for (num in this) {
        sum += num
    }
    return sum
}

fun main() {
    println(isValidChecking("name"))
    println(isValidChecking("_name"))
    println(isValidChecking("_12"))
    println(isValidChecking(""))
    println(isValidChecking("012"))
    println(isValidChecking("no$"))

    val sum = listOf(1, 2, 3).summarize()
    println(sum)
}
