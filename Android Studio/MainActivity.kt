package com.example.tictactoe

import android.content.Context
// This is used to save data
import android.content.SharedPreferences
import android.os.Bundle
import android.view.View
import android.widget.Button
// This can display a note on the screen
import android.widget.Toast
// This displays an alert on the screen
import androidx.appcompat.app.AlertDialog
// This was needed for button compatibility
import androidx.appcompat.app.AppCompatActivity
import com.example.tictactoe.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {

    // This just made it easier to read what turn it is
    enum class Turn {
        O,
        X
    }
    // Initializing who's turn it is, starting with x
    private var firstTurn = Turn.X
    private var currentTurn = Turn.X
    // Keeping track of the score
    private var xScore = 0
    private var oScore = 0
    // Get a list of the buttons
    private var boardList = mutableListOf<Button>()
    // Initialize the buttons
    private lateinit var binding : ActivityMainBinding

    // On page startup
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Set up the buttons
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        // Load saved data
        loadData()
        // Add buttons to the board
        initBoard()
    }

    // This just adds all the buttons to the board
    private fun initBoard() {
        boardList.add(binding.a1)
        boardList.add(binding.a2)
        boardList.add(binding.a3)
        boardList.add(binding.b1)
        boardList.add(binding.b2)
        boardList.add(binding.b3)
        boardList.add(binding.c1)
        boardList.add(binding.c2)
        boardList.add(binding.c3)
    }
    // What happens when the screen is touched
    fun boardTapped(view: View) {
        // Check if a button was pressed
        if(view !is Button)
            return
        // If so then add that button to the board
        addToBoard(view)

        // Check if O's have won
        if(checkForVictory("O")) {
            oScore++
            result("O Wins!")
        }
        // Check if X's have won
        if(checkForVictory("X")) {
            xScore++
            result("X Wins!")
        }
        // Check if all the spaces have been filled
        if(fullBoard()){
            result("Draw")
        }
    }

    private fun checkForVictory(s: String): Boolean {
        // Check for horizontal win conditions
        if(match(binding.a1, s) && match(binding.a2, s) && match(binding.a3, s))
            return true
        if(match(binding.b1, s) && match(binding.b2, s) && match(binding.b3, s))
            return true
        if(match(binding.c1, s) && match(binding.c2, s) && match(binding.c3, s))
            return true

        // Check for vertical win conditions
        if(match(binding.a1, s) && match(binding.b1, s) && match(binding.c1, s))
            return true
        if(match(binding.a2, s) && match(binding.b2, s) && match(binding.c2, s))
            return true
        if(match(binding.a3, s) && match(binding.b3, s) && match(binding.c3, s))
            return true

        // Check for diagonal win conditions
        if(match(binding.a1, s) && match(binding.b2, s) && match(binding.c3, s))
            return true
        if(match(binding.a3, s) && match(binding.b2, s) && match(binding.c1, s))
            return true

        return false
    }
    // This just checks if two strings are the same
    private fun match(button: Button, symbol: String) = button.text == symbol
    // This saves data and displays the score
    private fun result(title: String) {
        saveData(xScore, oScore)
        val message = "\n O: $oScore \n\n X: $xScore"
        // Display the score via an alert message (also resets the board)
        AlertDialog.Builder(this)
            .setTitle(title)
            .setMessage(message)
            .setPositiveButton("Reset")
            { _,_ ->
                resetBoard()
            }
            .setCancelable(false)
            .show()
    }
    // This will save two integer inputs to sharedPreferences
    private fun saveData(X: Int = 0, O: Int = 0) {
        val sharedPreferences: SharedPreferences = getSharedPreferences("sharedPrefs", Context.MODE_PRIVATE)
        val editor : SharedPreferences.Editor = sharedPreferences.edit()
        editor.apply {
            putInt("xScore", X)
            putInt("oScore", O)

        }.apply()
        // Show that data saving worked
        Toast.makeText(this, "Data Saved", Toast.LENGTH_SHORT).show()
    }
    // Put sharedPreferences data into the score variables
    private fun loadData() {
        val sharedPreferences: SharedPreferences = getSharedPreferences("sharedPrefs", Context.MODE_PRIVATE)
        val xInt: Int = sharedPreferences.getInt("xScore", 0)
        val oInt: Int = sharedPreferences.getInt("oScore", 0)

        xScore = xInt
        oScore = oInt

    }
    // Set all button's text to blank and swap who starts
    private fun resetBoard() {
        for(button in boardList) {
            button.text = ""
        }
        // Swap who's turn it is
        if(firstTurn == Turn.O)
            firstTurn = Turn.X
        else if (firstTurn == Turn.X)
            firstTurn = Turn.O

        currentTurn = firstTurn
        // Print who's turn it is now
        setTurnLabel()
    }
    // Check for cat's game
    private fun fullBoard(): Boolean {
        // Will return false if any spot is still blank
        for(button in boardList) {
            if(button.text == "")
                return false
        }
        return true
    }
    // Add a selection to the board
    private fun addToBoard(button: Button) {
        // Check that the button hasn't been pressed yet
        if(button.text != "")
            return
        // Place an O if it's that turn
        if(currentTurn == Turn.O) {
            button.text = "O"
            currentTurn = Turn.X
        }
        // Place an X if it's that turn
        else if(currentTurn == Turn.X) {
            button.text = "X"
            currentTurn = Turn.O
        }
        // Display the change in turns
        setTurnLabel()
    }
    // Displays the change in turn
    private fun setTurnLabel() {
        var turnText = ""
        // Displays Turn X
        if(currentTurn == Turn.X)
            turnText = "Turn X"
        // Displays Turn O
        else if (currentTurn == Turn.O)
            turnText = "Turn O"
        binding.turnTV.text = turnText
    }
}
