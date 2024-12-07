# /*****************************************************************************************/
# Autor: Matheus Silva Rodrigues
# Componente Curricular: MI Algoritmos
# Concluido em: 08/12/2024
# Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
# trecho de código de outro colega ou de outro autor, tais como provindos de livros e
# apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
# de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
# do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.
# ******************************************************************************************/
# SO utilizado: Windows 10
# Bibliotecas utilizadas: JSON, RANDOM e TIME
# NÃO FUNCIONA EM CAPSLOOK
# Versão do Python: 3.13 em 64-bit
# ******************************************************************************************/

# Código modularizado em funções

# Bibliotecas utilizadas:
# JSON foi para ler os arquivos;
# time para temporizar o modo 2 do jogo;
# random foi para randomizar as perguntas de maneira aleatória
import json, time, random

# Função para carregar arquivo das perguntas e o hall da fama
# Utilizando tratamento de erros try exception e a biblitoeca json
def arquivosjs():
    try:
        with open("meuquiz.json", "r", encoding='utf-8') as arquivo:
            perguntas = json.load(arquivo)           
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        perguntas = []
    try:
        with open("hall.json", "r", encoding='utf-8') as arquivo:
            hall = json.load(arquivo)
    except FileNotFoundError:
        print("Arquivo não encontrado, criando um novo.")
        hall = {"questfixa": [],
                 "questemp": [],
                 "hardcore": []
                 }

    return perguntas, hall

# Função desenvolvida para salvar o Hall, caso não consiga ler o arquivo, ele desenvolve um novo na 
# mesma pasta do arquivo main.py
# A função mescla dados existentes com novos, ao invés de substituílos;
# A função garantir que não ultrapasse os 10 melhores

def salvar_hall(hall):
    try:
        with open("hall.json", "r", encoding='utf-8') as arquivo:
            dados_existentes = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        dados_existentes = {"questfixa": [], "questemp": [], "hardcore": []}

    for modo, jogadores in hall.items():
        if modo in dados_existentes:
            dados_existentes[modo] = jogadores
            jogadores_unicos = {jogador['nome']: jogador for jogador in dados_existentes[modo]}
            dados_existentes[modo] = list(jogadores_unicos.values())
            if modo == "questemp":
                dados_existentes[modo] = sorted(
                    dados_existentes[modo], key=lambda x: x["tempo"])[:10]
            else:
                dados_existentes[modo] = sorted(
                    dados_existentes[modo], key=lambda x: x["pontos"], reverse=True)[:10]
        else:
            dados_existentes[modo] = jogadores

    with open("hall.json", "w", encoding='utf-8') as arquivo:
        json.dump(dados_existentes, arquivo, indent=4, ensure_ascii=False)

# Função desenvolvida para apresentar o Hall da Fama
# A função pega os dados da função salvar_hall e retorna os 10 melhores jogadores
def mostrar_hall(hall):
    print("\n----------------- HALL DA FAMA -----------------")
    for modo, jogadores in hall.items():
        print(f"\nModo de jogo: {modo}")
        if modo == "questemp":
            for jogador in jogadores:
                print(f"[{jogador['nome']}]: Tempo: {jogador['tempo']} segundos")
        else:
            for jogador in jogadores:
                print(f"[{jogador['nome']}]: Pontuação: {jogador['pontos']}")

# Função principal do jogo, nela é coordenado todas as diretrizes principais, como os modos de jogos, as respostas,
# os resultados e a pré definição entre os pontos e as respostas certas, para definir o ranking e as ajudas surpresas.
def quiz(perguntas, modo, ajudas):
    respostas_certas = 0 
    pontos = 0
    inicio = time.time()
    random.shuffle(perguntas)

    for pergunta in perguntas:
        if modo == "questfixa" and pontos >= ajudas["questoes_fixas"]:
            break
        if modo == "questemp" and time.time() - inicio >= ajudas["tempoesgotado"]:
            print("Tempo esgotado!")
            break
        if modo == "hardcore" and pontos >= len(perguntas):
            break

        resultado = fazer_pergunta(pergunta, ajudas)
        if resultado is None:
            continue
        elif resultado:
            pontos += int(pergunta["value"])
            respostas_certas += 1 

            ajudanova(ajudas, respostas_certas)
        else:
            if modo == "hardcore":
                print("Você errou! Fim do jogo.")
                break
    if modo == "questemp":
        return round(time.time() - inicio, 2)
    return pontos

