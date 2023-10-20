from wit import Wit
from intents import ProductInfoIntent, OtherIntent

# Configure wit.ai client
WIT_ACCESS_TOKEN = 'JXZASC7XCYTMV5ATAT3IX6H6WV4IVXAF'
wit_client = Wit(WIT_ACCESS_TOKEN)

# Create instances of intent classes
product_info_intent = ProductInfoIntent()
other_intent = OtherIntent()

# Process user input and determine the intent
def process_input(user_input):
    wit_response = wit_client.message(user_input)
    intent = wit_response['intents'][0]['name']

    if intent == 'product_info':
        entities = wit_response['entities']
        response = product_info_intent.handle_product_info(entities)
        print(response)
        # You can perform further actions with the response as needed

    elif intent == 'other_intent':
        entities = wit_response['entities']
        response = other_intent.handle_other_intent(entities)
        print(response)
        # You can perform further actions with the response as needed

    else:
        # Handle unrecognized intent or provide default behavior
        pass
