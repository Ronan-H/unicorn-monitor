import unicornhathd
import socket

HOST = '192.168.0.28'
PORT = 41624

unicornhathd.brightness(0.3)
unicornhathd.rotation(270)
unicornhathd.clear()


def draw_usage_bar(x_start, y_start, w, h, r, g, b):
    for y in range(y_start, y_start - h, -1):
        for x in range(x_start, x_start + w):
            unicornhathd.set_pixel(15 - x, y, r, g, b)


def draw_bar_with_background(x_start, y_start, w, h, max_h, r, g, b, background_opacity=0.05):
    br, bg, bb = (x * background_opacity for x in (r, g, b))
    draw_usage_bar(x_start, y_start, w, max_h, br, bg, bb)
    draw_usage_bar(x_start, y_start, w, h, r, g, b)


def byte_to_height(b, max_height):
    return round(b / 255 * max_height)


def draw_usages(usages):
    # draw cpu usage
    num_cpus = 12
    max_bar_height = 4
    num_cols = 3
    for i in range(num_cpus):
        height = byte_to_height(usages[i], max_bar_height)
        x = i % num_cols
        y = 15 - ((i // num_cols) * max_bar_height)
        backround_opacity = 0.05 if i % 2 == 0 else 0.025
        draw_bar_with_background(x, y, 1, height, max_bar_height, 255, 0, 0, backround_opacity)

    max_bar_height = 16
    # draw memory usage (RAM)
    height = byte_to_height(usages[12], max_bar_height)
    draw_bar_with_background(3, 15, 4, height, max_bar_height, 0, 255, 0)

    # draw gpu usage
    height = byte_to_height(usages[13], max_bar_height)
    draw_bar_with_background(7, 15, 3, height, max_bar_height, 0, 0, 255)

    # draw gpu memory usage
    height = byte_to_height(usages[14], max_bar_height)
    draw_bar_with_background(10, 15, 3, height, max_bar_height, 0, 255, 255)

    # draw main disk usage
    height = byte_to_height(usages[15], max_bar_height)
    draw_bar_with_background(13, 15, 3, height, max_bar_height, 255, 0, 255)


def serve_next_client():
    print('Waiting for a client to connect...')
    conn, addr = s.accept()
    with conn:
        print('Client connected with address: ', addr)
        while True:
            usages = conn.recv(16)
            if not usages:
                return
            unicornhathd.clear()
            draw_usages(usages)
            unicornhathd.show()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        serve_next_client()
        unicornhathd.clear()
        unicornhathd.show()
