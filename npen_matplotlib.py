import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from NPendulum import NPendulum

N = 5
def init_state(angle, angle_dot):
	global N
	init_state_1 = []
	init_state_2 = []
	for i in range(N):
		init_state_1.append(angle)
	for j in range(N):
		init_state_2.append(angle_dot)
	init_state_F = np.concatenate([init_state_1, init_state_2])
	return init_state_F

pendulum = NPendulum(N=N, l=[0.4] * N)
dt = 1/24

limits = 0.4 * N + 1
fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, frameon=False, xlim=(-limits, limits), ylim=(-limits, limits))
ax.grid()

line, = ax.plot([], [], 'o-', lw=2, markersize=40/N)

Writer = animation.writers['ffmpeg']
writer = Writer(fps=24, metadata=dict(artist='Me'), bitrate=1800)

def init():
	line.set_data([], [])
	return line

def animate(i):
 	global pendulum, dt
 	pendulum.step(dt)
 	pos = pendulum.calcPosition()
 	pos = np.insert(pos, 0, [0, 0], axis=1)
 	line.set_data(*pos)
 	return line

interval = 1000 * dt
ani = animation.FuncAnimation(fig, animate, interval=interval, init_func=init)

#ani.save(f'renders/{N}-pendulum.mp4', writer=writer)

print("Done")

plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
plt.show()

