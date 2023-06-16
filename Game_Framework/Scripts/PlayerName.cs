using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Text = TMPro.TextMeshProUGUI;
using System.Data;
using Mono.Data.Sqlite;

public class PlayerName : MonoBehaviour
{
    [SerializeField] private Text nameText;
    
    private string dbName = "URI=file:GameData.db";

    public string playerName = "name";
    public bool name_ok = false;
    
    //public string saveName;

    //public Text inputText;
    //public Text loadedName;
    void Start()
    {
        // So it carries through the game
        DontDestroyOnLoad(this.gameObject);
    }

    public void GetNameFromLoad(string name)
    {
        Debug.Log("hello");
    }

    public void AddPlayerName()
    {
        // Check that name was not already taken
        name_ok = true;
        playerName = nameText.text;
        using (var connection = new SqliteConnection(dbName))
        {
            connection.Open();
            using (var command = connection.CreateCommand())
            {
                command.CommandText = $"SELECT * FROM kiwiscollected";
                using (IDataReader reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        // Get name and level from the Database
                        string  row_name = reader["name"].ToString();
                        Debug.Log(row_name);
                        string row_level = reader["level"].ToString();
                        //Debug.Log(row_level);
                        //Debug.Log(playerName);
                        if (row_name == playerName && row_level == "Level 0") {
                            // Set ok variable to false if already in data
                            name_ok = false;
                            //Debug.Log(row_name);
                        }
                        //Debug.Log(reader["kiwiname"]);
                    }
                    reader.Close();
                }
                command.ExecuteNonQuery();
            }
            connection.Close();
        }
        // Add player name with Level 0
        if (name_ok == true)
        {
            using (var connection = new SqliteConnection(dbName))
            {
                connection.Open();
                using (var command = connection.CreateCommand())
                {
                    command.CommandText = "INSERT INTO kiwiscollected (name, level, kiwiname) VALUES ('" + playerName + "', 'Level 0', 'N/A');";
                    command.ExecuteNonQuery();
                }
                connection.Close();
            }
        }
        
    }
    // public void SetName()
    // {
    //     // Set the public variable
    //     playerName = nameText.text;
    // }
}
