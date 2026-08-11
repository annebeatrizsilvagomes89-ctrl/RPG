import random

from itens import Inventario, PocaoDeVida


class Personagem:
    def __init__(self, nome, vida, ataque, defesa, pocoes):
        self.nome = nome
        self._vida = vida
        self._vida_maxima = vida
        self.ataque = ataque
        self.defesa = defesa
        self.defendendo = False
        self.nivel = 1
        self._bonus_ataque = 0
        self._turnos_bonus_ataque = 0
        self._bonus_defesa = 0
        self._turnos_bonus_defesa = 0

        self.recarga = 0

        self.inventario = Inventario()
        for _ in range(pocoes):
            self.inventario.adicionar(PocaoDeVida())

    @property
    def vida(self):
        return self._vida

    @property
    def vida_maxima(self):
        return self._vida_maxima

    def __str__(self):
        return f"{self.nome} ({self._vida}/{self._vida_maxima})"

    def recarga_habilidade(self):
        return self.recarga

    def mostrar_status(self):
        print("\n", self.nome)
        print("Vida:", self._vida, "/", self._vida_maxima)
        print("Mochila:", self.inventario.quantidade(), "item(ns)")

        if self.recarga  == 0:
            print("Pode usar a habilidade especial")

        else:
            print("Espere mais ", self.recarga, " turno(s)")

    def esta_vivo(self):
        return self._vida > 0

    def iniciar_turno(self):
        self.defendendo = False

        if self.recarga >0:
            self.recarga -= 1

        if self._turnos_bonus_ataque >  0:
            self._turnos_bonus_ataque -= 1

            if self._turnos_bonus_ataque == 0:
                self.ataque -= self._bonus_ataque
                self._bonus_ataque = 0

                print(self.nome, "sente o ataque voltar ao normal")

        if self._turnos_bonus_defesa >  0:
            self._turnos_bonus_defesa -= 1

            if self._turnos_bonus_defesa == 0:
                self.defesa -= self._bonus_defesa
                self._bonus_defesa = 0

                print(self.nome, "sente a defesa voltar ao normal")

    def curar(self, quantidade):
        if quantidade <= 0:
            return
        self._vida = min(self._vida + quantidade, self._vida_maxima)

    def receber_dano(self, quantidade):
        dano_real = quantidade - self.defesa

        if self.defendendo:
            dano_real = dano_real // 2

        dano_real = max(0, dano_real)
        self._vida = max(0, self._vida - dano_real)

    def atacar(self, alvo):
        rolagem = random.randint(1, 20)

        if rolagem < 5:
            print(self.nome, "errou o ataque")
            return

        dano = random.randint(self.ataque - 3, self.ataque + 3)
        alvo.receber_dano(dano)
        print(self.nome, "causou", dano, "de dano")

    def defender(self):
        self.defendendo = True
        print(self.nome, "preparou a defesa")

    def melhorar_ataque(self, quantidade):
        self.ataque += quantidade

    def melhorar_defesa(self, quantidade):
        self.defesa += quantidade

    def melhorar_vida_maxima(self, quantidade):
        self._vida_maxima += quantidade
        self._vida += quantidade

    def subir_nivel(self):
        self.nivel += 1
        self.melhorar_ataque(4)
        self.melhorar_defesa(2)
        self.melhorar_vida_maxima(20)

        print(self.nome, "subiu para o nível", self.nivel)

    def aplicar_bonus_ataque_temporario(self, quantidade, turnos):
        self.ataque += quantidade
        self._bonus_ataque = quantidade
        self._turnos_bonus_ataque = turnos
        print(self.nome, "sente o ataque aumentar por um tempo")

    def aplicar_bonus_defesa_temporario(self, quantidade, turnos):
        self.defesa += quantidade
        self._bonus_defesa = quantidade
        self._turnos_bonus_defesa = turnos
        print(self.nome, "sente a defesa aumentar por um tempo")

    def habilidade_especial(self, alvo):
        print(self.nome, "ainda não possui uma habilidade especial.")
        if self.recarga >0:
            print(self.nome, "precisa aguardar mais", self.recarga, "turno(s) para usar a Bola de Fogo!")
            return

        dano_magico = self.ataque + 10
        print(self.nome, "lança Bola de Fogo em", alvo.nome, "!")

        self.recarga = 2 

    def agir(self, alvo):
        self.atacar(alvo)