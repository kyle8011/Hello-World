using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Text = TMPro.TextMeshProUGUI;
using System.Data;
using Mono.Data.Sqlite;

public class KiwiData : MonoBehaviour
{
    private string dbName = "URI=file:GameData.db";
    [SerializeField] public Text kiwiAmount;
    [SerializeField] private string level;
    // Start is called before the first frame update
    void Start()
    {
        int count = 0;
        string playerName = GetPlayerName();
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
                        // Determine if name and level match what is selected
                        if (row_name == playerName && row_level == level) {
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
        kiwiAmount.text = count.ToString();
    }

    private string GetPlayerName()
    {
        GameObject go = GameObject.Find("PlayerName");
        PlayerName cs = go.GetComponent<PlayerName>();
        return (cs.playerName);
    }

}
