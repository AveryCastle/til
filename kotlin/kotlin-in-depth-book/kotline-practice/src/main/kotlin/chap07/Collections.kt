package chap07

class Person(
    val firstName: String,
    val familName: String,
    val age: Int
) : Comparable<Person> {
    val fullName get() = "$firstName $familName"

    override fun compareTo(other: Person): Int = fullName.compareTo(other.fullName)
}

val numbers = sequence {
    yield(10)
    yield(100)
    yieldAll(listOf(1, 3, 5, 7))
}

fun main() {
    println(numbers.toList())

    val mutableList = mutableListOf(1, 2, 3)
    mutableList += 4

    mutableList[2]


    println(listOf(1, 2, 3).fold(0) { sum, element -> sum + element })
    println(listOf(1, 2, 3).reduce { sum, element -> sum + element })

}
