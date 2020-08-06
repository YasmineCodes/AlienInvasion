import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    '''overall class to manage game assets'''

    def __init__(self):
        """initialize the game and create game resources"""
        pygame.init()
        # create settings attribute from our settings class
        self.settings = Settings()

        # Create a display window on which to draw the game's graphical elements
        # Tuple argument contains window dimensions
        # for default fullscreen: self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption('Alien Invasion')

        # Create an instance to store game stats and create scoreboard
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        # Create elements of the game
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Make the play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        ''' start the main loop for the game'''
        while True:
            self._check_events()
            self._update_screen()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

    def _check_events(self):
        '''listen/watch for keyboard and mouse events'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """Starts a new game when the player clicks Play. """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset game settings
            self.settings.initialize_dynamic_settings()

            # Reset the game in case the player is starting a new game after finishing one
            self.stats.reset_stats()
            # Update scoreboard with reset stats
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()

            # Switch to active mode
            self.stats.game_active = True

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and re-center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Hide mouse cursor
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        '''Responds to keypresses'''
        if event.key == pygame.K_RIGHT:
            # move ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # move ship to the left
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        '''Responds to releases'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_q:
            sys.exit()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """Responds to bullet alien collisions. Removes bullets and aliens that collide"""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            # Increase score
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet, when all aliens in first fleet are shot
            self.bullets.empty()
            self._create_fleet()
            # Level up the difficulty of the game
            self.settings.increase_speed()
            self.stats.level += 1
            self.scoreboard.prep_level()

    def _create_fleet(self):
        '''Create a fleet of aliens on the screen'''
        # make an aliens
        # create a fleet, with space to the right of each alien = to one alien's width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        ship_height = self.ship.rect.height

        # allowing for margin of one alien's width on either side
        available_space_x = self.settings.screen_width - (2 * alien_width)
        # allowing for space for the ship, two alien heights between ship and aliens and one alien heigh at the top
        available_space_y = self.settings.screen_height - \
            (3 * alien_height) - ship_height
        # each elien will take up with of 2 aliens because of one lien width gap between
        number_aliens_x = available_space_x // (2 * alien_width)
        number_rows = available_space_y // (2 * alien_height)

        # create full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        '''Update the position of the aliens in the fleet 
        after checking if any reached the  edges. '''
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by an alien. """
        if self.stats.ships_left > 0:
            # Decrement ships_left in stats and update scoreboard
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            # Get rid of remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet of aliens and re-center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            # Make mouse cursor visible again
            pygame.mouse.set_visible(True)

    def _check_fleet_edges(self):
        ''' Responds when any aliens reach the edges. '''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''Drop the entire fleet and change the fleet's direction. '''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        '''redraw screen during each pass through the loop'''
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # draw aliens on screen
        self.aliens.draw(self.screen)

        # Draw score info
        self.scoreboard.show_score()

        # Draw the play button if game is inactive
        # Drawing after all other elements to make sure it is visible above all elements
        if not self.stats.game_active:
            self.play_button.draw_button()

        # render most recently drawn screen
        pygame.display.flip()


if __name__ == '__main__':
    # make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
