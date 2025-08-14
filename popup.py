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
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle



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
        Classe que irá abrir a janela dos gráficos
    """
    def __init__(self, xmax, dic_cores, **kwargs):
        super().__init__(**kwargs)
        self.dic_cores = dic_cores
        self.plots = {}
        self.tag_types = {
            'current': ['bc.corrente_r', 'bc.corrente_s', 'bc.corrente_n', 'bc.corrente_t', 'bc.corrente_media'],
            'voltage': ['bc.tensao_rs', 'bc.tensao_st', 'bc.tensao_tr'],
            'power': ['bc.ativa_r', 'bc.ativa_s', 'bc.ativa_t', 'bc.ativa_total'],
            'thd': ['bc.thd_tensao_sn', 'bc.thd_tensao_rn', 'bc.thd_tensao_tn', 'bc.thd_tensao_rs', 'bc.thd_tensao_st', 'bc.thd_tensao_tr']
        }

        # Criar LinePlot para cada tag, mas não adicionar ao gráfico ainda
        for tag_type, tags in self.tag_types.items():
            for tag in tags:
                if tag in self.dic_cores:
                    plot_color = self.dic_cores[tag]['color']
                    plot = LinePlot(line_width=1.5, color=plot_color)
                    self.plots[tag] = {'plot': plot, 'type': tag_type}

        self.ids.graph.xmax = xmax
        self.update_plot_visibility()

    def on_pre_open(self):
        self.update_plot_visibility()

    def update_plot_visibility(self):
        active_type = None
        if self.ids.graph.current_visible:
            active_type = 'current'
            self.ids.graph.ylabel = 'Amper [A]'
            self.ids.graph.ymax = 200
            self.ids.graph.y_ticks_major = 40
        elif self.ids.graph.voltage_visible:
            active_type = 'voltage'
            self.ids.graph.ylabel = 'Volts [V]'
            self.ids.graph.ymax = 500
            self.ids.graph.y_ticks_major = 100
        elif self.ids.graph.power_visible:
            active_type = 'power'
            self.ids.graph.ylabel = 'Power [W]'
            self.ids.graph.ymax = 1000
            self.ids.graph.y_ticks_major = 200
        elif self.ids.graph.thd_visible:
            active_type = 'thd'
            self.ids.graph.ylabel = 'THD [%]'
            self.ids.graph.ymax = 100
            self.ids.graph.y_ticks_major = 20

        # Remover todos os plots do gráfico
        for plot in self.ids.graph.plots[:]:  # Usar cópia para evitar modificação durante iteração
            self.ids.graph.remove_plot(plot)

        # Adicionar apenas os plots do tipo ativo
        for tag, plot_info in self.plots.items():
            plot = plot_info['plot']
            tag_type = plot_info['type']
            if tag_type == active_type:
                self.ids.graph.add_plot(plot)
            else:
                plot.points = []  # Limpar os dados do plot inativo

        # Atualizar legenda
        self.ids.legend.clear_widgets()
        legend_title = Label(text='Legenda', size_hint_y=0.1, color=(1, 1, 1, 1))
        self.ids.legend.add_widget(legend_title)
        if active_type:
            for tag in self.tag_types[active_type]:
                if tag in self.dic_cores:
                    legend_item = BoxLayout(orientation='horizontal', size_hint_y=0.1)
                    color = self.dic_cores[tag]['color']
                    color_box = Label(text='', size_hint_x=0.2)
                    with color_box.canvas:
                        Color(rgba=color)
                        Rectangle(pos=(color_box.x + 5, color_box.y + 5), size=(20, 10))
                    label = Label(text=tag.replace('bc.', ''), color=(1, 1, 1, 1))
                    legend_item.add_widget(color_box)
                    legend_item.add_widget(label)
                    self.ids.legend.add_widget(legend_item)


                
    
        
class LabeledCheckBoxDataGraph(BoxLayout):
    pass

from kivy.uix.popup import Popup
from kivymd.uix.selectioncontrol import MDCheckbox  # Ajuste conforme sua implementação de LabeledCheckBoxHistGraph

class LabeledCheckBoxHistGraph(BoxLayout):  # Defina esta classe se não estiver em outro lugar
    pass  # Implemente conforme necessário (ex.: com Label e Checkbox)

class HistGraphPopup(Popup):
    def __init__(self, **kwargs):
        # Extrai o argumento 'tags' de kwargs e define como atributo da classe
        self.tags = kwargs.pop('tags', {})
        
        # Chama o construtor da classe base com os kwargs restantes
        super().__init__(**kwargs)
        
        # Inicializa o conteúdo após o super().__init__
        for key, value in self.tags.items():
            cb = LabeledCheckBoxHistGraph()
            cb.ids.label.text = key
            cb.ids.label.color = value['color']
            cb.id = key
            self.ids.sensores.add_widget(cb)

    
class LabeledCheckBoxHistGraph(BoxLayout):
    pass
    
        

    
           




