document.getElementById('send-btn').addEventListener('click', sendMessage);
document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (!userInput.trim()) return;

    displayMessage(userInput, 'user');
    document.getElementById('user-input').value = '';

    fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => displayMessage(data.response, 'bot'))
    .catch(error => console.error('Error:', error));
}

function displayMessage(message, sender) {
    const chatbox = document.getElementById('chatbox');
    const messageElement = document.createElement('div');
    messageElement.className = sender === 'user' ? 'user-message' : 'bot-message';
    messageElement.textContent = message;
    chatbox.appendChild(messageElement);
    chatbox.scrollTop = chatbox.scrollHeight;
}
