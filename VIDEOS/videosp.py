from moviepy.editor import TextClip

# Criar um clipe de texto para teste
text_clip = TextClip("Teste do ImageMagick com MoviePy", fontsize=50, color='white', size=(640, 360))
text_clip = text_clip.set_duration(5)

# Salvar o vídeo
text_clip.write_videofile("teste_imagemagick.mp4", fps=24)
