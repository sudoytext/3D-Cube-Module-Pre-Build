import pygame
import numpy as np
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D RGB Cube")

CUBE_SIZE = 200
FPS = 60  # 90FPS is also good fot it trust me

COLOR_CHANGE_INTERVAL = 1  # in seconds

vertices = np.array([
    [-CUBE_SIZE, -CUBE_SIZE, -CUBE_SIZE],
    [CUBE_SIZE, -CUBE_SIZE, -CUBE_SIZE],
    [CUBE_SIZE, CUBE_SIZE, -CUBE_SIZE],
    [-CUBE_SIZE, CUBE_SIZE, -CUBE_SIZE],
    [-CUBE_SIZE, -CUBE_SIZE, CUBE_SIZE],
    [CUBE_SIZE, -CUBE_SIZE, CUBE_SIZE],
    [CUBE_SIZE, CUBE_SIZE, CUBE_SIZE],
    [-CUBE_SIZE, CUBE_SIZE, CUBE_SIZE]
])

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]


# Rotation matrices
def rotate_x(angle):
    return np.array([
        [1, 0, 0],
        [0, np.cos(angle), -np.sin(angle)],
        [0, np.sin(angle), np.cos(angle)]
    ])


def rotate_y(angle):
    return np.array([
        [np.cos(angle), 0, np.sin(angle)],
        [0, 1, 0],
        [-np.sin(angle), 0, np.cos(angle)]
    ])


def rotate_z(angle):
    return np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])

def project(vertex, width, height):
    epsilon = 0.0001
    factor = width / (vertex[2] + CUBE_SIZE + epsilon)

    x = int(vertex[0] * factor + width / 2)
    y = int(-vertex[1] * factor + height / 2)

    return x, y

def get_rgb_color(t):
    r = int((np.sin(t * np.pi * 2 / COLOR_CHANGE_INTERVAL) + 1) / 2 * 255)
    g = int((np.cos(t * np.pi * 2 / COLOR_CHANGE_INTERVAL) + 1) / 2 * 255)
    b = int((np.sin(t * np.pi * 2 / COLOR_CHANGE_INTERVAL + np.pi / 2) + 1) / 2 * 255)
    return (r, g, b)

def main():
    clock = pygame.time.Clock()
    angle_x, angle_y, angle_z = 0, 0, 0
    last_color_change_time = time.time()

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        current_time = time.time()
        elapsed_time = current_time - last_color_change_time

        if elapsed_time >= COLOR_CHANGE_INTERVAL:
            last_color_change_time = current_time

        color = get_rgb_color(elapsed_time)

        # Rotate cube vertices
        rotated_vertices = vertices.copy()
        rotated_vertices = np.dot(rotated_vertices, rotate_x(angle_x))
        rotated_vertices = np.dot(rotated_vertices, rotate_y(angle_y))
        rotated_vertices = np.dot(rotated_vertices, rotate_z(angle_z))

        projected_vertices = [project(vertex, WIDTH, HEIGHT) for vertex in rotated_vertices]

        for edge in edges:
            pygame.draw.line(screen, color, projected_vertices[edge[0]], projected_vertices[edge[1]], 2)

        pygame.display.flip()

        angle_x += 0.02
        angle_y += 0.02
        angle_z += 0.02

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
