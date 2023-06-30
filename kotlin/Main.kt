import java.util.Random
import kotlin.math.sqrt

val random = Random()

fun main(args: Array<String>) {
    // Get the name and age from text function
    val (name, age) = test()
    println("Got $name and $age from test function")

    // Create two people, introduce the first one
    val person = Person(name, age)
    person.introduce()
    val testPerson = Person("bot", 100)

    // Move the people
    person.moveRand()
    testPerson.moveRand()

    // Calculate the distance
    val distance = person.getDistance(testPerson.getLocation())
    println("Distance between people: $distance")

    // Try adding program arguments via Run/Debug configuration.
    // Learn more about running applications: https://www.jetbrains.com/help/idea/running-applications.html.
    println("Program arguments: ${args.joinToString()}")
}

/**
 * This class can introduce itself with the given
 * name and age through the introduce method.
 * You can also change the person's location and
 * get the location through the other methods
 */
class Person(private val firstName: String, private var age: Int) {
    // Original person location
    private var x = 5
    private var y = 5

    /**
     * Have the person introduce him or herself
     */
    fun introduce() {
        println("My name is $firstName and I am $age years old")
    }

    /**
     * Get an (x, y) pair location of the person
     */
    fun getLocation(): Pair<Int, Int> {
        return Pair(x, y)
    }
    /**
     * Calculate the distance between the person and an x, y coordinate
     */
    fun getDistance(coordinates: Pair<Int, Int>): Double {
        // These are expressions!
        val xDiff = (x - coordinates.first)
        val yDiff = (y - coordinates.second)
        return sqrt((xDiff * xDiff + yDiff * yDiff).toDouble())
    }
    private fun moveUp() {
        println("UP")
        y += 1
    }
    private fun moveDown() {
        if (y > 0) {
            println("DOWN")
            y -= 1
        }
    }
    private fun moveLeft() {
        if (x > 0) {
            println("LEFT")
            x -= 1
        }
    }
    private fun moveRight() {
        println("RIGHT")
        x += 1
    }

    /**
     * Move the person in 10 random directions
     */
    fun moveRand() {
        val movements = List(10) {random.nextInt(0, 4)}
        println("\n($firstName) Starting location: " + getLocation())
        for (x in movements) {
            if (x == 0) moveUp()
            if (x == 1) moveDown()
            if (x == 2) moveLeft()
            if (x == 3) moveRight()
        }
        println("($firstName) Final location: " + getLocation())
    }
}

/**
 * This function prints out several different data types,
 * then asks for user input of name and age. It checks if
 * age is a valid number than returns both the name and age.
 *
 * You can input a default age as an argument to return if
 * user input does not match the integer requirements.
 */
fun test(defaultAge: Int = 0): Pair<String, Int> {
    // Mutable - the contents of a list can be changed (var)
    // Read-Only - The contents of a collection are not changed,
    // the underlying data can be changed though
    // Immutable - Nothing can change the contents of a collection (val)
    val list: List<String> = listOf("This", "Is", "Totally", "Immutable")
    println(list)
    (list as MutableList<String>)[2] = "Not"
    println(list)

    // Variable types
    val int = 5
    val long = int.toLong()
    val double = 3.14
    val char = 'P'
    val bool = true
    val text = "Hello"
    val array = arrayOf(int, long, double, char, bool, text)
    val types = arrayOf("int", "long", "double", "char", "bool", "string")
    //https://www.tutorialkart.com/kotlin/kotlin-array-size/#gsc.tab=0
    for (x in 1 until array.size) {
        print(array[x])
        print(" is of type ")
        println(types[x])
    }

    // Creating a variable with val can not be changed
    // val should only be used with constant variables
    print("Enter your name: ")
    val name = readln()
    print("Enter your age: ")
    val age = readln()
    val check = age.intOrString()
    if (check) {
        if (age.toInt() in 1..100) {
            println("\nvalid inputs")
            return Pair(name, age.toInt())
        }
        else {
            println("That is not a valid age range")
        }
    }
    else {
        println("That is not an integer")
    }
    return Pair(name, defaultAge)
}

/**
 * This function will return true if the value
 * is a string and false if it is not.
 */
fun String.intOrString(): Boolean{
    // Using the "when" expression
    return when(toIntOrNull()) {
        null -> false
        else -> true
    }
}