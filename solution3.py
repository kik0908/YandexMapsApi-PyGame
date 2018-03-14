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
            print('Ok file')
            file.write(response.content)
            return map_file
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)


def _show_map(ll_spn=None, map_type="map", add_params=None):
    pygame.init()
    screen = pygame.display.set_mode((600, 450))

    ll = ll_spn

    clock = pygame.time.Clock()
    while True:
        screen.fill((0, 0, 0))
        map_file = show_map('ll=' + ll, map_type, add_params)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.remove(map_file)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    print('r')
                elif event.key == pygame.K_LEFT:
                    print('l')
                elif event.key == pygame.K_UP:
                    print('u')
                elif event.key == pygame.K_DOWN:
                    print('d')

        clock.tick(60)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    _show_map(ll_spn='46.011582,51.550745', )
