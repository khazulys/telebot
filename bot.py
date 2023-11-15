import telebot
from telebot import types
from src.cek_resi import status_detail, get_history
from src.tts import main

bot = telebot.TeleBot("6761159331:AAHLaTrCnr_TAtrTA0x2BW7SGKrQIUs8P8I")

user_status = {}

# Membuat keyboard inline untuk submenu
def create_tracking_submenu():
  keyboard = types.InlineKeyboardMarkup(row_width=2)
  jne_button = types.InlineKeyboardButton(text="JNE", callback_data='track_jne')
  jnt_button = types.InlineKeyboardButton(text="JNT", callback_data='track_jnt')
  # Tambahkan tombol kurir lainnya di sini
  keyboard.add(jne_button, jnt_button)
  return keyboard

# Membuat keyboard inline utama
def create_main_keyboard():
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  lacak_button = types.KeyboardButton(text="🚚 Lacak Paket")
  tts_button = types.KeyboardButton(text="🗣 Text to Speech")
  keyboard.add(lacak_button, tts_button)
  return keyboard

# Menanggapi perintah /start
@bot.message_handler(commands=['start'])
def handle_start(message):
  username = message.from_user.username
  main_keyboard = create_main_keyboard()
  bot.send_message(message.chat.id, f"Hai @{username}, mau ngapain?", reply_markup=main_keyboard)

# Menanggapi callback dari tombol di dalam keyboard inline
@bot.message_handler(func=lambda message: True)
def handle_message(message):
  chat_id = message.chat.id

  if message.text == '🚚 Lacak Paket':
    # Menampilkan submenu lacak paket
    submenu_keyboard = create_tracking_submenu()
    bot.send_message(
      chat_id,
      "Pilih kurir untuk melacak paket:",
      reply_markup=submenu_keyboard
    )
  
  if message.text == "🗣 Text to Speech":
    bot.send_message(chat_id, "Ketikan teks yang mau diconvert ke suara bang")
    user_status[chat_id] = {"teks": message.text, "status": "waiting_for_convert"} 
  
  elif user_status.get(chat_id) and user_status[chat_id]["status"] == "waiting_for_convert":
    del user_status[chat_id]
    user_status[chat_id] = {"teks":message.text}
    #bot.send_message(chat_id, user_status[chat_id]["teks"]
    audio_path = main(user_status[chat_id]["teks"])
    
    audio_file = open(audio_path, "rb")
    bot.send_audio(chat_id, audio_file)
    del user_status[chat_id]

  if user_status.get(chat_id) and user_status[chat_id]['status'] == 'waiting_for_resi':
    chosen_courier = user_status[chat_id]['courier']
    tracking_number = message.text.upper()  # Menggunakan huruf besar untuk memudahkan pembandingan
    if chosen_courier == 'jne':
      result = status_detail(chosen_courier, tracking_number)
      if result:
        (
          courier, service, status,
          date, desc, weight,
          origin, destination, shipper, receiver
        ) = result

      history = get_history(chosen_courier, tracking_number)
      
      batas = "="*16
      text = f"Informasi Paket Kamu\n{batas}\n\nKurir : {courier}\nLayanan : {service}\nStatus : {status}\nTanggal : {date}\nBarang : {desc}\nBerat : {weight}\n\nKota asal : {origin}\nKota Tujuan : {destination}\nPengirim : {shipper}\nPenerima : {receiver}\n\nHistori Perjalanan\n{batas}\n\nStatus : {history}"
      bot.send_message(chat_id, text)
      #bot.send_message(chat_id, history)
      del user_status[chat_id]
      # Mengirim pesan "Coming soon" dan menghapus status pengguna
      

@bot.callback_query_handler(func=lambda call: True)
def handle_inline_callback(call):
  chat_id = call.message.chat.id
  
  if call.data.startswith('track_'):
    # Menanggapi pemilihan kurir
    chosen_courier = call.data.replace('track_', '')
    bot.send_message(chat_id, "Kirim nomor resinya bang 😁")
    
    # Mengubah status pengguna menjadi "waiting_for_resi"
    user_status[chat_id] = {'courier': chosen_courier, 'status': 'waiting_for_resi'}

  #bot.send_message(chat_id, user_message[chat_id])

# Menjalankan bot
bot.polling(none_stop=True)
