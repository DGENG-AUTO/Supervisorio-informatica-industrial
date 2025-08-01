from kivymd.app import MDApp
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.screen import Screen
from kivy.core.window import Window
from kivy.lang.builder import Builder
from popup import Modbus_Popup, Scan_Popup, Atuacao
from pyModbusTCP.client import ModbusClient




class MainWidget(Screen):
    """
        Classe que contrói a interface gráfica do supervisório com imagens,
        botões, caixas de textos, popup e etc...
    """
    def __init__(self,**kwargs):
        """Construtor princial da classe MainWidget."""
        super().__init__()

        #kwargs será usado para permitir inúmeras passagens de variável de argumentos nomeados,
        #devem ser usados os mesmos nomes para não haver erros ou conflitos
        self._scan_time = kwargs.get('scan_timemain')
        self._ip = kwargs.get('ipmain')
        self._porta = kwargs.get('portamain')

        #Chamada das janelas segundárias (popup) já definido os valores nas linhas 23,24 e 25
        self._j_modbusPopup = Modbus_Popup(ip=self._ip, porta=self._porta)
        self._j_scanPopup = Scan_Popup(scan_time=self._scan_time)
        self._j_atuacao = Atuacao()

        #criando a conexão MODBUS-TCP
        
   


class CardWidget(Screen):
    """
        Classe que armazena dados como corrente, tensão, velocidade etc...
    """
    pass    


class MainWidgetApp(MDApp):
    """
        Classe principal de desing da aplicação KivyMD.

        Esta classe herda de MDApp e é responsável por configurar e iniciar
        a interface gráfica do supervisório. Ou seja ela define a estrutura principal
        da aplicação, incluindo a inicialização de temas e a construção da tela.
    """ 
    def build(self):
        """Método que gera a janela matriz do Widget principal"""
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Gray'
        self.theme_cls.primary_hue = "500"
        self.widget = MainWidget(scan_timemain = 1000, ipmain='127.0.0.1', portamain=502) #Mesmos nome dos get
        Window.maximize()        
        return self.widget
   
    
