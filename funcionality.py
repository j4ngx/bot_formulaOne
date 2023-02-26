import requests
from bs4 import BeautifulSoup
import json
import datetime
from datetime import date
import logging
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)
import numpy as np
import yaml
from yaml.loader import SafeLoader

with open('config.yaml') as f:
    CONFIG = yaml.load(f, Loader=SafeLoader)

URL = CONFIG['FONE']['URL_SCHEDULE']

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def get_schedule_fone(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")

    return [ json.loads(gp.contents[0]) for gp in soup.find_all(type='application/ld+json')]

RACES = get_schedule_fone(URL)

async def get_full_shedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for race in RACES:
        date_race = datetime.datetime.strptime(race['startDate'], '%Y-%m-%dT%H:%M:%S')
        await update.message.reply_text('Race: {location} \nLocation: {city} \nDate: {date_race}' \
            .format(location = race['location']['name'], city = race['location']['address'], date_race = date_race.strftime('%d-%m-%Y')))

async def get_next_race(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    today = date.today()

    for race in RACES:
        date_race = datetime.datetime.strptime(race['startDate'], '%Y-%m-%dT%H:%M:%S')
        if date_race.date() > today:
            await update.message.reply_text('Race: {location} \nLocation: {city} \nDate: {date_race}' \
            .format(location = race['location']['name'], city = race['location']['address'], date_race = date_race.strftime('%d-%m-%Y')))
            break
def build_url(url, gp):
    country = gp['location']['address'].split(', ')[1]

    if 'Las Vegas' in gp['location']['address']:
        country = 'Las Vegas'
    elif 'Abu Dhabi' in gp['location']['address']:
        country = 'United_Arab_Emirates'

    country = country.replace(" ", "_")
    return url.format(country = country)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
 
    listKeyboard = [[InlineKeyboardButton(race['location']['name'], callback_data=str(RACES.index(race)))] for race in RACES]

    keyboard = listKeyboard
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    await update.message.reply_text("Choose the race do you want see information", reply_markup=reply_markup)

async def get_info_gp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    index = int(update.callback_query.data)

    gp = RACES[index]
    
    with open('config.yaml') as f:
        CONFIG = yaml.load(f, Loader=SafeLoader)
    print(gp['location']['address'])

    html = requests.get(build_url(CONFIG['FONE']['URL_COUNTRY'], gp))
    soup = BeautifulSoup(html.text, "html.parser")
    info_gp = soup.find_all(type='application/ld+json')

    json_info_gp = json.loads(str(info_gp[0].text))

    html = requests.get(build_url(CONFIG['FONE']['URL_CIRCUIT'], gp))
    soup = BeautifulSoup(html.text, "html.parser")

    country = gp['location']['address'].split(', ')[1]

    if 'Las Vegas' in gp['location']['address']:
        country = 'Las Vegas'
    elif 'Abu Dhabi' in gp['location']['address']:
        country = 'United_Arab_Emirates'

    image_url_circuit = soup.findAll(alt = country+'_Circuit.png')
    date_race = datetime.datetime.strptime(gp['startDate'], '%Y-%m-%dT%H:%M:%S')
    
    text_sessions = ''
    for session in json_info_gp['subEvent']:
        date_session = datetime.datetime.strptime(session['startDate'], '%Y-%m-%dT%H:%M:%SZ')
        text_sessions += '  _*{session_name}*_ \n   _{date_session}_ \n'.format(session_name = session['name'].split(' - ')[0], date_session= date_session.strftime('%d-%m-%Y %H:%M'))
    
    text_gp = '*{gp_name}* \n Date: _{date_gp}_\n\n Race weekend\n {gp_sessions}'.format(gp_name = gp['location']['name'].upper(), date_gp = date_race, gp_sessions = text_sessions)

    await context.bot.send_message(chat_id = context._chat_id, text = text_gp.replace('-','\-'), parse_mode='MarkdownV2')
    await context.bot.send_photo(chat_id = context._chat_id, photo = image_url_circuit[0]['data-src'])

