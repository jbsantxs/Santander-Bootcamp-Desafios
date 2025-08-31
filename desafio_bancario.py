menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[u] Usuário
[c] Conta
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
agencia = "0001"
contas = []
usuarios = []

def depositar(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso\n")

    else:
        print("Operação falhou! O valor informado é inválido.")
        
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo

    excedeu_limite = valor > limite

    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print(f"Saque de R$ {valor:.2f} realizado com sucesso")

    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato
   
def exibir_extrato(saldo, *, extrato):
    
    
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")
    
    return saldo, extrato
    
def criar_usuario():
    cpf = input("Digite seu CPF (apenas números): ")
    cpf = "".join(c for c in cpf if c.isdigit())
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            print("CPF já cadastrado")
            return
    nome = input("Digite seu nome Completo: ")
    data_nascimento = input("Digite sua data de nascimento (dd/mm/aaaa): ")
    logradouro = input("Digite o Logradouro do seu endereço (apenas rua/avenida/etc): ")
    numero = input("Digite o número de seu endereço: ")
    bairro = input("Digite o bairro de seu endereço: ")
    cidade = input("Digite a cidade de seu endereço: ")
    uf = input("Digite o UF de seu endereço: ")
    
    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{uf}"
    
    usuario = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    }
    
    usuarios.append(usuario)
    print("Usuário criado com sucesso")
    return usuarios
   
def criar_conta():
    cpf = input("Digite o seu CPF (apenas números): ")
    cpf = "".join(c for c in cpf if c.isdigit())
    
    usuario = None
    
    for u in usuarios:
        if u["cpf"] == cpf:
            usuario = u
            break
    if not usuario:
        print("CPF não cadastrado")
        return
         
    numero_conta = len(contas) + 1
    conta = {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "usuario": cpf
    }
    
    contas.append(conta)
    print(f"Conta {numero_conta} criada com sucesso")
    return contas

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        
        saldo, extrato = depositar(saldo, valor, extrato)

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))

        saldo, extrato = sacar(
            saldo=saldo,
            valor=valor,
            extrato=extrato,
            limite=limite,
            numero_saques=numero_saques,
            limite_saques=LIMITE_SAQUES,
        )
        

    elif opcao == "e":
        exibir_extrato(saldo, extrato=extrato)
        
    elif opcao == "u":
        criar_usuario()
        
    elif opcao == "c":
        criar_conta()

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
