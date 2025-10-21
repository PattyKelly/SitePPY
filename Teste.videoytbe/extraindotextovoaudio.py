import os
from pydub import AudioSegment
import speech_recognition as sr

# Configurar o caminho do FFmpeg e do ffprobe
AudioSegment.converter = r"C:\Users\Patty\Desktop\PY\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\Users\Patty\Desktop\PY\ffprobe.exe"

# Caminhos dos arquivos
mp4_path = r"C:\Users\Patty\Downloads\MP4\Atividades Thi Silva - 2024_12_24 10_00 GMT-03_00 - Recording.mp4"
wav_path = r"C:\Users\Patty\Downloads\MP4\Atividades Thi Silva - 2024_12_24 10_00 GMT-03_00 - Recording.wav"

# Verificar se o arquivo MP4 existe
if not os.path.exists(mp4_path):
    raise FileNotFoundError(f"O arquivo MP4 não foi encontrado no caminho: {mp4_path}")

# Verificar se o FFmpeg e o ffprobe estão acessíveis
if not os.path.exists(AudioSegment.converter):
    raise FileNotFoundError(f"O executável FFmpeg não foi encontrado no caminho: {AudioSegment.converter}")
if not os.path.exists(AudioSegment.ffprobe):
    raise FileNotFoundError(f"O executável ffprobe não foi encontrado no caminho: {AudioSegment.ffprobe}")

# Extrair o áudio do MP4 e salvar como WAV
try:
    audio = AudioSegment.from_file(mp4_path, format="mp4")
    audio.export(wav_path, format="wav")
    print(f"Áudio extraído com sucesso: {wav_path}")
except Exception as e:
    print(f"Erro ao extrair o áudio do MP4: {e}")
    raise

# Inicializar o reconhecedor de fala
r = sr.Recognizer()

# Carregar o arquivo WAV e preparar para a transcrição
try:
    with sr.AudioFile(wav_path) as source:
        audio_data = r.record(source)
except Exception as e:
    print(f"Erro ao carregar o arquivo WAV: {e}")
    raise

# Tentar reconhecer o áudio usando a API do Google
try:
    texto = r.recognize_google(audio_data, language="pt-BR")
    print("Texto extraído:", texto)
except sr.RequestError as e:
    print(f"Erro na requisição ao serviço: {e}")
except sr.UnknownValueError:
    print("Não foi possível compreender o áudio.")
