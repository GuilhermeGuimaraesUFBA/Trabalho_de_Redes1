import socket
import threading
import constants
import json
import sys
import os
from enums import Command, Status


class Server:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.servers_ids = [sn+1 for sn in range(constants.NUMBER_OF_SERVERS)]
    self.current_server_id = 1

  def receive_all(self, client_conn, size):
    received_chunks = []
    remaining = size
    while remaining > 0:
        received = client_conn.recv(min(remaining, constants.BASE_MSG_SIZE))
        received_chunks.append(received)
        remaining -= len(received)
    return b''.join(received_chunks)
  
  def get_server_with_file(self, filename):
    for server_id in self.servers_ids:
      if os.path.isfile(f"./server_storage_{server_id}/{filename}"):
        return server_id
    return -1

  def get_servers_file_status(self, filename):
    server_existence = [False for _ in self.servers_ids]
    for server_id in self.servers_ids:
      server_existence[server_id-1] = os.path.isfile(f"./server_storage_{server_id}/{filename}")
    return server_existence
  
  def deposit_file(self, filename, data, number_of_replicas):
    counter = 1
    server_file_status_list = self.get_servers_file_status(filename)
    if all(server_file_status_list):
      return {
        "status":Status.ERROR,
        "message":f"Esse arquivo ja está replicado em todos os servidores disponíveis!"
      } 
    actual_replicas = 0
    while counter <= number_of_replicas:
      if not server_file_status_list[self.current_server_id - 1]:
        with open(f"./server_storage_{self.current_server_id}/{filename}","wb") as file:
          file.write(data)
        actual_replicas+=1
      counter+=1
      # Round Robin
      self.current_server_id = (self.current_server_id  % constants.NUMBER_OF_SERVERS ) +1

    message = "Seu arquivo foi armazenado com sucesso!"
    if actual_replicas != number_of_replicas:
      message = f"Seu arquivo ja estava replicado e só conseguimos replicar mais {actual_replicas} ao invés de {number_of_replicas} pois ele ja se encontra em todos servidores disponíveis!"
    return {
      "status":Status.OK,
      "message":message
    } 
  
  def recover_file(self, filename):
    server_with_file = self.get_server_with_file(filename)
    if server_with_file == -1:
      return [{
        "status":Status.ERROR,
        "message":f"Esse arquivo não existe em nenhum dos nossos servidores!",
        "size": 0
      }, None]
    
    with open(f"./server_storage_{server_with_file}/{filename}","rb") as file:
      data = file.read()

    return [{
      "status":Status.OK,
      "message":f"Arquivo disponível!",
      "size": len(data)
    }, data]

  def handle_client(self, client_conn, address):
    print(f"[Conexão Estabelecida] {address}")
    
    while True:
      # Esperando a primeira mensagem do client -> command_message
      raw_command_msg = client_conn.recv(constants.BASE_MSG_SIZE).decode(constants.FORMAT) 
      if not raw_command_msg:
        print(f"[Conexão Removida] {address}")

        return
      
      command_msg = json.loads(raw_command_msg)
      print(f"[MENSAGEM DE COMANDO]: {command_msg}")

      filename = command_msg["filename"]

      if command_msg["command"] == Command.DEPOSIT:

        client_conn.sendall(json.dumps({
          "status":Status.OK,
          "message":f"Mensagem de deposit0 recebida!",
        }).encode(constants.FORMAT))

        number_of_replicas = int(command_msg["number_of_replicas"])
        file_content_bytes = self.receive_all(client_conn, command_msg["size"])
        response = self.deposit_file(filename, file_content_bytes, number_of_replicas)
        client_conn.sendall(json.dumps(response).encode(constants.FORMAT))
      elif command_msg["command"] == Command.RECOVERY:
        response = self.recover_file(filename)
        client_conn.sendall(json.dumps(response[0]).encode(constants.FORMAT))
        if response[0]["status"] == Status.OK:
          client_conn.recv(constants.BASE_MSG_SIZE).decode(constants.FORMAT) 
          client_conn.sendall(response[1])

  def run(self):
    self.server_socket.bind((self.host, self.port))
    self.server_socket.listen()

    print('Servidor inicializado e pronto para receber conexões.')
    while True:
      client_conn, address = self.server_socket.accept()
      threading.Thread(target=self.handle_client, args=(client_conn, address)).start()

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print("A chamada ao server.py precisa ter 2 argumentos: IP (Host), Porta (Host)")
    exit()

  server = Server(str(sys.argv[1]), int(sys.argv[2]))
  server.run()