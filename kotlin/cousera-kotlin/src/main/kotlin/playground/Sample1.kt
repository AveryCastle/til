package playground

fun main(args: Array<String>) {
    val s1: String? = null
    val s2: String? = ""

    s1.isEmptyOrNull() eq true
    s2.isEmptyOrNull() eq false

    val s3 = " "
    s3.isEmptyOrNull() eq false
}

fun String?.isEmptyOrNull(): Boolean = this.isNullOrEmpty()

infix fun <T> T.eq(other: T) {
    if (this == other) println("Ok")
    else println("Error: $this != $other")
}

