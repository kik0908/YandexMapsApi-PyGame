# coding:utf-8
import pygame
import requests
import sys
import os


def show_map(ll_spn=None, map_type="map", add_params=None):
    if ll_spn:
        map_request = "http://static-maps.yandex.ru/1.x/?{ll_spn}&l={map_type}".format(**locals())
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


def _show_map(ll_spn=None, map_type="map", add_params=None):
    pygame.init()
    screen = pygame.display.set_mode((600, 450))

    ll = ll_spn

    z = 'z=17'
    scale_x, scale_y = 0.0019, 0.001

    flag_new_foto = True

    clock = pygame.time.Clock()
    while True:
        screen.fill((0, 0, 0))
        if flag_new_foto:
            map_file = show_map('ll=' + ll, map_type, z)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.remove(map_file)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    dol, shir = list(map(float, ll.split(',')))
                    dol = float(dol) + scale_x
                    ll = '{},{}'.format(dol, shir)
                elif event.key == pygame.K_LEFT:
                    dol, shir = list(map(float, ll.split(',')))
                    dol = float(dol) - scale_x
                    ll = '{},{}'.format(dol, shir)
                elif event.key == pygame.K_UP:
                    dol, shir = list(map(float, ll.split(',')))
                    shir = float(shir) + scale_y
                    ll = '{},{}'.format(dol, shir)
                elif event.key == pygame.K_DOWN:
                    dol, shir = list(map(float, ll.split(',')))
                    shir = float(shir) - scale_y
                    ll = '{},{}'.format(dol, shir)



        clock.tick(60)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    _show_map(ll_spn='46.011582,51.550745')
