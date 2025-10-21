import subprocess

# Ajuste os caminhos dos seus arquivos
video_entrada = r"C:\Users\Patty\Desktop\Videos Automatics PY\Som da Chuva 9 horas.mp4"
audio_extraido = r"C:\Users\Patty\Desktop\Videos Automatics PY\chuva_9h.wav"
audio_estendido = r"C:\Users\Patty\Desktop\Videos Automatics PY\chuva_20h.wav"
video_saida = r"C:\Users\Patty\Desktop\Videos Automatics PY\chuva_20h_video.mp4"

def rodar_comando(cmd):
    print("Executando:", " ".join(cmd))
    processo = subprocess.run(cmd, capture_output=True, text=True)
    if processo.returncode != 0:
        print("Erro:", processo.stderr)
        raise Exception("Erro ao executar o comando")
    else:
        print("Sucesso:", processo.stdout)

def extrair_audio():
    cmd = [
        "ffmpeg",
        "-i", video_entrada,
        "-vn",
        "-acodec", "pcm_s16le",
        audio_extraido
    ]
    rodar_comando(cmd)

def esticar_audio():
    cmd = [
        "ffmpeg",
        "-i", audio_extraido,
        "-filter_complex", "atempo=2.0,atempo=1.11",
        audio_estendido
    ]
    rodar_comando(cmd)

def criar_video_preto():
    cmd = [
        "ffmpeg",
        "-f", "lavfi",
        "-i", "color=c=black:s=1920x1080:d=72000",
        "-i", audio_estendido,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        video_saida
    ]
    rodar_comando(cmd)

if __name__ == "__main__":
    try:
        extrair_audio()
        esticar_audio()
        criar_video_preto()
        print("Processo finalizado com sucesso!")
    except Exception as e:
        print("Erro geral:", e)
