import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math

# Константы
NUM_SNOWBALLS = 50
MAX_SNOWBALLS = 100
WAVE_SPEED = 0.05  # Скорость движения руки
AMPLITUDE = 0.4  # Амплитуда маха
NUM_SPIRALS = 4

def create_snowball():
    return {
        'x': random.uniform(-3.0, -0.6) if random.random() < 0.6 else random.uniform(0.6, 3.0),
        'y': random.uniform(2.0, 5.0),
        'z': random.uniform(-1.0, -0.6) if random.random() < 0.6 else random.uniform(0.6, 2.0),
        'radius': random.uniform(0.025, 0.07),
        'dx': random.uniform(-0.01, 0.01)  # Случайное смещение по оси X
    }

def fall_snowball(snowball):
    snowball['y'] -= 0.02  # Скорость падения
    snowball['x'] += snowball['dx']  # Случайное смещение по оси X

    # Если снежинка коснулась нижнего предела, возвращаем её на место
    if snowball['y'] < -3.1:
        return None  # Остановить снежинку
    return snowball

def draw_sphere(radius, position):
    # Рисуем сферу
    quadric = gluNewQuadric()
    glPushMatrix()
    glTranslatef(*position)
    gluSphere(quadric, radius, 90, 30)
    glPopMatrix()
    gluDeleteQuadric(quadric)

def draw_cone(radius, height, position):
    # Рисуем конус (нос снеговика)
    quadric = gluNewQuadric()
    glPushMatrix()
    glTranslatef(*position)
    glRotatef(-25, 1, 90, 30)  # Поворачиваем конус
    gluCylinder(quadric, radius, 0, height, 30, 30)
    glPopMatrix()
    gluDeleteQuadric(quadric)

def draw_cones(radius, height, position, color):
    # Рисуем елки
    quadric = gluNewQuadric()
    glPushMatrix()
    glTranslatef(*position)
    glRotatef(-90, 1, 0, 0)  # Поворачиваем конус
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, color)
    gluCylinder(quadric, radius, 0, height, 30, 10)
    glPopMatrix()
    gluDeleteQuadric(quadric)


def draw_cylinder(radius, height):
    # Рисуем руки
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricOrientation(quadric, GLU_OUTSIDE)

    # Рисуем цилиндр
    glPushMatrix()
    glRotatef(90, 1, 0, 0)  # Поворачиваем цилиндр, чтобы он стоял вертикально
    gluCylinder(quadric, radius, radius, height, 32, 32)
    glPopMatrix()

