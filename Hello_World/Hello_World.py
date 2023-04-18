# The colorama library can change the color printed to the terminal
import colorama

# Print "Hello World" in different colors to the output terminal. Then turn the color back to white.
print(colorama.Fore.BLUE + "Hello " + colorama.Fore.RED + "World" + colorama.Fore.WHITE)

