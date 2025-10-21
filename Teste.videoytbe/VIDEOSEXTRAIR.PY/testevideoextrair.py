from moviepy.editor import VideoFileClip

# Caminho do vídeo e do áudio de saída
caminho_video = r"C:\Users\Patty\Downloads\Patricio tratamento Thi Correia.MP3"  # Usando o prefixo 'r'
caminho_audio = r"C:\Users\Patty\Downloads\audio_extraido.mp3"

# Carregar o vídeo e extrair o áudio
video = VideoFileClip(caminho_video)
audio = video.audio
audio.write_audiofile(caminho_audio)

# Liberar recursos
audio.close()
video.close()

print("Áudio extraído com sucesso!")
