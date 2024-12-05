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
# Caso não tenha o arquivo, o sistema retorna o print com o valor Não encontrado.            
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        perguntas = []
    try:
        with open("hall.json", "r", encoding='utf-8') as arquivo:
            hall = json.load(arquivo)
# Caso não tenha o arquivo, o sistema retorna o print com o valor Não encontrado e cria um novo.        
    except FileNotFoundError:
        print("Arquivo não encontrado, criando um novo.")
        hall = {"fixo": [], "tempo": [], "sem_erros": []}

    return perguntas, hall

# Função desenvolvida para salvar o Hall, caso não consiga ler o arquivo, ele desenvolve um novo na 
# mesma pasta do arquivo main.py
def salvar_hall(hall):
    try:
# Tentar carregar os dados existentes do hall.json
        with open("hall.json", "r", encoding='utf-8') as arquivo:
            dados_existentes = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
# Se o arquivo não existir ou estiver corrompido, começar com um novo
        dados_existentes = {"fixo": [], "tempo": [], "sem_erros": []}

# Mesclar os dados existentes com os novos
    for modo, jogadores in hall.items():
        if modo in dados_existentes:
            dados_existentes[modo].extend(jogadores)
# Garantir que não ultrapasse os 10 melhores
            dados_existentes[modo] = sorted(dados_existentes[modo], key=lambda x: x["pontos"], reverse=True)[:10]

# Salvar o conteúdo atualizado no arquivo
    with open("hall.json", "w", encoding='utf-8') as arquivo:
        json.dump(dados_existentes, arquivo, indent=4, ensure_ascii=False)

# Função desenvolvida para apresentar o Hall da Fama
# A função pega os dados da função salvar_hall e retorna os 10 melhores jogadores
def mostrar_hall(hall):
    print("\n----------------- HALL DA FAMA -----------------")
    for modo, jogadores in hall.items():
        print(f"\nModo de jogo: {modo}")
        for jogador in jogadores:
            print(f"[NOME DO JOGADOR]: {jogador['nome']} - Pontuação: {jogador['pontos']}")

# Função principal do jogo
def jogar(perguntas, modo, ajudas):
    random.shuffle(perguntas)
    pontos = 0
    inicio = time.time()

    for pergunta in perguntas:
        if modo == "fixo" and pontos >= ajudas["questoes_fixas"]:
            break
        if modo == "tempo" and time.time() - inicio >= ajudas["tempo_maximo"]:
            print("Tempo esgotado!")
            break
        if modo == "sem_erros" and pontos >= len(perguntas):
            break

        resultado = fazer_pergunta(pergunta, ajudas)
        if resultado is None:
            continue
        elif resultado:
            pontos += int(pergunta["value"])
        else:
            if modo == "sem_erros":
                print("Você errou! Fim do jogo.")
                break

    return pontos

# Função para fazer perguntas ao jogador
def fazer_pergunta(pergunta, ajudas):
    print(f"\nCategoria: {pergunta['category']} (Valor: {pergunta['value']})")   
    print(pergunta['questionText'])

    # Mostrar opções de resposta
    opcoes = [pergunta[f"option{i}"] for i in range(1, 6) if f"option{i}" in pergunta]
    for i, opcao in enumerate(opcoes, start=1):
        print(f"{i}. {opcao}")

    # Controla o uso de ajudas
    ajuda_usada = {"dicas": False, "pulos": False, "eliminar": False}

    while True:
        # Montar o menu de ajuda dinamicamente
        print("\nAjuda disponível:")
        if ajudas['dicas'] > 0 and not ajuda_usada['dicas']:
            print(f"1. Usar dica ({ajudas['dicas']} restantes)")
        if ajudas['pulos'] > 0 and not ajuda_usada['pulos']:
            print(f"2. Pular questão ({ajudas['pulos']} restantes)")
        if ajudas['eliminar'] > 0 and not ajuda_usada['eliminar']:
            print(f"3. Eliminar opções erradas ({ajudas['eliminar']} restantes)")
        print("4. Responder")

        escolha = input("\nEscolha sua opção (1-4): ")

        if escolha == "1" and ajudas['dicas'] > 0 and not ajuda_usada['dicas']:
            print("Dica:", pergunta["hint"])
            ajudas['dicas'] -= 1
            ajuda_usada['dicas'] = True

        elif escolha == "2" and ajudas['pulos'] > 0 and not ajuda_usada['pulos']:
            print("Você pulou a questão!")
            ajudas['pulos'] -= 1
            return None

        elif escolha == "3" and ajudas['eliminar'] > 0 and not ajuda_usada['eliminar']:
            erradas = [op for op in opcoes if f"option{opcoes.index(op)+1}" != pergunta["answer"]]
            removidas = random.sample(erradas, len(erradas) - 2)
            print("Opções erradas eliminadas:", ", ".join(removidas))
            ajudas['eliminar'] -= 1
            ajuda_usada['eliminar'] = True

        elif escolha == "4":
            resposta = input("Digite o número da sua resposta: ")
            try:
                resposta_int = int(resposta)
                if resposta_int in range(1, len(opcoes) + 1):
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
def recuperar_ajuda(ajudas, respostas_certas):

    if respostas_certas > 0 and respostas_certas % 6 == 0:  # Verifica se é múltiplo de 6
        ajudas_disponiveis = ["dicas", "pulos", "eliminar"]
        ajuda_escolhida = random.choice(ajudas_disponiveis)  # Escolhe uma ajuda aleatória
        ajudas[ajuda_escolhida] += 1
        print(f"\nSortudo! Você ganhou uma {ajuda_escolhida.upper()} extra!")
        

# Função para atualizar o Hall da Fama
def atualizar_hall(hall, modo, pontos):
    nome = input("Digite seu nome: ")
    hall[modo].append({"nome": nome, "pontos": pontos})
    hall[modo] = sorted(hall[modo], key=lambda x: x["pontos"], reverse=True)[:10]

# Função principal que controla o menu
def main():
    perguntas, hall = arquivosjs()

    # Configuração inicial das ajudas
    ajudas = {
        "dicas": 1,
        "pulos": 1,
        "eliminar": 1,
        "questoes_fixas": 20,
        "tempo_maximo": 300
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
                modo = "fixo"
            elif modo == "2":
                modo = "tempo"
            elif modo == "3":
                modo = "sem_erros"
            else:
                print("Modo inválido!")
                continue

            pontos = jogar(perguntas, modo, ajudas)
            print(f"Sua pontuação foi: {pontos}")
            atualizar_hall(hall, modo, pontos)

        elif opcao == "2":
            mostrar_hall(hall)

        elif opcao == "3":
            salvar_hall(hall)
            print("Até a próxima!")
            break

        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
