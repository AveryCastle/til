package ch05

import ch05.Direction.*
import java.time.Period

enum class Direction {
    NORTH, EAST, SOUTH, WEST;

    val lowerCaseName get() = name.lowercase()
    fun isUpper() = this == NORTH
}

enum class RainbowColor(val isCold: Boolean) {
    RED(false), ORANGE(false), YELLOW(false),
    GREEN(true), BLUE(true), INDIGO(true);

    val isWarm get() = !isCold
}

fun rotateClockWise(direction: Direction) = when (direction) {
    NORTH -> EAST
    EAST -> SOUTH
    SOUTH -> WEST
    WEST -> NORTH
}

fun main() {
    println(rotateClockWise(EAST))

    println(NORTH.isUpper())
    println(NORTH.lowerCaseName)
    println(EAST.isUpper())
    println(EAST.lowerCaseName)

    println(RainbowColor.BLUE.isCold)
    println(RainbowColor.ORANGE.isCold)

    println(WeekDay.valueOf("MONDAY"))
//    println(WeekDay.valueOf("MONDAY_TUESDAY")) // error!

    val weekDays = enumValues<WeekDay>()

    println(weekDays[2])
    println(enumValueOf<WeekDay>("THURSDAY"))

    val jimin = Person("Jimin", "Park").apply { age = 28 }
    jimin.show()

    jimin.copy().show()
    jimin.copy().apply { age = 10 }.show()
    val v = jimin.copy("V", "Kim").apply { age = 28 }
    v.show()

    val (firstName, secondName) = jimin
    println("$firstName, $secondName")

}

enum class WeekDay {
    MONDAY {
        fun startWork() = println("Work week started!")
    },
    TUESDAY, WEDNESDAY, THURSDAY, SUNDAY
}


data class Person(
    val firstName: String,
    val familyName: String
) {
    var age = 0
}

fun Person.show() = println("$firstName $familyName: $age")
