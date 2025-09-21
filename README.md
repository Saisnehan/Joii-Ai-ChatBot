# Joii-Ai-ChatBot
A WhatsApp chatbot built with Flask, Twilio, and OpenAI’s ChatGPT API. Supports natural language reminders like “Remind me at 8:30 pm to drink water” and delivers WhatsApp notifications. Also answers general queries using ChatGPT, combining productivity with intelligent conversation in one assistant.
WhatsApp Chatbot with Reminders & ChatGPT

This project is a WhatsApp chatbot built using Flask, Twilio, and OpenAI’s ChatGPT API.
It allows users to:

✅ Set personal reminders via WhatsApp (e.g., “Remind me at 10:30 pm to drink water”).

🤖 Chat with AI to get instant answers powered by ChatGPT (e.g., “What is Python?”).

⏰ Receive scheduled WhatsApp notifications for reminders using threading.Timer.

🌍 Easily extend with APIs (e.g., weather, news, etc.).

🚀 Features

Twilio WhatsApp integration.

ChatGPT API for intelligent responses.

Natural language reminder parsing (time + task).

Flask server with webhook handling.

Background reminder scheduling.

🛠️ Tech Stack

Flask → Web server to handle WhatsApp messages.

Twilio API → Send & receive WhatsApp messages.

OpenAI GPT → AI-powered responses.

Python threading + schedule → Reminder scheduling.
