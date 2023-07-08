package ch09

fun main() {
    val treeNode = TreeNode("Hello").apply {
        addNode("World")
        addNode("BTS")
    }

    println(treeNode)

    val personRegistry = Registry<Person>()
    val person1 = Person("Jimin", 1)
    val person2 = Person("V", 2)

    personRegistry.items.add(person1)
    personRegistry.items.add(person2)

    for (person in personRegistry.items) {
        println("Name: ${person.name}, ID: ${person.id}")
    }

    val collection: Collection<Int> = setOf(1, 2, 3)

    if (collection is List<Int>) {
        println("list")
    }
}

class TreeNode<T>(val data: T) {
    private val _children = arrayListOf<TreeNode<T>>()
    var parent: TreeNode<T>? = null
        private set

    val children: List<TreeNode<T>> get() = _children

    fun addNode(data: T) = TreeNode(data).also {
        _children += it
        it.parent = this
    }

    override fun toString(): String =
        _children.joinToString(prefix = "$data {", postfix = "}")
}

interface Named {
    val name: String
}

interface Identified {
    val id: Int
}

class Registry<T> where T : Named, T : Identified {
    val items = ArrayList<T>()
}

class Person(override val name: String, override val id: Int) : Named, Identified
