import os
import logging
import traceback
from datetime import datetime
from moviepy.editor import (
    VideoFileClip,
    concatenate_videoclips,
    TextClip,
    CompositeVideoClip,
    AudioFileClip,
    CompositeAudioClip
)
from moviepy.audio.fx.all import audio_loop
from moviepy.config import change_settings

# -----------------------------------------------------------------------------
# CONFIGURAÇÕES E CAMINHOS
# -----------------------------------------------------------------------------

# Configurar logging
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

# Caminho completo do ImageMagick
IMAGEMAGICK_PATH = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_PATH})

# Determinar o caminho base do ano e da data de hoje
base_path = r"C:\Users\Patty\Desktop\YT\BEFREE\Automatic\2025"
today_date = datetime.now().strftime("%Y-%m-%d")  # Data de hoje no formato YYYY-MM-DD
day_folder = os.path.join(base_path, today_date)

# Determinar os caminhos das subpastas automaticamente
video_folder = os.path.join(day_folder, "Video")
subtitle_file = os.path.join(day_folder, "Legenda", "legenda.txt")
music_file = os.path.join(day_folder, "Music", "music.mp3")
output_folder = os.path.join(base_path, "Prontos")

# Caminho para a música de fundo suave adicional
background_music_file = r"C:\Users\Patty\Desktop\YT\BEFREE\Automatic\2025\2025-01-14\Music\Piano Suave Reflexão Happy\inspirational-uplifting-calm-piano-254764.mp3"

# Nome do arquivo final
output_filename = f"Video_{today_date}.mp4"

# -----------------------------------------------------------------------------
# FUNÇÕES
# -----------------------------------------------------------------------------

def merge_videos(video_folder):
    """
    Lê todos os arquivos .mp4 em 'video_folder', ordena e concatena usando o MoviePy.
    Retorna o objeto concatenado (VideoFileClip).
    """
    video_files = sorted(
        [os.path.join(video_folder, f) for f in os.listdir(video_folder) if f.endswith(".mp4")]
    )

    if not video_files:
        raise FileNotFoundError("Nenhum vídeo encontrado na pasta de entrada!")

    logging.info(f"Vídeos encontrados: {video_files}")
    clips = [VideoFileClip(video) for video in video_files]
    merged_clip = concatenate_videoclips(clips, method="compose")
    return merged_clip


def create_intro_clips(video_size):
    """
    Cria clipes de texto para a introdução do vídeo. 
    Cada clipe possui duração específica e posicionamento.
    Retorna uma lista de TextClip.
    """
    intro_clips = []

    # "Be Free" (6 segundos)
    clip1 = TextClip(
        "Be Free",
        fontsize=90,
        font="Arial-Bold",
        color="white",
        stroke_color="black",
        stroke_width=3,
        size=(video_size[0] - 100, None),
        method="caption",
    ).set_position("center").set_duration(6)
    intro_clips.append(clip1)

    # "Presents" (6 segundos após "Be Free")
    clip2 = TextClip(
        "Presents",
        fontsize=70,
        font="Arial-Bold",
        color="white",
        stroke_color="black",
        stroke_width=3,
        size=(video_size[0] - 100, None),
        method="caption",
    ).set_position("center").set_start(6).set_duration(6)
    intro_clips.append(clip2)

    # Mensagem de incentivo (8 segundos)
    clip3 = TextClip(
        "Ajude esse pequeno canal\nSabia que 99% das pessoas que assistem não se inscrevem? 🤔\nSeja diferente, faça parte do 1%! 😉",
        fontsize=50,
        font="Arial-Bold",
        color="white",
        stroke_color="black",
        stroke_width=2,
        size=(video_size[0] - 100, None),
        method="caption",
    ).set_position("center").set_start(12).set_duration(8)
    intro_clips.append(clip3)

    return intro_clips


def add_subtitles_with_intervals(video_clip, subtitle_file):
    """
    Lê as linhas do arquivo de legenda e cria clipes de texto, cada um com duração proporcional
    à quantidade de linhas. Cada legenda é exibida em sequência, com crossfade.
    Retorna um CompositeVideoClip com as legendas adicionadas.
    """
    if not os.path.exists(subtitle_file):
        raise FileNotFoundError(f"Legenda não encontrada: {subtitle_file}")

    with open(subtitle_file, "r", encoding="utf-8") as f:
        subtitles = f.readlines()

    if not subtitles:
        logging.warning("Nenhuma legenda encontrada no arquivo.")
        return video_clip

    interval = video_clip.duration / max(len(subtitles), 1)
    clips = []

    for i, line in enumerate(subtitles):
        line = line.strip()

        # Aumentamos um pouco a fonte para melhor leitura
        txt_clip = TextClip(
            line,
            fontsize=80,  # Aumentado de 70 para 80
            font="Arial-Bold",
            color="white",
            stroke_color="black",
            stroke_width=3,
            method="caption",
            size=(video_clip.size[0] - 100, None),
            bg_color="rgba(0, 0, 0, 0.5)",
        ).set_position(
            # Subindo um pouco para ficar mais visível
            ("center", video_clip.size[1] - 200)
        ).set_duration(interval).set_start(i * interval).crossfadein(0.5).crossfadeout(0.5)

        clips.append(txt_clip)

    video_with_subtitles = CompositeVideoClip([video_clip] + clips)
    return video_with_subtitles


