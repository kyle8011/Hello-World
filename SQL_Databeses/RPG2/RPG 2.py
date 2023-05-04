#Ideas: Left Click to attack, sword, bow, or magic
#Different spells, custom art with draw2d (Just save screen shot if you have to)
#Able to open inventory and add items to character
import pygame
import random
import math
import time
import sqlite3 as SQL
# from Player_Class import Player
#page = 1
Background = (255, 200, 255)
Red = (255, 0, 0)
Gray = (200, 200, 200)
Dark_gray = (150, 150, 150)
Blue = (0, 0, 200)
White = (255, 255, 255)
Yellow = (200, 200, 0)



def main():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(.15)

    pygame.time.set_timer(pygame.USEREVENT, 100)
    clock = pygame.time.Clock()
    counter = 0
    pygame.mixer.music.load("SQL_Database\Music\Dearly Beloved.mp3")
    pygame.mixer.music.play()
    songs = ["SQL_Database\Music\Mario.mp3", "SQL_Database\Music\Dearly Beloved.mp3"]
    
    hover_button = (250, 250, 0)
    neutral_button = (200, 200, 200)
    primary_button = (0, 0, 200)

    mouse_x = 0
    mouse_y = 0
    controller_connected = True
    # *** For two players include Controller functionality ***
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    if(len(joysticks) < 1):
        controller_connected = False
    for joystick in joysticks:
        print(joystick.get_init())
        print(joystick.get_numhats())

    # Figure out Joystick button control
    for joystick in joysticks:
        # The dpad is the "hat" use joystick.get_hat(0)
        # A = 0
        # B = 1
        # X = 2
        # Y = 3
        # LB = 4
        # RB = 5
        # Select = 6
        # Start = 7
        # L Stick = 8
        # R Stick = 9
        pass
        # Print if a button has been pressed??
    A = 0
    B = 1
    X = 2
    Y = 3
    #Game
    difficulty_i = 0
    new_game_i = 100
    load_game_i = 100
    game = ["Easy"]
    players = []
    projectiles = []
    enemies = []
    enemy_projectiles = []
    spawners = []
    walls = []
    fired_i = 0
    state = [False]
    item_types = ["sword", "bow", "wand", "shield", "quiver", "book", "helmet", "necklace", "chest", "pants", "boots"]
    all_items = []
    items_in_inventory = []
    items_equipped = []
    item_types_equipped = []

    selling_i = 0
    buying_i = 1
    shopping = [False, False]

    #Screen Management
    inventory_i = 0
    stats_i = 1
    paused_i = 2
    running_i = 3
    done_i = 4
    enter_i = 5
    game_state = [False, False, False, True, False, False]

    #buttons
    buttons = []
    locations = []
    menu_selection = ["New Game", "Load Game", "Quit"]
    class_selection = ["Warrior", "Mage", "Archer"]
    Warrior_initial = [150, 20, 2, 3, 2, 1] # Health, damage, attack speed, defense, ability, mana 
    Mage_initial =    [100, 20, 2, 1, 5, 3]
    Archer_initial =  [100, 25, 3, 1, 3, 2]
    archer_abilities = ["ATTACK SPEED"]
    mage_abilities = ["CHAIN LIGHTNING"]
    warrior_abilities = ["HEAL"]

    pointer_y = 220
    offset = 20

    paused = False
    screen_x = 1950
    screen_y = 800 # 1100 max
    window = pygame.display.set_mode((screen_x, screen_y), pygame.RESIZABLE)
    window.fill(Background) # Purple
    pygame.display.flip()

    def write_line(x, y, label, color, text_size = 32):
        font = pygame.font.SysFont("Arial", text_size)
        text_width, text_height = font.size(label)
        window.blit(font.render(label, True, color), (x-text_width/2, y-text_height/2))

    class Pointer:
        def __init__(self, points, color, speed):
            self.points = points
            self.color = color
            self.speed = speed
            self.draw()
        
        def draw(self):    
            pygame.draw.polygon(surface = window, color = self.color, points = self.points)

        def goto(self, x, y):
            self.color = Background
            self.draw()
            self.points = ([x, y-15], [x+20, y], [x, y+15])
            self.color = Red
            self.draw()

        def get_x(self):
            return self.points[0][0]

        def get_y(self):
            return self.points[1][1]

        def move_up(self):
            # Change the location based on what button is now selected
            for i in range(1, len(buttons)):
                if self.get_y() == locations[i][1] + offset:
                    self.goto(locations[i-1][0] - 50, locations[i-1][1] + offset)
                    return

        def move_down(self):
            # Change the location based on what button is now selected
            for i in range(len(buttons)-1):
                if self.get_y() == locations[i][1] + offset:
                    self.goto(locations[i+1][0] - 50, locations[i+1][1] + offset)
                    return

    pointer = Pointer(([800, pointer_y - 15], [820, pointer_y], [800, pointer_y + 15]), Red, 30)
    
    class Spawner:
        def __init__(self, x, y, enemy_type, level):
            self.image = pygame.image.load(f"SQL_Database\Images\Chest.gif")
            self.x = x
            self.y = y
            self.timer = 0
            self.image_w = self.image.get_width()
            self.level = level
            self.max_health = level * 100
            self.health = level * 100
            self.spawned = False
            self.type = enemy_type
            self.draw_health_bar()
            spawners.append(self)

        def draw(self):
            if (self.x < player.get_x() + screen_x/2 and self.x > player.get_x() - screen_x/2 and self.y < player.get_y() + screen_y/2 and self.y > player.get_y() - screen_y/2) or self.health < self.max_health:
                window.blit(self.image, (self.x+page.scrolled_x, self.y+page.scrolled_y))
                self.draw_health_bar()
                self.take_damage()

        def spawn_enemies(self):
            nearby_count = 0
            # Spawns an enemy every 5 seconds if 5 or less enemies are near the spawner
            if counter > self.timer + 50:
                self.timer = counter
                for enemy in enemies:
                    if self.get_distance(enemy.get_coordinates()) < 450:
                        nearby_count += 1
                if nearby_count <= 5:
                    make_enemy(self.x, self.y, self.type, self.level)

        def get_distance(self, coordinates):
            distance_x = (self.x) - coordinates[0]
            distance_y = (self.y) - coordinates[1]
            return math.sqrt(distance_x**2 + distance_y**2)

        def take_damage(self):
            for projectile in projectiles:
                if self.get_distance(projectile.get_coordinates()) < 80:
                    self.health -= player.damage
                    projectiles.remove(projectile)
                    if self.health < 1:
                        spawners.remove(self)
                        player.xp += 1*self.level

        def draw_health_bar(self):
            # Outline
            pygame.draw.rect(window, Red, pygame.Rect(self.x+page.scrolled_x, self.y+page.scrolled_y - 20, self.image_w, 20), 2)
            # Fill
            pygame.draw.rect(window, Red, pygame.Rect(self.x+page.scrolled_x, self.y+page.scrolled_y - 20, self.image_w*(self.health/self.max_health), 20))

    class Enemy:
        # skeleton, blob,  rat, bat, drawings in paint with 4 different aspects of each for direction changing
        def __init__(self, x, y, enemy_type, level):
            self.image = pygame.image.load(f'SQL_Database\Images\{enemy_type}_down.gif')
            self.x = x
            self.y = y
            self.timer = 0
            self.pace_counter = 0
            self.fired = False
            self.type = enemy_type
            attack = random.randint(0, 1)
            if attack == 0:
                self.attack_type = "melee"
            else:
                self.attack_type = "ranged"
            self.image_w = self.image.get_width()
            self.max_health = 100 * level
            self.health = 100 * level
            self.damage = 10 * level
            self.level = level
            self.draw_health_bar()
            enemies.append(self)

        def draw(self):
            if (self.x < player.get_x() + screen_x/2 and self.x > player.get_x() - screen_x/2 and self.y < player.get_y() + screen_y/2 and self.y > player.get_y() - screen_y/2) or self.health < self.max_health:
                window.blit(self.image, (self.x+page.scrolled_x, self.y+page.scrolled_y))
                self.draw_health_bar()
                self.take_damage()

        def draw_health_bar(self):
            # Outline
            pygame.draw.rect(window, Red, pygame.Rect(self.x+page.scrolled_x, self.y+page.scrolled_y - 20, self.image_w, 20), 2)
            # Fill
            pygame.draw.rect(window, Red, pygame.Rect(self.x+page.scrolled_x, self.y+page.scrolled_y - 20, self.image_w*(self.health/self.max_health), 20))
            write_line(self.x + 35 + page.scrolled_x, self.y + page.scrolled_y - 30, f"{self.type} - LV{self.level}", White, 20)

        def ranged_attack(self):
            # Get within range
            if (self.x < player.get_x() + screen_x/2 - 150 and self.x > player.get_x() - screen_x/2 + 150 and self.y < player.get_y() + screen_y/2-150 and self.y > player.get_y() - screen_y/2 + 150) or self.health < self.max_health:
                if player.get_x() > self.x - 200:
                    self.x += 2
                if player.get_x() < self.x + 200:
                    self.x -= 2
                if player.get_y() > self.y - 200:
                    self.y += 2
                if player.get_y() < self.y + 200:
                    self.y -= 2
                else:
                    self.pace()
            # Fire a projectile
            if self.get_distance(player.get_coordinates()) < 400:
                if counter > self.timer + 10:
                    self.timer = counter
                    projectile = Projectile(self.x, player.get_x() + 25, self.y, player.get_y() - 25, self.type, self.damage, "enemy")
                    enemy_projectiles.append(projectile)

        def get_coordinates(self):
            return (self.x, self.y)

        def pace(self):
            if counter > self.pace_counter + 5:
                self.pace_counter = counter
                direction = random.randint(1, 4)
                if direction == 1:
                    self.image = pygame.image.load(f'SQL_Database\Images\{self.type}_right.gif')
                    self.x += 3
                elif direction == 2:
                    self.image = pygame.image.load(f'SQL_Database\Images\{self.type}_left.gif')
                    self.x -= 3
                elif direction == 3:
                    self.image = pygame.image.load(f'SQL_Database\Images\{self.type}_down.gif')
                    self.y += 3
                elif direction == 4:
                    self.image = pygame.image.load(f'SQL_Database\Images\{self.type}_up.gif')
                    self.y -= 3

        def chase(self):
            if self.attack_type == "melee":
                if (self.x < player.get_x() + screen_x/2 - 150 and self.x > player.get_x() - screen_x/2 + 150 and self.y < player.get_y() + screen_y/2-150 and self.y > player.get_y() - screen_y/2 + 150) or self.health < self.max_health:
                    if player.get_x() > self.x:
                        self.image = pygame.image.load(f'SQL_Database\Images\{self.type}_right.gif')
                        self.x += 2
                    if player.get_x() < self.x:
                        self.image = pygame.image.load(f'SQL_Database\Images\{self.type}_left.gif')
                        self.x -= 2
                    if player.get_y() > self.y:
                        self.image = pygame.image.load(f'SQL_Database\Images\{self.type}_down.gif')
                        self.y += 2
                    if player.get_y() < self.y:
                        self.image = pygame.image.load(f'SQL_Database\Images\{self.type}_up.gif')
                        self.y -= 2
                    self.deal_damage()
                else:
                    self.pace()
            elif self.attack_type == "ranged":
                self.ranged_attack()
            
            self.draw()
            
        def get_distance(self, coordinates):
            distance_x = (self.x) - coordinates[0]
            distance_y = (self.y) - coordinates[1]
            return math.sqrt(distance_x**2 + distance_y**2)

        def take_damage(self):
            for projectile in projectiles:
                if self.get_distance(projectile.get_coordinates()) < 80:
                    self.health -= player.damage
                    projectiles.remove(projectile)
            if self.health < 1:
                enemies.remove(self)
                player.xp += self.level
                # Drop gold and items
                drop_amount = random.randint(10, 25)
                player.gold += drop_amount * self.level
                drop_item = random.randint(0, 1)
                if len(items_in_inventory) < 48 and drop_item == 1:
                    make_item(0, 0, False, self.level)

        def deal_damage(self):
            if self.get_distance(player.get_coordinates()) < 80:
                if counter > self.timer + 10:
                    self.timer = counter
                    if player.defense < self.damage:
                        player.health -= (self.damage - player.defense)
                    else:
                        player.health -= 1

        def goto(self, x, y):
            self.x = x + page.scrolled_x
            self.y = y + page.scrolled_y
            window.blit(self.image, (self.x, self.y))

    class Projectile:
        def __init__(self, initial_x, final_x, initial_y, final_y, type, damage, attacker):
            self.speed = 4
            self.damage = damage
            self.attacker = attacker
            self.type = type
            self.x = initial_x 
            self.y = initial_y 
            self.point_x = final_x 
            self.point_y = final_y 
            # Calculate theta between the player position and the position the mouse was clicked
            # tan^-1((y1-y2)/(x2-x1))
            # If the mouse x location is smaller than the player x location we have to use the other value of tangent
            if self.point_x - self.x != 0:
                if (self.x > self.point_x):
                    self.theta = math.atan((-self.point_y + self.y) / (self.point_x - self.x)) + math.pi
                else:
                    self.theta = math.atan((-self.point_y + self.y) / (self.point_x - self.x))
            else:
                if final_y < initial_y:
                    self.theta = math.pi / 2
                elif final_y > initial_y:
                    self.theta = 3 * math.pi / 2
            # Rotate the image
            degrees = self.theta * 180 / math.pi
            self.image = pygame.image.load(f'SQL_Database\Images\{type}_Projectile.gif')
            self.image = pygame.transform.rotate(self.image, degrees)
            # Solve the amount that the projectile should move in the x direction, out of 1 total space
            self.move_x = math.cos(self.theta)
            # Solve the amount that the projectile should move in the y direction, out of 1 total space
            # Flip the y value because the screen is inverted
            self.move_y = -math.sin(self.theta)
            
        def get_coordinates(self):
            return [self.x, self.y]
        
        def move_forward(self):
            self.x += self.move_x * self.speed
            self.y += self.move_y * self.speed
            window.blit(self.image, (self.x + page.scrolled_x, self.y + page.scrolled_y))
            if self.x > player.get_x() + screen_x/2 or self.x < player.get_x() - screen_x/2 or self.y > player.get_y() + screen_y/2 or self.y < player.get_y() - screen_y/2:
                if self.attacker == "player":
                    projectiles.remove(self)
                elif self.attacker == "enemy":
                    enemy_projectiles.remove(self)
    
    class Wall:
        def __init__(self, x, y, w, h, color):
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.color = color
            walls.append(self)

        def draw(self):
            pygame.draw.rect(window, Background, pygame.Rect(self.x + page.scrolled_x, self.y + page.scrolled_y, self.w, self.h))

    class Player:
        def __init__(self):
            self.type = "Class"
            self.name = "none"
            self.max_health = 100
            self.health = 80
            self.damage = 15
            self.bonus_damage1 = 1
            self.bonus_damage2 = 1
            self.attack_speed = 1
            self.boost_timer = 0
            self.attack_speed_boost = False
            self.attack_speed_boost_amount = 2
            self.defense = 1
            self.ability = 1
            self.max_mana = 3
            self.mana = 2
            self.xp = 1
            self.max_xp = 10
            self.level = 1
            self.gold = 100
            self.timer = 0
            self.image = "SQL_Database\Images\pic_name.gif"
            self.projectile = "Arrow"
            self.left = False
            self.right = False
            self.x = 0
            self.y = 0
        
        def level_up(self):
            self.level += 1
            self.xp -= self.max_xp
            self.max_xp += 10
            if player.type == "Warrior":
                self.max_health += 25
            else:
                self.max_health += 15
            self.health = self.max_health
            self.max_mana += 1
            self.mana = self.max_mana
            if player.type == "Archer":
                self.damage += 10
            else:
                self.damage += 5
            if self.attack_speed < 5:
                self.attack_speed += .25
            if player.type == "Mage":
                self.ability += 2
            else:
                self.ability += 1
            self.defense += 1

        def e_ability(self):
            # If there is enough mana
            if self.mana > 0:
                self.mana -= 1
                # Do something helpful
                if self.type == "Archer":
                    # Increase Attack Speed
                    self.attack_speed_boost = True
                elif self.type == "Warrior":
                    # Heal
                    self.health += 10*self.ability
                elif self.type == "Mage":
                    # Chain Lightning
                    for enemy in enemies:
                        # If the enemy is on the screen or has been previously damaged
                        if (enemy.x < self.get_x() + screen_x/2 and enemy.x > self.get_x() - screen_x/2 and enemy.y < self.get_y() + screen_y/2 and enemy.y > self.get_y() - screen_y/2) or enemy.health < enemy.max_health:
                            enemy.health -= 10*self.ability

        def draw(self):
            window.blit(self.image, (self.x-32, self.y-32))
            self.draw_hud()
            self.status()

        def status(self):
            if self.xp >= self.max_xp:
                self.level_up()
            # For archer attack speed boost
            if self.attack_speed_boost == True:
                self.attack_speed_boost_amount = 3
                self.boost_timer = counter
                self.attack_speed_boost = False
            elif counter > self.boost_timer + 10*self.ability:
                self.attack_speed_boost_amount = 0

            for item in items_equipped:
                if item.slot == "right_hand":
                    if (self.type == "Warrior" and item.type == "sword") or (self.type == "Mage" and item.type == "wand") or (self.type == "Archer" and item.type == "bow"):
                        self.bonus_damage1 = player.level
                    else:
                        self.bonus_damage1 = 0
                if item.slot == "left_hand":
                    if (self.type == "Warrior" and item.type == "shield") or (self.type == "Mage" and item.type == "book") or (self.type == "Archer" and item.type == "quiver"):
                        self.bonus_damage2 = player.level
                    else:
                        self.bonus_damage2 = 0
            if len(items_equipped) < 1:
                self.bonus_damage1 = 0
                self.bonus_damage2 = 0

        def goto(self, x, y):  
            self.x = x
            self.y = y
            self.draw()
        
        def draw_hud(self):
            # Health Bar
            pygame.draw.rect(window, Gray, pygame.Rect(screen_x-300, 15, 200, 25), 3)
            pygame.draw.rect(window, Dark_gray, pygame.Rect(screen_x-297, 18, 194, 19))
            pygame.draw.rect(window, Red, pygame.Rect(screen_x-297, 18, 200*self.health/self.max_health - 6, 19))
            write_line(1600, 28, f"{self.health:.0f} / {self.max_health:.0f}", White, 18)
            # Mana Bar
            pygame.draw.rect(window, Gray, pygame.Rect(screen_x-300, 45, 200, 25), 3)
            pygame.draw.rect(window, Dark_gray, pygame.Rect(screen_x-297, 48, 194, 19))
            pygame.draw.rect(window, Blue, pygame.Rect(screen_x-297, 48, 200*self.mana/self.max_mana - 6, 19))
            write_line(1600, 58, f"{self.mana:.0f} / {self.max_mana:.0f}", White, 18)
            # XP Bar
            pygame.draw.rect(window, Gray, pygame.Rect(screen_x-300, 75, 200, 25), 3)
            pygame.draw.rect(window, Dark_gray, pygame.Rect(screen_x-297, 78, 194, 19))
            pygame.draw.rect(window, Yellow, pygame.Rect(screen_x-297, 78, 200*self.xp/self.max_xp - 6, 19))
            write_line(1600, 88, f"{self.xp:.0f} / {self.max_xp:.0f}", White, 18)
            # level, gold
            write_line(1400, 45, f"level: {self.level}", White, 20)
            write_line(1400, 15, f"Gold: {self.gold}", White, 20)
            # Abilities
            # Draw a button that describes the ability when the mouse hovers over it
            # if page.draw_button(screen_x/2 - 100, 200, 200, 50, (200, 0, 0), "New Game", game_state, primary_button):
            #     pass
            if self.type == "Archer":
                write_line(100, screen_y - 15, f"E: {archer_abilities[0]}", White, 20)
            if self.type == "Mage":
                write_line(100, screen_y - 15, f"E: {mage_abilities[0]}", White, 20)
            if self.type == "Warrior":
                write_line(100, screen_y - 15, f"E: {warrior_abilities[0]}", White, 20)

        def clear(self, x, y):
            pygame.draw.rect(window, Background, pygame.Rect(x-52, y-52, 150, 200))

        def get_distance(self, coordinates):
            distance_x = (self.get_x()) - coordinates[0]
            distance_y = (self.get_y()) - coordinates[1]
            return math.sqrt(distance_x**2 + distance_y**2)

        def take_damage(self):
            for projectile in enemy_projectiles:
                if self.get_distance(projectile.get_coordinates()) < 80:
                    if self.defense < projectile.damage:
                        self.health -= (projectile.damage - self.defense)
                    else:
                        self.health -= 1
                    enemy_projectiles.remove(projectile)
            # What happens when the player dies
            # if self.health < 1:
            #     enemies.remove(self)
            #     player.xp += 1

        def attack(self):
            for item in items_equipped:
                if item.slot == "right_hand":
                    if controller_connected:
                        if (joysticks[0].get_button(A) == 1):
                            projectile = Projectile(self.get_x(), mouse_x - page.scrolled_x, self.get_y(), mouse_y - page.scrolled_y, item.type, self.damage+self.bonus_damage1+self.bonus_damage2, "player")
                            projectiles.append(projectile)
                            state[fired_i] = True
                            self.timer = counter
                    if (pygame.mouse.get_pressed() == (1, 0, 0)) and counter > self.timer + (10-self.attack_speed-self.attack_speed_boost_amount):
                        projectile = Projectile(self.get_x(), mouse_x - page.scrolled_x, self.get_y(), mouse_y - page.scrolled_y, item.type, self.damage+self.bonus_damage1+self.bonus_damage2, "player")
                        projectiles.append(projectile)
                        state[fired_i] = True
                        self.timer = counter
                    for projectile in projectiles:
                        projectile.move_forward()
            self.take_damage()

        def equip(self, item):
            if item.slot not in item_types_equipped:
                item.stats_values[8] = True
                items_in_inventory.remove(item)
                items_equipped.append(item)
                item_types_equipped.append(item.slot)
                player.damage += item.damage
                player.defense += item.defense
                player.max_health += item.health
                player.max_mana += item.mana
                player.ability += item.ability
                player.attack_speed += item.speed
            
                if item.type == "helmet":
                    item.goto(1050, 150)
                if item.type == "necklace":
                    item.goto(1175, 200)
                if item.type == "chest":
                    item.goto(1050, 275)
                if item.type == "sword" or item.type == "wand" or item.type == "bow":
                    item.goto(925, 350)
                if item.type == "book" or item.type == "quiver" or item.type == "shield":
                    item.goto(1175, 350)
                if item.type == "pants":
                    item.goto(1050, 400)
                if item.type == "boots":
                    item.goto(1050, 525)

                self.status()
                
        def unequip(self, item):
            item.stats_values[8] = False
            items_in_inventory.append(item)
            items_equipped.remove(item)
            item_types_equipped.remove(item.slot)
            player.damage -= item.damage
            player.defense -= item.defense
            player.max_health -= item.health
            player.max_mana -= item.mana
            player.ability -= item.ability
            player.attack_speed -= item.speed
            
            distribute_items()
            self.status()

        def get_coordinates(self):
            return [self.get_x(), self.get_y()]

        def get_x(self):
            return -page.scrolled_x + self.x

        def get_y(self):
            return -page.scrolled_y + self.y

        def move_up(self, tilt_amount = 1):
            if self.left == False and self.right == False:
                self.image = pygame.image.load(f'SQL_Database\Images\{self.type}_Up.gif')
            # Allow centering for the player
            if player.y > screen_y/2:
                player.goto(player.x, player.y - 5 * tilt_amount)
            # Only scoot the screen so far up  this works ***
            elif page.scrolled_y < page.max_y:
                page.scrolled_y += 5 * tilt_amount
            # Don't let the player leave the screen
            elif player.get_y() >= page.min_y:
                player.goto(player.x, player.y -  5 * tilt_amount)

        def move_down(self, tilt_amount = 1):
            if self.left == False and self.right == False:
                self.image = pygame.image.load(f'SQL_Database\Images\{self.type}_Down.gif')
            # If the player is not centered, allow centering
            if player.y < screen_y/2:
                player.goto(player.x, player.y + 5 * tilt_amount)
            # Only scoot the screen so far down
            elif page.scrolled_y > page.min_y + screen_x/2 + 75:
                page.scrolled_y -= 5 * tilt_amount
            # Don't allow the player to leave the screen
            elif player.get_y() <= page.max_y - 75:
                player.goto(player.x, player.y + 5 * tilt_amount)

        def move_left(self, tilt_amount = 1):
            self.image = pygame.image.load(f'SQL_Database\Images\{self.type}_Left.gif')            
            # Allow centering for the player
            if player.x > screen_x/2:
                player.goto(player.x - 5 * tilt_amount, player.y)
            # Only scoot the screen so far to the left
            elif page.scrolled_x < page.max_x:
                page.scrolled_x += 5 * tilt_amount
            # Don't let the player leave the screen
            elif player.get_x() >= page.min_x:
                player.goto(player.x - 5 * tilt_amount, player.y)  
            self.left = True

        def move_right(self, tilt_amount = 1):
            self.image = pygame.image.load(f'SQL_Database\Images\{self.type}_Right.gif')
            # If the player is not centered, allow centering
            if player.x < screen_x/2:
                player.goto(player.x + 5 * tilt_amount, player.y)
            # Only scoot the screen so far to the right
            elif page.scrolled_x > page.min_x + screen_x:
                page.scrolled_x -= 5 * tilt_amount
            # Don't allow the player to leave the screen
            elif player.get_x() <= page.max_x - 100:
                player.goto(player.x + 5 * tilt_amount, player.y)
            self.right = True
    
    player = Player()
    
    class Item:
        def __init__(self, x, y, type = "none", damage = 0, defense = 0, health = 0, mana = 0, ability = 0, speed = 0, level = player.level, equipped = False):
            self.x = x
            self.y = y
            self.equipped = equipped
            self.slot = type
            self.stats_list = ["type", "damage", "defense", "health", "mana", "ability", "speed", "level"]
            self.level = level
            # Item type
            self.type = type
            if type == "none":
                self.type = random.choice(item_types)
            self.stats_values = [self.type, damage, defense, health, mana, ability, speed, level, equipped]
            # Which slot it uses up
            if self.type == "sword" or self.type == "wand" or self.type == "bow":
                self.slot = "right_hand"
            if self.type == "shield" or self.type == "quiver" or self.type == "book":
                self.slot = "left_hand"
            if self.type == "helmet":
                self.slot = "head"
            if self.type == "necklace":
                self.slot = "neck"
            if self.type == "boots":
                self.slot = "feet"
            if self.type == "pants":
                self.slot = "legs"
            if self.type == "chest":
                self.slot = "chest"
            # Item Image
            #self.image = pygame.image.load("SQL_Database\Images\Sword Drop.gif")
            self.image = pygame.image.load(f'SQL_Database\Images\{self.type}_item.gif')
            # Item Damage
            self.damage = damage
            self.stats_values[1] = damage
            if damage == 0:
                if self.type == "sword" or self.type == "wand" or self.type == "bow" or self.type == "quiver" or self.type == "book":
                    damage_multiplier = random.randint(1, 5)
                    self.damage = damage_multiplier*self.level
                    self.stats_values[1] = self.damage
                
            # Item Defense
            self.defense = defense
            self.stats_values[2] = defense
            if defense == 0:
                if self.type != "wand" and self.type != "bow" and self.type != "quiver" and self.type != "book":
                    defense_multiplier = random.randint(1, 3)
                    self.defense = defense_multiplier*self.level
                    self.stats_values[2] = self.defense
            # Item Health
            self.health = health
            self.stats_values[3] = health
            if health == 0:
                if self.type != "sword" and self.type != "wand" and self.type != "bow" and self.type != "quiver" and self.type != "book":
                    health_multiplier = random.randint(5, 10)
                    self.health = health_multiplier*self.level
                    self.stats_values[3] = self.health
            # Item Mana
            self.mana = mana
            self.stats_values[4]
            if mana == 0:
                if self.type == "necklace" or self.type == "book" or self.type == "wand":
                    mana_multiplier = random.randint(1, 3)
                    self.mana = mana_multiplier*self.level
                    self.stats_values[4] = self.mana
            # Item Ability
            self.ability = ability
            self.stats_values[5] = ability
            if ability == 0:
                if self.type == "necklace" or self.type == "book" or self.type == "wand":
                    ability_multiplier = random.randint(1, 3)
                    self.ability = ability_multiplier*self.level
                    self.stats_values[5] = self.ability
            # Item Speed
            self.speed = speed
            self.stats_values[6] = speed
            if speed == 0:
                if self.type == "quiver" or self.type == "bow":
                    self.speed = random.randint(1, 2)
                    self.stats_values[6] = self.speed
            
            self.draw()
            all_items.append(self)
            items_in_inventory.append(self)

        def draw(self):
            window.blit(self.image, (self.x, self.y))

        def goto(self, x, y):
            self.x = x
            self.y = y
            self.draw()

        def show_stats(self):
            # Head
            #pygame.draw.rect(window, (200, 100, 0), pygame.Rect(1050, 150, 100, 100), 5)
            pygame.draw.rect(window, (200, 100, 0), pygame.Rect(910, 125, 130, 150))
            write_line(975, 135, f"{self.type} - level {self.level}", (100, 50, 0), 20)
            for x in range(1, len(self.stats_list)):
                if self.stats_values[x] > 0:
                    write_line(975, 160 + 20*x, f"{self.stats_list[x]}: {self.stats_values[x]}", (100, 50, 0), 20)
            # This draws it on the mouse, would be useful if the items drop on the ground
            # write_line(mouse_x, mouse_y - 40, f"{self.type} - level {self.level}", Red, 20)
            # for x in range(len(self.stats_list)):
            #     write_line(mouse_x, mouse_y - 15 + 20*x, f"{self.stats_list[x]}: {self.stats_values[x]}", Red, 20)
            
            
    class Page:
        # Draw the background using draw 2D, figure out how to redraw the characters without messing up the background
        def __init__(self):
            self.number = 1
            self.done = False
            self.max_x = 1000
            self.min_x = -1000
            self.max_y = 1000
            self.min_y = -1000
            self.scrolled_x = 0
            self.scrolled_y = 0
            

        def initialize(self, title = "None"):
            if self.done == False:                
                buttons.clear()
                locations.clear()
                projectiles.clear()
                walls.clear()
                enemies.clear()
                enemy_projectiles.clear()
                spawners.clear()
                window.fill(Background)
                
                # Choosing a random background
                back = random.randint(0, 2)
                if back == 0:
                    background_image = "Mario"
                elif back == 1:
                    background_image = "Plains"
                else:
                    background_image = "Mountains"
                self.background = pygame.transform.scale(pygame.image.load(f'SQL_Database\Images\{background_image}.gif'), (4000, 2000))
                
                if title != "None":
                    write_line(screen_x/2, 100, title, Red, 50)
                for x in [1, 2, 5]:
                    if page.number == x:
                        pointer.draw()
                for x in [6, 7]:
                    if self.number == x:
                        self.scrolled_x = screen_x/2
                        self.scrolled_y = screen_y/2
                        player.goto(self.scrolled_x, self.scrolled_y)
                pygame.display.flip()
        
        def show_stats(self, stats):
            pygame.draw.rect(window, Background, pygame.Rect(200, 250, 500, 200))
            write_line(250, 300, f"Health: {stats[0]}", Red)
            write_line(400, 300, f"Damage: {stats[1]}", Red)
            write_line(550, 300, f"Speed: {stats[2]}", Red)
            write_line(250, 400, f"Defense: {stats[3]}", Red)
            write_line(400, 400, f"Mana: {stats[4]}", Red)
            write_line(550, 400, f"Ability: {stats[5]}", Red)

        def draw_button(self, x, y, w, h, text_color, label, game_state, button_color = neutral_button, button_color1 = hover_button):
            # Change coordinates relative to the scrolled location
            x = x + self.scrolled_x
            y = y + self.scrolled_y
            # If the mouse is hovering over the button
            if mouse_y < y+h and mouse_y > y and mouse_x < x+w and mouse_x > x or (pointer.get_y() == y + offset and game_state[enter_i] == True):
                # Move the pointer
                pointer.goto(x-50, y + offset)
                # Draw the button yellow
                pygame.draw.rect(window, button_color1, pygame.Rect(x, y, w, h))
                # Return true if it is clicked on or enter is pressed
                if pygame.mouse.get_pressed() == (1, 0, 0) or game_state[enter_i] == True:
                    game_state[enter_i] = False
                    return True
            # Draw the normal button color
            else:
                pygame.draw.rect(window, button_color, pygame.Rect(x, y, w, h))
            # Draw the text centered on the button
            write_line(x+w/2, y+h/2, label, text_color)
            if self.done == False:
                buttons.append(len(buttons))
                locations.append((x, y))

        def show_selected(self, x, y, image_selection):
            # Display image of character
            for i in range(len(buttons) - 1):
                    if pointer.get_y() == locations[i][1] + offset:
                        player.image = pygame.image.load(f'SQL_Database\Images\{image_selection[i]}_Down.gif')
                        if image_selection[i] == "Warrior":
                            self.show_stats(Warrior_initial)
                        elif image_selection[i] == "Archer":
                            self.show_stats(Archer_initial)
                        elif image_selection[i] == "Mage":
                            self.show_stats(Mage_initial)
                        player.clear(x, y)
                        player.goto(x, y)

        def play_song(self, song):
            if pygame.mixer.music.get_busy() == False:
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()
        
        def play_new_song(self, song):
            if self.done == False:
                pygame.mixer.music.set_volume(.25)
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()

    page = Page()


    # Paused Menu options
    def display_stats():
        #pygame.draw.rect(window, Background, pygame.Rect(175, 250, 1500, 200))
        write_line(250, 300, f"Health: {player.max_health}", Red)
        write_line(400, 300, f"Damage: {player.damage+player.bonus_damage1+player.bonus_damage2}", Red)
        write_line(550, 300, f"Speed: {player.attack_speed}", Red)
        write_line(250, 400, f"Defense: {player.defense}", Red)
        write_line(400, 400, f"Mana: {player.max_mana}", Red)
        write_line(550, 400, f"Ability: {player.ability}", Red)
        if player.type == "Archer":
            write_line(1000, 300, f"E Ability: Increases attack speed for ({player.ability}) seconds.", Red)
        if player.type == "Warrior":
            write_line(1000, 300, f"E Ability: Heals the character ({player.ability*10}) health (can overheal).", Red)
        if player.type == "Mage":
            write_line(1000, 300, f"E Ability: Deals ({player.ability*10}) damage to each enemy on the screen.", Red)
    
    def display_inventory():
        # Backdrop for items
        pygame.draw.rect(window, (100, 50, 0), pygame.Rect(100, 100, screen_x - 750, screen_y - 200))
        # Slots
        for x in range(8):
            for y in range(round((screen_y-200)/100)):
                pygame.draw.rect(window, (200, 100, 0), pygame.Rect(100 + x*100, 100 + y*100, 100, 100), 3)
                
        # Items equipped
        # Helmet
        pygame.draw.rect(window, (200, 100, 0), pygame.Rect(1050, 150, 100, 100), 5)
        # Necklace
        pygame.draw.rect(window, (200, 100, 0), pygame.Rect(1175, 200, 100, 100), 5)
        # Chest
        pygame.draw.rect(window, (200, 100, 0), pygame.Rect(1050, 275, 100, 100), 5)
        # Right hand
        pygame.draw.rect(window, (200, 100, 0), pygame.Rect(925, 350, 100, 100), 5)
        # Left hand
        pygame.draw.rect(window, (200, 100, 0), pygame.Rect(1175, 350, 100, 100), 5)
        # Pants
        pygame.draw.rect(window, (200, 100, 0), pygame.Rect(1050, 400, 100, 100), 5)
        # Boots
        pygame.draw.rect(window, (200, 100, 0), pygame.Rect(1050, 525, 100, 100), 5)
        for item in items_in_inventory:
            item.draw()
        for item in items_equipped:
            item.draw()
        
    def distribute_items():
        for x in range(len(items_in_inventory)):
            items_in_inventory[x].goto(100+(x%8)*100, 100+math.floor(x/8)*100)
                
    def display_paused():
        # Inventory
        if page.draw_button(1475 - page.scrolled_x, 300 - page.scrolled_y, 200, 50, (200, 0, 0), "Inventory", game_state, primary_button):
            window.fill(Background)
            game_state[stats_i] = False
            game_state[inventory_i] = True
            distribute_items()
        # Stats
        if page.draw_button(1475 - page.scrolled_x, 400 - page.scrolled_y, 200, 50, (200, 0, 0), "Stats", game_state, primary_button):
            window.fill(Background)
            game_state[stats_i] = True
            game_state[inventory_i] = False
            player.status()
            display_stats()
        # Main Menu
        if page.draw_button(1475 - page.scrolled_x, 600 - page.scrolled_y, 200, 50, (200, 0, 0), "Main Menu", game_state, primary_button):
            page.scrolled_x = 0
            page.scrolled_y = 0
            game_state[paused_i] = False
            time.sleep(.25)
            page.number = 1
            page.done = False
            window.fill(Background)
            return
        
        if game_state[inventory_i] == True:
            display_inventory()
            
            for item in all_items:
                x = item.x
                y = item.y
                # If the mouse is hovering over the item
                if mouse_y < y+100 and mouse_y > y and mouse_x < x+100 and mouse_x > x:
                    item.show_stats()
                    # Equip an item if clicked on
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        if item in items_in_inventory:
                            player.equip(item)
                        elif item in items_equipped:
                            player.unequip(item)
        
        # Save Game save_game
        if page.draw_button(1475 - page.scrolled_x, 500 - page.scrolled_y, 200, 50, (200, 0, 0), "Save Game", game_state, primary_button):
            game_state[stats_i] = False
            # Create a list of items to pass to update_items
            items_list = []
            for item in all_items:
                items_list.append(item.stats_values)       
            # Deletes items previously in data and replaces them with current items     
            update_items(player.name, items_list)
            save_stats = [player.level, player.xp, player.max_health, player.damage, player.attack_speed, player.defense, player.ability, player.max_mana, player.gold]
            # Save the stats of the 'player', not the items
            for x in range(len(items_equipped)-1, -1, -1):
                player.unequip(items_equipped[x])
            save_stats = [player.level, player.xp, player.max_health, player.damage, player.attack_speed, player.defense, player.ability, player.max_mana, player.gold]
            # Upolad current player stats into memory
            edit_character_data(player.name, save_stats)
            # Equip all items back to player
            load_character(player.name)
        
    
    def load_character(character_name):
        character = get_character_data(character_name)
        # Upload character stats to current player
        player.name = character[0]
        player.image = pygame.image.load(f'SQL_Database\Images\{character[1]}_Down.gif')
        player.type = character[1]
        player.level = character[2]
        player.xp = character[3]
        player.max_xp = player.level * 10
        player.max_health = character[4]
        player.health = player.max_health
        player.damage = character[5]
        player.attack_speed = float(character[6])
        player.defense = character[7]
        player.ability = character[8]
        player.max_mana = character[9]
        player.mana = player.max_mana
        player.gold = character[10]
        
        # Load items into inventory
        # First delete all items
        item_types_equipped.clear()
        all_items.clear()
        items_in_inventory.clear()
        items_equipped.clear()
        # Create all of the equipment stored in memory
        equipment = get_item_data(character_name)
        if equipment != "none":
            for item in equipment:
                new_item = Item(0, 0, item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9])
                # Equip items that were marked as equipped when the game was saved
                if item[9] == True:
                    player.equip(new_item)

        game_state[paused_i] = False

    def display_shop():
        #pygame.draw.rect(window, Background, pygame.Rect(275, 100, 1000, 600))
        #display_inventory()
        if page.draw_button(1475 - page.scrolled_x, 300 - page.scrolled_y, 200, 50, (200, 0, 0), "Sell Items", game_state, primary_button):
            shopping[selling_i] = True
        if shopping[selling_i] == True: 
            display_inventory()

        if page.draw_button(1475 - page.scrolled_x, 200 - page.scrolled_y, 200, 50, (200, 0, 0), "Buy Items", game_state, primary_button):
            shopping[buying_i] = True
        if shopping[buying_i] == True:
            #display_shop()
            pass

    # Functions for making objects and drawing the grid
    def drawGrid():
        blockSize = 20 #Set the size of the grid block
        for x in range(0, screen_x, blockSize):
            for y in range(0, screen_y, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(window, Gray, rect, 1)
    def make_enemy(x, y, enemy_type, level):
        enemy = Enemy(x, y, enemy_type, level)
    def make_spawner(x, y, enemy_type, level):
        spawner = Spawner(x, y, enemy_type, level)
    def make_wall(x, y, w, h, color):
        wall = Wall(x, y, w, h, color)
    def make_item(x, y, need_item = False, level = player.level):
        item = Item(x, y, level = level)
        if need_item == True:
            return item

    def up(tilt_amount = 1):
        for x in [1, 2, 5]:
            if page.number == x:
                pointer.move_up()
        for x in [6, 7]:
            if page.number == x:
                player.move_up(tilt_amount)
                for wall in walls:
                    # If the player is standing below the wall
                    if wall.y + wall.h < player.get_y() and (wall.x) < player.get_x() + 25 and (wall.x+wall.w) > player.get_x() - 15:
                        # If the player is 25 pixels below the wall, don't move anymore
                        if wall.y + wall.h + 25 > player.get_y():
                            player.move_down()

    def down(tilt_amount = 1):
        for x in [1, 2, 5]:
            if page.number == x:
                pointer.move_down()
        for x in [6, 7]:
            if page.number == x:
                player.move_down(tilt_amount)
                for wall in walls:
                    # If the player is standing below the wall
                    if wall.y > player.get_y() and (wall.x) < player.get_x() + 25 and (wall.x+wall.w) > player.get_x() - 15:
                        # If the player is 25 pixels below the wall, don't move anymore
                        if wall.y < player.get_y() + 55:
                            player.move_up()

    def left(tilt_amount = 1):
        for x in [6, 7]:
            if page.number == x:
                player.move_left(tilt_amount)
                for wall in walls:
                    # If the player is standing below the wall
                    if wall.x < player.get_x() and (wall.y) < player.get_y() + 50 and (wall.y+wall.h) > player.get_y() - 25:
                        # If the player is 25 pixels below the wall, don't move anymore
                        if wall.x > player.get_x() - (wall.w + 15):
                            player.move_right()

    def right(tilt_amount = 1):
        for x in [6, 7]:
            if page.number == x:
                player.move_right(tilt_amount)
                for wall in walls:
                    # If the player is standing below the wall
                    if wall.x + wall.w > player.get_x() and (wall.y) < player.get_y() + 50 and (wall.y + wall.h) > player.get_y() - 25:
                        # If the player is 25 pixels below the wall, don't move anymore
                        if wall.x < player.get_x() + 25:
                            player.move_left()
    
    def enter():
        game_state[enter_i] = True

    


    def main_menu():                                   # Page 1
        # Initialize the page
        page.initialize("Main Menu")
        page.play_song("SQL_Database\Music\Dearly Beloved.mp3")

        # New Game button
        if page.draw_button(screen_x/2 - 100, 200, 200, 50, (200, 0, 0), "New Game", game_state, primary_button):
            time.sleep(.25)
            page.number = 2
            page.done = False
            return
        
        # Load Game button
        if page.draw_button(screen_x/2 - 100, 300, 200, 50, (200, 0, 0), "Load Game", game_state, primary_button):
            time.sleep(.25)
            page.number = 3
            page.done = False
            return
        
        # Options button
        if page.draw_button(screen_x/2 - 100, 400, 200, 50, (200, 0, 0), "Options", game_state):
            time.sleep(.25)
            page.number = 4
            page.done = False
            return
        
        # Quit button
        if page.draw_button(screen_x/2 - 100, 500, 200, 50, (200, 0, 0), "Quit", game_state):
            game_state[running_i] = False
        
        page.done = True

    def new_game():                                     # Page 2
        # Initialize the page
        page.initialize("New Game")
        page.play_song("SQL_Database\Music\Dearly Beloved.mp3")

        # Easy button
        if page.draw_button(screen_x/2 - 100, 200, 200, 50, (200, 0, 0), "Easy", game_state):
            game[difficulty_i] = "Easy"
            time.sleep(.5)
            page.number = 5
            page.done = False
            return
        # Medium button
        if page.draw_button(screen_x/2 - 100, 300, 200, 50, (200, 0, 0), "Medium", game_state):
            game[difficulty_i] = "Medium"
            time.sleep(.25)
            page.number = 5
            page.done = False
            return
        # Hard button
        if page.draw_button(screen_x/2 - 100, 400, 200, 50, (200, 0, 0), "Hard", game_state):
            game[difficulty_i] = "Hard"
            time.sleep(.25)
            page.number = 5
            page.done = False
            return
        # Back button
        if page.draw_button(screen_x/2 - 100, 500, 200, 50, (200, 0, 0), "Back", game_state):
            time.sleep(.25)
            page.number = 1
            page.done = False
            return
        page.done = True

    def load_game():                                   # Page 3
        # Initialize the page
        page.initialize("Load Game")
        page.play_song("SQL_Database\Music\Dearly Beloved.mp3")
        #if page.done == False:
        characters = get_table("characters")

        for x in range(len(characters)):
            
            if page.draw_button(screen_x/2 - 150, 200 + 75*x, 200, 50, (200, 0, 0), characters[x][0], game_state, primary_button):
                character_name = characters[x][0]
                load_character(character_name)
                time.sleep(.25)
                page.number = 6
                window.fill(Background)
                page.done = False
                return

            if page.draw_button(screen_x/2 + 150, 200 + 75*x, 200, 50, (200, 0, 0), "delete", game_state, Red):
                print("before:")
                table = get_table("characters")
                for y in table:
                    print(y)
                delete_character(characters[x][0])
                print("after:")
                table = get_table("characters")
                for y in table:
                    print(y)
                time.sleep(.25)
                page.done = False
                window.fill(Background)
                return

        # Back button
        if page.draw_button(screen_x/2 - 100, 700, 200, 50, (200, 0, 0), "Back", game_state):
            time.sleep(.25)
            page.number = 1
            page.done = False
            return
        page.done = True

    def character_select():                           # Page 5
        # Initialize the page
        page.initialize("Class Selection")
        page.show_selected(screen_x-300, 300, class_selection)
        page.play_song("SQL_Database\Music\Dearly Beloved.mp3")

        # Warrior button
        if page.draw_button(screen_x/2 - 100, 200, 200, 50, (200, 0, 0), "Warrior", game_state):

            character_name = input("Type the name of your character: ")
            valid_name = add_new_character_data(character_name, "Warrior")
            time.sleep(.25)
            if valid_name == False:
                page.number = 6
                load_character(character_name)
                item = Item(0, 0, "sword", 1, 0, 0, 0, 0, 0, 1)
                player.equip(item)
            else:
                page.number = 5
                page.done = False
                page.initialize("Class Selection")
                page.show_selected(screen_x-300, 300, class_selection)
                page.play_song("SQL_Database\Music\Dearly Beloved.mp3")
            page.done = False
            return
        # Mage button
        if page.draw_button(screen_x/2 - 100, 300, 200, 50, (200, 0, 0), "Mage", game_state):
            
            character_name = input("Type the name of your character: ")
            valid_name = add_new_character_data(character_name, "Mage")
            time.sleep(.25)
            if valid_name == False:
                page.number = 6
                load_character(character_name)
                item = Item(0, 0, "wand", 2, 0, 0, 0, 0, 0, 1)
                player.equip(item)
            else:
                page.number = 5
                page.done = False
                page.initialize("Class Selection")
                page.show_selected(screen_x-300, 300, class_selection)
                page.play_song("SQL_Database\Music\Dearly Beloved.mp3")
            page.done = False
            return
        # Archer button
        if page.draw_button(screen_x/2 - 100, 400, 200, 50, (200, 0, 0), "Archer", game_state):

            character_name = input("Type the name of your character: ")
            print("before:")
            table = get_table("characters")
            for x in table:
                print(x)
            valid_name = add_new_character_data(character_name, "Archer")
            print("after:")
            table = get_table("characters")
            for x in table:
                print(x)
            time.sleep(.25)
            if valid_name == False:
                page.number = 6
                load_character(character_name)
                item = Item(0, 0, "bow", 1, 0, 0, 0, 0, 0, 1)
                player.equip(item)
            else:
                page.number = 5
                page.done = False
                page.initialize("Class Selection")
                page.show_selected(screen_x-300, 300, class_selection)
                page.play_song("SQL_Database\Music\Dearly Beloved.mp3")
            page.done = False
            return
        # Back button
        if page.draw_button(screen_x/2 - 100, 500, 200, 50, (200, 0, 0), "Back", game_state):
            time.sleep(.25)
            page.number = 2
            page.done = False
            return
        page.done = True
    


    def level_select():                                     # Page 6
        # Initialize the page
        # Set up a "gauntlet style" level entry, figure out how to scroll the screen when the player moves
        # Make holding down a button continuously move the player
        page.initialize()
        page.play_song("SQL_Database\Music\Dearly Beloved.mp3")
        page.max_y = screen_y
        page.min_y = -screen_y
        page.max_x = screen_x
        page.min_x = -screen_x
        
        # Testing out new functions
        if page.done == False:

            # Draw the opening area
            make_wall(200, -300, 200, 75, (200, 200, 200)) # Upper right horizontal
            make_wall(-400, -300, 200, 75, (200, 200, 200)) # Upper left horizontal
            make_wall(200, 300, 200, 75, (200, 200, 200)) # Lower right horizontal
            make_wall(-400, 300, 200, 75, (200, 200, 200)) # Lower left horizontal

            make_wall(325, -300, 75, 200, (200, 200, 200)) # Upper right vertical
            make_wall(-400, -300, 75, 200, (200, 200, 200)) # Upper left vertical
            make_wall(325, 175, 75, 200, (200, 200, 200)) # Lower right vertical
            make_wall(-400, 175, 75, 200, (200, 200, 200)) # Lower left vertical

            # for x in range(10):
            #     if len(items_in_inventory) < 48:
            #         make_item(100, 100)

        if game_state[paused_i] == False:
            # Drawing the background
            
            window.blit(page.background, (-screen_x + page.scrolled_x, -screen_y + page.scrolled_y))
            '''
            pygame.draw.rect(window, (0, 0, 200), pygame.Rect(-screen_x+page.scrolled_x, -screen_y+page.scrolled_y, screen_x, screen_y)) # Upper Left
            pygame.draw.rect(window, (200, 0, 0), pygame.Rect(0+page.scrolled_x, -screen_y+page.scrolled_y, screen_x, screen_y)) # Upper Right
            pygame.draw.rect(window, (0, 200, 0), pygame.Rect(-screen_x+page.scrolled_x, 0+page.scrolled_y, screen_x, screen_y)) # Bottom Left
            pygame.draw.rect(window, (200, 100, 0), pygame.Rect(0+page.scrolled_x, 0+page.scrolled_y, screen_x, screen_y)) # Bottom Right
            '''
            # Just testing this function
            for enemy in enemies:
                enemy.chase()
            for projectile in enemy_projectiles:
                projectile.move_forward()
            for wall in walls:
                wall.draw()
            player.draw()
            player.attack()
            
            # For the Shop
            pygame.draw.rect(window, (0, 200, 0), pygame.Rect(page.scrolled_x+225, page.scrolled_y-225, 100, 100))
            if player.get_distance([275, -175]) < 75:
                display_shop()
            else:
                shopping[selling_i] = False
            
            # Starting a level
            if page.draw_button(-1000, -500, 200, 50, Red, "Level 1", game_state):
                time.sleep(.25)
                page.number = 7
                page.done = False
                return
        else:
            display_paused()
        
        page.done = True

    def level_1():
        page.initialize()
        page.max_x = 3000
        page.min_x = -3000
        page.max_y = 3000
        page.min_y = -3000
        if page.done == False:
            # Make walls and spawners (Low level enemies)
            make_wall(500, 0, 75, 300, (0, 0, 200))
            make_spawner(1000, 0, "Fish", 3)
            make_wall(-500, 0, 75, 300, (0, 0, 200))
            make_spawner(-1000, 0, "Skeleton", 1)
            make_wall(0, 500, 300, 75, (0, 0, 200))
            make_spawner(0, 1000, "Troll", 2)
            make_wall(0, -500, 300, 75, (0, 0, 200))
            make_spawner(0, -1000, "Zombie", 2)
            # Higher level spawners
            make_wall(1000, 1000, 50, 50 ,(0, 0, 200))
            make_spawner(1500, 1500, "Slime", 4)
            make_wall(-1000, -1000, 50, 50 ,(0, 0, 200))
            make_spawner(-1500, -1500, "Troll", 5)
            make_wall(1000, -1000, 50, 50 ,(0, 0, 200))
            make_spawner(1500, -1500, "Skeleton", 6)
            make_wall(-1000, 1000, 50, 50 ,(0, 0, 200))
            make_spawner(-1500, 1500, "Zombie", 7)
            # Random enemies
            make_enemy(0, 600, "Slime", 1)
            make_enemy(1100, 0, "Slime", 1)
            
        #While the level is in play
        if game_state[paused_i] == False:
            #window.blit(page.background, (-screen_x + page.scrolled_x, -screen_y + page.scrolled_y))
            pygame.draw.rect(window, (200, 200, 200), pygame.Rect(0, 0, screen_x, screen_y)) # Backdrop
            for spawner in spawners:
                spawner.draw()
                spawner.spawn_enemies()
            for wall in walls:
                wall.draw()

            for enemy in enemies:
                enemy.chase()
            for projectile in enemy_projectiles:
                projectile.move_forward()
            player.draw()
            player.attack()
        else:
            display_paused()
        
        # How to complete the level
        # Maybe set up like a finish line, kind of gauntlet style
        if len(enemies) == 0:
            # When you kill all of the enemies go to level select
            time.sleep(.25)
            page.number = 6
            page.done = False
            return

        page.done = True

    # Loop
    while game_state[running_i]:
        pygame.display.update()
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]
        if page.number == 1:
            main_menu()
        elif page.number == 2:
            new_game()
        elif page.number == 3:
            load_game()
        elif page.number == 5:
            character_select()
        elif page.number == 6:
            level_select()
        elif page.number == 7:
            level_1()
        # Setting up butons
        # For holding a button use this syntax
        keys = pygame.key.get_pressed()
        for x in [6, 7]:
            if page.number == x and game_state[paused_i] == False:
                if keys[pygame.K_UP] or keys[ord("w")]:
                    up()
                
                if keys[pygame.K_DOWN] or keys[ord("s")]:
                    down()
                
                if keys[pygame.K_LEFT] or keys[ord("a")]:
                    left()
                else:
                    player.left = False
                
                if keys[pygame.K_RIGHT] or keys[ord("d")]:
                    right()
                else:
                    player.right = False

                if controller_connected:
                    if joysticks[0].get_axis(1) < -.1:
                        up(joysticks[0].get_axis(1))

                    if joysticks[0].get_axis(1) > .1 :
                        down(joysticks[0].get_axis(1))

                    if joysticks[0].get_axis(0) > .1:
                        left(joysticks[0].get_axis(0))
                    else:
                        player.left = False

                    if joysticks[0].get_axis(0) > .1:
                        left(joysticks[0].get_axis(0))
                    else:
                        player.left = False
        
        # Controller triggers, dpad, and stick movement
        if controller_connected:
            if joysticks[0].get_hat(0)[0] != 0:
                print("D-Pad x", joysticks[0].get_hat(0)[0])
            if joysticks[0].get_hat(0)[1] != 0:
                print("D-Pad y", joysticks[0].get_hat(0)[1])
            if abs(joysticks[0].get_axis(0)) > .1:
                print("left stick x", joysticks[0].get_axis(0))
            if abs(joysticks[0].get_axis(1)) > .1:    
                print("left stick y", joysticks[0].get_axis(1))
            if abs(joysticks[0].get_axis(2)) > .1:
                print("right stick x", joysticks[0].get_axis(2))
            if abs(joysticks[0].get_axis(3)) > .1:
                print("right stick y", joysticks[0].get_axis(3))
            if joysticks[0].get_axis(4) > -.9:
                print("left trigger", joysticks[0].get_axis(4))
            if joysticks[0].get_axis(5) > -.9:
                print("right trigger", joysticks[0].get_axis(5))

        # For pressing a button use this syntax
        for event in pygame.event.get():
            # Moving the clock forward
            if event.type == pygame.USEREVENT:
                counter += 1
            if event.type == pygame.JOYBUTTONDOWN:
                # Mapped out all the xbox controller buttons
                for check in range(0, 16):
                    if joysticks[0].get_button(check) > 0:
                        print(check, joysticks[0].get_button(check))
            # Clicking on the red X
            if event.type == pygame.QUIT:
              game_state[running_i] = False
              pygame.quit()
            if event.type == pygame.KEYDOWN or event.type == pygame.JOYBUTTONDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    enter()
                if event.key == pygame.K_ESCAPE:
                    game_state[running_i] = False
                    pygame.quit()
                for x in [1, 2, 3, 5]:
                    if page.number == x:
                        if event.key == pygame.K_UP or event.key == ord("w"):
                            up()
                        if event.key == pygame.K_DOWN or event.key == ord("s"):
                            down()
                        if controller_connected:
                            if joysticks[0].get_axis(1) < -.1:
                                up()
                            if joysticks[0].get_axis(1) > .1:
                                down()
                for x in [6, 7]:
                    if page.number == x:
                        if event.key == ord("e"):
                            if game_state[paused_i] == False:
                                player.e_ability()
                        if event.key == ord("i"):
                            if game_state[paused_i] == False:
                                game_state[paused_i] = True
                                window.fill(Background)
                                pointer.goto(1425, 320)
                                display_paused()
                                distribute_items()
                                game_state[inventory_i] = True
                            else:
                                game_state[paused_i] = False
                        # if event.key == pygame.K_RIGHT:
                        #     right()
        clock.tick(60)


