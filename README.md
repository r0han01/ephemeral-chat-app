
# 🛠️ Realtime Socket Chat

## 🌟 Overview
**Realtime Socket Chat** is a full-stack chat application built with **Python, Flask, and Sockets**, integrated with **AWS DynamoDB** for message logging.  
It supports **real-time communication, ephemeral messaging, and a responsive front-end**.

This project **does NOT use WebSockets**; instead, we rely on **pure socket programming** to handle **real-time communication** between users.

---

## 📂 **Project Structure**
```sh
ephemeral-chat-app/
├── static/                 # Frontend files (CSS & JS)
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── script.js
├── codeEC2/                # Lightweight version for EC2 deployment
│   ├── index.html
│   ├── server.py
├── index.html              # Main frontend file
├── server.py               # Main Python server (Sockets + HTTP)
├── Dockerfile              # Docker setup for containerization
├── requirements.txt        # Python dependencies
├── LICENSE                 # MIT License
└── README.md               # Project documentation (this file)
```

### 🔹 **Why `codeEC2/` Directory?**
On **AWS EC2 servers**, creating directories and setting up dependencies can be time-consuming.  
The `codeEC2/` folder contains a **minimal version** of the application with just `server.py` and `index.html`.  
Users can **easily copy this directory** and start the server on EC2 without extra setup.

---

## ⚡ **How the Chat Application Works**
### 📡 **Sockets for Real-Time Communication**
- Unlike WebSockets, **traditional sockets** provide **low-level** network communication.
- The **server listens on a TCP socket** (`localhost:5555`).
- **Clients connect to the socket** and exchange messages **instantly**.
- Messages are **logged into AWS DynamoDB** for persistence.

### 🛠 **Key Features**
✅ **Real-time messaging** using **TCP sockets**.  
✅ **Authentication via 8-digit access codes**.  
✅ **DynamoDB logging** for session tracking & message storage.  
✅ **Ephemeral chat** (data is deleted when the server shuts down).  
✅ **Docker support** for easy deployment.  
✅ **AWS EC2 compatibility** with a lightweight `codeEC2/` version.  

---

## 🔗 **Docker Setup**
This application is containerized using **Docker**, making it easy to run anywhere.  

### 🚀 **Pull & Run from Docker Hub**
```sh
docker pull r0han01/realtime-socket-chat:latest
docker run -it -p 8000:8000 -p 5555:5555 --env-file .env realtime-socket-chat
```

📌 **Docker Repository:** [r0han01/realtime-socket-chat](https://hub.docker.com/repository/docker/r0han01/realtime-socket-chat/general)

### 🏗 **Building the Image Locally**
If you modify the code, build a new Docker image:
```sh
docker build -t realtime-socket-chat .
docker run -it -p 8000:8000 -p 5555:5555 --env-file .env realtime-socket-chat
```

---

## ☁️ **AWS DynamoDB Integration**
This project uses **AWS DynamoDB** to log:
- **User sessions** (`join` and `leave` events)
- **Messages sent** (`message` events)
- **Server start/stop timestamps**  

### 🔧 **DynamoDB Table Setup**
1. Go to **AWS Console → DynamoDB**.
2. **Create a new table**:
   - **Table name:** `ChatHistory`
   - **Partition key:** `session_id`
   - **Sort key:** `timestamp`
3. Add the following **environment variables** to your `.env` file:
   ```sh
   AWS_ACCESS_KEY_ID=your-access-key
   AWS_SECRET_ACCESS_KEY=your-secret-key
   AWS_DEFAULT_REGION=us-east-2
   ```
4. **Run the server**, and messages will be logged automatically!

---

## 🌍 **Deploying on AWS EC2**
To run this chat app on **AWS EC2**, follow these steps:

### 1️⃣ **Connect to EC2**
```sh
ssh -i your-key.pem ec2-user@your-ec2-ip
```

### 2️⃣ **Install Dependencies**
```sh
sudo yum install python3
pip install boto3
```

### 3️⃣ **Copy & Run the Minimal Version**
Copy the **`codeEC2/`** folder to EC2 and run:
```sh
python3 server.py
```

The **server will start**, and the chat application will be accessible via:
```
http://your-ec2-ip:8000
```

---

## 🔌 **How to Use the Chat**
### 🏁 **Starting the Server**
Run the Python server:
```sh
python server.py
```
You'll see an **authentication code** like:
```
🚀 DEBUG: Authentication Code = 12345678
🚀 DEBUG: Session ID = 87654321
```

### 💬 **Joining the Chat**
1. Open `http://localhost:8000` in a browser.
2. Enter a **username** and the **8-digit authentication code**.
3. Start chatting in real time! 🎉

---

## 🛑 **Stopping the Server**
To stop the chat server, press **`CTRL + C`**.  
It will **automatically clear chat history** in **DynamoDB** and **log the shutdown time**.

---

## ⚠️ **Troubleshooting**
### 🔹 **Docker Port Already in Use?**
If you see an error:
```sh
Bind for 0.0.0.0:5555 failed: port is already allocated
```
Free the port:
```sh
sudo lsof -i :5555
sudo kill -9 <PID>
```

### 🔹 **AWS Credentials Not Found?**
Check if **AWS credentials** are set inside Docker:
```sh
docker exec -it <container_id> printenv | grep AWS
```

---

## 📜 **License**
This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.

---

## ❤️ **Contributing**
Feel free to contribute by **opening a PR** or **suggesting features**.  
Fork the repository and submit a pull request! 🚀
