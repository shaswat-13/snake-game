# Snake Game

This repository contains a Python implementation of the classic Snake game using the Pygame library. The game features a glowing border, a grid-like layout, and various game states such as Menu, Pause, and Game Over.

---

## Features

- **Dynamic Background Colors**: The background color changes dynamically each game session.
- **Game States**: Includes a Menu, Pause, and Game Over screen.
- **Smooth Animations**: Optimized snake movement with adjustable speed based on the score.
- **Custom Fonts and Assets**: Custom fonts and images for a unique visual experience.
- **Game Music**: Background music with volume control.

---

## Prerequisites

Make sure you have Python installed along with the following libraries:

- `pygame`

To install Pygame, run:

```bash
pip install pygame
```

---

## How to Run

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/snake-game.git
cd snake-game
```

2. Place the required assets (`space_invaders.ttf`, `food.png`, and `sound_track.mp3`) in the project directory.

3. Run the game:

```bash
python snake_game.py
```

---

## Controls

- **Arrow Keys**: Move the snake in the desired direction.
- **Enter**: Start or restart the game.
- **Escape**: Pause or resume the game.

---

## Gameplay

1. Navigate the snake using the arrow keys.
2. Collect food to grow the snake and increase your score.
3. Avoid colliding with the edges or the snake's tail.
4. The game speeds up every 5 points.

---

## Project Structure

```plaintext
snake-game/
├── snake_game.py       # Main game logic
├── space_invaders.ttf  # Custom font file
├── food.png            # Food image asset
├── sound_track.mp3     # Background music
├── README.md           # Project documentation
```

---

## Customization

- **Change Background Colors**: Modify the `get_bg_color()` function for custom color schemes.
- **Snake Speed**: Adjust the `pygame.time.set_timer(SNAKE_UPDATE, 200)` interval for slower or faster gameplay.
- **Assets**: Replace `food.png` or `sound_track.mp3` for a personalized experience.

---

## Known Issues

- None reported as of now. Feel free to open an issue if you encounter any bugs.

---

## Future Improvements

- Add more game modes (e.g., timed mode, infinite mode).
- Introduce power-ups for enhanced gameplay.
- Implement a high-score leaderboard.

---

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute this code.

---

## Acknowledgements

- Pygame Library: [https://www.pygame.org/](https://www.pygame.org/)
- Font and Music Assets: Ensure to use properly licensed assets for your version.

---

Enjoy playing Snake!

