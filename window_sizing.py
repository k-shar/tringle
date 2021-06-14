import pygame


class ScaleWindow:
    """A Class containing a Surface, that scales to fill a fraction of its parent surface"""
    def __init__(self, color, size_relative_to_parent: tuple, pos_relative_to_parent: tuple):

        # create surface and rect with some arbitrary non-zero size
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()

        # color in the surface, this would not work if surface was of size (0, 0)
        self.color = color
        self.image.fill(self.color)

        # define the relative pos and scale of the window
        self.rel_pos = pos_relative_to_parent
        self.rel_size = size_relative_to_parent

    def resize(self, parent: pygame.Surface):
        """Resize the surface and the rect's position, to a fraction of the parent (usually ...Window.image)"""
        self.image.fill(self.color)
        
        # new size is a fraction of the parents size
        size = (int(parent.get_size()[0] * self.rel_size[0]), int(parent.get_size()[1] * self.rel_size[1]))
        # scale surface to this new size
        self.image = pygame.transform.scale(self.image, size)

        # create new rect
        self.rect = self.image.get_rect()
        # position of rect is some fraction of the parents size relative to the parent surface
        self.rect.centerx = parent.get_size()[0] * self.rel_pos[0]
        self.rect.centery = parent.get_size()[1] * self.rel_pos[1]


class AspectWindow:
    """a Class containing a Surface, that scales to be as large as possible, while maintaining a given aspect ratio"""
    def __init__(self, color, aspect_ratio: tuple, pos: tuple, padding: float):

        # create surface and rect with some arbitrary non-zero size
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()

        # color in the surface, this would not work if surface was of size (0, 0)
        self.color = color
        self.image.fill(self.color)

        # define aspect ratio and padding
        self.aspect_ratio = aspect_ratio
        # if padding = 0, there *may* be some small overflow
        # if padding = 1, there will never be overflow
        # if padding > 1, padding will shrink the windows size
        self.pos = pos
        self.padding = padding

    def resize(self, parent: pygame.Surface):
        """Resize the surface and the rect's position, maintaining the aspect_ratio"""
        self.image.fill(self.color)

        max_size = list(parent.get_size())
        # reduce max size down dependant on padding
        max_size[0] *= self.padding
        max_size[1] *= self.padding
        current_size = [1, 1]

        # search for the max size we can grow to, while not overflowing parent
        overflown = False
        while not overflown:
            # increase size of image while maintaining aspect ratio
            current_size[0] += self.aspect_ratio[0]
            current_size[1] += self.aspect_ratio[1]

            # if this new size is >= to the size of our container,
            if current_size[0] >= max_size[0] or current_size[1] >= max_size[1]:
                # scale surface and rect to this new found size
                self.image = pygame.transform.scale(self.image, current_size)
                self.rect = self.image.get_rect()

                # set position of rect to a fraction of the size of parent
                # after removing the shrinking effect of the padding variable
                self.rect.centerx = (max_size[0] / self.padding) * self.pos[0]
                self.rect.centery = (max_size[1] / self.padding) * self.pos[1]
                overflown = True


class TextWindow(AspectWindow):
    def __init__(self, color, aspect_ratio: tuple, pos: tuple, padding: float, text: str):
        super().__init__(color, aspect_ratio, pos, padding)
        self.text = text
        self.font = "this needs to be redefined every resize event, as the size will change"

    def resize(self, parent: pygame.Surface):
        super().resize(parent)
        self.font = pygame.freetype.SysFont("bell", self.image.get_height())
        text_surf, text_rect = self.font.render(self.text, fgcolor=(255, 255, 255))
        self.image.blit(text_surf, text_surf.get_rect(center=self.image.get_rect().center))





