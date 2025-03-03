let userName;
let displayedMessages = new Set();
let currentUsers = [];

function joinChat() {
    userName = document.getElementById('name-input').value.trim();
    const code = document.getElementById('code-input').value.trim();
    if (!userName || !code) {
        alert('Please enter both a name and an 8-digit code!');
        return;
    }

    fetch('/join', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: userName,
            code: code
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.message || 'Invalid authentication code');
            });
        }
        return response.json();
    })
    .then(() => {
        document.getElementById('name-container').classList.add('hidden');
        setTimeout(() => {
            document.getElementById('name-container').style.display = 'none';
            document.getElementById('chat-notice').style.display = 'block';
            document.getElementById("toggle-sidebar").style.display = "block";
            document.getElementById("mobile-logo").style.display = "block";
            pollMessages();
        }, 500);
    })
    .catch(error => {
        alert(error.message || 'Error joining chat');
        console.error('Error joining chat:', error);
    });
}

function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    if (message) {
        const messageId = Date.now() + Math.random().toString(36).substr(2);
        fetch('/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: userName,
                message: message,
                id: messageId
            })
        })
        .then(() => {
            input.value = '';
        })
        .catch(error => console.error('Error sending message:', error));
    }
}

function editSubject() {
    const currentSubject = document.querySelector('#chat-subject span').textContent.replace("Chat Subject: ", "");
    const newSubject = prompt("Enter new chat subject:", currentSubject);
    if (newSubject && newSubject.trim()) {
        const messageId = Date.now() + Math.random().toString(36).substr(2);
        fetch('/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: userName,
                message: `changed chat subject to: ${newSubject.trim()}`,
                id: messageId,
                new_subject: newSubject.trim()
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update subject');
            }
            return response.json();
        })
        .then(() => {
            console.log(`Subject change request sent: ${newSubject}`);
            setTimeout(pollMessages, 100);
        })
        .catch(error => console.error('Error changing subject:', error));
    }
}

function pollMessages() {
    fetch('/messages', { cache: 'no-store' })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log("Polling data:", data);
            const usersDisplay = document.getElementById('users-display');
            const onlineUsers = document.getElementById('online-users');
            const chatDisplay = document.getElementById('chat-display');
            const joinMessages = document.getElementById('join-messages');
            const subjectSpan = document.querySelector('#chat-subject span');

            usersDisplay.textContent = `Users online: ${data.user_count}`;
            subjectSpan.textContent = `Chat Subject: ${data.chat_subject}`;

            if (JSON.stringify(data.users) !== JSON.stringify(currentUsers)) {
                onlineUsers.innerHTML = '';
                data.users.forEach(user => {
                    const userCard = document.createElement('div');
                    userCard.className = 'user-card';
                    userCard.textContent = user;
                    onlineUsers.appendChild(userCard);
                });
                currentUsers = data.users;
            }

            data.messages.forEach(message => {
                if (!displayedMessages.has(message)) {
                    displayedMessages.add(message);
                    if (message.includes("has joined the chat!")) {
                        const joinDiv = document.createElement('div');
                        joinDiv.className = 'join-message';
                        joinDiv.textContent = message;
                        joinMessages.appendChild(joinDiv);
                    } else {
                        const messageDiv = document.createElement('div');
                        messageDiv.className = 'message ' + (message.startsWith(userName) ? 'sent' : 'received');

                        const contentDiv = document.createElement('div');
                        contentDiv.className = 'message-content';

                        const [sender, ...contentParts] = message.split(': ');
                        const content = contentParts.join(': ');
                        const senderSpan = document.createElement('span');
                        senderSpan.className = 'sender-name';
                        senderSpan.textContent = sender;

                        const messageText = document.createTextNode(': ' + content);
                        contentDiv.appendChild(senderSpan);
                        contentDiv.appendChild(messageText);

                        const timeDiv = document.createElement('div');
                        timeDiv.className = 'message-time';
                        timeDiv.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

                        messageDiv.appendChild(contentDiv);
                        messageDiv.appendChild(timeDiv);
                        chatDisplay.appendChild(messageDiv);
                    }
                }
            });
            chatDisplay.scrollTop = chatDisplay.scrollHeight;
            joinMessages.scrollTop = joinMessages.scrollHeight;
        })
        .catch(error => console.error('Error polling messages:', error))
        .finally(() => {
            setTimeout(pollMessages, 500);
        });
}

document.getElementById('message-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

document.getElementById("toggle-sidebar").addEventListener("click", function () {
    document.querySelector(".header").classList.toggle("active");
});

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("mobile-logo").style.display = "none";
});