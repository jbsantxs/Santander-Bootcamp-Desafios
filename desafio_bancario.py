menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
conta_saques = 1

while True:
    opcao = input(menu)
    
    if opcao == "d":
        deposito = float(input("Digite O valor que deseja depositar: "))
        saldo += deposito
        if deposito < 0:
            deposito = 0
            print("Valor inválido Erro na operação")
        extrato += f"\nDepósito no valor de R$ {deposito:.2f}"
        
    elif opcao == "s":
        saque = float(input("Digite o valor de saque: "))
        if saque < 0:
            print("Valor inválido")
            saque = 0
        if saque > 500:
            print("O Limite de saque é de R$ 500.00")
            saque = 0
        if conta_saques > LIMITE_SAQUES:
            print("Limite de 3 saques diários excedido")
            saque = 0
        if saque > saldo:
            print("Saldo insuficiente")
            saque = 0
        if saque > 0:
            saldo -= saque
            print(f"\nSaque de R$ {saque:.2f} realizado. Saldo atual de: {saldo:.2f}")
            conta_saques += 1
            extrato +=  f"\nSaque no valor de R$ {saque:.2f}"
        
        
    elif opcao == "e":
        print(extrato)
        print(f"\nSaldo atual de R$ {saldo:.2f}")
        
    elif opcao == "q":
        break
    
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
        print(saldo)
