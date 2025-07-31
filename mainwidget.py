from kivymd.app import MDApp
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.screen import Screen
from kivy.core.window import Window
from kivy.lang.builder import Builder
from bottonlist import Botton_list
from popup import Modbus_Popup, Scan_Popup




class MainWidget(Screen):
    """
        Classe que contrói a interface gráfica do supervisório com imagens,
        botões, caixas de textos, popup e etc...
    """
    def __init__(self,scan_timemain, **kwargs):
        """Construtor princial da classe MainWidget."""
        super().__init__(**kwargs)
        #kwargs será usado para permitir inúmeras passagens de variável de argumentos nomeados,
        #devem ser usados os mesmos nomes para não haver erros ou conflitos
        self._scan_time = kwargs.get('scan_timemain')
        self.ip = kwargs.get('ipmain')
        self.porta = kwargs.get('portamain')
        #Chamada das janelas segundárias (popup) já definido os valores nas linhas 22,23 e 24
        self._j_modbusPopup = Modbus_Popup(ip=self.ip, porta=self.porta)
        self._j_scanPopup = Scan_Popup(scan_time=self._scan_time)
   


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
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.primary_hue = "A100"
        self.widget = MainWidget(scan_timemain = 1000) #Mesmos nome dos get
        Window.maximize()        
        return self.widget
    
    def on_start(self):
        """
            Método do KivyMD que será inicializado logo após a execução do metódo build.
            Tal método servirá para carregar e executar a lista ao clicar no botão dos dados
        """
        self.list1 = Botton_list(self.root)
        self.list1.lista()
        
    
