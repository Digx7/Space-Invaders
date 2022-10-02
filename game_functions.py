import sys
from time import sleep

import pygame
import pygame as pg
from vector import Vector
from Alien import *
from Bunker import *

movement = {pg.K_LEFT: Vector(-1, 0),   # dictionary to map keys to Vector velocities
            pg.K_RIGHT: Vector(1, 0),
            pg.K_UP: Vector(0, -1),
            pg.K_DOWN: Vector(0, 1)
            }


# update and draw managers ===============


def start_menu_update(g):
    pg.mouse.set_visible(True)
    check_events(g)
    g.ship.center_ship()


def start_menu_draw(g):
    g.screen.fill(g.settings.bg_color)

    g.ship.draw()
    g.start_ui.draw()


def main_update(g):
    pg.mouse.set_visible(False)
    check_events(g)

    try_to_make_new_fleet(g.settings, g.stats, g.screen, g.ship, g.aliens, g.lasers)
    try_to_make_ufo(g.settings, g.stats, g.screen, g.aliens)
    # try_to_make_new_bunkers(g.settings, g.stats, g.screen, g.bunkers)

    g.ship.update()
    g.lasers.update()
    g.aliens.update()
    g.alien_lasers.update()

    check_laser_collisions(g.settings, g.stats, g.game_ui, g.aliens, g.lasers, g.bunkers)
    check_player_hit_by_aliens(g.settings, g.stats, g.screen, g.ship, g.aliens, g.lasers)
    check_aliens_bottom(g.settings, g.stats, g.screen, g.ship, g.aliens, g.lasers)

    g.game_ui.update()


def main_update_animations(g):
    g.ship.update_animation()


def main_draw(g):
    g.screen.fill(g.settings.bg_color)
    g.lasers.draw()
    g.aliens.draw()
    g.alien_lasers.draw()
    g.ship.draw()
    g.bunkers.draw()
    g.game_ui.draw()


def end_update(g):
    pg.mouse.set_visible(True)
    check_events(g)
    g.settings.reset_speed()
    g.stats.reset_stats()


def end_draw(g):
    g.screen.fill(g.settings.bg_color)
    # g.buttons.draw_button("retry_button")
    g.end_ui.draw()


# event listeners ===================


def main_check_keydown_events(event, g):
    key = event.key
    if key == pg.K_q:
        sys.exit()
    elif key == pg.K_SPACE:
        g.ship.shooting = True
    elif key in movement.keys(): g.ship.vel = g.settings.ship_speed_factor * movement[key]


def main_check_keyup_events(event, g):
    key = event.key
    if key == pg.K_SPACE: g.ship.shooting = False
    elif key in movement.keys(): g.ship.vel = Vector()


def check_events(g):
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()
        if g.stats.is_current_scene("menu"): start_events(event, g)
        elif g.stats.is_current_scene("main"): main_events(event, g)
        elif g.stats.is_current_scene("end"): end_events(event, g)


def start_events(event,g):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if g.start_ui.current_mode == g.start_ui.modes["Main"]:
            if g.start_ui.buttons.check_button("play_button", mouse_x, mouse_y): on_play_click(g)
            elif g.start_ui.buttons.check_button("score_button", mouse_x, mouse_y):
                on_leaderboard_click(g)
                print("Score got clicked")
            elif g.start_ui.buttons.check_button("leaderboard_back_button", mouse_x, mouse_y):
                print("Back got clicked")
                on_leaderboard_back_click(g)
        elif g.start_ui.current_mode == g.start_ui.modes["LeaderBoard"]:
            if g.start_ui.buttons.check_button("leaderboard_back_button", mouse_x, mouse_y):
                print("Back got clicked")
                on_leaderboard_back_click(g)


def main_events(event, g):
    if event.type == pg.KEYDOWN: main_check_keydown_events(event, g)
    elif event.type == pg.KEYUP: main_check_keyup_events(event, g)
    elif event.type == pg.USEREVENT:
        g.ship.update_animation()
        g.aliens.update_animations()
    elif event.type == pg.USEREVENT + 1:
        reset(g)


def end_events(event, g):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if g.end_ui.buttons.check_button("retry_button", mouse_x, mouse_y): on_retry_click(g)
        elif g.end_ui.buttons.check_button("quit_button", mouse_x, mouse_y): on_quit_click(g)

# on button click ======================


def on_play_click(g):
    g.stats.reset_stats()
    g.stats.set_current_scene("main")
    reset(g)


def on_leaderboard_click(g):
    g.start_ui.current_mode = g.start_ui.modes["LeaderBoard"]


def on_leaderboard_back_click(g):
    g.start_ui.current_mode = g.start_ui.modes["Main"]
    print("Back")


def on_retry_click(g):
    reset(g)
    g.stats.reset_stats()
    g.stats.set_current_scene("main")


def on_quit_click(g):
    g.stats.set_current_scene("menu")


# helper functions =================


def clamp(posn, rect, settings):
    left, top = posn.x, posn.y
    width, height = rect.width, rect.height
    left = max(0, min(left, settings.screen_width - width))
    top = max(0, min(top, settings.screen_height - height))
    return Vector(x=left, y=top), pg.Rect(left, top, width, height)

# alien fleet functions


def try_to_make_ufo(settings, stats, screen, aliens):
    if random.randint(0, 10000) <= settings.ufo_odds:
        create_ufo(settings, stats, screen, aliens)


def create_ufo(settings, stats, screen, aliens):
    print("A UFO appeared !!!!!!")
    ufo = Alien(settings, stats, screen, "ufo")
    ufo_width = ufo.rect.width
    ufo.x = ufo_width + 2
    ufo.rect.x = ufo.x
    ufo.rect.y = ufo.rect.height + 2
    aliens.spawn(ufo)


