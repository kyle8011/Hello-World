using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Text = TMPro.TextMeshProUGUI;
using System.Data;
using Mono.Data.Sqlite;

public class ButtonText : MonoBehaviour
{
    private string dbName = "URI=file:GameData.db";
    [SerializeField] private Text slotText;
    // Start is called before the first frame update
    void Start()
    {
        slotText.text = "empty";
        int button_count = 0;
        int button_num = 0;
        if (this.name == "Button (2)") button_num = 1;
        if (this.name == "Button (3)") button_num = 2;
        // Get the first 3 names, based on which button this is
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
                        string row_level = reader["level"].ToString();
                        if (row_level == "Level 0") {
                            // Set names to buttons
                            if (button_count == button_num) slotText.text = row_name;
                            button_count++;
                        }
                    }
                    reader.Close();
                }
                command.ExecuteNonQuery();
            }
            connection.Close();
        }

    }

    public void GetNameFromLoad()
    {
        GameObject go = GameObject.Find("PlayerName");
        PlayerName cs = go.GetComponent<PlayerName>();
        cs.playerName = slotText.text;
    }
}
