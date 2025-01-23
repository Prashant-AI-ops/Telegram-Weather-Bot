# Telegram Weather Bot

A Telegram bot that provides current weather information for any city using the OpenWeatherMap API.

## Features

- Get current weather conditions for any city
- Temperature in Celsius
- Feels like temperature
- Humidity percentage
- Wind speed
- Weather description
- Error handling for invalid cities
- User-friendly messages

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `config/.env` file with your API keys:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   OPENWEATHER_API_KEY=your_openweather_api_key
   ```
4. Run the bot:
   ```bash
   python src/bot.py
   ```

## Usage

1. Start a chat with the bot on Telegram
2. Send `/start` to get welcome message
3. Send `/help` to get usage instructions
4. Send any city name to get current weather information

## Error Handling

The bot handles:
- Invalid city names
- API connection issues
- Data formatting errors

## Dependencies

- python-telegram-bot
- python-dotenv
- requests

## License

This project is open source and available under the MIT License. 