def try_to_make_new_fleet(settings, stats, screen, ship, aliens, lasers):
    """Try's to make a new alien fleet if all aliens are dead"""
    if len(aliens.aliens) == 0:
        # Destroy existing bullets and create new fleet.
        lasers.lasers.empty()
        settings.increase_speed()

        stats.level += 1

        create_fleet(settings, stats, screen, ship, aliens)


def create_fleet(settings, stats, screen, ship, aliens):
    """Create a full fleet of aliens"""
    # Create an alien and find the number of aliens in a row
    alien = Alien(settings, stats, screen)
    number_aliens_x = get_number_aliens_x(settings, alien.rect.width)
    number_rows = get_number_rows(settings, ship.rect.height, alien.rect.height)

    alien_type_change_point1 = number_rows/3
    alien_type_change_point2 = alien_type_change_point1 * 2

    alien_type = "default"

    # Create the first row of aliens
    for row_number in range(number_rows):
        if row_number < alien_type_change_point1: alien_type = "03"
        elif alien_type_change_point1 <= row_number < alien_type_change_point2: alien_type = "02"
        elif row_number >= alien_type_change_point2: alien_type = "default"
        else: alien_type = "default"
        for alien_number in range(number_aliens_x):
            create_alien(settings, stats, screen, aliens, alien_number, row_number, alien_type)


def create_alien(settings, stats, screen, aliens, alien_number, row_number, alien_type="default"):
    """Create an alien and place it in the row"""
    alien = Alien(settings, stats, screen, alien_type)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.spawn(alien)


def get_number_rows(settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def get_number_aliens_x(settings, alien_width):
    """Determine the number of aliens that fit in row"""
    available_space_x = settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


# bunker functions


def try_to_make_new_bunkers(settings, stats, screen, bunkers):
    """Try to make a new row of bunkers if all are dead"""
    if len(bunkers.bunkers) == 0:
        create_bunkers_row(settings, screen, bunkers)


def create_bunkers_row(settings, screen, bunkers):
    """Will create a row of bunkers"""
    bunker = Bunker(settings, screen)
    number_bunkers_x = get_number_bunkers_x(settings, bunker.rect.width, settings.bunker_padding)

    for bunker_number in range(number_bunkers_x):
        create_bunker(settings, screen, bunkers, bunker_number, settings.bunker_padding)


def create_bunker(settings, screen, bunkers, bunker_number, bunker_padding):
    """Create a bunker and place it in the row"""
    bunker = Bunker(settings, screen)
    bunker_width = bunker.rect.width
    bunker.x = bunker_width + 2 * (bunker_width + bunker_padding) * bunker_number
    bunker.rect.x = bunker.x
    bunker.rect.y = bunker.rect.height + settings.bunker_height

    bunkers.spawn(bunker)


def get_number_bunkers_x(settings, bunker_width, bunker_padding):
    """Determine the number of bunkers that fit in row"""
    available_space_x = settings.screen_width - 2 * (bunker_width + bunker_padding)
    number_bunkers_x = int(available_space_x / (2 * bunker_width + bunker_padding))
    return number_bunkers_x


# collision manager functions


def check_laser_collisions(settings, stats, ui, aliens, lasers, bunkers):
    """Checks if the lasers have collided with any aliens.  Deletes both if collsion is detected"""
    alien_laser_collisions = pygame.sprite.groupcollide(lasers.lasers, aliens.aliens, True, True)
    laser_laser_collisions = pygame.sprite.groupcollide(lasers.lasers, aliens.lasers.lasers, True, True)
    plaser_bunker_collisions = pygame.sprite.groupcollide(lasers.lasers, bunkers.bunkers, True, True)
    alaser_bunker_collisions = pygame.sprite.groupcollide(aliens.lasers.lasers, bunkers.bunkers, True, True)

    if alien_laser_collisions:
        for aliens in alien_laser_collisions.values():
            # stats.score += settings.alien_points * len(aliens)
            ui.update()
            if isinstance(aliens, Alien):
                print("I was an alien")
                alien_type = aliens.alien_type


def check_player_hit_by_aliens(settings, stats, screen, ship, aliens, lasers):
    """Check if the player was hit"""
    if ship.moving:
        if pygame.sprite.spritecollideany(ship, aliens.aliens) or pygame.sprite.spritecollideany(ship, aliens.lasers.lasers):
            print("Ship hit!!!")
            ship_hit(settings, stats, screen, ship, aliens, lasers)


def reset(g):
    """Resets after player dead"""
    g.aliens.aliens.empty()
    g.aliens.lasers.lasers.empty()
    g.lasers.lasers.empty()

    g.ship.center_ship()
    g.ship.Animations.set_current_animation("idle")
    g.ship.moving = True
    try_to_make_new_bunkers(g.settings, g.stats, g.screen, g.bunkers)


def ship_hit(settings, stats, screen, ship, aliens, lasers):
    """Respond to ship being hit by alien."""
    if stats.lives_left > 0:
        # Decrement lives_left
        stats.lives_left -= 1
        ship.kill()
        aliens.freeze()

        pygame.time.set_timer(pygame.USEREVENT + 1, 3000, 1)

        # Empty the list of aliens and bullets
        # aliens.aliens.empty()
        # lasers.lasers.empty()

        # Create a new fleet and center the ship
        # create_fleet(settings, screen, ship, aliens)
        # ship.center_ship()

        # Pause
        # sleep(0.5)
    else:
        stats.set_current_scene("end")
        stats.check_high_score()


def check_aliens_bottom(settings, stats, screen, ship, aliens, lasers):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(settings, stats, screen, ship, aliens, lasers)
            break