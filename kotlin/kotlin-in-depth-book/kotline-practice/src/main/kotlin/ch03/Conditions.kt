package ch03

fun max(a: Int, b: Int): Int {
    if (a > b) return a
    return b
}

fun divide(s: String, i: Int): String {
    val result: String = if (i > 5) {
        val a = s.substring(0, i).toInt()
        val b = s.substring(i + 1).toInt()
        (a / b).toString()
    } else ""

    return result
}

fun hexDigit(n: Int): Char = when (n) {
    in 0..9 -> '0' + n
    in 10..15 -> 'A' + n - 10
    else -> '?'
}

fun length(s: String?): Int? = s?.length

fun strictLength(s: String?): Int = length(s) ?: 0