# Função para realizar as perguntas ao jogador, e administrar o menú e as opções de jogo.
def fazer_pergunta(pergunta, ajudas):
    print(f"\nCategoria: {pergunta['category']} (Valor: {pergunta['value']})")   
    print(pergunta['questionText'])

    alternativas = [pergunta[f"option{i}"] for i in range(1, 6) if f"option{i}" in pergunta]
    for i, opcao in enumerate(alternativas, start=1):
        print(f"{i}. {opcao}")

    ajuda_usada = {"dicas": False, "pularquestao": False, "eliminar": False}

    while True:
        # Montar o menu de ajuda dinamicamente
        print("\nAjuda disponível:")
        if ajudas['dicas'] > 0 and not ajuda_usada['dicas']:
            print(f"1. Usar dica ({ajudas['dicas']} restantes)")
        if ajudas['pularquestao'] > 0 and not ajuda_usada['pularquestao']:
            print(f"2. Pular questão ({ajudas['pularquestao']} restantes)")
        if ajudas['eliminar'] > 0 and not ajuda_usada['eliminar']:
            print(f"3. Eliminar opções erradas ({ajudas['eliminar']} restantes)")
        print("4. Responder")

        escolha = input("\nEscolha sua opção (1-4): ")

        if escolha == "1" and ajudas['dicas'] > 0 and not ajuda_usada['dicas']:
            print("Dica:", pergunta["hint"])
            ajudas['dicas'] -= 1
            ajuda_usada['dicas'] = True

        elif escolha == "2" and ajudas['pularquestao'] > 0 and not ajuda_usada['pularquestao']:
            print("Você pulou a questão!")
            ajudas['pularquestao'] -= 1
            return None

        elif escolha == "3" and ajudas['eliminar'] > 0 and not ajuda_usada['eliminar']:
            numeros = [str(i) for i in range(1, len(alternativas) + 1)]
            alternativas_numeros = {numeros[i]: op for i, op in enumerate(alternativas)}

            erradas = [
                numero for numero, texto in alternativas_numeros.items()
                if f"option{numero}" != pergunta["answer"]]

            removidas = random.sample(erradas, len(erradas) - 2)
            eliminadas_formatadas = [f"[{numero}] {alternativas_numeros[numero]}" for numero in removidas]

            print("Opções erradas eliminadas:", ", ".join(eliminadas_formatadas))

            ajudas['eliminar'] -= 1
            ajuda_usada['eliminar'] = True

        elif escolha == "4":
            resposta = input("Digite o número da sua resposta: ")
            try:
                resposta_int = int(resposta)
                if resposta_int in range(1, len(alternativas) + 1):
                    if f"option{resposta_int}" == pergunta["answer"]:
                        print("Resposta correta!")
                        print()
                        return True
                    else:
                        print()
                        print(f"Resposta errada! A correta era: {pergunta[pergunta['answer']]}")
                        print(f"Explicação: {pergunta['explanation']}")
                        return False
                else:
                    print("Opção inválida.")
            except ValueError:
                print("Entrada inválida! Digite um número.")

        else:
            print("Escolha inválida ou ajuda indisponível.")

# Função para recuperar ajuda (meta)
# A função contabiliza se as respostas certas forem maior que 0 e se forem multiplos de 6 (se ele tiver acertado 6 certas)
# Ele recebe mais uma ajuda
def ajudanova(ajudas, respostas_certas):
    if respostas_certas > 0 and respostas_certas % 6 == 0:  
        ajudas_disponiveis = ["dicas", "pularquestao", "eliminar"]
        ajuda_escolhida = random.choice(ajudas_disponiveis)  
        ajudas[ajuda_escolhida] += 1
        print(f"\nSortudo! Você ganhou uma {ajuda_escolhida.upper()} extra!")

# Função principal do jogo, que controla menú e adjacentes.
def askme():
    perguntas, hall = arquivosjs()
    print("Olá, bem vindo ao AskMe Game!")
    nome = input("Digite seu nome: ").strip()
    print(f"Bem-vindo(a), {nome}!")

    # Configuração inicial das ajudas
    ajudas = {
        "dicas": 1,
        "pularquestao": 1,
        "eliminar": 1,
        "questoes_fixas": 20,
        "tempoesgotado": 30
    }

    while True:
        print("\n----------------- ASKME - QUIZ GERAL -----------------")
        print("[1] ESCOLHER MODO DE JOGO")
        print("[2] HALL DA FAMA")
        print("[3] SAIR")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("\nEscolha um modo:")
            print("1. QUESTÕES FIXAS")
            print("2. TEMPO LIMITADO")
            print("3. HARDCORE")
            modo = input("Modo escolhido (1-3): ")

            if modo == "1":
                modo = "questfixa"
            elif modo == "2":
                modo = "questemp"
            elif modo == "3":
                modo = "hardcore"
            else:
                print("Modo inválido!")
                continue
            # Chamar a função quiz e processar o resultado
            valor = quiz(perguntas, modo, ajudas)

            if modo == "questemp":
                print(f"Você jogou por {valor} segundos.")
            else:
                print(f"Sua pontuação foi de: {valor}")

            hallatt(hall, modo, valor, nome)
            salvar_hall(hall)
            
        elif opcao == "2":
            mostrar_hall(hall)      

        elif opcao == "3":
            salvar_hall(hall)
            print("Obrigado por jogar o quiz conosco. Até breve.")
            break

        else:
            print("Tente outra vez.")

# Função para atualizar o Hall da Fama
# Função solicita que o usuário após o finalizar dos modos de jogo, insira os dados
def hallatt(hall, modo, valor, nome):
    novo_registro = {"nome": nome}
    if modo == "questemp":
        novo_registro["tempo"] = valor
    else:
        novo_registro["pontos"] = valor
    hall[modo].append(novo_registro)

# inicializa o game
if __name__ == "__main__":
    askme()
