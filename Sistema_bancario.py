menu = '''
########-Seja bem vindo ao Banco Py!-########

1 - Sacar
2 - Depositar
3 - Extrato
0 - Sair
-------------------------------------------
'''

saldo = 1500
depositos = []
saques = []
id_deposito = 1
id_saque = 1
quant_saques = 3
while True:
    print(menu)

    operacao = input('Qual operação você deseja realizar? ')

    if operacao == '1':
        print('-------ÁREA DE SAQUE!-------')
        print('-'*28)
        print(f'O limite de saques diarios é 3. Saques disponiveis-> {quant_saques}')
        print('O valor maximo por saque é de R$500,00')
        print(f'Seu saldo atual é de R${saldo :.2f}')
        print('-'*28)

        if quant_saques > 0:
        
            valor = float(input('Digite o valor que voce deseja sacar: '))
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

            else:
                print('Valor Inválido! O valor tem que ser maior que 0 (ZERO)')
        else:
            print('Você ja realizou os 3 saques diarios! O serviço de saques so estará disponivel amanhã.')

    elif operacao == '2':
        print('-------ÁREA DE DEPOSITO!-------')
        valor = float(input('Digite o valor que deseja depositar em sua conta: '))
        if valor > 0:
            saldo += valor 
            depositos.append({'id' : id_deposito, 'Valor': valor})
                  
            id_deposito += 1
        else:
            print('Valor Inválido! O valor tem que ser maior que 0 (ZERO)')


    elif operacao == '3':
        print('------ÁREA DE EXTRATO!-------')
        
        if depositos or saques:

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
        else:
            print('Não houve transaçoes na sua conta!')
    
    elif operacao == '0':
        print('Obrigado por usar nossos serviços! Banco Py ')
        break

    else:
        print('Operação invalida! Digite um numero Válido.')