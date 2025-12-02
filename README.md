# Maxwell's Demon - Nested Fidget Spinner Systems

This project contains interactive simulations of Maxwell's Demon using nested fidget spinner systems. The demon sorts particles by kinetic energy, creating a visual and auditory representation of thermodynamic sorting.

## Project Structure

The project contains both Python (Pygame) and HTML/JavaScript implementations, each with three variants:

### Python Files (Pygame-based)
- `isolated.py` - Full-featured version with visualization and audio
- `light.py` - Visualization-only version (no audio)
- `sound.py` - Audio-focused version (minimal visualization)

### HTML Files (Browser-based)
- `isolated.html` - Full-featured version with visualization and audio
- `light.html` - Visualization-only version (no audio)
- `sound.html` - Audio-focused version (minimal visualization)

---

## File Descriptions

### `isolated.py` & `isolated.html`
**Full-featured implementation with nested spinners, Maxwell's Demon, and stereo audio**

**Features:**
- **Nested Spinner Systems**: Three independent fidget spinner systems, each with 3 levels of nesting
- **Particle Physics**: Particles move within circular lobes, bouncing off boundaries with realistic collision physics
- **Maxwell's Demon**: Automatically sorts particles by kinetic energy - high-energy particles move to one side, low-energy to the other
- **Stereo Audio**: Each particle generates tones based on its kinetic energy:
  - Base frequencies: 220Hz, 330Hz, 440Hz (one per lobe)
  - Frequency varies with particle energy
  - Stereo panning creates spatial audio effects
- **Visualization**: Real-time rendering of nested spinner arms, lobes, and particles
- **Info Panel**: Displays total particle count and system energy

**How to Run:**
- **Python**: `python3 isolated.py` (requires pygame and numpy)
- **HTML**: Open `isolated.html` in a web browser

**Key Components:**
- `SpinnerNode` class: Recursive structure for nested spinners
- `Particle` class: Physics simulation with velocity, position, and energy
- `maxwells_demon()`: Energy-based particle sorting algorithm
- Audio tone generation with stereo panning

---

### `light.py` & `light.html`
**Visualization-only version (no audio)**

**Features:**
- **Nested Spinner Systems**: Same nested structure as `isolated` versions
- **Particle Physics**: Identical physics simulation with bouncing and random fluctuations
- **Maxwell's Demon**: Same energy sorting mechanism
- **Deterministic Random Seed**: Uses seed=42 for reproducible particle initialization
- **Visualization**: Full visual rendering of the spinner systems
- **Info Panel**: Shows total particles and energy statistics

**Differences from `isolated`:**
- No audio generation
- More particles per lobe (10 vs 6)
- Focuses purely on visual representation

**How to Run:**
- **Python**: `python3 light.py` (requires pygame)
- **HTML**: Open `light.html` in a web browser

**Use Case:** Best for environments where audio is not needed or desired, or for studying the visual aspects of the Maxwell's Demon effect.

---

### `sound.py` & `sound.html`
**Audio-focused version with minimal visualization**

**Features:**
- **Three Lobe System**: Simplified structure with 3 independent lobes (no nesting)
- **Particle-Based Audio**: Each particle generates tones based on kinetic energy
- **Stereo Panning**: Each lobe has a different stereo position (left, center, right)
- **Maxwell's Demon**: Sorts particles by energy within each lobe
- **Minimal Visualization**: Simple bar chart representation of particle energies
- **Base Frequencies**: 220Hz, 330Hz, 440Hz for the three lobes

**Differences from `isolated`:**
- No nested spinner structure
- Simplified visualization (bar charts instead of circular lobes)
- Focus on audio generation and energy distribution
- Each lobe operates independently

**How to Run:**
- **Python**: `python3 sound.py` (requires pygame and numpy)
- **HTML**: Open `sound.html` in a web browser (click or press a key to start audio)

**Use Case:** Best for studying the audio characteristics and energy distribution patterns of Maxwell's Demon without the complexity of nested structures.

---

## Technical Details

### Maxwell's Demon Algorithm
The demon sorts particles by kinetic energy:
- **High-energy particles** (KE > 0.05): Moved to the positive x side of the lobe
- **Low-energy particles** (KE ≤ 0.05): Moved to the negative x side of the lobe

This creates a temperature gradient within each lobe, demonstrating the thought experiment of Maxwell's Demon.

### Physics Simulation
- **Collision Detection**: Particles bounce off lobe boundaries with perfect elastic collisions
- **Random Fluctuations**: Small random velocity changes simulate thermal motion
- **Energy Calculation**: Kinetic energy = 0.5 × (vx² + vy²)

### Audio Generation
- **Frequency Modulation**: Base frequency + (kinetic energy × 300Hz)
- **Volume Modulation**: Volume proportional to kinetic energy (capped at maximum)
- **Stereo Panning**: Each lobe positioned in stereo field (0.0 = left, 1.0 = right)

### Color Scheme
- **Lobe 1**: Red (#FF6B6B)
- **Lobe 2**: Yellow (#FFD93D)
- **Lobe 3**: Green (#6BE36B)
- **Background**: Dark blue (#0B1020)
- **Panel**: Darker blue (#141E2D)

---

## Requirements

### Python Versions
- Python 3.x
- `pygame` library
- `numpy` library (for `isolated.py` and `sound.py`)

Install dependencies:
```bash
pip install pygame numpy
```

### HTML Versions
- Modern web browser with:
  - Canvas API support
  - Web Audio API support
  - JavaScript enabled

**Note:** HTML audio versions require user interaction (click or keypress) to start audio due to browser autoplay policies.

---

## Usage Tips

1. **For Visual Study**: Use `light.py` or `light.html` - clean visualization without audio distraction
2. **For Audio Study**: Use `sound.py` or `sound.html` - focus on energy-to-sound mapping
3. **For Full Experience**: Use `isolated.py` or `isolated.html` - complete visual and audio simulation

4. **Performance**: HTML versions may perform better in browsers, while Python versions offer more control and precision

5. **Audio Volume**: Adjust system volume as needed - particle sounds can be numerous and frequent

---

## Project Philosophy

This project demonstrates Maxwell's Demon, a thought experiment in thermodynamics, through interactive visualization and sonification. The nested spinner structure creates complex, beautiful patterns while the demon's sorting mechanism provides insight into energy distribution and entropy.

Each implementation (Python vs HTML) offers different advantages:
- **Python**: More control, better for experimentation and modification
- **HTML**: No installation required, easy to share, runs in any browser

