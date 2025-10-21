from cs50 import get_string
from flask import Flask, render_template


# a = 2
# b = 3
# print(a + b)
# print ( a - b )
# Acho = 1
# Que = 3
# estou = 5 
# Bem = 7
# print (Acho + Que + estou + Bem)


#APENASUMTESTE
def perguntas_():
    # Dicionario com Perguntas
    Perguntas_dict = {
        "Qual é o nome do gato azul mais divertido?" : "Gumball",
        "Qual é a árvore mais alta do mundo?" : "Sequoia",
        "Qual a palavra menos falada no mundo?" : "Perdão",
        "Qual o segundo nome do Tinho?":"Bart",
        "Qual o segundo nome do Tinho?":"Bart",
        "Qual o segundo nome do Tinho?":"Bart"
        }
# Loop para apresentar perguntas e obter respostas
    for pergunta, resposta_correta in Perguntas_dict.items():
        resposta_usuario = input(pergunta + " ")
        # Verificar se a resposta está correta
        if resposta_usuario.lower() == resposta_correta.lower():
            print("Resposta correta!\n")
        else:
            print(f"Resposta incorreta. A resposta correta é: {resposta_correta}\n")

app = Flask(__name__)

@app.route('/xx')
def index():
    return render_template('hello_world.html')

if __name__ == '__main__':
    app.run(debug=True)
