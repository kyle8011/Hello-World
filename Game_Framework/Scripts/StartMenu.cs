using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;
using System.Data;
using Mono.Data.Sqlite;
using Text = TMPro.TextMeshProUGUI;

public class StartMenu : MonoBehaviour
{
    private string dbName = "URI=file:GameData.db";
    //private string currentName = "none";
    //public List<string> kiwiDestroyList = new List<string>();
    private void Start()
    {
        // Make sure there is a database
        CreateDB();
    }

    public void Intro()
    {
        SceneManager.LoadScene(0);
    }
    
    public void NameCreator()
    {
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex + 1);
    }

    public void LoadGame()
    {
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex + 2);
    }
    private string GetPlayerName()
    {
        GameObject go = GameObject.Find("PlayerName");
        PlayerName cs = go.GetComponent<PlayerName>();
        return (cs.playerName);
    }
    private bool GetValidName()
    {
        GameObject go = GameObject.Find("PlayerName");
        PlayerName cs = go.GetComponent<PlayerName>();
        return (cs.name_ok);
    }
    public void LevelSelect()
    {
        Debug.Log("Entering Level Select");
        GameObject music = GameObject.Find("IntroMusic");
        if (music != null)
        {
            Debug.Log("Intro Music Destroyed");
            Destroy(music);
        }
        SceneManager.LoadScene(3);
    }

    public void EnterLevel(string levelName)
    {
        SceneManager.LoadScene(levelName);
    }

    private void CreateDB()
    {
        using (var connection = new SqliteConnection(dbName))
        {
            connection.Open();
            using (var command = connection.CreateCommand())
            {
                    command.CommandText = "CREATE TABLE IF NOT EXISTS kiwiscollected (name VARCHAR(20), level VARCHAR(20), kiwiname VARCHAR(20));";
                    command.ExecuteNonQuery();
            }
            connection.Close();
        }
    }

}