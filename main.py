from classes import Dragao, Goblin, Guerreiro, Mago, Orc, Troll, Esqueleto, Berserker
from itens import AnelDeProtecao, ElixirDeFuria, PocaoDeVida

CLASSES = {
    "1": Guerreiro,
    "2": Mago,
}


class Fase:
    def __init__(self, nome, descricao, inimigo, premio):
        self.nome = nome
        self.descricao = descricao
        self.inimigo = inimigo
        self.premio = premio


def escolher_personagem():
    print("Escolha o seu personagem:")
    for tecla, classe in CLASSES.items():
        print(tecla, "-", classe.__name__)

    escolha = input("Opção: ")
    while escolha not in CLASSES:
        print("Opção inválida")
        escolha = input("Opção: ")

    nome = input("Nome: ")
    return CLASSES[escolha](nome)


def turno_do_jogador(jogador, inimigo):
    acoes = {
        "1": ("\n1 - Atacar", lambda j, i: j.atacar(i)),
        "2": ("2 - Defender", lambda j, i: j.defender()),
        "3": ("3 - Abrir a mochila", lambda j, i: abrir_mochila(j, i)),
        "4": ("4 - Usar habilidade especial", lambda j, i: j.usar_habilidade(i)),
    }

    for rotulo, _ in acoes.values():
        print(rotulo)

    escolha = input("Escolha: ")

    if escolha not in acoes:
        print("Opção inválida")
        return

    _, funcao = acoes[escolha]
    funcao(jogador, inimigo)


def abrir_mochila(jogador, inimigo):
    if jogador.inventario.esta_vazio():
        print("A mochila esta vazia")
        return

    jogador.inventario.listar()
    escolha = input("Qual item? (0 para voltar) ")

    if not escolha.isdigit() or escolha == "0":
        return

    item = jogador.inventario.tirar(int(escolha))
    if item is None:
        print("Esse item nao existe")
        return

    item.usar(jogador, inimigo)


def combate(jogador, inimigo):
    while jogador.esta_vivo() and inimigo.esta_vivo():
        jogador.mostrar_status()
        inimigo.mostrar_status()

        jogador.iniciar_turno()
        turno_do_jogador(jogador, inimigo)

        if inimigo.esta_vivo():
            inimigo.iniciar_turno()
            inimigo.agir(jogador)

    if jogador.esta_vivo():
        print("Vitória contra", inimigo.nome)
        return True

    print("Você foi derrotado")
    return False


def recompensar(jogador, fase):
    jogador.subir_nivel()

    jogador.curar(50)
    print(jogador.nome, "descansa e recupera 50 de vida")

    jogador.inventario.adicionar(fase.premio)
    print(fase.inimigo.nome, "deixou cair:", fase.premio)


def main():
    jogador = escolher_personagem()

    fases = [
        Fase("Floresta Sombria", "Um Goblin salta na sua frente.", Goblin(), PocaoDeVida()),
        Fase("Cemitério de Sombras", "Um Esqueleto reanimado junta seus ossos para o combate.", Esqueleto(), AnelDeProtecao()),
        Fase("Vale dos Selvagens", "Um Berserker enfurecido corre em sua direção!", Berserker(), PocaoDeVida()),
        Fase("Trilha da Montanha", "Um Orc bloqueia o caminho.", Orc(), ElixirDeFuria()),
        Fase("Ponte Quebrada", "Um Troll ronca embaixo da ponte.", Troll(), AnelDeProtecao()),
        Fase("Covil do Dragão", "O Dragão Ancião desperta.", Dragao(), PocaoDeVida()),
    ]

    for fase in fases:
        print("\n==", fase.nome, "==")
        print(fase.descricao)

        venceu = combate(jogador, fase.inimigo)
        if not venceu:
            print("Fim de jogo.")
            return

        recompensar(jogador, fase)

    print("\nVocê derrotou todos os inimigos. Fim.")


if __name__ == "__main__":
    main()