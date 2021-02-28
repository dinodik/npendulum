import pygame, sys, random
import numpy as np
from pygame.locals import *
from collections import deque
from NPendulum import NPendulum

pygame.init()

font = pygame.font.Font(None, 20)

fps = 30
max_dt = 1 / fps
clock = pygame.time.Clock()

width, height = 400, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("N-Pendulum")

bob_radius = 10
origin = np.array((width / 2, height / 2))
pendulum = NPendulum(N=5, l=[0.4] * 5)
lastTime = pygame.time.get_ticks()

x, y = pendulum.calcPosition()
tracer = deque([[x[-1] * 100 + origin[0], y[-1] * 100 + origin[1]]])

while True:
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			pygame.quit()
			sys.exit()

	currentTime = pygame.time.get_ticks()
	dt = (currentTime - lastTime) / 1000
	lastTime = currentTime

	screen.fill((153, 255, 153))

	pendulum.step(min(1 / dt, max_dt))

	texts = ["Time elapsed: %.1fs", "Energy: %.3fJ", "FPS: %.1f (%s)"]
	values = [pendulum.time_elapsed, pendulum.calcEnergy(), (1 / dt, fps)]
	for i in range(len(texts)):
		text = font.render(texts[i] % values[i], True, (0, 0, 0))
		screen.blit(text, (15, 15 + i * 15))

	x, y = pendulum.calcPosition()
	x =  x * 100 + origin[0]
	y = -y * 100 + origin[1]

	if len(tracer) < 200:
		tracer.append([x[-1], y[-1]])
	else:
		tracer.rotate(-1)
		tracer[-1] = [x[-1], y[-1]]
	pygame.draw.aalines(screen, (255, 102, 102), False, tracer)

	pygame.draw.line(screen, (253, 185, 200), origin, [x[0], y[0]])
	for q in range(pendulum.N - 1):
		pygame.draw.line(screen, (253, 185, 200), [x[q], y[q]], [x[q + 1], y[q + 1]])
		pygame.draw.circle(screen, (253, 185, 200), [x[q], y[q]], bob_radius)
	pygame.draw.circle(screen, (253, 185, 200), [x[-1], y[-1]], bob_radius)

	pygame.display.update()
	clock.tick(fps)
