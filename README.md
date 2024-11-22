AskMe - Quiz Configurável
📋 O que é o AskMe?
AskMe é um jogo de perguntas e respostas configurável, desenvolvido como parte de um processo seletivo para a Intrusa Games. Ele permite que jogadores respondam a questões personalizadas, organizadas em diferentes modos de jogo.

Este projeto foi idealizado para praticar conceitos de programação, lógica de jogos, persistência de dados e interatividade com o jogador.

🎯 Propósito do Projeto
O AskMe tem como objetivo:

Proporcionar uma experiência de jogo educativa e divertida.
Demonstrar habilidades de programação e design de jogos.
Criar um jogo que possa ser personalizado por projetistas de perguntas, facilitando sua aplicação em diferentes contextos, como testes educacionais ou competições.
Além disso, o projeto destaca a capacidade de lidar com persistência de dados (salvar informações no Hall da Fama) e de implementar interatividade com o jogador por meio de um menu intuitivo.


🛠️ Como foi feito?
O jogo foi desenvolvido em Python utilizando conceitos como:

Manipulação de Arquivos JSON:
Para carregar e salvar dados de perguntas e do Hall da Fama.

Estruturas de Controle:
Menus interativos, modos de jogo e validações de entrada.

Funções e Modularidade:
Código dividido em funções para facilitar a manutenção e a expansão do jogo.

Randomização:
Questões embaralhadas para garantir uma experiência única a cada partida.

Persistência de Dados:
Uso de arquivos JSON para manter o histórico de melhores pontuações.

📂 Estrutura de Arquivos

├── AskMe.py           # Código principal do jogo
├── questao.json       # Arquivo com as perguntas configuráveis
├── hall.json          # Arquivo com o Hall da Fama
├── README.md          # Documentação do projeto
