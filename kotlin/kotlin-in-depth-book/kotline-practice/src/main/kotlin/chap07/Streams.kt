package chap07

import java.io.*


fun main() {
    FileWriter("src/main/resources/data.txt").use { it.write("BTS JIMIN!") }

    val writer = StringWriter()
    FileReader("src/main/resources/data.txt").use { it.copyTo(writer) }
    println(writer.buffer)

    val output = ByteArrayOutputStream()
    FileInputStream("src/main/resources/data.txt").use { it.copyTo(output) }
    println(output.toString("UTF-8"))

    File("src/main/resources/old/dir").mkdirs()
    File("src/main/resources/old/dir/ori.txt").also { it.writeText("Jimin") }
    File("src/main/resources/old/dir/change.txt").also { it.writeText("JK") }

    File("src/main/resources/old").copyRecursively(
        File("src/main/resources/new"))

    println(File("src/main/resources/new/dir/ori.txt").readText())
    println(File("src/main/resources/new/dir/change.txt").readText())
}
