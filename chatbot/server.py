#Server file that connects to flask server and deilvers message to back-end through approute

#Flask is the application (server), a request is made and access is given.
#Jsonify was needed to convert python objects (such as request sent by client) to JSON data
from flask import Flask, render_template, request, jsonify
import sys
sys.path.append('/path/to/intents')
from intents import process_input

app = Flask(__name__)

#Allows for the interaction between server and front-end (interface)
@app.route('/')
def home():
    # Render the template for the chat interface
    return render_template('index.html')

@app.route('/receive-message', methods=['POST'])

def receive_message():
        data = request.get_json()
        message = data['message'] #variable named message in js where it contains user's input.
        #message is in stringified json data format.
        
        # Process the received message
        response = process_input(message)
        bot = { 'status': 'success',
        'message': format(response)}

        return jsonify(bot) #bot must be serialised to a JSON reponse since that what the js code will be taking
        
if __name__ == '__main__':
    app.run()
    


