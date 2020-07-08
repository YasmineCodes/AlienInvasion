import sys

import pygame

from settings import settings

class AlienInvasion:
    #overall class to manage game assets
    
    def __init__(self):
        #initialize the game and create game resources
        pygame.init()
        
        #create settings attribute from our settings class
        self.settings = settings()

        #create a display window on which to draw the game's graphical elements
        #tuple argument contains window dimensions
        self.screen = pygame.display.set_mode((self.settings.screen_height, self.settings.screen_width))
        pygame.display.set_caption('Alien Invasion')

        #set background color using RGB values (default is back) derived from our settings class
        self.bg_color = (self.settings.bg_color)


    def run_game(self):
        #start the main loop for the game
        while True:
            #listen/watch for keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            #redraw screen during each pass through the loop
            self.screen.fill(self.bg_color)
            #render most recently drawn screen
            pygame.display.flip()
    
    if __name__ == '__main__':
        #make a game instance and run the game
        ai = AlienInvasion()
        ai.run_game()
        