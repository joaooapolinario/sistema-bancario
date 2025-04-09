
def menu():
    print('''
########-Seja bem vindo ao Banco Py!-########

1 - Sacar
2 - Depositar
3 - Extrato
4 - Cadastrar usuario
5 - Criar conta
6 - Listar contas
0 - Sair
-------------------------------------------
''')
    return input('Digite o número da operação desejada: ')


def saque(*, saldo, valor, quant_saques, saques, id_saque):

    if quant_saques > 0:

        if valor > 0:
            if valor > saldo:
                print('TRANSAÇÃO NÃO CONCLUIDA! Você nao possui saldo suficiente')
            else:
                if valor > 500:
                    print('TRANSAÇÃO NÃO CONCLUIDA! Você so pode sacar até R$500,00')
                else:
                    print(f'TRANSAÇÃO CONCLUIDA! Seu saque de R${valor :.2f} foi realizado com sucesso.')
                    saldo -=valor
                    quant_saques -= 1
                    saques.append({'id': id_saque, 'Valor' : valor})
                    id_saque +=1
                    print(f'saldo, {saldo}')

        else:
            print('Valor Inválido! O valor tem que ser maior que 0 (ZERO)')
        
    else:
        print('Você ja realizou os 3 saques diarios! O serviço de saques so estará disponivel amanhã.')

    return(saldo, quant_saques, saques, id_saque)
    
def deposito(saldo, valor, depositos, id_deposito,/):
    if valor > 0:
        saldo += valor 
        depositos.append({'id' : id_deposito, 'Valor': valor})
        id_deposito += 1
        print(f'TRANSAÇÃO CONCLUIDA! Seu deposito de R${valor :.2f} foi realizado com sucesso.')
        print(f'Seu saldo atual é de R${saldo :.2f}')
    else:
        print('Valor Inválido! O valor tem que ser maior que 0 (ZERO)')
    
    return(saldo, depositos, id_deposito)

def extrato(saldo,/,*, depositos, saques):
    print('Depositos')
    for dep in depositos:
        print(f'Id: {dep["id"]}, Valor: R${dep["Valor"]:.2f}')

    print('-'*29)
    print('Saques')
    for saq in saques:
        print(f'Id: {saq["id"]}, Valor: R${saq["Valor"]:.2f}')
    print('-'*29)

    print(f'O saldo atual da conta é de R${saldo :.2f}')
    print('-'*29)

def criar_usuario(usuarios):
    cpf = input('Digite o seu CPF: ')
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print('Esse CPF ja existe!')
    else:
        nome = input('Digite o seu nome: ')
        data_nascimento = input('Digite a sua data de nascimento: ')
        endereco = input('Digite o seu endereço(rua, N - bairro - cidade/estado): ')
        usuarios.append({'cpf': cpf, 'nome': nome, 'data_nascimento': data_nascimento, 'endereco': endereco})
        print('Usuario cadastrado com sucesso!')

def criar_conta(usuarios, agencia, n_conta):
    cpf = input('Digite o seu CPF: ')
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print('Conta criada com sucesso!')
        return ({'agencia': agencia, 'numero_conta': n_conta, 'usuario' : usuario})
        

    else:
        print('Usuario não encontrado!')
        return
    
def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def listar_contas(contas):

    for conta in contas:
        linha = f"""
        Agência:{conta['agencia']}
        Conta:{conta['numero_conta']}
        Titular:{conta['usuario']['nome']}
        """
        print('#'*30)
        print(linha)


def main():
    AGENCIA = '0001'
    saldo = 1500
    depositos = []
    saques = []
    id_deposito = 1
    id_saque = 1
    quant_saques = 3
    usuarios = []
    contas = []
    while True:
        operacao = menu()

        if operacao == '1': 
            print('-------ÁREA DE SAQUE!-------')
            print('-'*28)
            print(f'O limite de saques diarios é 3. Saques disponiveis-> {quant_saques}')
            print('O valor maximo por saque é de R$500,00')
            print(f'Seu saldo atual é de R${saldo :.2f}')
            print('-'*28)

            valor = float(input('Digite o valor que voce deseja sacar: '))

            saldo, quant_saques, saques, id_saque = saque(saldo=saldo, 
                                                        valor=valor, 
                                                        quant_saques=quant_saques, 
                                                        saques=saques, 
                                                        id_saque=id_saque)
            

        elif operacao == '2':
            print('-------ÁREA DE DEPOSITO!-------')

            valor = float(input('Digite o valor que deseja depositar em sua conta: '))

            saldo, depositos, id_deposito = deposito(saldo, 
                                                    valor, 
                                                    depositos, 
                                                    id_deposito)


        elif operacao == '3':
            print('------ÁREA DE EXTRATO!-------')
            extrato(saldo,
                    depositos=depositos, 
                    saques=saques)
        
        elif operacao == '4':
            print('------CADASTRO DE USUARIO-------')
            criar_usuario(usuarios)
        
        elif operacao == '5':
            print('------CRIAR CONTA-------')
            n_conta = len(contas) + 1
            conta = criar_conta(usuarios, AGENCIA, n_conta)

            if conta:
                contas.append(conta)

        elif operacao == '6':
            listar_contas(contas)


        elif operacao == '0':
            print('Obrigado por usar nossos serviços! Banco Py ')
            break

        else:
            print('Operação invalida! Digite um numero Válido.')

main()