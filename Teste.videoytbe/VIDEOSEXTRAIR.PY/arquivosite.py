import streamlit as st
from moviepy.editor import VideoFileClip
import tempfile

# Configuração da interface do Streamlit
st.title("Extrator de Áudio de Vídeos")
st.write("Faça o upload de um vídeo em MP4 e baixe o áudio extraído em MP3.")

# Upload do vídeo pelo usuário
video_file = st.file_uploader("Carregue seu vídeo em MP4", type=["mp4"])

if video_file:
    # Cria um arquivo temporário para armazenar o vídeo
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(video_file.read())
        caminho_video = temp_video.name

    # Extrai o áudio do vídeo e salva em um arquivo temporário MP3
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        caminho_audio = temp_audio.name

    # Carregar o vídeo e extrair o áudio
    video = VideoFileClip(caminho_video)
    audio = video.audio
    audio.write_audiofile(caminho_audio)

    # Libera os recursos
    audio.close()
    video.close()

    # Permitir o download do áudio extraído
    with open(caminho_audio, "rb") as file:
        st.download_button(
            label="Baixar Áudio em MP3",
            data=file,
            file_name="audio_extraido.mp3",
            mime="audio/mp3"
        )

    st.success("Áudio extraído com sucesso!")
