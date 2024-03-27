from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

Token: Final = "token"
bot_username: Final = "@Superrdownloader_bot"

# Commands
async def start(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! This bot will help you download content from 'YOUTUBE' or 'INSTAGRAM'.")

async def help(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("1. Choose the application you want to download from.\n"
                                    "2. Enter the address of the file you want to download.\n")

async def instagram(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please send the Instagram file address in the correct format to download.\n"
                                    "Example: https://www.instagram.com/reel/C4ulyEsq5Rj/?igsh=dHU4eHR5dmd4OXZ.w")
    
    # Wait for the user to send the Instagram link
    user_input = await Context.get_message_text(update)
    
    # Process the Instagram link using instagram_downloader function
    modified_link = instagram_downloader(text=user_input)
    
    # Send the modified link back to the user
    await update.message.reply_text(modified_link)


# Respond
def instagram_downloader(text: str):
    modified_text = text.replace("instagram", "DDinstagram", 1)

    return "HERE IS YOUR VIDEO",modified_text

def handles_responses(text: str):
    process = str(text.lower())
    if "hello" in process:
        return "Hey there!"
    if "how are you?" in process:
        return "I'm fine, thank you. How about you?"
    if "what can you do?" in process:
        return "I'm here to help you download videos from Instagram or YouTube."
    return "I'm sorry, I didn't catch that. Could you please rephrase?"

async def handle_message(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text
    print(f"user({update.message.chat.id}) in {message_type}: '{text}'")
    
    if message_type == 'group':
        if bot_username in text:
            new_text = text.replace(bot_username, "").strip()
            response = handles_responses(new_text)
        else:
            return
    else:
        if 'http' in text:
            modified_link = instagram_downloader(text)
            await update.message.reply_text(modified_link)
            return
    
        response = handles_responses(text)

    print('bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    print(f"update {update} caused error {Context.error}")

if __name__ == "__main__":
    print('Starting bot....')
    app = Application.builder().token(Token).build()
    
    # Commands
    app.add_handler(CommandHandler('START', start))
    app.add_handler(CommandHandler('HELP', help))
    app.add_handler(CommandHandler('INSTAGRAM', instagram))
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Error handling
    app.add_error_handler(error)
    
    # Polling
    print('Polling.....')
    app.run_polling(poll_interval=3)
    
# a