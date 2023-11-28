from io import StringIO
from django.test import TestCase
from django.core.management import call_command
from unittest.mock import patch
from app.models import Product
from django.test import TestCase
class Test(TestCase):
    def test_1(self):
        self.assertEqual(1, 1)
    def test_add_product_command(self):
        # Mocking user input
        user_input = "/add TestProduct 10.0 TestDescription 5"
        
        with patch('builtins.input', side_effect=user_input.split()), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            # Call the management command
            call_command('run_telegram_bot')

        # Check if the product is added to the database
        product = Product.objects.get(name="TestProduct")
        self.assertEqual(product.price, 10.0)
        self.assertEqual(product.description, "TestDescription")
        self.assertEqual(product.quantity_available, 5)

        # Check the output for success message
        self.assertIn("Product 'TestProduct' added successfully!", mock_stdout.getvalue())

    def test_invalid_add_product_command(self):
        # Mocking invalid user input
        invalid_user_input = "/add InvalidInput"
        
        with patch('builtins.input', side_effect=invalid_user_input.split()), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            # Call the management command
            call_command('run_telegram_bot')

        # Check the output for the error message
        self.assertIn("Invalid format. Use: /add <product_name> <product_price> <product_description> <quantity_available>", mock_stdout.getvalue())
    
    def test_help_command(self):
        # Mocking user input for /help command
        user_input = "/help"
        
        with patch('builtins.input', side_effect=user_input.split()), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            # Call the management command
            call_command('run_telegram_bot')

        # Check the output for the help message
        commands_list = [
            "/start - Start the bot",
            "/help - Display available commands",
            "/products - Display a list of products",
            "/add <product_name> <product_price> <product_description> <quantity_available> - Add a new product",
            "any text - Echo the text"
        ]
        expected_output = "\n".join(commands_list)
        self.assertIn(expected_output, mock_stdout.getvalue())

    def test_echo_command(self):
        # Mocking user input for any text command
        user_input = "Hello, bot!"
        
        with patch('builtins.input', side_effect=user_input.split()), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            # Call the management command
            call_command('run_telegram_bot')

        # Check the output for the echoed message
        self.assertIn(user_input, mock_stdout.getvalue())