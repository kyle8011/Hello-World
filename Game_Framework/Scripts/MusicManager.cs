using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class MusicManager : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        // Don't destroy music for 3 intro screens
        Debug.Log("Music Created");
        if (SceneManager.GetActiveScene().buildIndex < 3)
        {
            DontDestroyOnLoad(this.gameObject);
        }
        
    }

    void update()
    {
        Debug.Log("Music Not Destroyed");
        if (SceneManager.GetActiveScene().buildIndex > 2)
        {
            DestroyMusic();
            Debug.Log("Music Destroyed");
        }
    }

    public void DestroyMusic()
    {
        Destroy(this.gameObject);
    }
}
