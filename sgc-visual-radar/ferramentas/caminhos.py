# -*- coding: utf-8 -*-
"""Resolucao de caminhos: funciona tanto na pasta de trabalho quanto no
pacote de fontes entregue (onde as entradas ficam em `entrada/`)."""
import os

FERRAMENTAS = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(FERRAMENTAS)


def entrada(nome):
    """Pasta de entrada `nome` (ex.: 'sgc', 'pkg', 'build_rev01')."""
    for candidato in (os.path.join(RAIZ, nome), os.path.join(RAIZ, 'entrada', nome)):
        if os.path.isdir(candidato):
            return candidato
    raise SystemExit(
        "Entrada '%s' nao encontrada. Esperado em %s ou %s."
        % (nome, os.path.join(RAIZ, nome), os.path.join(RAIZ, 'entrada', nome)))


def saida(nome='build'):
    return os.path.join(RAIZ, nome)