def delete_character(name):
    con = SQL.connect('SQL_Database\RPG2/save_data.db')
    cur = con.cursor()

    if(check_for_table(cur, "characters") == False):
        print("No character data available")
    else:
        # Check to make sure the name is in the table
        for names in cur.execute(f"SELECT name FROM characters ORDER BY name"):
            if name in names:
                print(f"'{name}' deleted")
                cur.execute(f"DELETE FROM characters WHERE name = '{name}'")
    if(check_for_table(cur, "items") == False):
        print("No item data available - update_items")
    else:
        # Check to make sure the name is in the table
        for names in cur.execute(f"SELECT name FROM characters ORDER BY name"):
            if name in names:
                # Delete each item previously associated
                cur.execute(f"DELETE FROM items WHERE name = '{name}'")
    con.commit()
    con.close()


def edit_character_data(character_name, stats):
    con = SQL.connect('SQL_Database\RPG2/save_data.db')
    cur = con.cursor()
    print(f"Editing {character_name} in table")

    # Check if there is a table
    if(check_for_table(cur, "characters") == False):
        print("No data in table")
    else:
        for names in cur.execute(f"SELECT name FROM characters ORDER BY name"):
            #print(names)
            for name in names:
                if name == character_name:
                    cur.execute(f"UPDATE characters SET level = {stats[0]}, xp = {stats[1]}, health = {stats[2]}, damage = {stats[3]}, speed = {stats[4]}, defense = {stats[5]}, ability = {stats[6]}, mana = {stats[7]}, gold = {stats[8]} WHERE name = '{character_name}'")
                    print(f"Save Successful - {character_name} {stats}")

    con.commit()
    con.close()



