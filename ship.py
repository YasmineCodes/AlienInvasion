import pygame


class ship:
    # a class to manage the ship

    # init parameters are self and a reference to the ai game using the ship (created from our alien_invasion class )
    def __init__(self, ai_game):
        # initialize the ship and set starting position

        # assign the game's screen and "rect" of screen to ship attributes for easy access
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # starting each ship at the bottom center of the screen (screen's rect has a midbottom attribute)
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        # draw the ship at its current location
        self.screen.blit(self.image, self.rect)
