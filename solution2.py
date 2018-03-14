# coding:utf-8
import pygame
import requests
import sys
import os


def update_static(ll, z, map_type="map", add_params=None):
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


def show_map(ll, z, map_type='map', add_params=None):
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    _z = z

    clock = pygame.time.Clock()
    while True:
        screen.fill((0, 0, 0))
        map_file = update_static(ll, _z, map_type)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.remove(map_file)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    if _z - 1 >= 2:
                        _z -= 1
                elif event.key == pygame.K_PAGEDOWN:
                    if _z + 1 <= 17:
                        _z += 1
        clock.tick(60)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()


def main():
    ll = "37.588392,55.734036"
    z = 13
    # ll_z = "ll={coordinates}&z={z}".format(**locals())
    show_map(ll, z, "map")


if __name__ == "__main__":
    main()
