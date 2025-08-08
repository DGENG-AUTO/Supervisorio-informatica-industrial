from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from pyModbusTCP.client import ModbusClient
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from timeseriesgraph import TimeSeriesGraph
from kivy_garden.graph import LinePlot


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
        self.title = ""
        self.addr = None
        self.estado_motor = 0

        self._modbusCliente = ModbusClient(host=self._ip, port=self._porta)

    def selecionar_partida(self, addr, option):
        self.tipo_partida_valor = option  
        self._modbusCliente.write_single_register(addr, option)

        if (option == 3):
            self.addr = 1319
            print("Partida direta")
            self.ids.coluna_velocidade.opacity = 0
            self.ids.coluna_velocidade.disable = False
        elif (option == 1):
            self.addr = 1316
            self.ids.coluna_velocidade.opacity = 1
            self.ids.coluna_velocidade.disable = True
            self.ids.slider_velocidade.disable = False
            self.ids.slider_velocidade.opacity = 0
            print("Partida soft-star")
        elif (option == 2):
            self.addr = 1312
            self.addr_hz = 1313
            self.ids.coluna_velocidade.opacity = 1
            self.ids.coluna_velocidade.disable = True
            self.ids.slider_velocidade.opacity = 1
            self.ids.slider_velocidade.disable = True
            print("Partida inversor")
        else:
            print("Falha ao selecionar tipo de partida")

    def rampa_velocidade(self,valor):
        """
            Define a velocidade do motor em termos de frequência (Hz) a partir a mudança do Slider        
        """
        self._modbusCliente.write_single_register(self.addr_hz,valor)
        print(valor)        
        

    def controla_partida(self,aciona):
        if (aciona == 0):
            self._modbusCliente.write_single_register(self.addr,aciona)
            self.ids.coluna_velocidade.opacity = 0
            self.ids.coluna_velocidade.disable = False
            self.ids.slider_velocidade.opacity = 0
            self.ids.slider_velocidade.disable = False
            self.addr = None
            self.addr_hz = None
            self.estado_motor = 0
            print("Motor desligado")
        elif(aciona == 1):
            self._modbusCliente.write_single_register(self.addr,aciona)
            self.estado_motor = 1
            print("Motor ligado")
        elif(aciona == 2):
            self._modbusCliente.write_single_register(self.addr,aciona)
            print("Motor resetado")
    
    def estado_motor_conticao(self):
        return (self.estado_motor)
        

class Medicao(Popup):
    """
        Classe que irá abrir a janela das medições elétricas
    """
    def __init__(self, **kwargs):
        super().__init__()

class Graficos(Popup):
    """
        Classe que irá abria a janela dos gráficos
    """
    def __init__(self,xmax,plot_color, **kwargs):
        super().__init__(**kwargs)
        self.plot = LinePlot(line_width=1.5,color = plot_color)
        self.ids.graph.add_plot(self.plot)
        self.ids.graph.xmax = xmax

class LabeledCheckBoxDataGraph(BoxLayout):
    pass
        

    
           




