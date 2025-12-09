import socket
import threading
import json
import time
import random
from datetime import datetime

class CurrencyServerUDP:
    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Permitir reuso de endereço (opcional)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Cotações iniciais (em relação ao USD)
        self.rates = {
            "USD": 1.0,
            "BRL": 4.95,
            "EUR": 0.92,
            "GBP": 0.79,
            "JPY": 149.50,
            "CAD": 1.36,
            "AUD": 1.53,
            "CHF": 0.88,
            "CNY": 7.24,
            "MXN": 17.12,
        }

        self.lock = threading.Lock()
        self.running = True

    def start(self):
        """Inicia o servidor UDP"""
        self.socket.bind((self.host, self.port))
        print(f"[SERVIDOR UDP] Iniciado em {self.host}:{self.port}")
        print(f"[SERVIDOR UDP] Aguardando requisições...\n")

        # Thread para atualizar cotações periodicamente
        update_thread = threading.Thread(target=self.update_rates, daemon=True)
        update_thread.start()

        try:
            while self.running:
                try:
                    data, address = self.socket.recvfrom(8192)
                    text = data.decode("utf-8").strip()
                    print(f"[RECEBIDO] De {address}: {text}")

                    # Para não bloquear o loop principal, processamos cada requisição em uma thread
                    handler_thread = threading.Thread(
                        target=self.handle_request,
                        args=(text, address),
                        daemon=True,
                    )
                    handler_thread.start()

                except Exception as e:
                    if self.running:
                        print(f"[ERRO] Erro ao receber dados: {e}")
        except KeyboardInterrupt:
            print("\n[SERVIDOR UDP] Encerrando...")
        finally:
            self.stop()

    def update_rates(self):
        """Atualiza as cotações periodicamente (simulação)"""
        while self.running:
            time.sleep(5)  # Atualiza a cada 5 segundos

            with self.lock:
                for currency in self.rates:
                    if currency != "USD":
                        # Variação aleatória entre -1% e +1%
                        variation = random.uniform(-0.01, 0.01)
                        self.rates[currency] *= 1 + variation

            print(
                f"[ATUALIZAÇÃO] Cotações atualizadas às {datetime.now().strftime('%H:%M:%S')}"
            )

    def handle_request(self, text, address):
        """Processa uma requisição recebida via UDP e envia resposta para address"""
        try:
            # Esperamos formato "<request_id>|<command>" para correlacionar respostas
            request_id = None
            command = text
            if "|" in text:
                request_id, command = text.split("|", 1)
                request_id = request_id.strip()

            response_body = self.process_command(command)

            if request_id:
                payload = f"{request_id}|{response_body}"
            else:
                payload = response_body

            # sendto porque UDP é connectionless; envia de volta para o cliente que pediu
            self.socket.sendto(payload.encode("utf-8"), address)

        except Exception as e:
            print(f"[ERRO] Falha ao processar requisição de {address}: {e}")

    def process_command(self, command):
        """Processa os comandos recebidos (mesma lógica do servidor TCP original)"""
        parts = command.split()

        if not parts:
            return "ERRO: Comando vazio\n"

        cmd = parts[0].upper()

        try:
            if cmd == "LIST":
                return self.cmd_list(parts)
            elif cmd == "RATE":
                return self.cmd_rate(parts)
            elif cmd == "CONVERT":
                return self.cmd_convert(parts)
            elif cmd == "QUIT":
                # Em UDP não há sessão — apenas devolvemos BYE (o cliente encerra localmente)
                return "BYE\n"
            else:
                return f"ERRO: Comando desconhecido '{cmd}'\n"
        except Exception as e:
            return f"ERRO: {str(e)}\n"

    def cmd_list(self, parts):
        base = "USD"
        if len(parts) > 1:
            base = parts[1].upper()

        with self.lock:
            if base not in self.rates:
                return f"ERRO: Moeda base '{base}' não encontrada\n"

            base_rate = self.rates[base]
            result = f"Cotações em relação a {base}:\n"
            result += "-" * 40 + "\n"

            for currency, rate in sorted(self.rates.items()):
                converted_rate = rate / base_rate
                result += f"{currency}: {converted_rate:.4f}\n"

            result += "-" * 40 + "\n"

        return result

    def cmd_rate(self, parts):
        if len(parts) < 3:
            return "ERRO: Uso correto: RATE <origem> <destino>\n"

        origin = parts[1].upper()
        destination = parts[2].upper()

        with self.lock:
            if origin not in self.rates:
                return f"ERRO: Moeda de origem '{origin}' não encontrada\n"
            if destination not in self.rates:
                return f"ERRO: Moeda de destino '{destination}' não encontrada\n"

            rate = self.rates[destination] / self.rates[origin]

        return f"TAXA: 1 {origin} = {rate:.4f} {destination}\n"

    def cmd_convert(self, parts):
        if len(parts) < 4:
            return "ERRO: Uso correto: CONVERT <origem> <destino> <valor>\n"

        origin = parts[1].upper()
        destination = parts[2].upper()

        try:
            value = float(parts[3])
        except ValueError:
            return "ERRO: Valor inválido\n"

        with self.lock:
            if origin not in self.rates:
                return f"ERRO: Moeda de origem '{origin}' não encontrada\n"
            if destination not in self.rates:
                return f"ERRO: Moeda de destino '{destination}' não encontrada\n"

            rate = self.rates[destination] / self.rates[origin]
            converted = value * rate

        return f"CONVERSÃO: {value:.2f} {origin} = {converted:.2f} {destination}\n"

    def stop(self):
        """Encerra o servidor"""
        self.running = False
        self.socket.close()
        print("[SERVIDOR UDP] Socket fechado.")

if __name__ == "__main__":
    server = CurrencyServerUDP()
    server.start()
