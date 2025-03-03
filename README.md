
# 🛠️ Realtime Socket Chat

## 🌟 Overview
**Realtime Socket Chat** is a full-stack chat application built with **Python, Flask, and Sockets**, integrated with **AWS DynamoDB** for message logging.  
It supports **real-time communication, ephemeral messaging, and a responsive front-end**.
###
![ScreenShot Tool -20250303044034](https://github.com/user-attachments/assets/65aff2ec-cfa2-41a3-aaeb-38559e7037fe)
###

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
###
![Screenshot from 2025-03-03 04-50-22](https://github.com/user-attachments/assets/bf42a8e2-5be7-47b2-a601-5b04c1b5bc22)
###

### 🔹 **Why `codeEC2/` Directory?**
On **AWS EC2 servers**, creating directories and setting up dependencies can be time-consuming.  
The `codeEC2/` folder contains a **minimal version** of the application with just `server.py` and `index.html`.  
Users can **easily copy this directory** and start the server on EC2 without extra setup.
###
![Screenshot from 2025-03-03 04-52-01](https://github.com/user-attachments/assets/066f3787-2e71-460e-b0ba-a3d00a9bc445)
###
---

## ⚡ **How the Chat Application Works**
### 📡 **Sockets for Real-Time Communication**
- Unlike WebSockets, **traditional sockets** provide **low-level** network communication.
- The **server listens on a TCP socket** (`localhost:5555`).
- **Clients connect to the socket** and exchange messages **instantly**.
- Messages are **logged into AWS DynamoDB** for persistence.

### 🛠 **Key Features**
✅ **Real-time messaging** using **TCP sockets**.
###
![ScreenShot Tool -20250303044034 (1)](https://github.com/user-attachments/assets/b79ad1b8-81ad-4808-879e-aa5eef6d199a)
###
✅ **Authentication via 8-digit access codes**.  
###
![Screenshot from 2025-03-03 05-03-39](https://github.com/user-attachments/assets/f58a06cd-9741-4053-b76e-c3e2f7518b40)
###
![ScreenShot Tool -20250303051043 (1)](https://github.com/user-attachments/assets/6fb3df06-e187-4fce-8694-592cad862773)
###
✅ **DynamoDB logging** for session tracking & message storage.
###
![ScreenShot Tool -20250303051413](https://github.com/user-attachments/assets/10d80ed8-77a0-437e-8aab-f5a644e44c5a)
###
![ScreenShot Tool -20250303051508](https://github.com/user-attachments/assets/bec293de-50ae-41d9-9aa1-442fc1487688)
###
✅ **Ephemeral chat** (data is deleted when the server shuts down).
###
![Screenshot from 2025-03-03 05-18-02](https://github.com/user-attachments/assets/795250af-effa-49ac-b797-9428cdc3730b)
###
![ScreenShot Tool -20250303052020](https://github.com/user-attachments/assets/3525bef2-9b23-436f-8471-34a0aed7a8cb)
###
✅ **Docker support** for easy deployment.
###
![Screenshot from 2025-03-03 05-22-02 (1)](https://github.com/user-attachments/assets/964c65e1-1a8d-4057-855c-4e75d2e515ca)
###
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
