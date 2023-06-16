using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class PlayerLife : MonoBehaviour
{
    private Rigidbody2D rb;
    private Animator anim;

    [SerializeField] AudioSource deathSoundEffect;
    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        anim = GetComponent<Animator>();
    }

    private void OnCollisionEnter2D(Collision2D collision)
    {
        // If you collide with a trap
        if (collision.gameObject.CompareTag("Trap")) {
            // Player dies
            Die();
        }
    }

    private void Die()
    {
        deathSoundEffect.Play();
        // Stop the player from moving
        rb.bodyType = RigidbodyType2D.Static;
        // Set Death to true
        anim.SetTrigger("Death");

    }

    private void RestartLevel()
    {
        SceneManager.LoadScene(SceneManager.GetActiveScene().name);
    }

}
