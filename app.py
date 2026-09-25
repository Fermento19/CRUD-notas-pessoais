import flet as ft
from files import Notas
from files import datetime

def main(page: ft.Page):
    page.theme_mode = "light"

    notas = Notas("notas.json")
    

    top_menu = ft.Container(
        height=90,
        padding=20,
        alignment=ft.Alignment.CENTER,
        bgcolor="blue"
    )



    conteudo = ft.Container(
        expand=True,
        padding=20
    )


    def tela_inicial():
        carregar_cards()
        top_menu.content = ft.Text(
            "Minhas Notas",
            size=30,
            align=ft.Alignment.CENTER
        )

        

        page.update()

    def mostrar_nota(nota):
        top_menu.content = ft.Row([
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda e: tela_inicial()
            ),

            ft.Text(
                "Voltar",
                size=30
            ),

            ft.VerticalDivider(),

            ft.IconButton(
                icon=ft.Icons.POWER_OFF,
                on_click=lambda e: excluir_nota(nota["id"])
            ),

            ft.Text(
                "Excluir",
                size=30
            ),

            ft.VerticalDivider(),

            ft.IconButton(
                icon=ft.Icons.SETTINGS,
                on_click=lambda e: editar_nota(nota["id"])
            ),

            ft.Text(
                "Editar",
                size=30
            )
        ])

        conteudo.content = ft.Column([
            ft.Text(
                nota["titulo"],
                size=40
            ),

            ft.Text(
                f'Arquivo Criado em {nota["data de criacao"]}',
                size=10,
                tooltip=f'Data de modificação: {nota["data de modificacao"]}'
            ),

            ft.Divider(),

            ft.Text(
                nota.get("conteudo", "Sem conteúdo."),
                size=18
            )
        ],scroll=ft.ScrollMode.AUTO)

        page.update()

    def buscar_nota(id_nota):
        for nota in notas.dado_bruto:
            if nota["id"] == id_nota:
                return nota

        return None

    def expandir_obj(e):
        nota = buscar_nota(e.control.data)
        if nota:
            mostrar_nota(nota)
               

    def excluir_nota(id_nota):
        for nota in notas.dado_bruto:
            if nota["id"] == id_nota:    
                notas.dado_bruto.remove(nota)
                break
            
        notas.salvar_alteracoes()
        tela_inicial()

    def criar_nova_nota():
        editar_nota(notas.criar_nota_branca())


    def editar_nota(id_nota):
        nota = buscar_nota(id_nota)

        campo_titulo = ft.TextField(
            label="Título",
            value=nota["titulo"],
            autofocus=True
        )

        campo_conteudo = ft.TextField(
            label="Conteúdo",
            value=nota.get("conteudo", ""),
            multiline=True,
            min_lines=10,
            max_lines=20,
            expand=True
        )

        def cancelar(e):
            mostrar_nota(nota)

        def submit(e):
            agr = datetime.now()
            for nota in notas.dado_bruto:
                if nota["id"] == id_nota and campo_titulo.value.strip() != "":    
                    nota["titulo"] = campo_titulo.value
                    nota["conteudo"] = campo_conteudo.value
                    nota["data de modificacao"] = f"{agr.day}/{agr.month}/{agr.year}"
                    break
            notas.salvar_alteracoes()

            mostrar_nota(nota)

        top_menu.content = ft.Row([
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                on_click=cancelar
            ),

            ft.Text(
                "Editar nota",
                size=30
            )
        ])

        conteudo.content = ft.Column([
            campo_titulo,

            campo_conteudo,

            ft.Row([
                ft.IconButton(
                    ft.Icons.CANCEL,
                    on_click=cancelar
                ),
                ft.Text("Cancelar"),
                ft.VerticalDivider(),
                ft.IconButton(
                    ft.Icons.SAVE,
                    on_click=submit
                ),
                ft.Text("Salvar Alterações")
            ])
        ], expand=True)

        page.update()

    def carregar_cards():
        notas.ler_notas()
        linha_cards = ft.Row(
        wrap=True,
        expand=True
        )
        
        for i in notas.dado_bruto:
            linha_cards.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(
                            icon=ft.Icons.BOOK,
                            size=100
                        ),

                        ft.Text(
                            i["titulo"],
                            text_align=ft.TextAlign.CENTER
                        )
                    ]),
                    alignment=ft.Alignment.CENTER,
                    width=150,
                    height=150,
                    bgcolor="blue",

                    data=i["id"],
                    on_click=expandir_obj
                )
            )
        linha_cards.controls.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    icon=ft.Icons.ADD,
                                    size=100
                                ),
        
                                ft.Text(
                                    "Criar Nota",
                                    text_align=ft.TextAlign.CENTER
                                )
                            ]),
                            alignment=ft.Alignment.CENTER,
                            width=150,
                            height=150,
                            bgcolor="blue",
                            on_click=criar_nova_nota
                        )
                    )
        conteudo.content = linha_cards

    tela_inicial()
    layout = ft.Column([
        top_menu,
        conteudo
    ], expand=True)

    page.add(layout)


ft.run(main)