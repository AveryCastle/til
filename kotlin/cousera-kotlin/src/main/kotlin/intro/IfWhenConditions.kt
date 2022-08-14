package intro

fun responseToInput(input: String) = when (input) {
    "y", "yes" -> "I'm glad you agree."
    "n", "no" -> "Sorry to hear that."
    else -> "I don't understand you."
}

fun mix(c1: Color, c2: Color) = when (setOf(c1, c2)) {
    setOf(Color.RED, Color.YELLOW) -> Color.ORANGE
    setOf(Color.YELLOW, Color.BLUE) -> Color.GREEN
    setOf(Color.BLUE, Color.VIOLET) -> Color.INDIGO
    else -> throw Exception("Dirty Color")
}


fun main() {
    println(responseToInput("yes"))

    println(mix(Color.BLUE, Color.VIOLET))

    val dog = Dog("Jimin")
    val cat = Cat("Suga")

    howling(dog)
    howling(cat)

    println(getSound())
}


fun howling(pet: Pet) = when (pet) {
    is Dog -> pet.woof() // Smart Cast
    is Cat -> pet.meow()
}

fun getSound(): String = when (val pet = getMyFavoritePet()) {
    is Cat -> pet.meow()
    is Dog -> pet.woof()
    else -> "no cat, no dog"
}

fun getMyFavoritePet(): Pet {
    return Dog("V")
}


fun updateWeather(degrees: Int) {
    val (description, color) = when {
        degrees < 15 -> "cold" to Color.BLUE
        degrees < 25 -> "mild" to Color.ORANGE
        else -> "hot" to Color.RED
    }
}


enum class Color {
    RED, YELLOW, GREEN, ORANGE, BLUE, VIOLET, INDIGO
}

sealed class Pet(open val name: String)

class Dog(override val name: String) : Pet(name) {
    fun woof() = "I'm $name. woof~"
}

class Cat(override val name: String) : Pet(name) {
    fun meow() = "I'm $name. meow~"
}
