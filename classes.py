import random

from personagem import Personagem

VIDA_BAIXA_GOBLIN = 0.3
VIDA_BAIXA_ORC = 0.5
VIDA_BAIXA_TROLL = 0.4

FORCA_DA_FURIA = 6
DURACAO_DA_FURIA = 3

FORCA_DO_ENDURENCIMENTO = 5
DURACAO_DO_ENDURENCIMENTO = 3

class Guerreiro(Personagem):
    def __init__(self, nome):
        super().__init__(nome, 120, 18, 8, 2)

    def atacar(self, inimigo):
        dano = self.calcular_dano()
        inimigo.receber_dano(dano)
        print(self.nome, "atacou sem falhar e causou", dano, "de dano")

    def mensagem_de_recarga(self):
        print(self.nome, "precisa aguardar mais", self.recarga, "turno(s) para usar o Golpe Esmagador!")

    def turnos_de_recarga(self):
        return 2

    def habilidade_especial(self, alvo):
        if self.recarga > 0:
            print(self.nome, "precisa aguardar mais", self.recarga, "turno(s) para usar o Golpe Esmagador!")
            return
        
        dano_especial = self.ataque + 10
        print(self.nome, "usa Golpe Esmagador em", alvo.nome, "!")
        alvo.receber_dano(dano_especial)

        self.recarga = 3

    def efeito_da_habilidade(self, alvo):
        dano_especial = self.ataque + 10
        print(self.nome, "usa Golpe Esmagador em", alvo.nome, "!")
        alvo.receber_dano(dano_especial)
        pass

class Mago(Personagem):
    def __init__(self, nome):
        super().__init__(nome, 70, 10, 3, 4)

    def mensagem_de_recarga(self):
        print(self.nome, "precisa aguardar mais", self.recarga, "turno(s) para usar a Bola de Fogo!")

    def turnos_de_recarga(self):
        return 2 

    def habilidade_especial(self, alvo):
        if self.recarga >0:
            self.mensagem_de_recarga()
            return
        
        dano_magico = self.ataque + 10
        print(self.nome, "lança Bola de Fogo em", alvo.nome, "!")
        alvo.receber_dano(dano_magico)
        
        self.recarga = 2 

    def efeito_da_habilidade(self, alvo):
        dano_magico = self.ataque + 10
        print(self.nome, "lança Bola de Fogo em", alvo.nome, "!")
        alvo.receber_dano(dano_magico)

    def defender(self):
        super().defender()
        self.curar(10)
        print(self.nome, "recuperou 10 de vida")

class Goblin(Personagem):
    def __init__(self):
        super().__init__("Goblin", 40, 8, 2, 0)

    def agir(self, alvo):
        if self._vida / self.vida_maxima <= VIDA_BAIXA_GOBLIN:
            print("O Goblin recua assustado!")
            self.defendendo = True
            pass
        else:
            self.atacar(alvo)

class Orc(Personagem):
    def __init__(self):
        super().__init__("Orc", 70, 12, 4, 0)

    def agir(self, alvo):
        if self._vida / self.vida_maxima <= VIDA_BAIXA_ORC and not self.enfureceu:
            print(self.nome, "entra em fúria!")

            self.aplicar_bonus_ataque_temporario(FORCA_DA_FURIA, DURACAO_DA_FURIA)

            self.aumentar_ataque_temporario(5, 3)

            self.enfureceu = True

            self.atacar(alvo)
        else:
            self.atacar(alvo)

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

    def agir(self, alvo):
        if self._vida / self.vida_maxima <= VIDA_BAIXA_TROLL and not self.protegeu:
            print(self.nome, "ergue o escudo para se proteger!")

            self.aplicar_bonus_ataque_temporario(FORCA_DO_ENDURENCIMENTO, DURACAO_DO_ENDURENCIMENTO)
            self.protegeu = True
        else:
            self.atacar(alvo)

class Esqueleto(Personagem):
    def __init__(self):
        super().__init__("Esqueleto", 55, 11, 3, 0)

    def receber_dano(self, quantidade):
        print("Os ossos rangem")
        super().receber_dano(quantidade)

    def habilidade_especial(self, alvo):
        cura = 20

        self.vida = min(self.vida_maxima, self.vida + cura)
        print(self.nome, "se junta novamente e recupera ", cura, " de vida!")
        self._recarga_habilidade = 3

    def agir(self, alvo):
        if self._recarga_habilidade == 0 and self.vida < self.vida_maxima:
            self.usar_habilidade(alvo)
        else:
            self.atacar(alvo)

class Dragao(Personagem):
    def __init__(self):
        super().__init__("Dragão Ancião", 110, 14, 4, 0)

    def mensagem_de_recarga(self):
        print(self.nome, "precisa aguardar mais", self.recarga, "turno(s) para usar o Sopro de Fogo!")

    def habilidade_especial(self, alvo):
        if self._recarga_habilidade == 0:
            dano = self.ataque + 8
            print("O Dragão solta um sopro de fogo!")
            alvo.receber_dano(dano + alvo.defesa)
            print("O sopro causou", dano, "de dano e ignorou a defesa")
            self._recarga_habilidade = 3  

    def efeito_da_habilidade(self, alvo):
        dano = self.ataque + 8
        print("O Dragão solta um sopro de fogo!")
        alvo.receber_dano(dano + alvo.defesa)
        print("O sopro causou", dano, "de dano e ignorou a defesa")
        self._recarga_habilidade = 3

    def atacar(self, alvo):
        super().atacar(alvo)

    def agir(self, alvo):
        if self._recarga_habilidade == 0:
            self.habilidade_especial(alvo)
        else:
            self.atacar(alvo)

class Arqueiro(Personagem):
    def __init__(self, nome, vida, ataque, defesa, pocoes):
        super().__init__(nome, vida, ataque, defesa, pocoes)

    def habilidade_especial(self, alvo):
        if self.recarga >0:
            print(self.nome, "precisa aguardar ", self.recarga, "turno(s) para usar Tiro Preciso")
            return

        dano_critico = int(self.ataque * 1.8)
        cura = 5

        print(self.nome, "dispara um Tiro Preciso em ", alvo.nome, " e recupera vida!")
        alvo.receber_dano(dano_critico)

        self._vida = min(self._vida_maxima, self._vida + cura)
        print(self.nome, "recuperou", cura, "de vida!")

        self.recarga = 3

class Berserker(Personagem):
    def __init__(self):
        super().__init__("Berserker", 70, 12, 2, 0)

    def habilidade_especial(self, alvo):
        vida_perdida = self.vida_maxima - self.vida
        dano_bonus = vida_perdida // 2
        dano_total = self.ataque + dano_bonus

        print(f"O {self.nome} entra em FÚRIA! (+{dano_bonus} de dano extra)")
        alvo.receber_dano(dano_total)
        self._recarga_habilidade = 2

    def agir(self, alvo):
        if self.vida <= (self.vida_maxima / 2) and self._recarga_habilidade == 0:
            self.habilidade_especial(alvo)
        else:
            self.atacar(alvo)