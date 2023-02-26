import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from funcionality import *
import yaml
from yaml.loader import SafeLoader

with open('config.yaml') as f:
    CONFIG = yaml.load(f, Loader=SafeLoader)

URL = CONFIG['FONE']['URL_SCHEDULE']

TOKEN = CONFIG['TELEGRAM']['TOKEN']

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("full_schedule",get_full_shedule))
    app.add_handler(CommandHandler("next_race",get_next_race))
    app.add_handler(CommandHandler("start",start))
    
    app.add_handler(CallbackQueryHandler(manage_menu_gp))
    app.run_polling()


if __name__ == '__main__':
    main()
    





