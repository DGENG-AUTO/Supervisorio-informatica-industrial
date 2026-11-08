# Supervisório de Informática Industrial

Este projeto foi desenvolvido no em 2025 para a disciplina de **Informática Industrial** administrada pelo prof. Guilherme Márcio. Foi meu primeiro supervisório: um trabalho feito com muito esforço para aprender, na prática, como conectar uma interface gráfica a dados de um processo industrial.

O programa apresenta uma visão de um sistema de bombeamento e reservatórios. Ele se comunica com um CLP (ou outro servidor compatível) por **Modbus TCP**, mostra medições na tela, oferece comandos para o motor e registra dados para consulta posterior. É um projeto acadêmico e uma primeira versão, com **bastante espaço para evoluir**.

## O que o programa faz

- Mostra uma representação visual do processo, incluindo reservatórios, motor, pressão e vazão.
- Permite informar o endereço IP e a porta do servidor Modbus pela interface. O valor inicial configurado no código é `10.15.30.181:502`.
- Faz leituras periódicas das tags definidas no projeto. O intervalo inicial é de **1.000 ms** e pode ser alterado na interface.
- Exibe medições de processo e elétricas, como nível, corrente, tensão, potência, rotação e temperaturas, conforme as tags configuradas.
- Oferece controles de acionamento do motor e parâmetros relacionados à partida e às rampas. Esses comandos escrevem registradores Modbus.
- Apresenta gráficos em tempo real por grupos de sinais, como corrente, tensão, potência, THD e temperatura.
- Salva amostras com data e hora em um banco SQLite e permite consultar um intervalo de tempo e visualizar as medições históricas selecionadas.

## Como o código está organizado

| Arquivo ou pasta | Responsabilidade |
| --- | --- |
| `main.py` | Ponto de entrada. Carrega as regras visuais do Kivy e inicia a aplicação. |
| `mainwidget.py` | Coordena a tela principal, a conexão Modbus, a leitura das tags, a atualização dos indicadores e os gráficos. |
| `mainwidget.kv` | Define o layout da tela principal e a disposição dos elementos visuais. |
| `popup.py` | Implementa as janelas auxiliares de conexão, varredura, acionamento, medições e gráficos. |
| `popup.kv` | Define o layout e as ações das janelas auxiliares. |
| `biblioteca_tags.py` | Reúne as tags do processo e informações usadas para localizar e interpretar os registradores, como endereço, tipo e divisor. |
| `timeseriesgraph.py` | Especializa o gráfico temporal para exibir as amostras recentes com rótulos de horário. |
| `db.py` | Configura a conexão SQLite e os recursos de sessão do SQLAlchemy. |
| `models.py` | Define o modelo `DadoCLP`, que representa uma amostra armazenada no banco. |
| `modulopersistencia.py` | Grava medições e busca dados históricos por período e tags selecionadas. |
| `requirements.txt` | Lista as dependências Python utilizadas pelo projeto. |
| `img/` | Contém imagens usadas na representação visual do supervisório. |
| `data/db.data` | Arquivo do banco de dados SQLite utilizado pela aplicação. |

Durante a execução, `mainwidget.py` faz a comunicação e atualiza os valores da tela. A interface é descrita nos arquivos `.kv`; a persistência fica separada nos módulos de banco e histórico. A leitura periódica ocorre em uma thread, e o código também usa o ciclo de eventos do Kivy para agendar algumas atualizações da interface.

## Tecnologias

- **Python**
- **Kivy** e **KivyMD** para a interface gráfica
- **Modbus TCP**, usando `pyModbusTCP` para a comunicação
- **SQLAlchemy** e **SQLite** para armazenamento e consulta dos dados
- **Kivy Garden Graph** para os gráficos

As versões das bibliotecas estão registradas em `requirements.txt`.

## Como executar

O projeto foi desenvolvido para uma configuração de desktop com Python. No Windows ou em um ambiente próprio para criação e execução de códigos, abra o PowerShell na pasta do projeto e execute, linha por linha:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
python -m pip install -r requirements.txt
python main.py
```

Para acompanhar dados reais, a máquina precisa alcançar pela rede um equipamento ou simulador com servidor Modbus TCP. Configure o IP e a porta adequados na janela de conexão e confira se os endereços, tipos e escalas das tags correspondem ao mapa de registradores do equipamento.

> **Atenção:** os controles de acionamento enviam comandos ao servidor Modbus. Antes de conectar a um CLP ou equipamento físico, valide os endereços e os comandos em um ambiente seguro, como um simulador ou bancada de testes.

## Sobre o projeto

Este supervisório representa meu primeiro passo no desenvolvimento de interfaces para automação industrial. Foi um projeto acadêmico de aprendizado, construído com dedicação em 2025. Sei que há pontos a melhorar e muitas possibilidades para evoluí-lo, mas concluir essa primeira versão foi uma conquista importante.

## 📄 Licença

Esse código é autoral e cunho educativo, logo é distribuído sob a licença **MIT** (ajuste conforme sua preferência). 

---

## 👤 Autor

**Douglas Carvalho**
[LinkedIn](https://www.linkedin.com/in/douglas-carvalho-4a6091300/) · [GitHub](https://github.com/DGENG-AUTO)
