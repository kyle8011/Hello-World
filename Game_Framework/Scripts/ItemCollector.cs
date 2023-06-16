using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using Text = TMPro.TextMeshProUGUI;
using System.Data;
using Mono.Data.Sqlite;

public class ItemCollector : MonoBehaviour
{
    private string dbName = "URI=file:GameData.db";
    private int kiwis = 0;

    [SerializeField] private Text kiwisText;

    [SerializeField] private AudioSource collectionSoundEffect;

    [SerializeField] private string playerName;

    private int maxKiwis = 0;

    // Add a boolean value that can be applied to the character
    // once all kiwis have been collected
    
    private void Start()
    {
        // Get the Player's name
        playerName = GetPlayerName();
        //Debug.Log(playerName);
        maxKiwis = GameObject.FindGameObjectsWithTag("Kiwi").Length;
        kiwis = KiwiDestroyer();
        kiwisText.text = "Kiwis:" + kiwis + "/" + maxKiwis;
    }
    private string GetPlayerName()
    {
        GameObject go = GameObject.Find("PlayerName");
        PlayerName cs = go.GetComponent<PlayerName>();
        return (cs.playerName);
    }
    private void OnTriggerEnter2D(Collider2D collision) 
    {
        // If you run into the kiwi
        if (collision.gameObject.CompareTag("Kiwi")) {
            // Delete the object
            Destroy(collision.gameObject);
            // Play noise
            collectionSoundEffect.Play();
            // Add 1 to kiwis
            kiwis++;
            kiwisText.text = "Kiwis:" + kiwis + "/" + maxKiwis;
            AddKiwi(collision.gameObject.scene.name, collision.gameObject.name);
        }
    }

    private int KiwiDestroyer()
    {
        string level = SceneManager.GetActiveScene().name;
        int count = 0;
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
                        // Get name, level, kiwiname from the Database
                        string  row_name = reader["name"].ToString();
                        string row_level = reader["level"].ToString();
                        string kiwi_name = reader["kiwiname"].ToString();
                        // Determine if name and level match what is selected
                        if (row_name == playerName && row_level == level) {
                            // Destroy the kiwi if it was already collected
                            Destroy(GameObject.Find(kiwi_name));
                            count++;
                        }
                        //Debug.Log(reader["kiwiname"]);
                    }
                    reader.Close();
                }
                command.ExecuteNonQuery();
            }
            connection.Close();
        }
        return count;
    }

    private void AddKiwi(string level, string kiwinumber)
    {
        using (var connection = new SqliteConnection(dbName))
        {
            connection.Open();
            using (var command = connection.CreateCommand())
            {
                command.CommandText = "INSERT INTO kiwiscollected (name, level, kiwiname) VALUES ('" + playerName + "', '" + level + "', '" + kiwinumber + "');";
                command.ExecuteNonQuery();
            }
            connection.Close();
        }
    }

    private void DisplayKiwis()
    {
        using (var connection = new SqliteConnection(dbName))
        {
            connection.Open();
            using (var command = connection.CreateCommand())
            {
                command.CommandText = "SELECT * FROM kiwiscollected;";
                using (IDataReader reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        Debug.Log("Name: " + reader["name"] + "\tlevel: " + reader["level"] + "\tkiwiname: " + reader["kiwiname"]);
                    }
                    reader.Close();
                }
                command.ExecuteNonQuery();
            }
            connection.Close();
        }
    }

}
