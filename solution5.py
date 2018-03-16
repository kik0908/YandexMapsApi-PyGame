# coding:utf-8
import sys
import os
import math

import pygame
from pygame import Color
import requests

from gui import GUI, ButtonFlag, TextBox, DivButtons, Div, ButtonImage
from geocoder import get_coordinates


pygame.init()


satellite = {'normal': 'image/buttons/satellite.png', 'hovered': 'image/buttons/satellite_hovered.png', 'clicked': 'image/buttons/satellite_active.png'}
scheme = {'normal': 'image/buttons/scheme.png', 'hovered': 'image/buttons/scheme_hovered.png', 'clicked': 'image/buttons/scheme_active.png'}
gibrid = {'normal': 'image/buttons/gibrid.png', 'hovered': 'image/buttons/gibrid_hovered.png', 'clicked': 'image/buttons/gibrid_active.png'}
buts = {'normal': 'image/buttons/but.png', 'hovered': 'image/buttons/but_hovered.png', 'clicked': 'image/buttons/but_active.png'}

def update_static(ll, z, map_type, add_params=None):
    if ll:
        map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={map_type}".format(**locals())
    else:
        map_request = "http://static-maps.yandex.ru/1.x/?l={map_type}".format(**locals())

    if add_params:
        map_request += "&" + add_params
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
            return map_file
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)

def chance_viev(_viev):
    global map_type, flag_update_map
    map_type = _viev
    flag_update_map = True

def get_coord(address, text_box_name=None):
    global _lon, _lat

    _address = address

    if text_box_name:
        text_box = GUI.get_object(text_box_name)
        if text_box.text != text_box.default_text:
            _address = text_box.text

    coords = get_coordinates(_address)

    _lon, _lat = coords

def show_map(ll, z, _map_type='map', add_params=None):
    global map_type, flag_update_map
    global _lon, _lat

    flag_update_map = False
    map_type =  _map_type


    pygame.init()
    screen = pygame.display.set_mode((600, 540))
    _z = z
    _lon, _lat = map(float, ll.split(','))

    #GUI.add_element(Button('Карта', (50, 465), (100, 26), lambda: chance_viev('map'), 'test_but', hovered=(180, 180, 180),
    #                       size_font=30))
    #GUI.add_element(Button('Спутник', (50, 495), (100, 26), lambda: chance_viev('sat'), 'test_but', hovered=(180, 180, 180),
    #                       size_font=30))
    #GUI.add_element(Button('Гидрид', (50, 525), (100, 26), lambda: chance_viev('sat,skl'), 'test_but', hovered=(180, 180, 180),
    #                       size_font=30))

    buttons_viev = DivButtons(ButtonFlag((545, 465), buts, func=lambda: chance_viev('map'), text='Схема',
                                         text_size=23,name='but_satellite', shift_text=(-4, 0)),
                              ButtonFlag((545, 495), buts, func=lambda: chance_viev('sat'), text='Спутник',
                                         text_size=23,name='but_scheme', shift_text=(4, 0)),
                              ButtonFlag((545, 525), buts, func=lambda: chance_viev('sat,skl'), text='Гибрид',
                                         text_size=23,name='but_gibrid', shift_text=(3, 0)))
    buttons_viev.elements[0].states['clicked'] = True
    GUI.add_element(buttons_viev)

    search_div = Div(TextBox((40, 5, 400, 26), '', default_text='Введите адрес...', name='tb_address'),
                     ButtonImage((495, 19), buts, 'Поиск', func=lambda: get_coord('', 'tb_address'),name='but_search'))
    GUI.add_element(search_div)

    map_file = update_static(','.join([str(_lon), str(_lat)]), _z, map_type)

    timer = 10
    clock = pygame.time.Clock()

    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.remove(map_file)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_PAGEUP:
                    if _z - 1 >= 2:
                        _z -= 1
                        map_file = update_static(ll, _z, map_type)

                elif event.key == pygame.K_PAGEDOWN:
                    if _z + 1 <= 17:
                        _z += 1
                        map_file = update_static(ll, _z, map_type)

                elif event.key == pygame.K_RIGHT:
                    _lon += 422.4 / (2 ** (_z - 1))
                    map_file = update_static(','.join([str(_lon), str(_lat)]), _z, map_type)

                elif event.key == pygame.K_LEFT:
                    _lon -= 422.4 / (2 ** (_z - 1))
                    map_file = update_static(','.join([str(_lon), str(_lat)]), _z, map_type)

                elif event.key == pygame.K_UP:
                    _lat += 178.25792 / (2 ** (_z - 1))
                    map_file = update_static(','.join([str(_lon), str(_lat)]), _z, map_type)

                elif event.key == pygame.K_DOWN:
                    _lat -= 178.25792 / (2 ** (_z - 1))
                    map_file = update_static(','.join([str(_lon), str(_lat)]), _z, map_type)

            GUI.apply_event(event)


        if flag_update_map:
            map_file = update_static(','.join([str(_lon), str(_lat)]), _z, map_type)
            flag_update_map = False


        clock.tick(60)
        timer -= 1
        if timer == 0:
            timer = 30

        screen.blit(pygame.image.load(map_file), (0, 0))

        GUI.update()
        GUI.render(screen)
        pygame.display.flip()


def main():
    ll = "37.620070,55.756640"
    z = 16
    # ll_z = "ll={coordinates}&z={z}".format(**locals())
    show_map(ll, z, "map")


if __name__ == "__main__":
    main()