def add_music_and_bg(video_clip, main_music_file, bg_music_file):
    """
    Adiciona duas trilhas de música ao vídeo:
      1. Música principal (main_music_file), que inicia após 6s.
      2. Música de fundo (bg_music_file), também com loop ou corte, em volume reduzido.

    Retorna um VideoClip (ou CompositeVideoClip) com áudio composto.
    """
    if not os.path.exists(main_music_file):
        raise FileNotFoundError(f"Música principal não encontrada: {main_music_file}")
    if not os.path.exists(bg_music_file):
        raise FileNotFoundError(f"Música de fundo não encontrada: {bg_music_file}")

    logging.info(f"Música principal: {main_music_file}")
    logging.info(f"Música de fundo: {bg_music_file}")

    # Carrega as faixas
    main_audio = AudioFileClip(main_music_file).set_start(6)
    bg_audio = AudioFileClip(bg_music_file).set_start(6)

    # Ajustar duração das faixas ao vídeo
    # Se a música for menor, repete; se for maior, corta.
    def adjust_audio(audio, duration):
        if audio.duration < duration:
            audio = audio_loop(audio, duration=duration)
        elif audio.duration > duration:
            audio = audio.subclip(0, duration)
        return audio

    main_audio = adjust_audio(main_audio, video_clip.duration)
    bg_audio = adjust_audio(bg_audio, video_clip.duration)

    # Ajustar volumes (ex.: música de fundo 30% do volume)
    main_audio = main_audio.volumex(1.0)
    bg_audio = bg_audio.volumex(0.3)

    # Mesclar as duas faixas em um CompositeAudioClip
    final_audio = CompositeAudioClip([main_audio, bg_audio])
    final_clip = video_clip.set_audio(final_audio)
    return final_clip


def process_videos(video_folder, subtitle_file, music_file, bg_music_file, output_folder):
    """
    Fluxo principal de processamento:
      1. Junta vídeos
      2. Cria introdução
      3. Adiciona legendas
      4. Mensagem final
      5. Adiciona as duas trilhas de música
      6. Redimensiona para 1920x1080 (opcional)
      7. Salva vídeo final
    """
    try:
        logging.info("Juntando vídeos...")
        merged_video = merge_videos(video_folder)
        logging.info("Vídeos juntados com sucesso.")

        logging.info("Criando introdução...")
        intro_clips = create_intro_clips(merged_video.size)
        intro = concatenate_videoclips(intro_clips)

        logging.info("Adicionando legendas...")
        video_with_subtitles = add_subtitles_with_intervals(merged_video, subtitle_file)
        logging.info("Legendas adicionadas com sucesso.")

        logging.info("Adicionando mensagem final...")
        final_message = TextClip(
            "Gostou do vídeo? 😊 Deixe seu like e inscreva-se no canal para me ajudar a crescer! 🚀",
            fontsize=50,
            font="Arial-Bold",
            color="white",
            stroke_color="black",
            stroke_width=2,
            size=(merged_video.size[0] - 100, None),
            method="caption",
        ).set_position("center").set_duration(6)

        outro = CompositeVideoClip([
            video_with_subtitles,
            final_message.set_start(video_with_subtitles.duration)
        ])

        logging.info("Adicionando música principal e música de fundo...")
        final_video = add_music_and_bg(outro, music_file, bg_music_file)
        logging.info("Músicas adicionadas ao vídeo.")

        # Exemplo para padronizar a resolução final em 1080p:
        # Se não quiser redimensionar, comente ou remova a linha abaixo.
        final_video = final_video.resize((1920, 1080))

        # Garantir que a pasta de saída exista
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, output_filename)

        logging.info(f"Salvando vídeo final em: {output_path}...")
        final_video.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            fps=30
        )
        logging.info(f"Processamento concluído! Vídeo salvo em: {output_path}")

    except Exception as e:
        logging.error(f"Ocorreu um erro durante o processamento: {e}")
        traceback.print_exc()


def main():
    """
    Ponto de entrada principal do script.
    """
    logging.info(f"Caminho do vídeo: {video_folder}")
    logging.info(f"Caminho da legenda: {subtitle_file}")
    logging.info(f"Caminho da música principal: {music_file}")
    logging.info(f"Caminho da música de fundo: {background_music_file}")
    logging.info(f"Pasta de saída: {output_folder}")

    process_videos(
        video_folder,
        subtitle_file,
        music_file,
        background_music_file,
        output_folder
    )


if __name__ == "__main__":
    main()
