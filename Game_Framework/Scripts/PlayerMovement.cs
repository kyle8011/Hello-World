using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    private Rigidbody2D rb;
    private Animator anim;
    private SpriteRenderer sprite;
    private BoxCollider2D coll;

    private float dirX = 0f; // The f makes sure it is a float value
    [SerializeField] private float moveSpeed = 7f; // [SerializeField] allows you to edit it in unity
    [SerializeField] private float jumpForce = 8f;
    [SerializeField] private LayerMask jumpableGround;

    // Create your own data type for holding the animation state
    private enum MovementState {idle, running, jumping, falling}

    [SerializeField] private AudioSource jumpSoundEffect;

    // Start is called before the first frame update
    private void Start()
    {
        // Debug.Log("Hello, World!");
        rb = GetComponent<Rigidbody2D>();
        anim = GetComponent<Animator>();
        sprite = GetComponent<SpriteRenderer>();
        coll = GetComponent<BoxCollider2D>();
    }

    // Update is called once per frame
    private void Update()
    {
        // Grab the x/y coordinates and change velocity accordingly
        dirX = Input.GetAxis("Horizontal"); // Use GetAxisRaw if you don't want sliding characters
        rb.velocity = new Vector2(dirX * moveSpeed, rb.velocity.y);
        
        // If the jump button is pressed
        //Debug.Log(Physics2D.BoxCast(coll.bounds.center, coll.bounds.size, 0f, Vector2.down, .1f, jumpableGround));
        if (Input.GetButtonDown("Jump") && IsGrounded()) {  // GetKey for holding a button GetKeyDown for pressing
            jumpSoundEffect.Play();
            rb.velocity = new Vector2(rb.velocity.x, jumpForce); // x, y
        }

        UpdateAnimation();
    }
    private void UpdateAnimation() 
    {
        MovementState state;
        // Running animation
        // If you are moving left
        if (dirX < 0f) {
            state = MovementState.running;
            sprite.flipX = true;
        } 
        // If you are running right
        else if (dirX > 0f) {
            state = MovementState.running;
            sprite.flipX = false;
        }
        // Idle animation
        else state = MovementState.idle;
        // Jumping animation
        if (rb.velocity.y > .1f) {
            state = MovementState.jumping;
        }
        else if (rb.velocity.y < -.1f) {
            state = MovementState.falling;
        }
        anim.SetInteger("State", (int)state);
    }

    private bool IsGrounded() {
        return Physics2D.BoxCast(coll.bounds.center, coll.bounds.size, 0f, Vector2.down, .1f, jumpableGround);
    }
}
