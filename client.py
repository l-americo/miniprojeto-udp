import socket
import sys
import threading
import time
import uuid

class CurrencyClientUDP:
    def __init__(self, host="localhost", port=15000, timeout=2.0, retries=3):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # timeout usado para permitir tentativas quando server não responde
        self.socket.settimeout(timeout)
        self.timeout = timeout
        self.retries = retries
        # endereço do servidor em formato de tupla
        self.server_addr = (self.host, self.port)
        # usado para indicar que o cliente deve encerrar a execução
        self.running = True

    def send_command(self, command):
        """Envia um comando ao servidor via UDP com retries e aguarda resposta correspondente ao request_id."""
        # cria um id único para correlacionar resposta com requisição
        request_id = str(uuid.uuid4())
        payload = f"{request_id}|{command}"
        attempts = 0

        while attempts < self.retries:
            try:
                # sendto é usado em UDP (connless)
                self.socket.sendto(payload.encode("utf-8"), self.server_addr)
                data, addr = self.socket.recvfrom(8192)
                text = data.decode("utf-8")

                # servidor deve responder com "<request_id>|<response>"
                if "|" in text:
                    resp_id, resp_body = text.split("|", 1)
                    if resp_id == request_id:
                        return resp_body
                    else:
                        # resposta de outra requisição, ignorar e continuar aguardando dentro do timeout
                        continue
                else:
                    # caso servidor não envie id, devolve tudo
                    return text

            except socket.timeout:
                attempts += 1
                print(f"[AVISO] Sem resposta, tentando novamente ({attempts}/{self.retries})...")
            except Exception as e:
                print(f"ERRO: Falha na comunicação UDP: {e}")
                return None

        return "ERRO: Sem resposta do servidor após várias tentativas.\n"

    def run(self):
        """Executa o cliente interativo (sem 'connect' pois UDP é connectionless)."""
        print(f"Cliente UDP preparado para enviar a {self.host}:{self.port}\n")
        print("-" * 50)
        print("SISTEMA DE COTAÇÕES DE MOEDAS (UDP)")
        print("-" * 50)
        print("\nComandos disponíveis:")
        print("  LIST [moeda_base]          - Lista todas as cotações")
        print("  RATE <origem> <destino>    - Taxa de câmbio")
        print("  CONVERT <origem> <destino> <valor> - Converter valor")
        print("  QUIT                       - Sair (cliente)\n")
        print("Exemplos: LIST USD | RATE BRL USD | CONVERT USD BRL 100")
        print("-" * 50 + "\n")

        try:
            while self.running:
                command = input(">>> ").strip()
                if not command:
                    continue

                # QUIT fecha somente o cliente
                if command.upper() == "QUIT":
                    print("Encerrando cliente localmente...")
                    self.running = False
                    break

                response = self.send_command(command)
                if response:
                    print(response)
                else:
                    print("Erro ao receber resposta do servidor")

        except KeyboardInterrupt:
            print("\n\nEncerrando cliente...")

        finally:
            self.close()

    def close(self):
        """Fecha o socket UDP"""
        if self.socket:
            self.socket.close()
            print("Socket UDP fechado.")

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 15000

    client = CurrencyClientUDP(host, port)
    client.run()