def main():
    pygame.init()
    display = (800, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Snowman with Falling Snowballs")
    gluPerspective(70, (display[0] / display[1]), 1.0, 50.0)
    glTranslatef(0.0, 0.0, -5.0)

    # Установка цвета фона (светло-голубой)
    glClearColor(0.20, 0.53, 0.7, 1.0)

    # Настройка освещения
    glLight(GL_LIGHT0, GL_POSITION, (5.0, 5.0, 5.0, 1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.5, 1.5, 1.5, 1.0))

    glEnable(GL_DEPTH_TEST)

    # Создаем начальные снежинки
    snowballs = [create_snowball() for _ in range(NUM_SNOWBALLS)]

    wave_angle = 0  # Угол для анимации махания рукой

    # Переменные для анимации
    animation_time = 0.0  # Время анимации
    animation_speed = 2.0  # Скорость анимации
    amplitude = 0.5  # Амплитуда движения

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        # Обновляем время анимации
        animation_time += 0.01  # Увеличиваем время на небольшой шаг

        # Рисуем елки
        tree_positions = [(i * 3.0 - 4.5, -1.0, -4.0) for i in range(NUM_SPIRALS)]
        for pos in tree_positions:
            # Вычисляем смещение по вертикали с помощью синуса
            vertical_offset = amplitude * math.sin(animation_time * animation_speed)

            # Для создания задержки используем разные временные смещения
            sphere_offset = vertical_offset * 1.5
            cone_offset_1 = vertical_offset * 1.0  # Задержка для первого конуса
            cone_offset_2 = vertical_offset * 0.8  # Задержка для второго конуса
            trunk_offset = vertical_offset * 0.6  # Задержка для ствола

            # Рисуем верхушку елки
            glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (1.0, 0.0, 0.0))  # Цвет звезды
            draw_sphere(0.2, (pos[0], -3.6 + 5.0 + sphere_offset, pos[2]))

            # Рисуем ветки (конусы)
            glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (1.0, 1.0, 0.0))
            center_cone_position = (pos[0], -3.7 + cone_offset_1 + 1.4, pos[2])
            draw_cones(0.9, 2.7, center_cone_position, (0.0, 0.3, 0.0))
            center_cone_position = (pos[0], -3.7 + cone_offset_2 + 2.5, pos[2])
            draw_cones(0.75, 1.8, center_cone_position, (0.0, 0.6, 0.0))
            center_cone_position = (pos[0], -3.7 + vertical_offset + 3.4, pos[2])
            draw_cones(0.5, 1.5, center_cone_position, (0.0, 1.0, 0.0))

            # Рисуем ствол елки (цилиндр)
            glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.54, 0.27, 0.07))  # Коричневый цвет для ствола
            trunk_position = (pos[0], -3.5 + trunk_offset + vertical_offset + 2.0, pos[2])  # Позиция ствола под елкой
            glPushMatrix()
            glTranslatef(trunk_position[0], trunk_position[1], trunk_position[2])
            draw_cylinder(0.3, 1.5)  # Рисуем ствол с радиусом и высотой
            glPopMatrix()

        # Рисуем снеговика
        # Нижний шар
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (1.0, 1.0, 1.0))
        draw_sphere(1.0, (0.0, -1.5, 0.0))

        # Средний шар
        draw_sphere(0.75, (0.0, -0.5, 0.0))

        # Верхний шар (голова)
        draw_sphere(0.5, (0.0, 0.25, 0.0))

        # Нос (конус)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (4.0, 0.5, 0.0))
        draw_cone(0.1, 0.5, (0.0, 0.25, 0.35))

        # Глаза и пуговицы (маленькие коричневые сферы)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.745, 0.271, 0.075))
        draw_sphere(0.05, (0.15, 0.4, 0.45))
        draw_sphere(0.05, (-0.15, 0.4, 0.45))
        draw_sphere(0.08, (0.0, -0.3, 0.8))
        draw_sphere(0.08, (0.0, -1.0, 1))

        # Рисуем палку (руку снеговика) с фиксированным концом и махающим концом
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.6, 0.3, 0.1))  # Коричневый цвет для палки

        # Положение неподвижного конца палки (крепление к снеговику)
        fixed_hand_position = (-0.9, -0.5, -1.7)
        # Устанавливаем толщину линии
        cylinder_radius = 0.05  # Радиус цилиндра

        # Вычисляем положение махающего конца палки
        swinging_hand_position = (
            fixed_hand_position[2],
            fixed_hand_position[1] + 0.5 + math.sin(wave_angle) * AMPLITUDE,
            fixed_hand_position[0]
        )

        # Рисуем палку от неподвижного конца до махающего конца
        glPushMatrix()
        glTranslatef(fixed_hand_position[0], fixed_hand_position[1], fixed_hand_position[2])
        glRotatef(-math.degrees(math.atan2(swinging_hand_position[1] - fixed_hand_position[1],
                                          swinging_hand_position[0] + fixed_hand_position[0])), 0, 0, 1)
        draw_cylinder(cylinder_radius, math.sqrt((swinging_hand_position[0] - 1.5 - fixed_hand_position[0]) ** 2 +
                                                 (swinging_hand_position[1] + fixed_hand_position[1]) ** 2))
        glPopMatrix()

        # Обновляем угол волны
        wave_angle += WAVE_SPEED
        if wave_angle > math.pi * 2:
            wave_angle -= math.pi * 2

        # Задаем фиксированное положение для второй палки
        horizontal_fixed_hand_position = (1, -0.72, -1.7)

        # Определяем наклон для второй палки
        angle_of_inclination = math.radians(60)
        length_of_hand = 1.75  # Длина второй палки

        # Рисуем вторую палку
        glPushMatrix()
        glTranslatef(horizontal_fixed_hand_position[0], horizontal_fixed_hand_position[1],
                     horizontal_fixed_hand_position[2])
        glRotatef(math.degrees(angle_of_inclination), 0, 0, 1)  # Поворачиваем на угол наклона
        draw_cylinder(cylinder_radius, length_of_hand)
        glPopMatrix()

        # Рисуем падающие снежинки
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (1.0, 1.0, 1.0))

        for i in range(len(snowballs)):
            if snowballs[i] is not None:
                draw_sphere(snowballs[i]['radius'], (snowballs[i]['x'], snowballs[i]['y'], snowballs[i]['z']))
                snowballs[i] = fall_snowball(snowballs[i])

                if snowballs[i] is None:
                    snowballs[i] = create_snowball()

                    if len(snowballs) < MAX_SNOWBALLS and snowballs[i] is None:
                        snowballs.append(create_snowball())

        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHTING)

        pygame.display.flip()
        pygame.time.wait(10)


main()