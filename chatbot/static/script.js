// script.js

// Get the elements for the modal and chatbot icon
var chatbotButton = document.getElementById('chatbot-button');
var modal = document.getElementById('modal');
var close = document.getElementById('close');

// Toggle modal visibility (when chatbot icon is clicked modal is opened)
chatbotButton.addEventListener('click', function() {
  modal.style.display = 'block';
});

// Close the modal (when x is clicked, modal closes)
close.addEventListener('click', function() {
  modal.style.display = 'none';
});


// Function to handle starting speech recognition
function startSpeechRecognition() {
  if ('webkitSpeechRecognition' in window) {
    var recognition = new webkitSpeechRecognition();

    // Set the recognition language
    recognition.lang = 'en-US';

    // Start speech recognition
    recognition.start();

    // Handle speech recognition result
    recognition.onresult = function(event) {
      var result = event.results[0][0].transcript;

      // Fill the input field with the recognized speech
      document.getElementById('user-input').value = result;
    };
  }
}





//Code for sending user inputs to server and displaying on the chatbox
var buttonGroup = document.getElementById('button-group');
var chatbox = document.getElementById('chatbox');
var userInput = document.getElementById('user-input');
var messageForm = document.getElementById('message-form');

//Event listener that looks out for one of the option buttons being clicked. 
//Function does not need to be called since the action of clicking will activate it
buttonGroup.addEventListener('click', function(event) {
  if (event.target.matches('.bot-options')) {
    var buttonText = event.target.textContent;

    //When the option is clicked, it appears in chatbox. the necessary elements are created and classes are attcahed so that css attributes can be added.
    var messageContainer = document.createElement('div');
    messageContainer.classList.add('message-container');

    var messageElement = document.createElement('div');
    messageElement.textContent = buttonText;

    messageContainer.classList.add('message');
    messageContainer.classList.add('user-message');

    //appendChild allows for the addition of new elemenys to DOM, without it no changes would be visisble
    messageContainer.appendChild(messageElement);
    chatbox.appendChild(messageContainer);

    // Scroll to the bottom of the chatbox
    chatbox.scrollTop = chatbox.scrollHeight;

    // Send the message to the server using fetch
    sendMessageToServer(buttonText); //function that enables intended message to be sent to server 
  }
});


function sanitizeInput(input) {
  // Replace single quotes with two single quotes to escape them
  return input.replace(/'/g, "''");
}



//Takes users input and upon "submit" sends them to server. 
messageForm.addEventListener('submit', function(event) {
  event.preventDefault();

  var message = userInput.value.trim(); //retrives value enetered by user and removes any whitespace

  //So long as there is an input aka not "blank" the message is shown on the chatbox
  if (message !== '') {
    var messageContainer = document.createElement('div');
    messageContainer.classList.add('message-container');

    var messageElement = document.createElement('div');
    messageElement.textContent = message;

    messageContainer.classList.add('message');
    messageContainer.classList.add('user-message');

    messageContainer.appendChild(messageElement);
    chatbox.appendChild(messageContainer);

    // Scroll to the bottom of the chatbox
    chatbox.scrollTop = chatbox.scrollHeight;

    // Send the message to the server using fetch
    sendMessageToServer(message);

    userInput.value = ''; //resets the input field
  }


});


var userResponded = false;
var systemResponse = "Sorry, it seems like you're taking too long to respond. How can I assist you?";

// Sends message to server by using fetch function. Network request is made
function sendMessageToServer(message) {
  if (userResponded) {
    clearTimeout(userTimeout);
  }

  // Sets timer that looks at how long user takes to input, improving human-computer interaction
  var userTimeout = setTimeout(function() {
    if (!userResponded) {
      var messageElement = createMessageElement(systemResponse, 'bot-message');
      chatbox.appendChild(messageElement);

      // Convert system response to speech
      speak(systemResponse);
    }
  }, 60000); // 60000 milliseconds = 1 minute

  var sanitizedMessage = sanitizeInput(message);

  fetch('http://127.0.0.1:5000/receive-message', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message: sanitizedMessage })
  })
    .then(function(response) {
      clearTimeout(userTimeout);

      if (response.ok) {
        response.json().then(function(data) {
          userResponded = true;

          var message = data.message;
          var messageElement = createMessageElement(message, 'bot-message');
          chatbox.appendChild(messageElement);

          // Convert server response to speech
          speak(message);
          chatbox.scrollTop = chatbox.scrollHeight;
        });
      } else {
        // Error occurred while sending the message
        // Handle the error if needed
      }
    })
    .catch(function(error) {
      console.log('Error:', error);
    });
}

function createMessageElement(message, messageType) {
  var messageElement = document.createElement('div');
  messageElement.classList.add('message', messageType);
  var messageText = document.createElement('p');
  messageText.textContent = message;
  messageElement.appendChild(messageText);
  return messageElement;
}
// Function to convert text to speech
function speak(text) {
  var utterance = new SpeechSynthesisUtterance(text);
  speechSynthesis.speak(utterance);
}


