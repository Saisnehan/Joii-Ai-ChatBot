import os
import re
import threading
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client as TwilioClient
from openai import OpenAI
from difflib import get_close_matches
import traceback

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
TW_SID = os.getenv("TWILIO_ACCOUNT_SID")
TW_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TW_FROM = os.getenv("TWILIO_WHATSAPP")
TW_TO = os.getenv("USER_WHATSAPP")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")

openai_client = OpenAI(api_key=OPENAI_KEY) if OPENAI_KEY else None
twilio_client = TwilioClient(TW_SID, TW_TOKEN)

app = Flask(__name__)

def send_message(body):
    try:
        twilio_client.messages.create(from_=TW_FROM, body=body, to=TW_TO)
        print(f"[{datetime.now().isoformat()}] ✅ Sent: {body}")
    except Exception as e:
        print(f"[{datetime.now().isoformat()}] ERROR sending message: {e}")
        traceback.print_exc()

def schedule_custom_reminder(reminder_time: datetime, reminder_text: str):
    delay = (reminder_time - datetime.now()).total_seconds()
    print(f"[{datetime.now().isoformat()}] Scheduling reminder in {delay:.1f}s -> {reminder_text}")
    if delay > 0:
        threading.Timer(delay, send_message, args=[f"⏰ Reminder: {reminder_text}"]).start()
        return True
    else:
        print("[WARN] Not scheduling: time is in the past.")
        return False

def parse_time_str_to_datetime(time_str, ampm=None, base_date=None):
    base = base_date or datetime.now()
    time_str = time_str.strip()
    try:
        if ampm:
            dt = datetime.strptime(time_str + " " + ampm, "%I:%M %p")
        else:
            dt = datetime.strptime(time_str, "%H:%M")
        dt = dt.replace(year=base.year, month=base.month, day=base.day)
        if dt < datetime.now():
            dt += timedelta(days=1)
        return dt
    except Exception:
        return None

def parse_reminder(user_msg: str):
    s = user_msg.lower().strip()
    if not ("remind" in s or "reminder" in s or get_close_matches("remind", s.split(), n=1, cutoff=0.7)):
        return None, None

    m = re.search(r"remind(?: me)?(?: to)? (?P<task>.+?) in (?P<num>\d+)\s*(?P<unit>minutes|minute|hours|hour)s?", s)
    if m:
        task = m.group("task").strip()
        num = int(m.group("num"))
        unit = m.group("unit")
        delta = timedelta(minutes=num) if unit.startswith("minute") else timedelta(hours=num)
        return datetime.now() + delta, task

    m = re.search(r"remind(?: me|er|et)?(?: on)? (?P<day>\d{1,2})\s+(?P<month>\w+)\s+(?:at\s+)?(?P<time>\d{1,2}:\d{2})(?:\s*(?P<ampm>am|pm))?(?: to)? (?P<task>.+)", s)
    if m:
        day, month, time_str, ampm, task = m.group("day"), m.group("month"), m.group("time"), m.group("ampm"), m.group("task")
        date_str = f"{day} {month} {time_str} {ampm or ''}".strip()
        try:
            reminder_time = datetime.strptime(date_str, "%d %b %I:%M %p")
        except Exception:
            try:
                reminder_time = datetime.strptime(date_str, "%d %B %I:%M %p")
            except Exception:
                return None, None
        reminder_time = reminder_time.replace(year=datetime.now().year)
        if reminder_time < datetime.now():
            reminder_time = reminder_time.replace(year=reminder_time.year + 1)
        return reminder_time, task.strip()

    m = re.search(r"remind(?: me)?(?: to)? (?P<task>.+?) tomorrow(?: at (?P<time>\d{1,2}:\d{2})(?:\s*(?P<ampm>am|pm))?)?", s)
    if m and m.group("task"):
        task = m.group("task").strip()
        t = m.group("time")
        ampm = m.group("ampm")
        if t:
            dt = parse_time_str_to_datetime(t, ampm, base_date=datetime.now() + timedelta(days=1))
        else:
            dt = datetime.now() + timedelta(days=1)
        return dt, task

    m = re.search(r"remind(?: me)? tomorrow at (?P<time>\d{1,2}:\d{2})(?:\s*(?P<ampm>am|pm))?(?: to)? (?P<task>.+)", s)
    if m:
        time_str, ampm, task = m.group("time"), m.group("ampm"), m.group("task")
        dt = parse_time_str_to_datetime(time_str, ampm, base_date=datetime.now() + timedelta(days=1))
        return dt, task.strip()

    m = re.search(r"remind(?: me)? to (?P<task>.+?) at (?P<time>\d{1,2}:\d{2})(?:\s*(?P<ampm>am|pm))?", s)
    if m:
        task = m.group("task").strip()
        time_str = m.group("time")
        ampm = m.group("ampm")
        dt = parse_time_str_to_datetime(time_str, ampm)
        return dt, task

    m = re.search(r"remind(?: me|er|et)? at (?P<time>\d{1,2}:\d{2})(?:\s*(?P<ampm>am|pm))?(?: to)? (?P<task>.+)", s)
    if m:
        time_str = m.group("time")
        ampm = m.group("ampm")
        task = m.group("task").strip()
        dt = parse_time_str_to_datetime(time_str, ampm)
        return dt, task

    return None, None

