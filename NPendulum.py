from numpy import sin, cos
import numpy as np
from scipy import integrate
import random

class NPendulum:
	def __init__(self, N, init_state=None, l=None, m=None, g=9.8):
		if not init_state: init_state = np.concatenate([np.array([random.randrange(-180, 180) for _ in range(N)], dtype='float'), np.zeros(N)])
		else: init_state = np.array(init_state, dtype='float')
		if not l: l = [0.5] * N
		if not m: m = [1] * N
		self.N = N
		self.params = (l, m, g)
		self.time_elapsed = 0
		self.state = init_state * np.pi / 180

	def calcPosition(self):
		(l, m, g) = self.params

		x = np.empty(self.N)
		y = np.empty(self.N)
		x[0], y[0] = l[0] *  sin(self.state[0]), l[0] * -cos(self.state[0])
		for q in range(1, self.N):
			x[q] = x[q - 1] + l[q] *  sin(self.state[q])
			y[q] = y[q - 1] + l[q] * -cos(self.state[q])

		return (x, y)

	def calcEnergy(self):
		(l, m, g) = self.params
		state = self.state

		T, V = 0, 0
		for q in range(self.N):
			t, v = 0, 0
			for j in range(q + 1):
				for i in range(q + 1):
					t += l[i] * l[j] * state[self.N + i] * state[self.N + j] * cos(state[i] - state[j])
				v += l[j] * cos(state[j])
			T += t * m[q]
			V += v * m[q]
		T *= 0.5
		V *= -g

		return abs(T + V)

	def dstate_dt(self, state, t):
		(l, m, g) = self.params
		N = self.N

		# A = np.zeros([N, N])
		# B = np.zeros([N, 1])

		# for q in range(N): 
		# 	for j in range(q, N): 
		# 		for i in range(j + 1): 
		# 			A[q][i] += m[j] * l[i] * cos(state[i] - state[q])
		# 			B[q][0] += m[j] * l[i] * state[N + i] ** 2 * sin(state[i] - state[q])
		# 		B[q][0] -= m[j] * g * sin(state[q])
		# solution = np.linalg.solve(A, B)

		A = np.zeros([N, N])
		B = np.zeros([N, N])

		for i in range(N): 
			for j in range(N): 
				for k in range(max(i,j), N): 
					A[i][j] += m[k]
					B[i][j] += m[k]
				if i == j:
					A[i][j] *= l[j]
					B[i][j] *= g * sin(state[i])
				else:
					A[i][j] *= l[j]*cos(state[i] - state[j])
					B[i][j] *= l[j] * state[N + j]**2 * sin(state[i] - state[j])
		
		E = np.zeros([N, 1])
		for u in range(N):
			E[u][0] += -1

		solution = (np.linalg.inv(A).dot(B)).dot(E)

		dydx = np.zeros_like(state)
		for q in range(N):
			dydx[q] = state[N + q]
			dydx[N + q] = solution[q, 0]
		
		return dydx

	def step(self, dt):
		# for q in range(N):
		# 	self.state[N + q] += self.dstate_dt(state)[N + q] * dt
		# 	self.state[q] += self.state[N + q] * dt
		self.state = integrate.odeint(self.dstate_dt, self.state, [0, dt])[1]
		self.time_elapsed += dt
