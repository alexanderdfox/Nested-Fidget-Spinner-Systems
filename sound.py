#!/usr/bin/env python3
"""
Maxwell's Demon - Stereo Audio Simulation (Fixed)
Each particle in each lobe produces its own tone based on kinetic energy.
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
NUM_LOBES = 3
PARTICLES_PER_LOBE = 6
BASE_FREQUENCIES = [220, 330, 440]  # Hz for each lobe
SAMPLE_RATE = 44100
DURATION = 0.05  # seconds per sound chunk

# ------------------------------
# Particle Class
# ------------------------------
class Particle:
	def __init__(self):
		self.vx = (random.random() - 0.5) * 0.5
		self.vy = (random.random() - 0.5) * 0.5

	def kinetic_energy(self):
		return 0.5 * (self.vx ** 2 + self.vy ** 2)

	def update(self):
		# Small random motion
		self.vx += (random.random() - 0.5) * 0.02
		self.vy += (random.random() - 0.5) * 0.02

# ------------------------------
# Lobe Class
# ------------------------------
class Lobe:
	def __init__(self, base_freq, pan=0.5):
		self.particles = [Particle() for _ in range(PARTICLES_PER_LOBE)]
		self.base_freq = base_freq
		self.pan = pan  # stereo position: 0.0=left, 1.0=right

	def update(self):
		for p in self.particles:
			p.update()
		# Maxwell's Demon: sort particles by energy
		avg_energy = sum(p.kinetic_energy() for p in self.particles) / PARTICLES_PER_LOBE
		for p in self.particles:
			if p.kinetic_energy() > avg_energy:
				p.vx += 0.01
			else:
				p.vx -= 0.01

# ------------------------------
# Tone Generation (Stereo)
# ------------------------------
def generate_tone(frequency, volume=0.5, duration=DURATION, pan=0.5):
	n_samples = int(SAMPLE_RATE * duration)
	t = np.linspace(0, duration, n_samples, False)
	waveform = np.sin(2 * np.pi * frequency * t) * volume

	# Stereo: pan left/right
	left = waveform * (1.0 - pan)
	right = waveform * pan
	stereo_waveform = np.column_stack((left, right))

	# Convert to int16
	stereo_waveform_int16 = np.int16(stereo_waveform * 32767)

	return pygame.sndarray.make_sound(stereo_waveform_int16)

# ------------------------------
# Main Simulation
# ------------------------------
def main():
	lobes = [
		Lobe(BASE_FREQUENCIES[0], pan=0.1),
		Lobe(BASE_FREQUENCIES[1], pan=0.5),
		Lobe(BASE_FREQUENCIES[2], pan=0.9),
	]

	clock = pygame.time.Clock()
	running = True

	while running:
		clock.tick(30)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		# Update lobes
		for lobe in lobes:
			lobe.update()

		# Play particle sounds
		for lobe in lobes:
			for p in lobe.particles:
				freq = lobe.base_freq + p.kinetic_energy() * 300
				vol = min(1.0, p.kinetic_energy() * 8)
				tone = generate_tone(freq, volume=vol, pan=lobe.pan)
				tone.play()

if __name__ == "__main__":
	main()
