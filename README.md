# Sistema de Cotações de Moedas (Câmbio) – UDP Cliente-Servidor

Sistema distribuído cliente-servidor usando **Sockets UDP** para fornecer cotações de moedas, com suporte a múltiplas requisições concorrentes e atualização periódica automática dos valores.

---

## 📋 Requisitos

* Python **3.7+**
* Nenhuma biblioteca externa (somente bibliotecas padrão)

---

## 🚀 Como Executar

### 1. Iniciar o Servidor

Abra um terminal e execute:

```bash
python server.py
```

O servidor será iniciado na porta **15000** por padrão.

**Saída esperada:**

```
[SERVIDOR] Iniciado em localhost:15000 (UDP)
[SERVIDOR] Aguardando requisições...
```

---

### 2. Iniciar o Cliente

Em outro terminal:

```bash
python client.py
```

**Opcional:** especificar host e porta

```bash
python client.py localhost 15000
```

---

## 📝 Comandos Disponíveis

### LIST [moeda_base]

Lista todas as moedas e suas cotações em relação à moeda base (padrão: USD).

```
>>> LIST
>>> LIST BRL
>>> LIST EUR
```

---

### RATE <origem> <destino>

Retorna a taxa de câmbio entre duas moedas.

```
>>> RATE USD BRL
>>> RATE BRL EUR
```

---

### CONVERT <origem> <destino> <valor>

Converte um valor de uma moeda para outra.

```
>>> CONVERT USD BRL 100
>>> CONVERT EUR JPY 50
```

---

### QUIT

Encerra apenas o **cliente**.

```
>>> QUIT
```

---

## 💱 Moedas Disponíveis

* USD — Dólar Americano
* BRL — Real Brasileiro
* EUR — Euro
* GBP — Libra Esterlina
* JPY — Iene Japonês
* CAD — Dólar Canadense
* AUD — Dólar Australiano
* CHF — Franco Suíço
* CNY — Yuan Chinês
* MXN — Peso Mexicano

---

## 🔄 Funcionalidades

### 🖥️ Servidor

* ✅ Armazena valores das moedas em memória
* ✅ Atualiza automaticamente as cotações a cada 5 segundos
* ✅ Responde cada requisição de forma imediata via UDP
* ✅ Concorrência com **threads**, cada cliente atendido individualmente
* ✅ Acesso seguro às cotações por meio de **locks** (thread-safe)
* ⚡ Baixa latência com UDP

---

### 🧑‍💻 Cliente

* Interface interativa via linha de comando
* Executa todos os comandos disponíveis
* Comunicação direta via datagramas UDP
* Tratamento robusto de erros

---

## 🧪 Testando Com Vários Clientes

Basta abrir múltiplos terminais, por exemplo:

Terminal 1:

```bash
python client.py
>>> LIST USD
```

Terminal 2:

```bash
python client.py
>>> RATE USD BRL
```

Terminal 3:

```bash
python client.py
>>> CONVERT BRL USD 1000
```

Cada requisição será respondida de forma independente.

---

## 📊 Exemplo de Sessão Completa

```
$ python client.py
Conectado ao servidor UDP localhost:15000

==================================================
SISTEMA DE COTAÇÕES DE MOEDAS
==================================================

Comandos disponíveis:
  LIST [moeda_base]
  RATE <origem> <destino>
  CONVERT <origem> <destino> <valor>
  QUIT
==================================================

>>> LIST USD
Cotações em USD:
AUD: 1.5300
BRL: 4.9500
CAD: 1.3600
CHF: 0.8800
CNY: 7.2400
EUR: 0.9200
GBP: 0.7900
JPY: 149.5000
MXN: 17.1200
USD: 1.0000

>>> RATE USD BRL
TAXA: 1 USD = 4.9500 BRL

>>> CONVERT USD BRL 100
CONVERSÃO: 100.00 USD = 495.00 BRL

>>> QUIT
Conexão encerrada.
```

---

## 🔧 Estrutura do Projeto

```
.
├── server.py
├── client.py
└── README.md
```

---

## ⚙️ Detalhes Técnicos

### Protocolo UDP

* Não possui garantia de entrega
* Baixa latência e alta velocidade
* Ideal para aplicações onde cada requisição é independente
* Implementado com resposta imediata a cada datagrama recebido

---

### Concorrência

* Cada requisição é tratada em uma nova thread
* Lock garante que a atualização das cotações seja consistente
* Uma thread dedicada mantém as taxas sempre atualizadas

---

### Simulação de Mercado

* As cotações variam aleatoriamente entre -1% e +1% a cada 5 segundos
* O sistema mantém valores realistas baseados nos iniciais armazenados

---

## 🛡️ Tratamento de Erros

Tratamento dedicado para:

* Comandos inválidos
* Moedas inexistentes
* Valores incorretos
* Perda de pacotes UDP
* Respostas com timeout (no cliente)

---

## 📚 Referências

* Sockets em Python (UDP): [https://docs.python.org/3/library/socket.html](https://docs.python.org/3/library/socket.html)
* Threading: [https://docs.python.org/3/library/threading.html](https://docs.python.org/3/library/threading.html)
---
---

