import telebot
import time
import os

# Botingiz tokini
TOKEN = "8643494585:AAFcDL6Y_YijDNK2Oys0DhUHR8Q1Io664MM"
bot = telebot.TeleBot(TOKEN)
DB_FILE = "users.txt"

# Foydalanuvchilar ro'yxatini yuklash
def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return [line.strip() for line in f if line.strip()]
    return []

# Yangi foydalanuvchini bazaga qo'shish
def save_user(user_id):
    users = load_users()
    if str(user_id) not in users:
        with open(DB_FILE, "a") as f:
            f.write(f"{user_id}\n")

# Adminlikni tekshirish
def is_admin(message):
    try:
        status = bot.get_chat_member(message.chat.id, message.from_user.id).status
        return status in ['administrator', 'creator']
    except:
        return False

# Har bir xabarni kuzatib, foydalanuvchilarni eslab qolish
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    if message.from_user and not message.from_user.is_bot:
        save_user(message.from_user.id)

    # Utag buyrug'i (faqat adminlar uchun)
    if message.text == '/utag':
        if is_admin(message):
            user_ids = load_users()
            if not user_ids:
                bot.send_message(message.chat.id, "❌ Ro'yxat bo'sh. O'yinchilar guruhda xabar yozishi kerak.")
                return
            
            bot.send_message(message.chat.id, "🚀 **KRYPTON MAFIA: Utag boshlandi...**")
            
            for uid in user_ids:
                try:
                    u = bot.get_chat_member(message.chat.id, int(uid)).user
                    if u.username:
                        bot.send_message(message.chat.id, f"@{u.username}")
                    else:
                        # Username bo'lmasa, ismi orqali chaqirish
                        link = f"[{u.first_name}](tg://user?id={uid})"
                        bot.send_message(message.chat.id, link, parse_mode="Markdown")
                    
                    time.sleep(0.5) # Bot bloklanib qolmasligi uchun pauza
                except Exception as e:
                    continue
        else:
            bot.reply_to(message, "⛔️ Bu buyruq faqat adminlar uchun!")

print("Krypton Bot GitHub-ga yuklashga tayyor...")
bot.infinity_polling()
                      
