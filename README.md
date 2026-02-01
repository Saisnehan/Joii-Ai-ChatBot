
Go to Twilio’s website.

Sign up and verify your account.

Get a Twilio phone number with WhatsApp capabilities.

2. Set Up Python Environment

Create a virtual environment.

Install required libraries: Flask, Twilio, python-dotenv, OpenAI, schedule.

3. Get Twilio Credentials

From the Twilio console, copy:

Account SID

Auth Token

WhatsApp-enabled phone number

Save them into a .env file.

4. Get OpenAI API Key (ChatGPT API)

Go to OpenAI API keys page.

Create a new key.

Save it in .env.

5. Build the Flask Application

Create a Flask app that:

Receives messages via Twilio webhook.

Parses reminder commands with regex.

Schedules reminders using threading/schedule.

Uses ChatGPT API for general responses.

6. Expose Flask App to the Internet

Run the Flask app locally.

Use ngrok to expose it to the internet.

Copy the HTTPS URL provided by ngrok.

7. Configure Twilio Webhook

Go to Twilio Console → Messaging → WhatsApp.

Set the Webhook URL to your ngrok HTTPS URL followed by /whatsapp.

8. Test Your Chatbot

Send a WhatsApp message to your Twilio number.

Example queries:

“What is Python?” → AI response from ChatGPT.

“Remind me at 10:30 pm to drink water” → Scheduled reminder on WhatsApp.
