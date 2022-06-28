import pygame


# Button class
class Button():
    def __init__(self, x, y, image, scale):
        w = image.get_width()
        h = image.get_height()
        self.image = pygame.transform.scale(image, (int(w * scale), int(h * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Draw button on the screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return action
