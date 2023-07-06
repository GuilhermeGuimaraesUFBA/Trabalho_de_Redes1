 # Projeto de Redes de Computadores 1
  ### Motivador:
  Este trabalho objetiva promover um entendimento aprofundado do
  funcionamento e importância das aplicações de redes. Para tal, o estudante deverá
  implementar um “deposito de arquivo com replicação”. A definição dos serviços
  dependerá dos requisitos da aplicação concebida e deverão ser também
  especificados e codificados por cada equipe.

## 📝 Sumário
- [1. Equipe](#equipe)
- [2. Estrutura do código](#estrutura_do_codigo)
- [3. Execução do código](#execucao_do_coddigo)

 ## 1. Equipe: <a name = "equipe"></a>

Erick Kokubum

Guilherme Guimaraes

Edyo de Andrade

Cleyton Solares
 
 
 ## 2. Estrutura do código: <a name = "estrutura_do_codigo"></a>
```
 
/Trabalho_de_Redes1-main      : pasta principal do projeto
  /client_storage             : armazenamento local do cliente
    |data.txt:
    |random.txt:
  /server_storage_1           : armazenamento do servidor 1

  /server_storage_2           : armazenamento do servidor 2

  /server_storage_3           : armazenamento do servidor 3

  /server_storage_4           : armazenamento do servidor 4

  /server_storage_5           : armazenamento do servidor 5

  |.gitignore                 : arquivo de configuração do git

  |README.md                  : arquivo markdown com especificações do projeto

  |client.py                  : arquivo de configuração do cliente

  |constants.py               : arquivo das constantes usadas no projeto

  |enums.py                   : arquivo com os enunciados de comandos e status de comunicação

  |server.py                  : arquivo de configuração do(s) servidor

 ```

## 3. Execução do código: <a name = "execucao_do_coddigo"></a>

   - 1.1 - Baixe a pasta Trabalho_de_Redes1;
   - 1.2 - Abra o terminal;
   - 1.3 - Utilizando o comando "*cd* " vá até o local onde a pasta baixada está;
   - 1.4 - Execute o arquivo **_server.py_** com "python server.py **host** **porta**", para poder simular o servidor da aplicação;
   - 1.5 - Em seguida, execute o arquivo **_client.py_** com "python client.py **host** **porta**", para poder simular o cliente da aplicação;
   - 1.6 - Por fim, siga os comandos que a aplicação mostrar na tela.
