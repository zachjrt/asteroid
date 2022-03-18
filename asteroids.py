"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others
This program implements the asteroids game.

You should make the FlyingObject an abstract base class.


"""
import arcade
import math
import random
from abc import ABC

from arcade.color import BLUE, RED

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1200

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
#Modifying ship for easier control
SHIP_THRUST_AMOUNT = 0.25/5
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2

COMET_AMOUNT = 5

"""
Creates Point class, used to keep track of location
"""
class Point:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
"""
Creates Velocity class, used to keep track of movement
"""        
class Velocity:
    def __init__(self):
        self.dx = 0.0
        self.dy = 0.0

"""
Creates Abstract Flying object class, used to help define other classes
"""     
class FlyingObject(ABC):

    
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        
    def advance(self):
        self.center.y += self.velocity.dy
        self.center.x += self.velocity.dx

    def draw(self):
        return

    def is_off_screen(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        is_off_screen = False
        
        #Creates Screen Wrapping effect
        if self.center.x > SCREEN_WIDTH:
            self.center.x = 0
        elif self.center.x < 0:
            self.center.x = 800
        elif self.center.y > SCREEN_HEIGHT:
            self.center.y = 0
        elif self.center.y < 0:
            self.center.y = 600
        return is_off_screen

"""
Creates comet class, which will be the base for all asteroids
currently set up as the large asteroid
"""
class Comet(FlyingObject):
    def __init__(self):
        super().__init__()
        self.center.x = random.randint(1, 200)
        self.center.y = random.randint(1, 600)
        self.velocity.dx = random.uniform(-1 * BIG_ROCK_SPEED, BIG_ROCK_SPEED)
        self.velocity.dy = random.uniform(-1 * BIG_ROCK_SPEED, BIG_ROCK_SPEED)
        self.angle = BIG_ROCK_SPIN
        self.rotateSpeed = BIG_ROCK_SPIN
        self.radius = BIG_ROCK_RADIUS
        self.alive = True
        self.size = 3
        self.image = "images/meteorGrey_big1.png"
        self.texture = arcade.load_texture(self.image)
        
    def draw(self):
        self.angle += self.rotateSpeed
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.texture.width, self.texture.height, self.texture, self.angle, 255)

    def split(self):
        self.alive = False
        medcomet1 = MediumComet(self.center.x, self.center.y)
        medcomet2 = MediumComet(self.center.x, self.center.y)
        smallcomet1 = SmallComet(self.center.x, self.center.y)
        window.comets.append(medcomet1)
        window.comets.append(medcomet2)
        window.comets.append(smallcomet1)
    



"""
Medium Comet
"""
class MediumComet(Comet):
    def __init__(self, x, y):
        super().__init__()
        self.center.x = x
        self.center.y = y
        self.angle = MEDIUM_ROCK_SPIN
        self.rotateSpeed = MEDIUM_ROCK_SPIN
        self.radius = MEDIUM_ROCK_RADIUS
        self.image = "images/meteorGrey_med1.png"
        self.texture = arcade.load_texture(self.image)
        self.size = 2
    def split(self):
        self.alive = False
        smallcomet1 = SmallComet(self.center.x, self.center.y)
        smallcomet2 = SmallComet(self.center.x, self.center.y)
        window.comets.append(smallcomet1)
        window.comets.append(smallcomet2)

"""
Small Comet
"""
class SmallComet(Comet):
    def __init__(self, x, y):
        super().__init__()
        self.center.x = x
        self.center.y = y
        self.angle = SMALL_ROCK_SPIN
        self.rotateSpeed = SMALL_ROCK_SPIN
        self.radius = SMALL_ROCK_RADIUS
        self.image = "images/meteorGrey_small1.png"
        self.texture = arcade.load_texture(self.image)
        self.size = 1
    def split(self):
        self.alive = False

        
             
"""
Sets up Spaceship class. this is the player
"""
class SpaceShip(FlyingObject):
    def __init__(self):
        super().__init__()
        self.center.y = SCREEN_HEIGHT/2
        self.center.x = SCREEN_WIDTH/2
        self.angle = 0;
        self.accelerate = SHIP_THRUST_AMOUNT
        self.rotateSpeed = SHIP_TURN_AMOUNT
        self.alive = True
        self.isShooting = True
        self.radius = SHIP_RADIUS
        self.lives = 10
        self.image = "images/playerShip1_orange.png"
        self.texture = arcade.load_texture(self.image)

    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.texture.width, self.texture.height, self.texture, self.angle, 255)

    def turnLeft(self):
        self.angle += self.rotateSpeed
        
    def turnRight(self):
        self.angle -= self.rotateSpeed
        
    def goForward(self):
        self.velocity.dy += math.sin(math.radians(self.angle + 90)) * self.accelerate
        self.velocity.dx += math.cos(math.radians(self.angle + 90)) * self.accelerate
       
        
    def goBack(self):
        self.velocity.dy -= math.sin(math.radians(self.angle + 90)) * self.accelerate
        self.velocity.dx -= math.cos(math.radians(self.angle + 90)) * self.accelerate
     
    def death(self):
        self.image = "images/playerShip1_gray.png"
        self.texture = arcade.load_texture(self.image)
        
        

"""
Creates class for bullets
"""
class Bullet(FlyingObject):
    def __init__(self, x, y):
        super().__init__()
        self.center.y = y
        self.center.x = x
        self.radius = BULLET_RADIUS
        self.rotateSpeed = SHIP_TURN_AMOUNT
        self.angle = BIG_ROCK_SPIN
        self.image = "images/laserBlue01.png"
        self.texture = arcade.load_texture(self.image)
        self.alive = True
        self.time = 0

    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.texture.width, self.texture.height, self.texture, self.angle, 255)

    def fire(self, angle, dx, dy):
        self.angle = angle + 90
        self.velocity.dy = math.sin(math.radians(self.angle)) * (dy + BULLET_SPEED)
        self.velocity.dx = math.cos(math.radians(self.angle)) * (dx + BULLET_SPEED)
        
    def advance(self):
        self.center.y += self.velocity.dy
        self.center.x += self.velocity.dx
        self.time += 1
        if self.time >= 60:
            self.alive = False
   
        


class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        self.held_keys = set()
        self.ship = SpaceShip()
        self.bullets = []
        self.comets = []
        self.create_comet()


        # TODO: declare anything here you need the game class to track
        

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()
        self.ship.draw()

        # TODO: draw each object
        for bullet in self.bullets:
            bullet.draw()

        for comet in self.comets:
            comet.draw()
        self.draw_lives()
        if self.ship.alive == False:
            self.game_over()

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()
        self.check_collisions()
        self.check_off_screen()
        self.cleanup()
        
        
        # TODO: Tell everything to advance or move forward one step in time
        for bullet in self.bullets:
            bullet.advance()
            

        for comet in self.comets:
            comet.advance()
        
        
            self.ship.advance()

        # TODO: Check for collisions
    def draw_lives(self):
        """
        Puts the current score on the screen
        """
        lives_text = "Life: {}".format(self.ship.lives)
        lives_x = 10
        lives_y = SCREEN_HEIGHT - 40
        arcade.draw_text(lives_text, start_x=lives_x, start_y=lives_y, font_size=30, color=arcade.color.WHITE)

    def game_over(self):
        """
        Puts the current score on the screen
        """
        gameOver_text = "Game Over"
        gameOver_x = SCREEN_WIDTH/2 - 220
        gameOver_y = SCREEN_HEIGHT/2
        arcade.draw_text(gameOver_text, start_x=gameOver_x, start_y=gameOver_y, font_size=60, color=arcade.color.WHITE)

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.turnLeft()
            

        if arcade.key.RIGHT in self.held_keys:
            self.ship.turnRight()
            

        if arcade.key.UP in self.held_keys:
            self.ship.goForward()

        if arcade.key.DOWN in self.held_keys:
            self.ship.goBack()

        # Machine gun mode...
        #if arcade.key.SPACE in self.held_keys:
        #    pass

    def check_off_screen(self):
        """
        Checks to see if bullets or targets have left the screen
        and if so wraps them around
        """
        for bullet in self.bullets:
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.bullets.remove(bullet)

        for comet in self.comets:
            comet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT)
            
        self.ship.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT)


    def check_collisions(self):
        """
        Checks Collisions
        """

       
        for bullet in self.bullets:
            for comet in self.comets:

               
                if bullet.alive and comet.alive:
                    too_close = bullet.radius + comet.radius

                    if (abs(bullet.center.x - comet.center.x) < too_close and
                                abs(bullet.center.y - comet.center.y) < too_close):
                        bullet.alive = False
                        comet.split()
                        
        for comet in self.comets:
            
            too_close = comet.radius + self.ship.radius

            if (abs(comet.center.x - self.ship.center.x) < too_close and
                    abs(comet.center.y - self.ship.center.y) < too_close):
                comet.rotateSpeed *= -1       
                self.ship.velocity.dx = (-.7 * self.ship.velocity.dx)
                self.ship.velocity.dy = (-.7 * self.ship.velocity.dy)
                self.ship.lives -= 1;
                if self.ship.lives <= 0:
                    self.ship.alive = False
                    
                          
                        # We will wait to remove the dead objects until after we
                        # finish going through the list

        # Now, check for anything that is dead, and remove it
        self.cleanup()

                
    def cleanup(self):
        for bullet in self.bullets:
            if bullet.alive == False:
                self.bullets.remove(bullet)
        for comet in self.comets:
            if comet.alive == False:
                self.comets.remove(comet)
        if self.ship.alive == False:
            self.ship.death()
      
                

    def create_comet(self):
        """
        Creates 5 initial comets of large size
        :return:
        """

        while len(self.comets) < COMET_AMOUNT:   
            comet = Comet()
            self.comets.append(comet)
        

    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive == True:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                bullet = Bullet(self.ship.center.x, self.ship.center.y)
                bullet.fire(self.ship.angle, self.ship.velocity.dx, self.ship.velocity.dy)

                self.bullets.append(bullet)
                pass

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()