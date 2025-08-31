from abc import ABC, abstractmethod
from datetime import datetime
import random

MENU = """

[d] Depositar
[s] Sacar
[e] Extrato
[u] Usuário
[c] Conta
[l] Listar Contas
[q] Sair

"""
AGENCIA_PADRAO = "0001"
contas = []
usuarios = {}

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        
    def adicionar_conta(self, conta):
        self.contas.append(conta)
        
class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = AGENCIA_PADRAO
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
        if valor > self.saldo:
            print(f"Operação falhou! O saldo atual de R$ {self.saldo:.2f} não é suficiente para sacar.")
               
        elif valor > 0:
            self._saldo -= valor
            print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
            return True
        
        else:
            print(f"O valor de {valor} é inválido.")
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"O depósito de R$ {valor:.2f} foi realizado com sucesso!")
            return True
        else:
            print("O valor informado é inválido para depositar.")
            return False
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["Tipo"] == "Saque"]
        )
        
        if valor > self.limite:
            print(f"A operação falhou. O valor solicitado para saque de R$ {valor:.2f} é maior do que o R$ {self.limite:.2f}")
            
        elif numero_saques >= self.limite_saques:
            print("A operação falhou. Você já realizou o número limite de saques diários.")
        
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self):
        return f"""
        Agência: {self.agencia}
        Conta Corrente: {self.numero}
        Titular: {self.cliente.nome}
    """
        
class Historico:
    def __init__(self):
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "Tipo": transacao.__class__.__name__,
                "Valor": transacao.valor,
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
        )
        
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
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
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)
            
def criar_usuario():
    cpf = input("Digite seu CPF (apenas números): ")
    
    if cpf in usuarios:
        print("CPF já está cadastrado.")
        return usuarios[cpf]
        
    nome = input("Digite seu nome completo: ").capitalize()
    data_nascimento = input("Digite sua data de nascimento (dd/mm/aaaa): ")
    logradouro = input("Logradouro: ").capitalize()
    numero = input("Número: ")
    bairro = input("Bairro: ").capitalize()
    cidade = input("Cidade: ").capitalize()
    uf = input("UF: ").upper()
    
    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{uf}"
    usuario = PessoaFisica(cpf, nome, data_nascimento, endereco)
    usuarios[cpf] = usuario
    print("Usuário criado com sucesso!")
    return usuario

def criar_conta(usuario=None):
    cpf = input("Digite o CPF do titular da conta: ")
    usuario = usuarios.get(cpf)
    
    if not usuario:
        print("O CPF digitado não está cadastrado.")
        usuario = criar_usuario()
    if usuario.contas:
        print("O CPF já está cadastrado!")
    else:
        numero_conta = random.randint(100000, 999999)
        
        while any(conta.numero == numero_conta for conta in contas):
            numero_conta = random.randint(100000, 999999)
        
        conta = ContaCorrente(numero=numero_conta, cliente=usuario)
        contas.append(conta)
        usuario.adicionar_conta(conta)
        print(f"Conta {numero_conta} criada com sucesso!")    
        return conta

def listar_contas():
    if not contas:
        print("Nenhuma conta cadastrada.")
        criar_conta_opcao = input("Gostaria de criar uma conta? (Y/N): ")
        
        if criar_conta_opcao.upper() == "Y":
            criar_conta()
        return
    
    for conta in contas:
        print(conta)

def depositar():
    cpf = input("CPF do titular: ")
    usuario = usuarios.get(cpf)
    
    if not usuario:
        print("Usuário não encontrado.")
        criar_usuario_opcao = input("Gostaria de criar um usuário? (Y/N): ")
        
        if criar_usuario_opcao.upper() == "N":
            print("Não é possível prosseguir.")
            return
        else:
            usuario = criar_usuario()
            conta = criar_conta(usuario)
            print(f"Conta criada automaticamente para {usuario.nome}")

    conta = usuario.contas[0]
    valor = float(input("Valor do depósito: "))
    transacao = Deposito(valor)
    usuario.realizar_transacao(conta, transacao)

def sacar():
    cpf = input("CPF do titular: ")
    usuario = usuarios.get(cpf)
    
    if not usuario:
        print("Usuário não encontrado.")
        criar_usuario_opcao = input("Gostaria de criar um usuário? (Y/N): ")
        
        if criar_usuario_opcao.upper() == "N":
            print("Não é possível prosseguir.")
            return
        else:
            usuario = criar_usuario()
            conta = criar_conta(usuario)
            print(f"Conta criada automaticamente para {usuario.nome}")

    conta = usuario.contas[0]
    valor = float(input("Valor do saque: "))
    transacao = Saque(valor)
    usuario.realizar_transacao(conta, transacao)

def exibir_extrato():
    cpf = input("CPF do titular: ")
    usuario = usuarios.get(cpf)
    
    if not usuario:
        print("Usuário não encontrado.")
        criar_usuario_opcao = input("Gostaria de criar um usuário? (Y/N): ")
        
        if criar_usuario_opcao.upper() == "N":
            print("Não é possível prosseguir.")
            return
        else:
            usuario = criar_usuario()
            conta = criar_conta(usuario)
            print(f"Conta criada automaticamente para {usuario.nome}")

    conta = usuario.contas[0]
    
    print("\n=============== EXTRATO ===============")
    
    if not conta.historico.transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in conta.historico.transacoes:
            print(f"{transacao['Tipo']}: R$ {transacao['Valor']:.2f} - {transacao['Data']}")
    
    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
    print("========================================")
    
def main():
    while True:
        opcao = input(MENU).lower()
        
        if opcao == "d":
            depositar()
            
        elif opcao == "s":
            sacar()
            
        elif opcao == "e":
            exibir_extrato()
        
        elif opcao == "u":
            criar_usuario()
            
        elif opcao == "c":
            criar_conta()
            
        elif opcao == "l":
            listar_contas()
            
        elif opcao == "q":
            print("Saindo...")
            break
        
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
