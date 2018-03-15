from pygame import Color, Rect
import pygame


def load_image(path):
    return pygame.image.load(path).convert_alpha()

class GUI:
    elements = []

    @staticmethod
    def add_element(element):
        GUI.elements.append(element)

    @staticmethod
    def del_element(name_element):
        for element in GUI.elements:
            if element.name == name_element:
                GUI.elements.remove(element)

    @staticmethod
    def update():
        for element in GUI.elements:
            element.update()

    @staticmethod
    def render(surface):
        for element in GUI.elements:
            element.render(surface)

    @staticmethod
    def apply_event(event):
        for element in GUI.elements:
            element.apply_event(event)

class Element:
    def __init__(self, pos = (0,0), size = (1, 1)):
        self.rect = Rect(pos, size)

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y


class Button(Element):
    def __init__(self, text, pos, size, func, name, text_color = Color('black'), but_color = (230, 230, 230), **kwargs):
        super().__init__()

        self.text = text
        self.pos = pos
        self.size = size
        self.function = func
        self.name = name

        self.text_color, self.color_but = text_color, but_color

        #self.rect.collidepoint(event.pos)

        self.rect = Rect(pos, size)
        self.rect.center = pos
        self.settings = {'but_color': but_color, 'hovered': None, 'clicked': None, 'size_font': 5}
        for name, value in kwargs.items():
            self.settings[name] = value

        self.font = pygame.font.Font(None, self.settings['size_font'])
        _x = pos[0]+pygame.font.Font(None, self.settings['size_font']).size(text)[0]//2
        self.font_rect = Rect(pos, size)
        self.font_rect.center = pos

        self.active = True

    def set(self, **kwargs):
        for name, value in kwargs.items():
            self.settings[name] = value

    def update(self):
        if self.active:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.settings['hovered']:
                    self.color_but = self.settings['hovered']
            else:
                self.color_but = self.settings['but_color']

    def render(self, surface):
        pygame.draw.rect(surface, self.color_but, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.text_color)
        surface.blit(self.rendered_text, self.font_rect)

    def apply_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if event.button == 1:
                    self.function()


class ButtonImage(Element):
    def __init__(self, pos, image_states, text='', font_path=None, text_color='black', text_size=20, name='test', func=lambda: None, shift_text = (0,0)):
        super().__init__()

        self.normal_image = load_image(image_states['normal'])
        self.hover_image = load_image(image_states['hovered'])
        self.click_image = load_image(image_states['clicked'])

        self.text = text
        self.font = pygame.font.Font(font_path, text_size)
        self.text_color = pygame.Color(text_color)

        self.pos = pos

        self.image = self.normal_image

        self.shift_text = shift_text

        self.name = name
        self.func = func

        self.states = {
            'hovered': False,
            'clicked': False,
            'after_click': False
        }

    def update(self, *args):
        if self.states['clicked']:
            #self.states['clicked'] = False
            self.image = self.click_image
            self.states['after_click'] = True
        elif self.states['after_click']:
            if self.states['hovered']:
                self.image = self.click_image
            else:
                self.states['after_click'] = False

        elif self.states['hovered']:
            self.image = self.hover_image

        else:
            self.image = self.normal_image

    def render(self, surface):
        surface.blit(self.image, self.image.get_rect(center=self.pos))
        text = self.font.render(self.text, 4, self.text_color)
        surface.blit(text, text.get_rect(center=(self.pos[0]+self.shift_text[0], self.pos[1]+self.shift_text[1])))

    def apply_event(self, event):
        self.states['hovered'] = self.image.get_rect(center=self.pos).collidepoint(*pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.states['hovered']:
                    self.states['clicked'] = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.states['hovered']:
                    self.states['after_click'] = False
                    self.func()


class ButtonFlag(ButtonImage):
    def apply_event(self, event):
        self.states['hovered'] = self.image.get_rect(center=self.pos).collidepoint(*pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.states['hovered']:
                    self.states['clicked'] = not self.states['clicked']
                    self.func()
                    if self.states['clicked']:
                        return self.name


        #elif event.type == pygame.MOUSEBUTTONUP:
        #    if event.button == 1:
        #        if self.states['hovered']:
        #            self.states['after_click'] = False
        #            self.func()


class Div:
    def __init__(self, *buttons):
        self.elements = [but for but in buttons]

    def update(self):
        for element in self.elements:
            element.update()

    def render(self, surface):
        for element in self.elements:
            element.render(surface)

    def move(self, x, y):
        for element in self.elements:
            element.move(x, y)


class DivButtons(Div):
    def apply_event(self, event):
        for but in self.elements:
            ans = but.apply_event(event)
            if ans:
                for but_ in self.elements:
                    if but_.name != ans:
                        but_.states['clicked'] = False


