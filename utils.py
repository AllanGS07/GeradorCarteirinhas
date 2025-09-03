# utils.py (VERSÃO FINAL COM MELHORIA NO TITLE CASE)

import os
import sys

def title_case_formatter(text: str) -> str:
    """ Formata texto para ter a primeira letra de cada palavra em maiúscula, tratando a entrada. """
    # Força para minúsculas primeiro para garantir que "NOME TODO EM CAIXA ALTA" funcione
    return text.lower().title() 

# Função para formatar números de telefone
def format_telefone(numero: str) -> str:
    """ Formata uma string de dígitos para (XX) XXXXX-XXXX ou (XX) XXXX-XXXX. """
    numeros_limpos = "".join(filter(str.isdigit, numero))
    
    if len(numeros_limpos) == 11:
        ddd = numeros_limpos[:2]
        parte1 = numeros_limpos[2:7]
        parte2 = numeros_limpos[7:]
        return f"({ddd}) {parte1}-{parte2}"
    elif len(numeros_limpos) == 10:
        ddd = numeros_limpos[:2]
        parte1 = numeros_limpos[2:6]
        parte2 = numeros_limpos[6:]
        return f"({ddd}) {parte1}-{parte2}"
    else:
        return numero

# Função para formatar o CEP
def format_cep(cep: str) -> str:
    """ Formata uma string de dígitos para XXXXX-XXX. """
    numeros_limpos = "".join(filter(str.isdigit, cep))
    
    if len(numeros_limpos) == 8:
        parte1 = numeros_limpos[:5]
        parte2 = numeros_limpos[5:]
        return f"{parte1}-{parte2}"
    else:
        return cep

def resource_path(relative_path):
    """ Obtém o caminho absoluto para o recurso. """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)