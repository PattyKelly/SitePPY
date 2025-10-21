import subprocess
import os

# ========== CONFIGURAÇÃO ==========
# Pasta do áudio original .weba
PASTA_MP3 = r"C:\Users\Patty\Desktop\Videos Automatics PY\Video da Chuva\MP3"
AUDIO_WEBA = os.path.join(PASTA_MP3, "videoplayback.weba")
AUDIO_MP3 = os.path.join(PASTA_MP3, "chuva_9h_sem_trovao.mp3")  # Nome novo após conversão

# Pasta de saída do vídeo pronto
PASTA_OUT = r"C:\Users\Patty\Desktop\Videos Automatics PY\Video da Chuva\Video finalizado"
os.makedirs(PASTA_OUT, exist_ok=True)
VIDEO_FINAL = os.path.join(PASTA_OUT, "chuva_9h_video_preto.mp4")

def rodar(cmd):
    print("\n>>>", " ".join(cmd))
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for linha in proc.stdout:
        print(linha, end="")
    proc.wait()
    if proc.returncode != 0:
        raise Exception("Erro ao executar: " + " ".join(cmd))
    print("\n✅ Comando finalizado.\n")

def converter_weba_para_mp3(audio_weba, audio_mp3):
    if os.path.exists(audio_mp3):
        print("Áudio MP3 já existe, pulando conversão.")
        return
    print("\n🚩 Convertendo .weba para .mp3...")
    cmd = [
        "ffmpeg", "-y",
        "-i", audio_weba,
        "-vn",
        "-ar", "44100",  # Taxa de amostragem padrão
        "-ac", "2",      # Estéreo
        "-b:a", "192k",
        audio_mp3
    ]
    rodar(cmd)

def pegar_duracao_audio(audio_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())

def criar_video_preto(audio_path, video_out):
    duracao = pegar_duracao_audio(audio_path)
    print(f"\n🚩 Gerando vídeo preto de {duracao/3600:.2f} horas...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"color=c=black:s=1920x1080:d={duracao}",
        "-i", audio_path,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-b:a", "256k",
        "-shortest",
        video_out
    ]
    rodar(cmd)
    print(f"\n🎉 Vídeo final pronto: {video_out}")

if __name__ == "__main__":
    try:
        converter_weba_para_mp3(AUDIO_WEBA, AUDIO_MP3)
        criar_video_preto(AUDIO_MP3, VIDEO_FINAL)
        print("\nTudo certo, vídeo gerado e salvo!")
    except Exception as e:
        print("\n❌ Erro:", e)
