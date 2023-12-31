import sqlite3
import random
from wit import Wit
import json
import os

# Configure wit.ai client
WIT_ACCESS_TOKEN = 'JXZASC7XCYTMV5ATAT3IX6H6WV4IVXAF'
wit_client = Wit(WIT_ACCESS_TOKEN)

class Greetings:
    """
    Class for handling greetings and generating random greeting messages.
    """

    def __init__(self, wit_client):
        self.wit_client = wit_client

    def get_random_greeting(self):
        """
        Returns a random greeting message.
        """
        greetings = ['Hello! How can I help?', 'Hi there! How can I assist you?', 'Hey! What would you like help with?', 'Greetings! Can I help you?']
        return random.choice(greetings)
    
class Fairwell:
    """
    Class for handling farewells and generating random farewell messages.
    """

    def __init__(self, wit_client):
        self.wit_client = wit_client

    def get_random_fairwell(self):
        """
        Returns a random farewell message.
        """
        bye = ['Goodbye!', 'Goodbye, hope I helped!', 'Goodbye, have a great day!']
        return random.choice(bye)  


class ProductInfoIntent:
    """
    Class for handling product information intent.
    """

    def handle_product_info(self, message):
        """
        Retrieves product information based on user message.

        Args:
            message (str): User input message.

        Returns:
            str: Response message with product information.
        """
        current = os.path.dirname(os.path.abspath(__file__))  # Current directory to ensure database is reached
        path_to_database = os.path.join(current, 'kakashi_motors.db')
        connection = sqlite3.connect(path_to_database)
        cursor = connection.cursor()
        response = wit_client.message(message)
        entities = response['entities']

        motorcycle_model_entities = entities.get('motorcycle_model:motorcycle_model', [])
        if not motorcycle_model_entities:
            motorcycle_model_entities = entities.get('motorcycle_model', [])

        models = list(set(entity['value'] for entity in motorcycle_model_entities))
        color = entities.get('color', {}).get('value')
        engine_size = entities.get('engine_size', {}).get('value')
        brand = entities.get('brand', {}).get('value')
        cost = entities.get('cost', {}).get('value')
        
        result = []

        if color:
            cursor.execute("SELECT * FROM products WHERE color=?", (color,))
            product = cursor.fetchone()
            if product:
                result.append(f"Products with color {color}: {product}")
            else:
                result.append(f"No products found with color {color}")

        elif engine_size:
            cursor.execute("SELECT * FROM products WHERE engine_size=?", (engine_size,))
            product = cursor.fetchone()
            if product:
                response = f"The product with an engine size of {engine_size} is {product[0]} {product[2]} with a price of {product[3]}."
            else:
                response = f"No products found with engine size {engine_size}"
            result.append(response)

        elif brand:
            cursor.execute("SELECT * FROM products WHERE brand=?", (brand,))
            products = cursor.fetchall()
            if products:
                result.append(f"Products of brand {brand}: {products}")
            else:
                result.append(f"No products found with brand {brand}")

        elif cost:
            if cost == 'expensive':
                cursor.execute("SELECT * FROM products ORDER BY price DESC LIMIT 1")
            else:
                cursor.execute("SELECT * FROM products ORDER BY price LIMIT 1")
            product = cursor.fetchone()
            if product:
                result.append(f"The {cost} product is {product[0]} {product[2]} with a price of {product[3]}.")
            else:
                result.append(f"No products found with the specified cost preference")

        if not result:
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
            if products:
                result.append(f"Here are all our products: {products}")
            else:
                result.append("No products found in the database")

        response = '\n'.join(result)

        cursor.close()
        connection.close()

        return response
   
class RecommendedProductIntent:
    """
    Class for handling recommended product intent.
    """

    def __init__(self, wit_client):
        self.wit_client = wit_client
    
    def show_product(self):
        """
        Retrieves the most expensive product and generates a response message.

        Returns:
            str: Response message with the most expensive product information.
        """
        current = os.path.dirname(os.path.abspath(__file__))  # Current directory to ensure database is reached
        path_to_database = os.path.join(current, 'kakashi_motors.db')
        connection = sqlite3.connect(path_to_database)
        cursor = connection.cursor()

        # Retrieve the most expensive product from the
        current = os.path.dirname(os.path.abspath(__file__)) #Current directory to ensure database is reached
        path_to_database = os.path.join(current, 'kakashi_motors.db')
        connection = sqlite3.connect(path_to_database)  # Replace 'your_database.db' with the actual database file name
        cursor = connection.cursor()

            # Retrieve the most expensive product from the database
        cursor.execute("SELECT * FROM products WHERE brand='Honda'")
        product = cursor.fetchone()

        if product:
                # Format the response with the product details
                response = f"The best product is {product[0]} {product[2]} with a price of {product[3]}."

        else:
                response = "At Kakashi Motors, we strongly believe one size DOES NOT fit all! We recommend visiting our store and having an attendant guide towards the right decision for you"


        cursor.close()
        connection.close()

        return response



#Outside of the class there is the process input class that processes the input and determines the type of intent it has before returning a reponse 

recommend = RecommendedProductIntent(wit_client)
greetings_intent = Greetings(wit_client)
product_info_intent = ProductInfoIntent()
bye_response = Fairwell(wit_client)

# Process user input and determine the intent
def process_input(user_input):
    # Extract entities using wit.ai
    response = wit_client.message(user_input)
    entities = response['entities']

    if ("greeting" in str(response)):
        return greetings_intent.get_random_greeting()
    
    elif "warranty" in user_input.lower():
        return 'We have a warranty of two years for all our products, click this link http//:Kakashi/help/warranty for more information'
    
    elif ("customer_services" in str(response)):
        return 'As a chatbot, I can only help with providing information on products. For more specialised help, visit https://Kakashi/contact-us or you can email customer-services@kakashi.com'
    
    elif ("recommendations" in str(response)):
        return recommend.show_product()
    
    elif "services" in user_input.lower():
        return "We provide a range of services for motorbikes and specialise in equiping and fixing, for more information just visit http://Kakashi/services"

    elif "service" in user_input.lower():
        return 'We recommend servicing your motorbike every six months. Regular maintenance ensures optimal performance and longevity of your bike'
    
    elif ("product_info" in str(response)):
        return product_info_intent.handle_product_info(entities)
    
    elif ("goodbye" in str(response)):
        return bye_response.get_random_fairwell()

    else:
        return "I'm sorry, I can only assist with specific topics. Here are some common topics I can help you with: [Product Enquiries][Product Care]. How can I assist you with any of these?"
