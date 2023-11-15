from gtts import gTTS
import os

def main(teks):
  tts = gTTS(text=teks, lang="id")
  audio_folder = os.path.join(os.path.dirname(__file__), "audio")  # Menggunakan jalur relatif ke folder 'audio' di dalam 'src'
  audio_path = os.path.join(audio_folder, "suara.mp3")

  # Pastikan folder 'audio' ada
  os.makedirs(audio_folder, exist_ok=True)

  tts.save(audio_path)
  return audio_path