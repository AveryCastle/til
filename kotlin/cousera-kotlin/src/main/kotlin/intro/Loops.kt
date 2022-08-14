package intro

val memberOfBts = mapOf("V" to 27, "Jimin" to 27, "SUGA" to 29)

fun main() {
//    for ((name, age) in memberOfBts) {
//        println("$name is $age years old.")
//    }
//
//    for ((index, element) in listOf(1, 2, 3, 4, 5).withIndex()) {
//        println("[$index] = $element")
//    }
//
//    for (i in 100..110) { // including
//        println(i)
//    }
//
    for (i in 1 until 10) { // excluding
        println(i)
    }
//
//    for (i in 100 downTo 90 step 3) {
//        println(i)
//    }
//
//    for (c in '0' until '9') {
//        print(c)
//    }
//
//
//    println(recognize('*'))
//    println(recognize('7'))
//    println(recognize('A'))
//
//    println("Kotlin" in "Java" .. "Scala") // "Java".compareTo("Kotlin") <= 0 && "Kotlin".compareTo("Scala") <= 0
//    println("Kotlin" in setOf("Java", "Scala"))

    println(isValidIdentifier("name"))   // true
    println(isValidIdentifier("_name"))  // true
    println(isValidIdentifier("_12"))    // true
    println(isValidIdentifier(""))       // false
    println(isValidIdentifier("012"))    // false
    println(isValidIdentifier("no$"))    // false

}

fun recognize(c: Char): String = when (c) {
    in '0'..'9' -> "It's a digit."
    in 'a'..'z', in 'A'..'Z' -> "It's a alphabet."
    else -> "I don't know."
}


fun isValidIdentifier(s: String): Boolean {
    fun isValidCharacter(ch: Char) = ch == '_' || ch.isLetterOrDigit()

    if (s.isEmpty() || s[0] in '0'..'9') return false
    for (ch in s) {
        if (!isValidCharacter(ch)) return false
    }

    return true
}
