from file.file_name.input import *
from scenario_object.Scenario import *

def main():
	scenario = Scenario(FILE_NAME_SCENARIO_1)
	_dict = scenario.get_request_object_list()
	for serviceName in _dict:
		_list = _dict[serviceName]
		print(serviceName)
		for request in _list:
			print(request.get_id(), request.get_service().get_name())

if __name__ == "__main__":
	main()

'''
* Simular uma lista de algoritmos de distribuição de carga
Entrada: lista de algoritmos e cenários
Saída: lista de estatísticas (número de requisições atendidas dentro do prazo, fora do prazo, e a taxa de aproveitamento)

* Simulação
Um grupo de usuários deve enviar requisições de serviços a um conjunto de nós mec. O usuário deve selecionar
o nó mec mais próximo para receber a requisição.

* Nó mec
Cada nó mec receberá suas requisições individualmente, sem a intervenção de um intermediário para distribuir
a carga. A requisição deve ser adicionada a uma fila de requisições, onde a primeira requisição da fila deverá
ser atendida primeiro. Caso o nó mec não seja capaz de processar e responder a requisição dentro do prazo então
deverá encaminhar a requisição a outro nó mec.

* Requisição
Cada requisição corresponde a uma solicitação de um usuário em algum momento temporal do relógio, ao nó MEC mais próximo,
para utilizar um determinado serviço fornecido pelo nó mec.

* Serviço
Cada serviço possui um tempo mínimo e máximo para ser completamente executado, assim como um prazo estabelecido
por contratos de nível de serviço.

* Scenario
Cada scenario possui uma lista de nós mec, lista de serviços e a lista de requisições que cada nó mec receberá para
cada tipo de serviço fornecido.

* LoadDistributor
Responsável por distribuir a carga entre os nós mec.

* RequestQueue
Ordena as requisições em uma fila de acordo com algum critério.

---------------------------------
Passo 1
- Ler o arquivo que contêm a definição do cenário (mec, serviços e requisições).
- Criar a lista de nós mec e a lista de serviços.
- Criar a lista de requisições a partir da lista de nós mec e a lista de serviços.
- Inicializar o Logger.

Passo 2
- Criar uma instância de simulação para cada algoritmo de distribuíção de carga.
- Criar nova lista de logs para receber os logs da instância de simulação.
- Gerar uma cópia da lista de requisições para cada algoritmo de entrada.
- Gerar uma lista de eventos (usuário enviando requisição para o nó mec) para cada lista de requisições,
  onde cada evento é gerado a partir de cada cópia de requisição.
- Passar a lista de eventos para a instância de simulação de cada algoritmo de distribuíção de carga.
	- Adicionar todos os eventos na fila ordenada de eventos do scheduler.
- Resetar todos os nós mecs.

Parte 3
- Obter a primeira instância de simulação da lista de instâncias e removê-la da lista.
- Iniciar a simulação.

Parte 4 (simulação)
- Obter e remover o primeiro evento da fila ordenada de eventos do scheduler.
- Mover o ponteiro do relógio até o momento temporal do acontecimento do evento.
- Obter a função de evento e invocar a função.
	- Cada função pode adicionar novos eventos no scheduler.
- Repetir até a fila de eventos acabar.

Parte 5
- Repetir a parte 3 até a lista de instâncias ficar vazia.

Parte 6
- Obter a lista de logs de cada simulação
- Salvar a lista de logs de cada simulação em uma planilha

Parte 7
- Finish :)

'''