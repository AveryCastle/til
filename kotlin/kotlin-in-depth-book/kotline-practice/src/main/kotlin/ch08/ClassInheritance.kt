package ch08

open class Vehicle {
    var currentSpeed = 0

    open fun start() {
        println("I'm moving")
    }

    open fun stop() {
        println("Stopped")
    }
}

open class FlyingVehicle : Vehicle() {
    fun takeOff() {
        println("Taking off")
    }

    fun land() {
        println("Landed")
    }
}

class Aircraft(val seats: Int) : FlyingVehicle()

class Car : Vehicle() {
    override fun start() {
        println("I'm riding")
    }
}

class Boat : Vehicle() {
    override fun start() {
        println("I'm sailing")
    }

    override fun stop() {
        println("I'm stopping sailing...")
    }
}

fun startAndStop(vehicle: Vehicle) {
    vehicle.start()
    vehicle.stop()
}

fun main() {
    val aircraft = Aircraft(300)
    val vehicle: Vehicle = aircraft

    vehicle.start()
    vehicle.stop()

    aircraft.start()
    aircraft.takeOff()
    aircraft.land()
    aircraft.stop()
    println(aircraft.seats)

    println("${People.birthday} ${People.name}")

    val john = JohnDoe

    startAndStop(Car())
    startAndStop(Boat())

    val suga = Korean("민윤기")
    println(suga.name)

    val onyou = Student("2010-11-12", "onyou", "secho")
    println("${onyou.name} - ${onyou.birthday} - ${onyou.school}")
}

data class Person(val birthday: String, val name: String)

open class People {
    val birthday: String
    val name: String

    constructor(birthday: String, name: String) {
        this.birthday = birthday
        this.name = name
    }

    constructor(birthday: String, firstName: String, familyName: String) :
            this(birthday, "$firstName $familyName") {
    }


    companion object : People("1995-10-03", "Jimin")

}

// object로 클래스를 정의하면, 싱클턴(Singleton) 패턴이 적용되어 객체가 한번만 생성되도록 합니다.
object JohnDoe : People("2020-04-01", "V")

//class Student(birthday: String, name: String, val school: String) : People(birthday, name)
class Student : People {
    val school: String

    constructor(birthday: String, name: String, school: String) : super(birthday, name) {
        this.school = school
    }
}

open class Entity {
    open val name: String get() = ""
}

class Korean(override val name: String) : Entity()

class American() : Entity() {
    override var name: String = ""
}
