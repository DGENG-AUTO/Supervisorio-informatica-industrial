from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivy.uix.label import Label


class Modbus_Popup(Popup):
    """
        Classe Modbus_Popup que abri uma segunda janela para configurar o protocolo Modbus.    
    """
    def __init__(self,ip,porta, **kwargs):
        """
            Contrutor da classe Modbus_Popup

            Parâmetros:
                ip: Parâmetro para ip do CLP.
                porta: Parâmetro para a porta que será conectada.
                **kwargs: Argumentos adicionais do Kivy.
            """
        super().__init__(**kwargs)
        self.ip = ip
        self.porta = porta
    
    def set_modbus(self):
        self.ids.entrada_ip.text = str(self.ip)
        self.ids.entrada_porta.text = str(self.porta)

class Scan_Popup(Popup):
    """
        Classe Scan_Poup que abri uma segunda janela para configurar o tempo de varredura    
    """
    def __init__(self,scan_time, **kwargs):
        """
            Construtor da classe Scan_Popup

            Parâmetros:
                scan_time (int): Tempo de varredura em milissegundos.
                **kwargs: Argumentos adicionais do Kivy.
        """
        super().__init__(**kwargs)
        self._scan_time = scan_time

    def set_time(self):
        """
            Método que atribui o valor para caixa de entrada do scan time. Foi usado 
            para encapsular o valor atribuido para 'self._scan_time'
         """
        self.ids.entrada_porta.text = str(self._scan_time) #Define um valor para a caixa de texto


    