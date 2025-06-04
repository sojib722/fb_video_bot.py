import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# টেলিগ্রাম বট টোকেন
TOKEN = '7399120336:AAHysTbMoGTrjxEkbOgjEJn45uak3zX1ga8'

# লগিং সেটআপ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ফেসবুক ভিডিও ডাউনলোড ফাংশন
def download_fb_video(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        video_url = soup.find('meta', property='og:video')['content']
        return video_url
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        return None

# স্টার্ট কমান্ড হ্যান্ডলার
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Send me a Facebook video link to download.')

# মেসেজ হ্যান্ডলার
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    if 'facebook.com' in user_message or 'fb.watch' in user_message:
        video_url = download_fb_video(user_message)
        if video_url:
            update.message.reply_text(f"Here is your video link:\n{video_url}")
        else:
            update.message.reply_text("Sorry, I couldn't download the video.")
    else:
        update.message.reply_text("Please send a valid Facebook video link.")

# মেইন ফাংশন
def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
