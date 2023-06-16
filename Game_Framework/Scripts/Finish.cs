using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using static ItemCollector;

public class Finish : MonoBehaviour
{

    private AudioSource finishSound;

    private bool levelCompleted = false;

    private int maxKiwis = 0;

    
    // Start is called before the first frame update
    private void Start()
    {
        finishSound = GetComponent<AudioSource>();
        maxKiwis = GameObject.FindGameObjectsWithTag("Kiwi").Length;
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.gameObject.name == "Player" && !levelCompleted) {
            if (true) // Add a boolean check if all kiwis have been collected
            {
                finishSound.Play();
                levelCompleted = true;
                Invoke("CompleteLevel", 2f); // Call CompleteLevel after 2 seconds
            }
        }
    }

    private void CompleteLevel()
    {
        SceneManager.LoadScene(3);
    }

}