def get_table(table_name):
    con = SQL.connect('SQL_Database\RPG2/save_data.db')
    cur = con.cursor()
    #print("Checking table")
    table = []

    # Checking if there is a table with that name
    if(check_for_table(cur, f"{table_name}") == False):
        print("No table with that name - get_table")
    else:
        for row in cur.execute(f"SELECT * FROM '{table_name}' ORDER BY name"):
            table.append(row)
            #print(row)
    con.close()
    return table



def add_new_character_data(name, type):
    con = SQL.connect('SQL_Database\RPG2/save_data.db')
    cur = con.cursor()
    already_taken = False

    # Checking if there is already a table
    if(check_for_table(cur, "characters") == False):
        # If not, create a new characters table
        cur.execute("CREATE TABLE characters (name, type, level, xp, health, damage, speed, defense, ability, mana, gold)")
    
    # Check to make sure the name is not already taken
    for names in cur.execute(f"SELECT name FROM characters ORDER BY name"):
        if name in names:
            already_taken = True
            print(f"Name '{name}' already taken")

    if already_taken == False:
        print(f"Adding {name} to table")
        # Creating a new character
        stats = ["name", "type", "level", "xp", "health", "damage", "speed", "defense", "ability", "mana", "gold"]
        Warrior_stats = [150, 20, 2, 3, 2, 1] # Health, damage, attack speed, defense, ability, mana 
        Mage_stats =    [100, 20, 2, 1, 5, 3]
        Archer_stats =  [100, 25, 3, 1, 3, 2]
        if type == "Archer":
            stats = Archer_stats
        if type == "Warrior":
            stats = Warrior_stats
        if type == "Mage":
            stats = Mage_stats

        # Adding the values to the characters table
        cur.execute(f"INSERT INTO characters VALUES ('{name}', '{type}', 1, 0, {stats[0]}, {stats[1]}, {stats[2]}, {stats[3]}, {stats[4]}, {stats[5]}, 0)")

        con.commit()
    con.close()
    return already_taken

