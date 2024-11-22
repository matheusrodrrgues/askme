import json
import random
import time

# Função para carregar os dados do JSON
def load_data():
    try:
        with open("questions.json", "r") as file:
            questions = json.load(file)
    except FileNotFoundError:
        questions = []

    try:
        with open("hall_of_fame.json", "r") as file:
            hall_of_fame = json.load(file)
    except FileNotFoundError:
        hall_of_fame = {"fixed": [], "timed": [], "no_mistakes": []}

    return questions, hall_of_fame

# Função para salvar o Hall da Fama no JSON
def save_hall_of_fame(hall_of_fame):
    with open("hall_of_fame.json", "w") as file:
        json.dump(hall_of_fame, file, indent=4)

# Exibir o Hall da Fama
def show_hall_of_fame(hall_of_fame):
    print("\n=== Hall da Fama ===")
    for mode, scores in hall_of_fame.items():
        print(f"\nModo: {mode}")
        for entry in scores:
            print(f"Jogador: {entry['name']} - Pontos: {entry['score']}")

# Perguntar ao jogador
def ask_question(question, helps):
    print(f"\nCategoria: {question['category']}")
    print(question['questionText'] + "\n")
    
    options = [question.get(f"option{i}", None) for i in range(1, 6) if question.get(f"option{i}", None)]
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")
    
    print("\nOpções de ajuda:")
    print(f"1. Dica ({helps['hints']} restantes)")
    print(f"2. Pular questão ({helps['skips']} restantes)")
    print(f"3. Eliminar opções erradas ({helps['eliminations']} restantes)")
    print("4. Responder")

    while True:
        choice = input("\nEscolha uma ação (1-4): ")
        if choice == "1" and helps['hints'] > 0:
            print(f"Dica: {question['hint'][0]}")
            helps['hints'] -= 1
        elif choice == "2" and helps['skips'] > 0:
            print("Você pulou a questão!")
            helps['skips'] -= 1
            return None
        elif choice == "3" and helps['eliminations'] > 0:
            incorrect_options = [opt for opt in options if opt != question['answer']]
            removed = random.sample(incorrect_options, len(incorrect_options) - 2)
            print("Opções eliminadas: " + ", ".join(removed))
            helps['eliminations'] -= 1
        elif choice == "4":
            answer = input("Sua resposta: ")
            if answer == question['answer']:
                print("Resposta correta!")
                return True
            else:
                print(f"Resposta errada! {question['explanation']}")
                return False
        else:
            print("Escolha inválida ou ajuda indisponível.")

# Jogo principal
def play_game(questions, mode, helps):
    random.shuffle(questions)
    score = 0
    total_questions = 0
    start_time = time.time()

    for question in questions:
        if mode == "1" and total_questions >= helps["fixed_questions"]:
            break
        if mode == "2" and time.time() - start_time >= helps["time_limit"]:
            print("\nTempo esgotado!")
            break
        if mode == "3" and total_questions >= len(questions):
            break

        result = ask_question(question, helps)
        if result is None:
            continue
        elif result:
            score += question['value']
        else:
            if mode == "3":
                print("\nVocê errou! Jogo encerrado.")
                break
        total_questions += 1

    return score

# Atualizar o Hall da Fama
def update_hall_of_fame(hall_of_fame, mode, score):
    name = input("\nDigite seu nome: ")
    hall_of_fame[mode].append({"name": name, "score": score})
    hall_of_fame[mode] = sorted(hall_of_fame[mode], key=lambda x: x["score"], reverse=True)[:10]

# Menu principal
def main():
    questions, hall_of_fame = load_data()

    helps_config = {
        "hints": 3,
        "skips": 3,
        "eliminations": 2,
        "fixed_questions": 5,
        "time_limit": 60
    }

    while True:
        print("\n=== Quiz Configurável: AskMe ===")
        print("1. Jogar")
        print("2. Ver Hall da Fama")
        print("3. Sair")
        choice = input("\nEscolha uma opção: ")

        if choice == "1":
            print("\nEscolha um modo de jogo:")
            print("1. Número de questões fixas")
            print("2. Limite de tempo")
            print("3. Tente não errar")
            mode = input("\nDigite o número do modo: ")

            if mode not in ["1", "2", "3"]:
                print("Modo inválido.")
                continue

            score = play_game(questions, mode, helps_config)
            print(f"\nSua pontuação: {score}")
            update_hall_of_fame(hall_of_fame, mode, score)

        elif choice == "2":
            show_hall_of_fame(hall_of_fame)

        elif choice == "3":
            save_hall_of_fame(hall_of_fame)
            print("Saindo do jogo. Até logo!")
            break

        else:
            print("Escolha inválida. Tente novamente.")

if __name__ == "__main__":
    main()
