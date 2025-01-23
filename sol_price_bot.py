import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Fetch the current price of Solana in USD
def get_sol_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data["solana"]["usd"]

# Command handler for the /start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Welcome to the Solana-USD Price Bot!\nSend /price followed by the USD amount to get its value in SOL.\n\nExample:\n/price 50"
    )

# Command handler for the /price command
async def price(update: Update, context: CallbackContext) -> None:
    try:
        # Get the amount in USD from the user's message
        usd_amount = float(context.args[0])
        sol_price = get_sol_price()
        sol_value = round(usd_amount / sol_price, 4)

        # Respond with the calculated SOL value
        await update.message.reply_text(
            f"The current price of Solana (SOL) is ${sol_price:.2f}.\n"
            f"${usd_amount} USD is approximately {sol_value} SOL."
        )
    except (IndexError, ValueError):
        await update.message.reply_text("Please provide a valid USD amount. Example:\n/price 50")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

# Main function to run the bot
def main():
    # Replace 'YOUR_API_TOKEN' with the token you received from BotFather
    application = Application.builder().token("8130094422:AAHILiBnzOJyohN0US6U7sCs_Nf-CGiheiA").build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("price", price))

    # Start the bot and run until interrupted
    application.run_polling()

if __name__ == "__main__":
    main()
