import socket
import threading
import json
from http.server import SimpleHTTPRequestHandler
import socketserver
import random
import boto3
from datetime import datetime, timezone
import os
import signal
import sys

# Store messages, users, and chat subject in memory
messages = []
message_ids = set()
users = set()
current_subject = "Group Chat"  # Default chat subject

# Generate an 8-digit authentication code and session ID
auth_code = ''.join([str(random.randint(0, 9)) for _ in range(8)])
session_id = ''.join([str(random.randint(0, 9)) for _ in range(8)])

# Initialize DynamoDB client with environment variables
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='us-east-2'  # Updated to us-east-2
)
table = dynamodb.Table('ChatHistory')

# Fancy terminal output
def print_server_status():
    print("+------------------------------------------------------------+")
    print("|       🚀 SERVER STATUS 🚀                                  |")
    print("+------------------------------------------------------------+")
    print("Server starting... ")
    print("Server started successfully!\n")
    print(f"| Authentication Code: {auth_code}                              |")
    print(f"| Session ID: {session_id}                                       |")
    print("\n+------------------------------------------------------------+")
    print(f"| HTTP server started at: http://localhost:8000              |")
    print(f"| Socket server started on: localhost:5555                   |")
    print("+------------------------------------------------------------+")
    print("🌟🌟🌟🌟🌟  CHAT RULES  🌟🌟🌟🌟🌟\n")
    print("+----------------------------------------------------------------------+")
    print("|                            📝  IMPORTANT CHAT RULES  📝                            |")
    print("+----------------------------------------------------------------------+")
    print("  1️⃣ **Respect Everyone**")
    print("   🤝 Treat all users with kindness and respect. Personal attacks, racism, or harassment will not be tolerated.\n")
    print("  2️⃣ **Keep It Clean**")
    print("   🚫 No profanity, explicit language, or inappropriate content. Keep the chat environment friendly.\n")
    print("  3️⃣ **No Spam**")
    print("   📢 Avoid flooding the chat with unnecessary messages, ads, or links. Keep it clear and concise.\n")
    print("  4️⃣ **Stay on Topic**")
    print("   🎯 Stay relevant to the chat purpose. Off-topic conversations should be kept to a minimum.\n")
    print("  5️⃣ **No Sharing Personal Info**")
    print("   🔒 Protect your privacy. Do not share personal details such as phone numbers or addresses.\n")
    print("  6️⃣ **Be Considerate of Others**")
    print("   🕊️ Be mindful of others. If you're asking for help, be patient and clear.\n")
    print("  7️⃣ **Moderators Have Final Say**")
    print("   ⚖️ Always follow moderator instructions. They're here to maintain order and fun.\n")
    print("  8️⃣ **Report Inappropriate Behavior**")
    print("   🚨 If you see inappropriate behavior, report it to moderators immediately.\n")
    print("+----------------------------------------------------------------------+")
    print("|          ✅ Let's keep the chat safe and fun! 😊          |")
    print("+----------------------------------------------------------------------+")

# Log server start time to DynamoDB
start_time = datetime.now(timezone.utc).isoformat()
table.put_item(Item={
    'session_id': session_id,
    'timestamp': start_time,
    'event': 'server_started',
    'details': 'Server started'
})

class ChatHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/messages':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                'messages': messages,
                'users': list(users),
                'user_count': len(users),
                'chat_subject': current_subject  # Always send current subject
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/send':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            name = data.get('name')
            message = data.get('message')
            message_id = data.get('id')
            new_subject = data.get('new_subject')  # Optional new subject
            
            if name and message and message_id:
                if message_id not in message_ids:
                    message_ids.add(message_id)
                    chat_message = f"{name}: {message}"
                    if new_subject:
                        global current_subject
                        current_subject = new_subject.strip()
                        chat_message = f"{name}: changed chat subject to: {current_subject}"
                    messages.append(chat_message)
                    broadcast(chat_message)
                    # Log to DynamoDB
                    timestamp = datetime.now(timezone.utc).isoformat()
                    table.put_item(Item={
                        'session_id': session_id,
                        'timestamp': timestamp,
                        'event': 'message',
                        'details': chat_message
                    })
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
        elif self.path == '/join':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            name = data.get('name')
            code = data.get('code')
            
            if name and code == auth_code:
                users.add(name)
                join_message = f"{name} has joined the chat!"
                messages.append(join_message)
                broadcast(join_message)
                # Log join to DynamoDB
                timestamp = datetime.now(timezone.utc).isoformat()
                table.put_item(Item={
                    'session_id': session_id,
                    'timestamp': timestamp,
                    'event': 'join',
                    'details': join_message
                })
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b'{"status": "ok"}')
            else:
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b'{"status": "error", "message": "Invalid authentication code"}')
        else:
            self.send_response(404)
            self.end_headers()

def start_socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5555))
    server_socket.listen(5)
    print("Socket server started on localhost:5555")
    
    while True:
        client_socket, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

def handle_client(client_socket):
    try:
        name = client_socket.recv(1024).decode()
        users.add(name)
        join_message = f"{name} has joined the chat!"
        messages.append(join_message)
        broadcast(join_message)
        # Log join to DynamoDB
        timestamp = datetime.now(timezone.utc).isoformat()
        table.put_item(Item={
            'session_id': session_id,
            'timestamp': timestamp,
            'event': 'join',
            'details': join_message
        })
        
        while True:
            message = client_socket.recv(1024).decode()
            if message:
                chat_message = f"{name}: {message}"
                messages.append(chat_message)
                broadcast(chat_message)
                # Log message to DynamoDB
                timestamp = datetime.now(timezone.utc).isoformat()
                table.put_item(Item={
                    'session_id': session_id,
                    'timestamp': timestamp,
                    'event': 'message',
                    'details': chat_message
                })
    except:
        if name in users:
            users.remove(name)
            leave_message = f"{name} has left the chat"
            messages.append(leave_message)
            broadcast(leave_message)
            # Log leave to DynamoDB
            timestamp = datetime.now(timezone.utc).isoformat()
            table.put_item(Item={
                'session_id': session_id,
                'timestamp': timestamp,
                'event': 'leave',
                'details': leave_message
            })
        client_socket.close()

def broadcast(message):
    messages.append(message)

def clear_chat_history():
    response = table.scan(FilterExpression='session_id = :sid', ExpressionAttributeValues={':sid': session_id})
    for item in response['Items']:
        table.delete_item(Key={'session_id': item['session_id'], 'timestamp': item['timestamp']})
    print("Chat history cleared from DynamoDB")

def signal_handler(sig, frame):
    stop_time = datetime.now(timezone.utc).isoformat()
    table.put_item(Item={
        'session_id': session_id,
        'timestamp': stop_time,
        'event': 'server_stopped',
        'details': 'Server stopped - All chat data will now vanish for privacy'
    })
    print(f"Server stopped at {stop_time}")
    print("🌐 Chat data is ephemeral: As long as you chat while the server is running, your messages are stored unencrypted in AWS DynamoDB. Once the server stops, all data vanishes entirely, ensuring no one can track your chat history afterward. Privacy guaranteed! 🔒")
    clear_chat_history()
    sys.exit(0)

if __name__ == "__main__":
    print_server_status()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    socket_thread = threading.Thread(target=start_socket_server)
    socket_thread.daemon = True
    socket_thread.start()
    
    PORT = 8000
    Handler = ChatHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()