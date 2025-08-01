"""from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem

class Botton_list():
    def __init__(self, root_widget):
        self.root = root_widget

    def lista(self):
        #------------PARTE DA CORRENTE------------
        menu_itens1 = [
            {"viewclass": "OneLineListItem",
             "text": "[b]Fase - R[/b]",
             "on_release": lambda texto1="Fase - R": self.selecionar_corrente(texto1)},
            {"viewclass": "OneLineListItem",
             "text": "[b]Fase - S[/b]",
             "on_release": lambda texto1="Fase - S": self.selecionar_corrente(texto1)},
            {"viewclass": "OneLineListItem",
             "text": "[b]Fase - T[/b]",
             "on_release": lambda texto1="Fase - T": self.selecionar_corrente(texto1)},
            {"viewclass": "OneLineListItem",
             "text": "[b]Neutro[/b]",
             "on_release": lambda texto1="Neutro": self.selecionar_corrente(texto1)},
            {"viewclass": "OneLineListItem",
             "text": "[b]Corrente média[/b]",
             "on_release": lambda texto1="Corrente média": self.selecionar_corrente(texto1)}
        ]

        self.menu1 = MDDropdownMenu(
            caller=self.root.ids.botao_corrente,
            items=menu_itens1,
            width_mult=5
        )
        #------------PARTE DA TENSÃO------------
        menu_itens2 = [
            {"viewclass": "OneLineListItem",
             "text": "[b]DDP entre fase R-S[/b]",
             "on_release": lambda texto2="DDP entre fase R-S": self.selecionar_tensao(texto2)},
            {"viewclass": "OneLineListItem",
             "text": "[b]DDP entre fase S-T[/b]",
             "on_release": lambda texto2="DDP entre fase S-T": self.selecionar_tensao(texto2)},
            {"viewclass": "OneLineListItem",
             "text": "[b]DDP entre fase T-R[/b]",
             "on_release": lambda texto2="DDP entre fase T-R": self.selecionar_tensao(texto2)}
        ]

        self.menu2 = MDDropdownMenu(
            caller=self.root.ids.botao_tensao,
            items=menu_itens2,
            width_mult=3
        )
        #------------PARTE DA THD TENSÃO------------
        menu_itens3 = [
            {"viewclass": "OneLineListItem",
             "text": "[b]THD Tensão entre fase R e Neutro[/b]",
             "on_release": lambda texto3="THD Tensão entre fase R e Neutro": self.selecionar_thd_tensao(texto3)},
            {"viewclass": "OneLineListItem",
             "text": "[b]THD Tensão entre fase S e Neutro[/b]",
             "on_release": lambda texto3="THD Tensão entre fase S e Neutro": self.selecionar_thd_tensao(texto3)},
            {"viewclass": "OneLineListItem",
             "text": "[b]THD Tensão entre fase T e Neutro[/b]",
             "on_release": lambda texto3="THD Tensão entre fase T e Neutro": self.selecionar_thd_tensao(texto3)},
             {"viewclass": "OneLineListItem",
             "text": "[b]THD Tensão entre fase R e S[/b]",
             "on_release": lambda texto3="THD Tensão entre fase R e S": self.selecionar_thd_tensao(texto3)},
             {"viewclass": "OneLineListItem",
             "text": "[b]THD Tensão entre fase S e T[/b]",
             "on_release": lambda texto3="THD Tensão entre fase S e T": self.selecionar_thd_tensao(texto3)},
             {"viewclass": "OneLineListItem",
             "text": "[b]THD Tensão entre fase R e S[/b]",
             "on_release": lambda texto3="THD Tensão entre fase T e R": self.selecionar_thd_tensao(texto3)}
        ]

        self.menu3 = MDDropdownMenu(
            caller=self.root.ids.botao_thd_tensao,
            items=menu_itens3,
            width_mult=6)
        #------------PARTE DA TEMPERATURA------------
        menu_itens4 = [
            {"viewclass": "OneLineListItem",
             "text": "[b]Temp. enrolamento fase R[/b]",
             "on_release": lambda texto4="Temp. enrolamento fase R": self.temp(texto4)},
            {"viewclass": "OneLineListItem",
             "text": "[b]Temp. enrolamento fase S[/b]",
             "on_release": lambda texto4="Temp. enrolamento fase S": self.temp(texto4)},
            {"viewclass": "OneLineListItem",
             "text": "[b]Temp. enrolamento fase T[/b]",
             "on_release": lambda texto4="Temp. enrolamento fase T": self.temp(texto4)},
             {"viewclass": "OneLineListItem",
             "text": "[b]Temp. da carcaça[/b]",
             "on_release": lambda texto4="Temp. da carcaça": self.temp(texto4)}
            ]

        self.menu4 = MDDropdownMenu(
            caller=self.root.ids.botao_temp,
            items=menu_itens4,
            width_mult=4)
        #------------PARTE DA POTÊNCIA ATIVA------------
        menu_itens5 = [
            {"viewclass": "OneLineListItem",
             "text": "[b]Fase R[/b]",
             "on_release": lambda texto5="Fase R": self.pot_ativa(texto5)},
            {"viewclass": "OneLineListItem",
             "text": "[b]Fase S[/b]",
             "on_release": lambda texto5="Fase S": self.pot_ativa(texto5)},
            {"viewclass": "OneLineListItem",
             "text": "[b]Fase T[/b]",
             "on_release": lambda texto5="Fase T": self.pot_ativa(texto5)},
             {"viewclass": "OneLineListItem",
             "text": "[b]Total[/b]",
             "on_release": lambda texto5= "Total": self.pot_ativa(texto5)}
            ]

        self.menu5 = MDDropdownMenu(
            caller=self.root.ids.botao_pt_ativa,
            items=menu_itens5,
            width_mult=4)
        #------------PARTE DA POTÊNCIA REATIVA------------
        menu_itens6 = [
            {"viewclass": "OneLineListItem",
             "text": "[b]Fase R[/b]",
             "on_release": lambda texto6="Fase R": self.pot_reativo(texto6)},
            {"viewclass": "OneLineListItem",
             "text": "[b]Fase S[/b]",
             "on_release": lambda texto6="Fase S": self.pot_reativo(texto6)},
            {"viewclass": "OneLineListItem",
             "text": "[b]Fase T[/b]",
             "on_release": lambda texto6="Fase T": self.pot_reativo(texto6)},
             {"viewclass": "OneLineListItem",
             "text": "[b]Total[/b]",
             "on_release": lambda texto6= "Total": self.pot_reativo(texto6)}
            ]

        self.menu6 = MDDropdownMenu(
            caller=self.root.ids.botao_pt_reativa,
            items=menu_itens6,
            width_mult=4)
        #------------PARTE DA POTÊNCIA REATIVA------------
        menu_itens7 = [
            {"viewclass": "OneLineListItem",
             "text": "[b]Fase R[/b]",
             "on_release": lambda texto7="Fase R": self.pot_aparente(texto7)},
            {"viewclass": "OneLineListItem",
             "text": "[b]Fase S[/b]",
             "on_release": lambda texto7="Fase S": self.pot_aparente(texto7)},
            {"viewclass": "OneLineListItem",
             "text": "[b]Fase T[/b]",
             "on_release": lambda texto7="Fase T": self.pot_aparente(texto7)},
             {"viewclass": "OneLineListItem",
             "text": "[b]Total[/b]",
             "on_release": lambda texto7= "Total": self.pot_aparente(texto7)}
            ]

        self.menu7 = MDDropdownMenu(
            caller=self.root.ids.botao_pt_aparente,
            items=menu_itens7,
            width_mult=4)


    def selecionar_corrente(self, texto1):
        self.root.ids.botao_corrente.text = texto1
        self.menu1.dismiss()

    def selecionar_tensao(self, texto2):
        self.root.ids.botao_tensao.text = texto2
        self.menu2.dismiss()

    def selecionar_thd_tensao(self, texto3):
        self.root.ids.botao_thd_tensao.text = texto3
        self.menu3.dismiss()
    
    def temp(self, texto4):
        self.root.ids.botao_temp.text = texto4
        self.menu4.dismiss()
    
    def pot_ativa(self, texto5):
        self.root.ids.botao_pt_ativa.text = texto5
        self.menu5.dismiss()

    def pot_reativo(self, texto6):
        self.root.ids.botao_pt_reativa.text = texto6
        self.menu6.dismiss()

    def pot_aparente(self, texto7):
        self.root.ids.botao_pt_aparente.text = texto7
        self.menu7.dismiss()"""

    
