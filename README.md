# Snake Game 🐍

A comprehensive Snake Game implementation in Python using the `turtle` graphics library, featuring multiple game modes, levels, and sound effects.

## Features ✨

- **Two Game Modes:**
  - **Classic Mode:** Traditional snake gameplay. The walls are permeable—passed through them to appear on the other side!
  - **Obstacle Mode:** Walls are solid and dangerous. New obstacle layouts appear every 4 levels.
- **Leveling System:** Speed increases and snake color changes as you level up.
- **Bonus Food:** Catch the Golden Apple for extra points and a slow-motion effect! 🍏
- **High Score Tracking:** Saves your best scores for each mode independently.
- **Visual Effects:** Particle effects when eating food, screen shake, and dynamic menus.
- **Sound Effects:** Munching sounds (requires `pygame`).

## Installation 🛠️

1. **Prerequisites:**
   - Python 3.x
   - `pygame` (optional, for sound effects)

2. **Install Dependencies:**
   ```bash
   pip install pygame
   ```
   *(Note: The game runs without pygame, but sound will be disabled.)*

3. **Clone the Repository:**
   ```bash
   git clone https://github.com/Furqan3234/Snack_Game.git
   cd Snack_Game
   ```

## How to Play 🎮

Run the game using Python:

```bash
python main.py
```

### Controls ⌨️

- **Arrow Keys:** Move Up, Down, Left, Right
- **Space:** Start Game
- **P:** Pause / Resume
- **Mouse:** Click on menu buttons to select modes or quit

## Game Modes 🕹️

### Classic
The classic experience. Walls wrap around the screen. Perfect for high-speed chases!

### Obstacle
A challenging mode with solid walls.
- **Level 1-4:** The Box
- **Level 5-8:** The Cross
- **Level 9-12:** Four Pillars
- **Level 13+:** Randomly Scattered Blocks

## Enjoy the Game! 🚀
