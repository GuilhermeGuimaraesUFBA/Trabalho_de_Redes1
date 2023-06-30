import socket
import sys
import json
import os
import constants
from enums import Command, Status

class Client:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def connect(self):
    try:
      self.client_socket.connect((self.host, self.port))
    except Exception:
      print(f"Erro de conexão - Host: {self.host}, Port: {self.port}")
      sys.exit()

  def save_file(self, file_data, filename):
    new_filename = filename
    name, extension = os.path.splitext(new_filename)
    counter = 1
    while os.path.isfile(f"./client_storage/{new_filename}"):
      new_filename = f"{name}({counter}){extension}"
      counter+=1

    with open(f"./client_storage/{new_filename}","wb") as file:
      file.write(file_data)
    return {
      "status": Status.OK,
      "message": "Arquivo recuperado com sucesso!"
    }

  def receive_all(self,  size):
    received_chunks = []
    remaining = size
    while remaining > 0:
        received = self.client_socket.recv(min(remaining, constants.BASE_MSG_SIZE))
        received_chunks.append(received)
        remaining -= len(received)
    return b''.join(received_chunks)
  
  def handle_response(self, response):
    status = response["status"]
    msg = response["message"]
    return f"\n[{status}] {msg}"
  
  def increase_replicas(self, filename, number_of_replicas=1):
    if not filename:
      return self.handle_response({
      "status": Status.ERROR,
      "message": "Nome do arquivo inválido. Tente Novamente!"
    })

    command_message = {
      "command":Command.INCREASE,
      "filename": filename,
      "number_of_replicas": number_of_replicas
    }

    self.client_socket.sendall(json.dumps(command_message).encode(constants.FORMAT))
    raw_increase_resp = self.client_socket.recv(constants.BASE_MSG_SIZE).decode(constants.FORMAT)
    increase_resp = json.loads(raw_increase_resp)

    return self.handle_response(increase_resp)
  
  def remove_file(self, filename, number_of_replicas=1):
    if not filename:
      return self.handle_response({
      "status": Status.ERROR,
      "message": "Nome do arquivo inválido. Tente Novamente!"
    })

    command_message = {
      "command":Command.REMOVE,
      "filename": filename,
      "number_of_replicas": number_of_replicas
    }
    self.client_socket.sendall(json.dumps(command_message).encode(constants.FORMAT))
    raw_remove_resp = self.client_socket.recv(constants.BASE_MSG_SIZE).decode(constants.FORMAT)
    remove_resp = json.loads(raw_remove_resp)

    return self.handle_response(remove_resp)

  def recover_file(self, filename):
    if not filename:
      return self.handle_response({
      "status": Status.ERROR,
      "message": "Nome do arquivo inválido. Tente Novamente!"
    })
    
    command_message = {
      "command":Command.RECOVERY,
      "filename": filename,
    }
    self.client_socket.sendall(json.dumps(command_message).encode(constants.FORMAT))
    
    raw_recover_resp = self.client_socket.recv(constants.BASE_MSG_SIZE).decode(constants.FORMAT)
    recover_resp = json.loads(raw_recover_resp)

    if recover_resp["status"] == Status.ERROR:
        return self.handle_response(recover_resp)
    
    self.client_socket.sendall(json.dumps({"status":Status.OK}).encode(constants.FORMAT))
    file_content_bytes = self.receive_all(recover_resp["size"])

    return self.handle_response(self.save_file(file_content_bytes, filename))



  def send_file(self, filename, number_of_replicas=1):
    if not filename:
      return self.handle_response({
        "status": Status.ERROR,
        "message": "Nome do arquivo inválido. Tente Novamente!"
      })
    
    with open(f"./client_storage/{filename}", 'rb') as file:
      data = file.read()
      
      command_message = {
        "command":Command.DEPOSIT,
        "filename": filename,
        "number_of_replicas": number_of_replicas,
        "size": len(data)
      }
      self.client_socket.sendall(json.dumps(command_message).encode(constants.FORMAT))

      raw_command_resp = self.client_socket.recv(constants.BASE_MSG_SIZE).decode(constants.FORMAT)
      command_resp = json.loads(raw_command_resp)
      if command_resp["status"] == Status.ERROR:
        return self.handle_response(command_resp)
      
      self.client_socket.sendall(data)
      raw_data_resp = self.client_socket.recv(constants.BASE_MSG_SIZE).decode(constants.FORMAT)
      data_resp = json.loads(raw_data_resp)

      
      return self.handle_response(data_resp)
       

  def run(self):
    self.connect()

    while True:
      print('--- MENU ---')
      print('1. Depositar arquivo')
      print('2. Recuperar arquivo')
      print('3. Remover arquivo')
      print('4. Aumentar replicas')
      print('0. Sair')

      option = input('Selecione uma opção: ')

      if option == '1':
        filename = input('Informe o nome do arquivo a ser enviado: ')
        replicas = input(f'Informe o nível de tolerância a falhas (MAX: {constants.NUMBER_OF_SERVERS}): ')
        response = self.send_file(filename, replicas)
        print(f"{response}\n")
      elif option == '2':
        filename = input('Informe o nome do arquivo a ser recuperado: ')
        response = self.recover_file(filename)
        print(f"{response}\n")
      elif option == '3':
        filename = input('Informe o nome do arquivo a ser removido: ')
        replicas = input(f'Informe o número de replicas a serem removidas: ')
        response = self.remove_file(filename, replicas)
        print(f"{response}\n")
      elif option == '4':
        filename = input('Informe o nome do arquivo a ser replicado: ')
        replicas = input(f'Informe o número de replicas a serem adicionadas: ')
        response = self.increase_replicas(filename, replicas)
        print(f"{response}\n")
      elif option == '0':
        break
      else:
        print('Opção inválida. Tente novamente.')

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print("A chamada ao client.py precisa ter 2 argumentos: IP (Host), Porta (Host)")
    exit()

  client = Client(str(sys.argv[1]), int(sys.argv[2]))
  client.run()