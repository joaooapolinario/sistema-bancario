from abc import ABC, abstractmethod
from datetime import datetime


def menu():
    print('''
########-Seja bem vindo ao Banco Py!-########

1 - Depositar
2 - Sacar
3 - Extrato
4 - Cadastrar usuario
5 - Criar conta
6 - Listar contas
0 - Sair
-------------------------------------------
''')
    return input('Digite o número da operação desejada: ')

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()
            
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        if valor > 0 and valor <= self._saldo:
            self._saldo -= valor
            return True
        else:
            print('Saque não realizado! Verifique o valor e o saldo.')
            return False
        
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('Depósito realizado com sucesso!')
            return True
        else:
            print('Depósito não realizado! Verifique o valor.')
            return False
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        
        excedeu_limite = valor> self._limite
        excedeu_saques =numero_saques >= self._limite_saques

        if excedeu_limite:
            print('Operação não foi realizada! O valor excedeu o limite')
        elif excedeu_saques:
            print('Operação não realizada, Número máximo de saques atingido!')

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f'''Agencia: {self.agencia},
        C/C : {self.numero},
        Titular: {self.cliente.nome}'''
        
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @property
    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
    
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('Cliente não possui conta!')
        return 
    return cliente.contas[0]

def depositar(clientes):
    cpf = input('Digite o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado!')
        return
    
    valor = float(input('Digite o valor a ser depositado: '))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)

    if not conta: 
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input('Digite o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado!')
        return
    
    valor = float(input('Digite o valor a ser sacado: '))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\nDATA:\n\t{transacao['data']}\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
            

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

def criar_conta(numero_conta, clientes, contas):
    cpf = input('Digite o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado!')
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print('Conta criada com sucesso!')

def listar_contas(contas):
    for conta in contas:
        print(f"Agência: {conta.agencia}, Conta: {conta.numero}, Titular: {conta.cliente.nome}")
        print('-'*30)

def criar_cliente(clientes):
    cpf = input('Digite o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print('Cliente já cadastrado!')
        return
    
    nome = input('Digite o nome do cliente: ')
    data_nascimento = input('Digite a data de nascimento (dd/mm/aaaa): ')
    endereco = input('Digite o endereço (rua, N - bairro - cidade/estado): ')

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print('Cliente cadastrado com sucesso!')

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "4":
            criar_cliente(clientes)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "0":
            print('Obrigado por usar nossos serviços. BANCO PY')
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


main()
