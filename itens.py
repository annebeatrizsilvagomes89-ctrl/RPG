class Item:
    """A base de todo item. Guarda o nome e promete um usar()."""

    def __init__(self, nome):
        self.nome = nome

    def usar(self, dono, inimigo):
        print(self.nome, "nao faz nada")

    def __str__(self):
        return self.nome


class PocaoDeVida(Item):
    def __init__(self):
        super().__init__("Poção de vida")
        self.cura = 25

    def usar(self, dono, inimigo):
        dono.curar(self.cura)
        print(dono.nome, "bebeu a poção e recuperou", self.cura, "de vida")


class Bomba(Item):
    def __init__(self):
        super().__init__("Bomba")
        self.dano = 30

    def usar(self, dono, inimigo):
        inimigo.receber_dano(self.dano)
        print("A bomba explodiu em", inimigo.nome, "causando", self.dano, "de dano")


class PocaoDeForca(Item):
    def __init__(self):
        super().__init__("Poção de força")
        self.forca = 5

    def usar(self, dono, inimigo):
        dono.ataque += self.forca
        print(dono.nome, "ganhou ataque")


class AnelDeProtecao(Item):
    def __init__(self):
        super().__init__("Anel de proteção")
        self.protecao = 5

    def usar(self, dono, inimigo):
        dono.defesa += self.protecao
        print(dono.nome, "ganhou defesa")


class Inventario:
    """Dono da colecao. Ninguem mexe na lista de fora."""

    def __init__(self):
        self._itens = []

    def adicionar(self, item):
        self._itens.append(item)

    def esta_vazio(self):
        return len(self._itens) == 0

    def quantidade(self):
        return len(self._itens)

    def listar(self):
        if self.esta_vazio():
            print("A mochila esta vazia")
            return
        for numero, item in enumerate(self._itens, 1):
            print(numero, "-", item)

    def tirar(self, numero):
        indice = numero - 1
        if indice < 0 or indice >= len(self._itens):
            return None
        return self._itens.pop(indice)

class ElixirDeFuria(Item):
    def __init__(self):
        super().__init__("Elixir de Fúria")
        self.forca = 6
        self.duracao = 3

    def usar(self, dono, inimigo):
        dono.aplicar_bonus_ataque_temporario(self.forca, self.duracao)
        print(dono.nome, "bebeu o elixir de fúria")