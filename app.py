from flask import Flask, render_template, request, jsonify
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

recomendacoes = {
    "fantasia": ["O Senhor dos Anéis", "Eragon", "As Crônicas de Nárnia"],
    "romance": ["Orgulho e Preconceito", "Como Eu Era Antes de Você", "A Culpa é das Estrelas"],
    "mistério": ["O Código Da Vinci", "Assassinato no Expresso do Oriente", "Garota Exemplar"],
    "terror": ["O Iluminado", "Drácula", "It: A Coisa"],
    "história": ["Guerra e Paz", "Os Pilares da Terra", "A Catedral do Mar"],
    "biografia": ["Steve Jobs", "O Diário de Anne Frank", "Longa Caminhada até a Liberdade"],
    "autoajuda": ["O Poder do Hábito", "Os 7 Hábitos das Pessoas Altamente Eficazes", "Mindset"],
    "filosofia": ["O Mundo de Sofia", "Meditações", "Assim Falou Zaratustra"],
    "ciência": ["Uma Breve História do Tempo", "Cosmos", "O Gene"],
    "negócios": ["Pai Rico, Pai Pobre", "A Startup Enxuta", "Do Mil ao Milhão"],
    "infantil": ["O Pequeno Príncipe", "Alice no País das Maravilhas", "Onde Vivem os Monstros"],
    "jovem": ["Harry Potter", "Jogos Vorazes", "Cidades de Papel"],
    "quadrinhos": ["Watchmen", "Turma da Mônica Jovem", "Naruto"],
    "poesia": ["Alguma Poesia", "A Rosa do Povo", "Sentimento do Mundo"],
}

ultimo_genero_recomendado = None
recomendacoes_dadas = set()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global ultimo_genero_recomendado
    data = request.get_json()

    if not data or 'message' not in data:
        return jsonify({'response': 'Erro: nenhuma mensagem recebida.'}), 400

    user_message = data['message']
    resposta = gerar_resposta(user_message)
    return jsonify({"response": resposta})

def gerar_resposta(mensagem):
    global ultimo_genero_recomendado, recomendacoes_dadas

    mensagem = mensagem.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(mensagem)
    stop_words = set(stopwords.words('portuguese'))
    palavras_filtradas = [palavra for palavra in tokens if palavra not in stop_words]

    if any(p in palavras_filtradas for p in ["li", "lido", "já", "conheço", "sim", "com certeza", "claro", "outro", "outra", "exemplo", "sugestão", "sugestao", "ja"]):
        if ultimo_genero_recomendado and ultimo_genero_recomendado in recomendacoes:
            sugestoes = [livro for livro in recomendacoes[ultimo_genero_recomendado] if livro not in recomendacoes_dadas]
            if sugestoes:
                nova_sugestao = sugestoes[0]
                recomendacoes_dadas.add(nova_sugestao)
                return f"Entendi! Que tal então '{nova_sugestao}'?"
            else:
                return "Acho que já sugeri todos os que conheço desse gênero! Quer tentar outro estilo de leitura?"
        else:
            return "Certo! Me diga um estilo de livro que você curte, e posso sugerir algo diferente."

    if any(p in palavras_filtradas for p in ["gostei", "curti", "legal", "bom", "massa", "show", "adorei", "interessante"]):
        if ultimo_genero_recomendado and ultimo_genero_recomendado in recomendacoes:
            sugestoes = [livro for livro in recomendacoes[ultimo_genero_recomendado] if livro not in recomendacoes_dadas]
            if sugestoes:
                nova_sugestao = sugestoes[0]
                recomendacoes_dadas.add(nova_sugestao)
                return f"Fico feliz que tenha gostado! Caso queira ajuda em algo mais é só falar!"
            else:
                return "Fico feliz que tenha gostado! Mas acho que já sugeri todos os livros desse gênero. Quer tentar outro estilo?"
        else:
            return "Que ótimo saber disso! Me diz outro gênero que você gosta pra eu sugerir mais livros legais."

    categorias = {
        "fantasia": ["ficção", "fantasia", "aventura"],
        "romance": ["romance", "amor", "relacionamento"],
        "mistério": ["mistério", "suspense", "detetive"],
        "terror": ["terror", "medo", "horror"],
        "história": ["história", "histórico", "época"],
        "biografia": ["biografia", "vida", "real"],
        "autoajuda": ["autoajuda", "desenvolvimento", "motivação"],
        "filosofia": ["filosofia", "pensamento", "reflexão"],
        "ciência": ["ciência", "universo", "tecnologia"],
        "negócios": ["negócios", "empreendedorismo", "carreira"],
        "infantil": ["infantil", "crianças", "conto"],
        "jovem": ["jovem", "juvenil", "adolescente"],
        "quadrinhos": ["quadrinhos", "hq", "mangá"],
        "poesia": ["poesia", "poema", "verso"],
    }

    for genero, palavras in categorias.items():
        if any(p in palavras_filtradas for p in palavras):
            ultimo_genero_recomendado = genero
            recomendacoes_dadas = set()
            livro = recomendacoes[genero][0]
            recomendacoes_dadas.add(livro)
            return f"Recomendo '{livro}'! Já ouviu falar?"

    if any(p in palavras_filtradas for p in ["recomenda", "indica", "sugere"]):
        return "Claro! Me diga que tipo de livro você gosta: romance, mistério, aventura, etc."
    elif any(p in palavras_filtradas for p in ["autor", "escritor", "escreveu"]):
        return "Você está procurando um autor específico? Posso ajudar a encontrar!"
    elif any(p in palavras_filtradas for p in ["biblioteca", "livraria", "livros"]):
        return "Aqui é o lugar certo! Me diga o que você gosta e te recomendo ótimos livros."
    elif any(p in palavras_filtradas for p in ["oi", "olá", "eai"]):
        return "Olá! Eu sou um assistente literário. Que tipo de livro você gosta de ler?"
    else:
        return "Desculpe, não entendi muito bem. Você pode me dizer o tipo de livro que gosta? Ex: romance, aventura, mistério..."

if __name__ == "__main__":
    app.run(debug=True)
