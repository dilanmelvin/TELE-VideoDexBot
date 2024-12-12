import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Path to store data
DATA_FILE = "video_data.json"

# Ensure data file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

# Load or initialize video data
def load_video_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

video_data = load_video_data()

# Command to start the bot and guide the user
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome! Use /name, /description, and /link to add video details. Then just type the name to get the link!")

# Command to set the name of the video
async def set_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Please provide a name for the video.")
        return
    name = ' '.join(context.args)
    video_data[name] = {"description": "", "link": ""}
    # Save video data
    with open(DATA_FILE, 'w') as f:
        json.dump(video_data, f)
    await update.message.reply_text(f"Name '{name}' added! Use /description to set the description and /link to set the link.")

# Command to set the description of the video
async def set_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Please provide a description for the video.")
        return
    description = ' '.join(context.args)
    
    # Get the last added name
    name = list(video_data.keys())[-1]
    video_data[name]["description"] = description
    
    # Save video data
    with open(DATA_FILE, 'w') as f:
        json.dump(video_data, f)
    
    await update.message.reply_text(f"Description for '{name}' set! Use /link to set the link.")

# Command to set the link of the video
async def set_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Please provide a link for the video.")
        return
    link = ' '.join(context.args)
    
    # Get the last added name
    name = list(video_data.keys())[-1]
    video_data[name]["link"] = link
    
    # Save video data
    with open(DATA_FILE, 'w') as f:
        json.dump(video_data, f)
    
    await update.message.reply_text(f"Link for '{name}' set! You can now use the name to get the link.")

# Handler to listen for name directly in the chat
async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    name = update.message.text.strip()
    
    if name in video_data:
        description = video_data[name]["description"]
        link = video_data[name]["link"]
        
        # Check if description or link is missing
        if not description or not link:
            await update.message.reply_text(f"Some details are missing for '{name}'. Please make sure to set both description and link.")
            return
        
        # Send a message with the name, description, and the link button
        keyboard = [
            [InlineKeyboardButton("Click here for the link", url=link)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f"Name: {name}\nDescription: {description}", reply_markup=reply_markup)
    else:
        await update.message.reply_text(f"No data found for '{name}'. Please ensure the name is correct.")

# Main function to set up the bot
def main():
    application = Application.builder().token("7540822881:AAH18Vuq4twmMiuH6jlpkzzzK6b4FPNgQ2k").build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("name", set_name))
    application.add_handler(CommandHandler("description", set_description))
    application.add_handler(CommandHandler("link", set_link))

    # Add a message handler to listen for names directly in the chat
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name))
    
    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
