import os
import logging
import csv
from datetime import datetime
from pathlib import Path
from typing import Final
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from weather_service import WeatherService

# Load environment variables
load_dotenv("config/.env")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
TOKEN: Final = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables. Please check your .env file.")
if TOKEN == "your_telegram_bot_token":
    raise ValueError("Please replace 'your_telegram_bot_token' with your actual bot token from BotFather")

# Initialize weather service
weather_service = WeatherService()

# Create logs directory if it doesn't exist
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)
admin_log_file = logs_dir / "user_interactions.csv"

# Create CSV file with headers if it doesn't exist
if not admin_log_file.exists():
    with open(admin_log_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'User ID', 'Username', 'First Name', 'Last Name', 'Message'])

def log_user_interaction(user: Update.effective_user, message: str):
    """Log user interaction to CSV file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_data = [
        timestamp,
        user.id,
        user.username or "N/A",
        user.first_name or "N/A",
        user.last_name or "N/A",
        message
    ]
    
    with open(admin_log_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(user_data)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    welcome_message = (
        "👋 Welcome to the Weather Bot!\n\n"
        "Simply send me a city name and I'll tell you the current weather there.\n"
        "For example: London, Paris, Tokyo\n\n"
        "Available commands:\n"
        "/start - Show this welcome message\n"
        "/help - Show help information"
    )
    log_user_interaction(update.effective_user, "/start command")
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_message = (
        "🌤 To get weather information, simply send me a city name.\n\n"
        "Examples:\n"
        "• London\n"
        "• Paris\n"
        "• Tokyo\n\n"
        "If you're having trouble, try including the country code:\n"
        "Example: London,UK"
    )
    log_user_interaction(update.effective_user, "/help command")
    await update.message.reply_text(help_message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages and respond with weather information."""
    city = update.message.text.strip()
    
    # Log the user interaction
    log_user_interaction(update.effective_user, f"Requested weather for: {city}")
    
    # Show "typing..." while processing
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, 
        action="typing"
    )
    
    # Get weather data
    weather_data = await weather_service.get_weather(city)
    
    if weather_data:
        response = weather_service.format_weather_message(weather_data)
    else:
        response = (
            "😕 Sorry, I couldn't find weather data for that city.\n"
            "Please check the city name and try again.\n"
            "You can also try adding the country code (e.g., London,UK)"
        )
    
    await update.message.reply_text(response)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors caused by Updates."""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Start the bot."""
    # Create application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add error handler
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main() 