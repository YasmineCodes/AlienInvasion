import pygame


class Ship:
    ''' a class to manage the ship'''

    # init parameters are self and a reference to the ai game using the ship (created from our alien_invasion class )
    def __init__(self, ai_game):
        '''Initialize the ship and set starting position'''

        # assign the game's screen and "rect" of screen to ship attributes for easy access
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # starting each ship at the bottom center of the screen (screen's rect has a midbottom attribute)
        self.rect.midbottom = self.screen_rect.midbottom

        # Store decimal val for ship's horizonal position
        self.x = float(self.rect.x)

        # movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flag"""
        # update the ship's x value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # update rect object from self.x
        self.rect.x = self.x

    # draw the ship at its current location
    def blitme(self):
        self.screen.blit(self.image, self.rect)

