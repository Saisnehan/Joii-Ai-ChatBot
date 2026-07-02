


# 🤖 Joii AI ChatBot

Joii AI ChatBot is a smart WhatsApp chatbot built using **Python**, **Flask**, **Twilio**, and **OpenAI GPT**. It can answer general questions using AI and schedule WhatsApp reminders from natural language commands.

## ✨ Features

- 💬 AI-powered conversations using OpenAI GPT
- 📱 WhatsApp messaging with Twilio API
- ⏰ Natural language reminder scheduling
- 🔔 Automatic WhatsApp reminder notifications
- 🌐 Flask web server for webhook handling
- ⚡ Simple and lightweight architecture

## 🛠️ Tech Stack

- Python
- Flask
- Twilio API
- OpenAI API
- APScheduler
- python-dotenv

## 📂 Project Structure

```
Joii-AI-ChatBot/
│
├── .env                 # Environment variables
├── joii.py              # Main Flask application
├── README.md
└── requirements.txt
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Saisnehan/Joii-Ai-ChatBot.git
cd Joii-Ai-ChatBot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file and add:

```env
OPENAI_API_KEY=your_openai_api_key
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=your_twilio_whatsapp_number
```

### 5. Run the application

```bash
python joii.py
```

## 📱 Example Commands

Ask anything:

```
What is Artificial Intelligence?
```

Create reminders:

```
Remind me at 8:30 PM to drink water
```

```
Remind me tomorrow at 9 AM to attend the meeting
```

## 📸 Screenshots

Add screenshots of your chatbot conversation here.

## 🚀 Future Enhancements

- Voice message support
- Multi-language conversations
- Reminder management (edit/delete)
- Database integration
- User authentication
- Conversation history

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

## 👨‍💻 Author

**K Sai Snehan**

- GitHub: https://github.com/Saisnehan
- LinkedIn: https://www.linkedin.com/in/k-saisnehan/

## ⭐ Support

If you found this project helpful, consider giving it a ⭐ on GitHub.
