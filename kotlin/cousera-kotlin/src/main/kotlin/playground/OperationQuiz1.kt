package playground

data class Hero(
    val name: String,
    val age: Int,
    val gender: Gender?,
)

enum class Gender {
    FEMALE, MALE,
}

fun main(args: Array<String>) {
    val heros = listOf(
        Hero("JungKook", 25, Gender.MALE),
        Hero("V", 27, Gender.MALE),
        Hero("Jimin", 27, Gender.MALE),
        Hero("J-Hope", 28, Gender.MALE),
        Hero("SUGA", 29, Gender.MALE),
        Hero("JIN", 30, Gender.MALE),
        Hero("RM", 28, Gender.MALE),
        Hero("Army", 0, null),
        Hero("The Captain", 37, Gender.FEMALE)
    )

    println(heros.last().name)

    println(heros.firstOrNull { it.age >= 30 }?.name)
//    println(heros.oldest { it.age >= 30 }?.name) // throw exception

    println(heros.map { it.age }.distinct().size)

    val (oldest, youngest) = heros.partition { it.age >= 30 }
    println("${oldest.size}, ${youngest.size}")

    println(heros.maxBy { it.age }?.name)

    println(heros.all { it.age < 30 })

    println(heros.any { it.gender == null })

    val mapByAge: Map<Int, List<Hero>> = heros.groupBy { it.age }
    val (age, size) = mapByAge.maxBy { (_, group) -> group.size }!!
    println(age)

    val mapByName: Map<String, Hero> = heros.associateBy { it.name }
    println(mapByName["V"]?.age)

    val mapByName2: Map<String, Int> = heros.associate { it.name to it.age }
    println(mapByName2.getOrElse("unknown") { 0 })

    val allPossibleCases = heros.flatMap { first -> heros.map { second -> first to second } }
    val (oldest1, youngest1) = allPossibleCases.maxBy { it.first.age - it.second.age }!!
    println("${oldest1.name}, ${youngest1.name}")
}