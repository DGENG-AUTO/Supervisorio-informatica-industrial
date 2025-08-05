from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.clock import Clock
from pyModbusTCP.client import ModbusClient


class Modbus_Popup(Popup):
    """
        Classe Modbus_Popup que abri uma segunda janela para configurar o protocolo Modbus.    
    """
    _aviso_lb = None
    def __init__(self,ip,porta, **kwargs):
        """
            Contrutor da classe Modbus_Popup

            Parâmetros:
                ip - str(): Parâmetro para ip do CLP.
                porta - int(): Parâmetro para a porta que será conectada.
                **kwargs: Argumentos adicionais do Kivy.
            """
        super().__init__(**kwargs)
        self.ip = ip
        self.porta = porta
        self.ids.entrada_ip.text = str(self.ip)     #Define um valor para a caixa de texto ip
        self.ids.entrada_porta.text = str(self.porta)   #Define um valor para a caixa de texto porta
        self.estado_motor = None
    
    def set_aviso(self, mensagem):
        """
        Exibe uma mensagem de erro de conectividade com o MODBUS na tela do popup.

        Parâmetros:
            mensagem (str): Mensagem que será exibida na tela.
        """
        self._aviso_lb = Label(text=mensagem)
        self.ids.layout1.add_widget(self._aviso_lb)
        tempo = 6 #DEFINIR O TEMPO QUE A MENSAGEM FICARÁ NA TELA
        Clock.schedule_once(lambda dt: self.clear_aviso(), tempo)
    
    def clear_aviso(self):
        """
            Método que limpará a mensagem de erro exibida na tela de popup Modbus_Popup
        """
        if self._aviso_lb is not None:
            self.ids.layout1.remove_widget(self._aviso_lb)
            self._aviso_lb = None
        

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
        self.ids.entrada_time.text = str(self._scan_time) #Define um valor para a caixa de texto

class Atuacao(Popup):
    """
        Classe que irá abrir a janela do comando do motor
    """
    def __init__(self, **kwargs):
        super().__init__()
        self._ip = kwargs.get('ipmain')
        self._porta = kwargs.get('portamain')

        self._modbusCliente = ModbusClient(host=self._ip, port=self._porta)

    def liga_desliga_motor(self, addrs, estado):
        
        
        if (estado == 1):
            self._modbusCliente.write_single_coil(addrs, 1)
            print("Ligando motor...")

        elif (estado == 0):
            self._modbusCliente.write_single_coil(addrs, 0)
            print("Desligando motor...")
        else:
            print("Erro ao acessar motor.")
        return estado





