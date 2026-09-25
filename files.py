import json
import uuid
import os
from datetime import datetime

class Notas:
    def __init__(self,caminho):
        self.caminho = caminho
        if not os.path.exists(self.caminho):
            self.criar_json()

    def criar_json(self):
        pasta = os.path.dirname(self.caminho)

        if pasta:
            os.makedirs(pasta, exist_ok=True)

        with open(self.caminho, 'w', encoding='utf-8') as file:
            json.dump([], file, ensure_ascii=False, indent=4)

    def ler_notas(self):
        with open(self.caminho,'r', encoding='utf-8') as file:
            self.dado_bruto = json.load(file)

    def gerar_id(self):
        return str(uuid.uuid4())

    def criar_nota_branca(self):
        agr = datetime.now()
        nova = {
            "id": self.gerar_id(),
            "titulo": "",
            "conteudo": "",
            "data de criacao": f"{agr.day}/{agr.month}/{agr.year}",
            "data de modificacao": f"{agr.day}/{agr.month}/{agr.year}"
        }
        self.dado_bruto.append(nova)
        return nova["id"]

    def qtd_notas(self):
        return len(self.dado_bruto)

    def salvar_alteracoes(self):
        with open(self.caminho,'w', encoding='utf-8') as file:
            json.dump(self.dado_bruto,file,ensure_ascii=False,indent=4)