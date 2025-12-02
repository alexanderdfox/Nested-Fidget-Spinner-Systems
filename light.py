#!/usr/bin/env python3
"""
Nested Fidget Spinner Systems with Maxwell's Demon
Each isolated system has a Demon that sorts particles by energy
"""

import pygame
import math
import random

# ------------------------------
# Constants
# ------------------------------
WIDTH, HEIGHT = 1200, 800
CENTER = (WIDTH // 2, HEIGHT // 2)
FPS = 60

BG_COLOR = (11, 16, 32)
SYSTEM_COLORS = [(255, 107, 107), (255, 217, 61), (107, 227, 107)]
TEXT_COLOR = (230, 238, 248)
PANEL_BG = (20, 30, 45)

LOBE_RADIUS = 110
ARM_LENGTH = 170

# ------------------------------
# Deterministic Random Seed
# ------------------------------
random.seed(42)

# ------------------------------
# Particle Class
# ------------------------------
class Particle:
    def __init__(self, x, y, vx, vy, radius):
        self.x, self.y = x, y
        self.vx, self.vy = vy, vy
        self.radius = radius

    def speed(self):
        return math.hypot(self.vx, self.vy)

    def kinetic_energy(self):
        return 0.5 * (self.vx ** 2 + self.vy ** 2)

    def update(self, center, lobe_radius, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Bounce inside lobe
        dx = self.x - center[0]
        dy = self.y - center[1]
        dist = math.hypot(dx, dy)
        if dist + self.radius > lobe_radius:
            nx, ny = dx / dist, dy / dist
            vdotn = self.vx * nx + self.vy * ny
            self.vx -= 2 * vdotn * nx
            self.vy -= 2 * vdotn * ny
            self.x = center[0] + nx * (lobe_radius - self.radius)
            self.y = center[1] + ny * (lobe_radius - self.radius)

        # Small random fluctuation
        self.vx += (random.random() - 0.5) * 0.01
        self.vy += (random.random() - 0.5) * 0.01

# ------------------------------
# Spinner Node
# ------------------------------
class SpinnerNode:
    def __init__(self, level, center, arm_length, lobe_radius, max_level):
        self.level = level
        self.center = center
        self.arm_length = arm_length
        self.lobe_radius = lobe_radius
        self.theta = 0
        self.particles = [[] for _ in range(3)]
        self.children = [[] for _ in range(3)] if level < max_level else None
        self.max_level = max_level

        if self.children:
            for i in range(3):
                lobe_center = self.get_lobe_center(i)
                for j in range(3):
                    child = SpinnerNode(level + 1,
                                        lobe_center,
                                        arm_length * 0.4,
                                        lobe_radius * 0.4,
                                        max_level)
                    self.children[i].append(child)

        self.init_particles()

    def get_lobe_center(self, idx):
        angle = idx * 2 * math.pi / 3 + self.theta
        return (self.center[0] + math.cos(angle) * self.arm_length,
                self.center[1] + math.sin(angle) * self.arm_length)

    def init_particles(self, num_particles=10):
        for lobe_idx in range(3):
            lc = self.get_lobe_center(lobe_idx)
            self.particles[lobe_idx] = []
            for _ in range(num_particles):
                angle = random.random() * 2 * math.pi
                speed = random.random() * 0.3
                r = 2 + random.random() * 2
                x = lc[0] + math.cos(angle) * (self.lobe_radius - r)
                y = lc[1] + math.sin(angle) * (self.lobe_radius - r)
                self.particles[lobe_idx].append(Particle(x, y, math.cos(angle) * speed, math.sin(angle) * speed, r))

    # --- Maxwell's Demon function ---
    def maxwells_demon(self):
        for lobe_idx, lc in enumerate([self.get_lobe_center(i) for i in range(3)]):
            for p in self.particles[lobe_idx]:
                dx = p.x - lc[0]
                # Sort particles: positive x for high energy, negative x for low energy
                if p.kinetic_energy() > 0.05:
                    p.x = lc[0] + abs(dx)  # move to “hot” side
                else:
                    p.x = lc[0] - abs(dx)  # move to “cold” side

        if self.children:
            for lobe_idx, child_list in enumerate(self.children):
                for child in child_list:
                    child.maxwells_demon()

    def update(self, dt):
        self.theta += dt * (1 + self.level * 0.3)
        for lobe_idx, lc in enumerate([self.get_lobe_center(i) for i in range(3)]):
            for p in self.particles[lobe_idx]:
                p.update(lc, self.lobe_radius, dt)
        if self.children:
            for lobe_idx, child_list in enumerate(self.children):
                lc = self.get_lobe_center(lobe_idx)
                for child in child_list:
                    child.center = lc
                    child.update(dt)

        # Apply Maxwell's Demon sorting
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
            pygame.draw.line(screen, (200, 200, 200), self.center, lc, 2)
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
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Nested Spinners - Maxwell's Demon")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)

    spinners = [SpinnerNode(0, CENTER, ARM_LENGTH, LOBE_RADIUS, 2) for _ in range(3)]

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
        panel_rect = pygame.Rect(10, 10, 280, 100)
        pygame.draw.rect(screen, PANEL_BG, panel_rect)
        total_particles = sum(sp.total_particles() for sp in spinners)
        total_energy = sum(sp.total_energy() for sp in spinners)
        texts = [
            f"Total Particles: {total_particles}",
            f"Total Energy: {total_energy:.2f}"
        ]
        for i, t in enumerate(texts):
            surf = font.render(t, True, TEXT_COLOR)
            screen.blit(surf, (20, 15 + i * 25))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
