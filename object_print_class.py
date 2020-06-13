import pygame


class ObjectPrint:

    """A class for objects that get printed on the screen"""

    def __init__(self, content, font_size, x_coord, y_coord, where):
        # what(where): the display screen must be used as input
        self.content = content
        self.font = pygame.font.Font('freesansbold.ttf', font_size)
        self.font_color = (0, 0, 0)
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.where = where

    # ------------------------------------------------------------------------

    """Functions"""

    def display_object(self):
        """Blits the object on the display."""
        output = self.font.render(str(self.content), True, self.font_color)
        self.where.blit(output, (self.x_coord, self.y_coord))


class FlashingObject(ObjectPrint):

    """A subclass of ObjectPrint, for objects which have flashing feedback."""

    def __init__(self, content, font_size, x_coord, y_coord, where):

        """Inherited Variables"""
        super(FlashingObject, self).__init__(content, font_size, x_coord, y_coord, where)

        """State Variables"""
        self.flashing_timer = 0
        self.flashing_state = 0

    # --------------------------------------------------------------------------------------

    """Functions"""

    def begin_flashing(self, variable, mode):
        """Begin flashing state for a given duration"""
        # what(state): string variable, either 'pos' or 'neg'
        if variable > 0:
            self.flashing_timer = variable
            if mode == 'pos':
                self.font_color = (0, 255, 0)
                self.flashing_state = self.font.render('+', True, (0, 255, 0))
            if mode == 'neg':
                self.font_color = (255, 0, 0)
                self.flashing_state = self.font.render('-', True, (255, 0, 0))

    def flashing_check(self, tic):
        self.flashing_timer -= tic
        """Check flashing timer and either erase object or reduce timer by tic."""
        if self.flashing_timer > 0:
            self.where.blit(self.flashing_state, (self.x_coord - 50, self.y_coord))
            self.where.blit(self.flashing_state, (self.x_coord + 50, self.y_coord))
        else:
            self.flashing_timer = 0
            self.font_color = (0, 0, 0)
