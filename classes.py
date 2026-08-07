import random

from personagem import Personagem


class Guerreiro(Personagem):
    def __init__(self, nome):
        super().__init__(nome, 120, 18, 8, 2)

    def atacar(self, alvo):
        dano = random.randint(self.ataque - 3, self.ataque + 3)
        alvo.receber_dano(dano)
        print(self.nome, "atacou sem falhar e causou", dano, "de dano")

    def habilidade_especial(self, alvo):
        if self.recarga > 0:
            print(self.nome, "precisa aguardar mais", self.recarga, "turno(s) para usar o Golpe Esmagador!")
            return
        
        dano_especial = self.ataque + 10
        print(self.nome, "usa Golpe Esmagador em", alvo.nome, "!")
        alvo.receber_dano(dano_especial)

        self.recarga = 3

class Mago(Personagem):
    def __init__(self, nome):
        super().__init__(nome, 70, 10, 3, 4)

    def habilidade_especial(self, alvo):
        if self.recarga >0:
            print(self.nome, "precisa aguardar mais", self.recarga, "turno(s) para usar a Bola de Fogo!")
            return
        
        dano_magico = self.ataque + 10
        print(self.nome, "lança Bola de Fogo em", alvo.nome, "!")
        alvo.receber_dano(dano_magico)
        
        self.recarga = 2 

    def defender(self):
        super().defender()
        self.curar(10)
        print(self.nome, "recuperou 10 de vida")


class Goblin(Personagem):
    def __init__(self):
        super().__init__("Goblin", 40, 8, 2, 0)


class Orc(Personagem):
    def __init__(self):
        super().__init__("Orc", 70, 12, 4, 0)


class Troll(Personagem):
    def __init__(self):
        super().__init__("Troll", 100, 16, 6, 0)

    def atacar(self, alvo):
        rolagem = random.randint(1, 20)
        if rolagem < 9:
            print("O Troll errou feio")
            return
        dano = random.randint(self.ataque, self.ataque + 10)
        alvo.receber_dano(dano)
        print("O Troll acertou um golpe de", dano)


class Esqueleto(Personagem):
    def __init__(self):
        super().__init__("Esqueleto", 55, 11, 3, 0)

    def receber_dano(self, quantidade):
        print("Os ossos rangem")
        super().receber_dano(quantidade)


class Dragao(Personagem):
    def __init__(self):
        super().__init__("Dragão Ancião", 110, 14, 4, 0)
        self._turnos = 0

    def atacar(self, alvo):
        self._turnos += 1

        if self._turnos % 3 == 0:
            dano = self.ataque + 8
            print("O Dragão solta um sopro de fogo!")
            alvo.receber_dano(dano + alvo.defesa)
            print("O sopro causou", dano, "de dano e ignorou a defesa")
            return

        super().atacar(alvo)