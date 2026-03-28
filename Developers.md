# Developer Guide

Welcome to the `math_videos` project! This guide will help you get your local environment set up and explain how the repository is structured so you can start contributing.

## Overview
This repository uses [Manim](https://www.manim.community/) to generate educational videos and animations for teaching Indic (Vedic) Mathematics. 

## Project Structure
- **`README.md`**: High-level overview of the project and some example commands.
- **`sourceme`**: A shell script to set up your environment variables (specifically `PYTHONPATH`) so that imports work correctly across the project.
- **`vedic_maths/`**: The main directory containing all the Manim scene scripts.
  - `nikhilam.py`: Animations related to Nikhilam sutra (subtraction).
  - `multiplication.py`: Animations related to multiplication (Ekadhikena, Yavadunam).
  - `division.py`, `square_root.py`, `folding.py`, `vinculum.py`, etc.: Other thematic animation scripts.
  - `common.py` & `brand.py`: Shared utilities, themes, or constants used across different video scenes.



## Environment Setup
1. **Install Manim**: You will need to install Manim and its dependencies (like FFmpeg and LaTeX). Please follow the official [Manim Installation Guide](https://docs.manim.community/en/stable/tutorials/quickstart.html).
2. **Python Dependencies**: Ensure you have Python 3.7+ installed.
3. **Set the Python Path**: Before running any scripts, source the provided script to set your `PYTHONPATH` correctly. This works for both bash (Linux/macOS) and Git Bash (Windows).
    ```bash
    source sourceme
    ```

## Running the Code
We use Manim's command-line interface to render the videos. The `-pql` flag is typically used for rapid development (Preview, Quality: Low).

Navigate to the root of the project and test rendering a scene:
```bash
# General format
manim -pql vedic_maths/<script_name>.py <SceneName>

# Example: Rendering the Nikhilam subtraction scene
manim -pql vedic_maths/nikhilam.py Subtraction
```

When you are ready to render the final, high-quality video, you can use the `-pqh` (Premium Quality, High) or similar production flags as described in the Manim documentation.
