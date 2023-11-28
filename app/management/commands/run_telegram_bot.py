from django.core.management.base import BaseCommand
from django.forms import ValidationError
import telebot
from app.models import Product
bot = telebot.TeleBot("6776453623:AAEoXqmKSS9hL4wtM-EutT0RRCXBqSPmjJQ") #токен

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello world!")

@bot.message_handler(commands=['help'])
def help(message):
    commands_list = [
        "/start - Start the bot",
        "/help - Display available commands",
        "/products - Display a list of products",
        "/add <product_name> <product_price> <product_description> <quantity_available> - Add a new product",
        "any text - Echo the text"
    ]
    bot.send_message(message.chat.id, "\n".join(commands_list))

@bot.message_handler(commands=['add'])
def add_product(message):
    try:
        _, product_name, product_price, product_description, quantity_available = message.text.split()
        product_price = float(product_price)
        quantity_available = int(quantity_available)
        
        Product.objects.create(
            name=product_name,
            price=product_price,
            description=product_description,
            quantity_available=quantity_available,
        )
        
        bot.send_message(message.chat.id, f"Product '{product_name}' added successfully!")
    except ValueError:
        bot.send_message(message.chat.id, "Invalid format. Use: /add <product_name> <product_price> <product_description> <quantity_available>")
    except ValidationError as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")

@bot.message_handler(commands=['products'])
def products(message):
    products = Product.objects.all()
    for product in products:
        bot.send_message(message.chat.id, product.name)

class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Starting bot...")
        bot.polling()
        print("Bot stopped")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)