def check_for_table(cur, table_name):
    cur.execute(f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    if cur.fetchone()[0] < 1:
        return False
    else:
        return True
    
def get_character_data(name):
    con = SQL.connect('SQL_Database\RPG2/save_data.db')
    cur = con.cursor()
    data = 'none'

    if(check_for_table(cur, "characters") == False):
        print("No character data available")
    else:
        # Check to make sure the name is in the table
        for names in cur.execute(f"SELECT name FROM characters ORDER BY name"):
            if name in names:
                cur.execute(f"SELECT * FROM characters WHERE name='{name}'")
                data = cur.fetchall()[0]
    return data

def add_item_to_database(name, item, cur):

    # Checking if there is already a table
    if(check_for_table(cur, "items") == False):
        # If not, create a new items table
        print("attempting to create table - add_items_to_database")
        cur.execute("CREATE TABLE items (name, type, damage, defense, health, mana, ability, speed, level, equipped)")

    # Adding the values to the characters table
    cur.execute(f"INSERT INTO items VALUES ('{name}', '{item[0]}', {item[1]}, {item[2]}, {item[3]}, {item[4]}, {item[5]}, {item[6]}, {item[7]}, {item[8]})")

def update_items(name, items_list):
    con = SQL.connect('SQL_Database\RPG2/save_data.db')
    cur = con.cursor()

    if(check_for_table(cur, "items") == False):
        for x in range(len(items_list)):
            add_item_to_database(name, items_list[x], cur)
        print("No item data available - update_items")
    else:
        # Check to make sure the name is in the table
        for names in cur.execute(f"SELECT name FROM characters ORDER BY name"):
            if name in names:
                # Delete each item previously associated
                cur.execute(f"DELETE FROM items WHERE name = '{name}'")
                # Add each item given in the list
                for x in range(len(items_list)):
                    add_item_to_database(name, items_list[x], cur)
    con.commit()
    con.close()

def get_item_data(name):
    con = SQL.connect('SQL_Database\RPG2/save_data.db')
    cur = con.cursor()
    data = 'none'

    if(check_for_table(cur, "items") == False):
        print("No item data available - get_item_data")
    else:
        # Check to make sure the name is in the table
        for names in cur.execute(f"SELECT name FROM items ORDER BY name"):
            if name in names:
                cur.execute(f"SELECT * FROM items WHERE name='{name}'")
                data = cur.fetchall()
    return data

if __name__ == "__main__":
    main()