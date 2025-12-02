#!/usr/bin/env python3
"""
Nested Fidget Spinner + Maxwell's Demon + Stereo Audio
Particles move in lobes, visualized and produce tones based on kinetic energy
"""

import pygame
import math
import random
import numpy as np

# ------------------------------
# Initialization
# ------------------------------
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# ------------------------------
# Constants
# ------------------------------
WIDTH, HEIGHT = 1200, 800
CENTER = (WIDTH//2, HEIGHT//2)
FPS = 60

NUM_SPINNERS = 3
LOBE_RADIUS = 110
ARM_LENGTH = 170
PARTICLES_PER_LOBE = 6
MAX_LEVEL = 2

SYSTEM_COLORS = [(255,107,107),(255,217,61),(107,227,107)]
BG_COLOR = (11,16,32)
PANEL_BG = (20,30,45)
TEXT_COLOR = (230,238,248)

BASE_FREQUENCIES = [220, 330, 440]  # Hz
SAMPLE_RATE = 44100
DURATION = 0.05  # seconds

# ------------------------------
# Audio Tone Function
# ------------------------------
def generate_tone(frequency, volume=0.5, pan=0.5):
	n_samples = int(SAMPLE_RATE * DURATION)
	t = np.linspace(0, DURATION, n_samples, False)
	waveform = np.sin(2*np.pi*frequency*t) * volume
	left = waveform * (1.0 - pan)
	right = waveform * pan
	stereo_waveform = np.column_stack((left, right))
	stereo_waveform_int16 = np.int16(stereo_waveform * 32767)
	return pygame.sndarray.make_sound(stereo_waveform_int16)

# ------------------------------
# Particle Class
# ------------------------------
class Particle:
	def __init__(self, x, y, vx, vy, radius):
		self.x, self.y = x, y
		self.vx, self.vy = vx, vy
		self.radius = radius

	def kinetic_energy(self):
		return 0.5*(self.vx**2 + self.vy**2)

	def update(self, center, lobe_radius, dt):
		self.x += self.vx*dt
		self.y += self.vy*dt
		dx = self.x - center[0]
		dy = self.y - center[1]
		dist = math.hypot(dx, dy)
		if dist + self.radius > lobe_radius:
			nx, ny = dx/dist, dy/dist
			dot = self.vx*nx + self.vy*ny
			self.vx -= 2*dot*nx
			self.vy -= 2*dot*ny
			self.x = center[0] + nx*(lobe_radius - self.radius)
			self.y = center[1] + ny*(lobe_radius - self.radius)
		# Random fluctuation
		self.vx += (random.random()-0.5)*0.01
		self.vy += (random.random()-0.5)*0.01

# ------------------------------
# Spinner Node
# ------------------------------
class SpinnerNode:
	def __init__(self, level, center, arm_length, lobe_radius, max_level):
		self.level = level
		self.center = list(center)
		self.arm_length = arm_length
		self.lobe_radius = lobe_radius
		self.theta = 0
		self.particles = [[] for _ in range(3)]
		self.children = [[] for _ in range(3)] if level < max_level else None
		self.max_level = max_level
		if self.children:
			for i in range(3):
				lc = self.get_lobe_center(i)
				for j in range(3):
					self.children[i].append(SpinnerNode(level+1, lc, arm_length*0.4, lobe_radius*0.4, max_level))
		self.init_particles()

	def get_lobe_center(self, idx):
		angle = idx*2*math.pi/3 + self.theta
		return [self.center[0]+math.cos(angle)*self.arm_length,
				self.center[1]+math.sin(angle)*self.arm_length]

	def init_particles(self, num_particles=PARTICLES_PER_LOBE):
		for lobe_idx in range(3):
			lc = self.get_lobe_center(lobe_idx)
			self.particles[lobe_idx] = []
			for _ in range(num_particles):
				angle = random.random()*2*math.pi
				speed = random.random()*0.3
				r = 2 + random.random()*2
				x = lc[0] + math.cos(angle)*(self.lobe_radius - r)
				y = lc[1] + math.sin(angle)*(self.lobe_radius - r)
				self.particles[lobe_idx].append(Particle(x, y, math.cos(angle)*speed, math.sin(angle)*speed, r))

	def maxwells_demon(self):
		for lobe_idx, lc in enumerate([self.get_lobe_center(i) for i in range(3)]):
			for p in self.particles[lobe_idx]:
				dx = p.x - lc[0]
				if p.kinetic_energy() > 0.05: p.x = lc[0] + abs(dx)
				else: p.x = lc[0] - abs(dx)
		if self.children:
			for child_list in self.children:
				for child in child_list:
					child.maxwells_demon()

	def update(self, dt):
		self.theta += dt*(1 + self.level*0.3)
		for lobe_idx, lc in enumerate([self.get_lobe_center(i) for i in range(3)]):
			for p in self.particles[lobe_idx]:
				p.update(lc, self.lobe_radius, dt)
				# Play tone based on KE
				freq = BASE_FREQUENCIES[lobe_idx] + p.kinetic_energy()*300
				vol = min(1.0, p.kinetic_energy()*8)
				tone = generate_tone(freq, vol, pan=lobe_idx/2)
				tone.play()
		if self.children:
			for lobe_idx, child_list in enumerate(self.children):
				lc = self.get_lobe_center(lobe_idx)
				for child in child_list:
					child.center = lc
					child.update(dt)
		self.maxwells_demon()

	def total_energy(self):
		energy = sum(p.kinetic_energy() for arr in self.particles for p in arr)
		if self.children:
			for child_list in self.children:
				for child in child_list:
					energy += child.total_energy()
		return energy

	def total_particles(self):
		count = sum(len(arr) for arr in self.particles)
		if self.children:
			for child_list in self.children:
				for child in child_list:
					count += child.total_particles()
		return count

	def render(self, screen):
		for i in range(3):
			lc = self.get_lobe_center(i)
			pygame.draw.line(screen, (200,200,200), self.center, lc, 2)
			pygame.draw.circle(screen, SYSTEM_COLORS[i], (int(lc[0]), int(lc[1])), int(self.lobe_radius), 1)
			for p in self.particles[i]:
				pygame.draw.circle(screen, SYSTEM_COLORS[i], (int(p.x), int(p.y)), int(p.radius))
		if self.children:
			for child_list in self.children:
				for child in child_list:
					child.render(screen)

# ------------------------------
# Main Loop
# ------------------------------
def main():
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Nested Spinners - Maxwell's Demon + Audio")
	clock = pygame.time.Clock()
	font = pygame.font.SysFont("Arial", 18)

	spinners = [SpinnerNode(0, CENTER, ARM_LENGTH, LOBE_RADIUS, MAX_LEVEL) for _ in range(NUM_SPINNERS)]

	running = True
	while running:
		dt = clock.tick(FPS) / 1.0
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		for spinner in spinners:
			spinner.update(dt)

		screen.fill(BG_COLOR)
		for spinner in spinners:
			spinner.render(screen)

		# Panel
		total_particles = sum(sp.total_particles() for sp in spinners)
		total_energy = sum(sp.total_energy() for sp in spinners)
		pygame.draw.rect(screen, PANEL_BG, (10,10,280,60))
		screen.blit(font.render(f"Total Particles: {total_particles}", True, TEXT_COLOR), (20,15))
		screen.blit(font.render(f"Total Energy: {total_energy:.2f}", True, TEXT_COLOR), (20,40))

		pygame.display.flip()

	pygame.quit()

if __name__ == "__main__":
	main()