def get_weather(city="New York,US"):
    if not WEATHER_API_KEY:
        return "Weather API not configured."
    try:
        city_q = requests.utils.quote(city)
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_q}&appid={WEATHER_API_KEY}&units=metric"
        resp = requests.get(url, timeout=8).json()
        if resp.get("main"):
            temp = resp["main"]["temp"]
            desc = resp["weather"][0]["description"]
            return f"🌤️ Weather in {city}: {temp}°C, {desc}"
        return "⚠️ Could not fetch weather data."
    except Exception as e:
        return f"⚠️ Error fetching weather: {e}"

@app.route("/", methods=["POST"])
def bot():
    user_msg = request.values.get("Body", "").strip()
    print(f"[{datetime.now().isoformat()}] Received -> {user_msg!r}")
    resp = MessagingResponse()

    reminder_time, reminder_text = parse_reminder(user_msg)
    if reminder_time and reminder_text:
        ok = schedule_custom_reminder(reminder_time, reminder_text)
        if ok:
            resp.message(f"✅ Reminder set for {reminder_time.strftime('%d %b %Y %H:%M')} to {reminder_text}")
        else:
            resp.message("⚠️ Could not schedule reminder (time in the past).")
        return str(resp)

    if "remind" in user_msg.lower() or "reminder" in user_msg.lower() or get_close_matches("remind", user_msg.lower().split(), n=1, cutoff=0.7):
        resp.message("⚠️ I detected a reminder request but couldn't understand the format. Try one of:\n"
                     "• Remind me to drink water at 8:10 pm\n"
                     "• Remind me at 20:10 to call Alex\n"
                     "• Remind me in 15 minutes to stretch\n"
                     "• Remind me on 25 Sep at 10:00 to submit project")
        return str(resp)

    lower = user_msg.lower()
    if "weather" in lower:
        m = re.search(r"weather(?: in (?P<city>.+))?", lower)
        city = m.group("city").strip() if m and m.group("city") else "New York,US"
        resp.message(get_weather(city))
        return str(resp)

    if not openai_client:
        resp.message("⚠️ OpenAI API key not configured — cannot answer general questions right now.")
        return str(resp)

    try:
        completion = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful WhatsApp assistant. Answer questions clearly. Do NOT claim to set reminders — the service handles reminders separately."},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=400
        )
        ai_reply = completion.choices[0].message.content
        resp.message(ai_reply)
    except Exception as e:
        print(f"OpenAI error: {e}")
        traceback.print_exc()
        resp.message("⚠️ Error contacting OpenAI. Try again later.")
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
