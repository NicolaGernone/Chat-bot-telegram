# 🚀 Rocket Launch Detection Bot

This repository contains the source code for **Rocket Launch Detection Bot**, a Telegram bot designed to identify the exact frame when a rocket launch occurs using a bisection algorithm on video frames. The bot interacts with users by showing them frames from a video and asking whether the rocket has launched, narrowing down the frame using a bisection method. 

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Source Code](#source-code)
- [Code Structure & Maintainability](#code-structure--maintainability)

## Features
- Interactive frame-based bisection algorithm for launch detection.
- Seamless interaction with users via Telegram buttons (Yes/No).
- Error handling and logging for robust performance.
- Async architecture to ensure smooth communication.
- Reset functionality for fresh searches after a frame is found.

## Installation for developers

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/rocket-launch-bot.git
   cd rocket-launch-bot
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   You'll need to provide your own Telegram bot token and FRAMEX API URL by creating a `.env` file in the root directory:
   ```
   TELEGRAM_BOT_TOKEN=your-telegram-bot-token
   FRAMEX_API_URL=https://your-framex-api-url
   ```

5. **Run the bot**:
   ```bash
   python3 bot/rocket_launch_bot.py
   ```

## Usage

**Bot name: @RocketLaunchBot**
**Bot username: @RocketLaunchBot_bot**

1. **Start the bot**:
   Once the bot is running, invite it to your Telegram group or chat with it directly.

2. **Begin the launch detection**:
   - Type `/start` to initiate the launch detection process.
   - The bot will start sending frames and asking whether the rocket has launched.
   - Click **Yes** or **No** to guide the bot in narrowing down the frame using the bisection algorithm.

3. **Reset the search**:
   - If the bot finds the launch frame, it will display the result and offer the option to reset for a new search.


## Source Code

### Main Files
- **bot/rocket_launch_bot.py**: The main bot logic that handles interactions, commands, and frame detection.
- **bot/frame_bisect.py**: Contains the `FrameBisection` class which implements the bisection algorithm to find the rocket launch frame.
- **config.py**: Configuration and logging setup.
- **tests/test_rocket_launch_bot.py**: Unit tests to ensure the correct functionality of the bot using `pytest`.

### How to Run Tests
```bash
pytest tests/
```

## Code Structure & Maintainability

Several practices were applied to ensure that the code is maintainable and scalable:

1. **Modular Code Structure**:
   - The code is divided into distinct modules (`bot/rocket_launch_bot.py` and `bot/frame_bisect.py`), each responsible for specific functionality.
   - This allows for easy maintenance and updates without affecting the entire system.

2. **Asynchronous Programming**:
   - By using `asyncio` for functions like API requests and Telegram bot interactions, the bot can handle multiple users and operations simultaneously without blocking.
   
3. **Testing**:
   - Comprehensive unit tests have been implemented using `pytest` and `unittest.mock` to mock asynchronous functions.
   - Tests cover various scenarios, including error handling and bisection logic.

4. **Logging**:
   - A robust logging system has been integrated via Python’s `logging` module.
   - Logs are stored in the `logs/` directory with timestamps, making it easier to track and debug any issues.

5. **Error Handling**:
   - Custom error handling has been implemented to gracefully manage unexpected issues like failed API requests or invalid user inputs.
   - Errors are logged for later review, ensuring transparency and debuggability.

6. **Decoupled Logic**:
   - The business logic for frame detection is separated from the Telegram interaction code, which makes the bot easier to extend (e.g., adding other platforms or features).