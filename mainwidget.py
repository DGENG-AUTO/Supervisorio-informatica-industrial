from kivymd.app import MDApp
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.screen import Screen
from kivy.core.window import Window
from kivy.lang.builder import Builder
from popup import Modbus_Popup, Scan_Popup, Atuacao, Medicao, Graficos
from pyModbusTCP.client import ModbusClient
from threading import Thread
from time import sleep
from kivy.clock import Clock
from biblioteca_tags import Biblioteca_tags
from datetime import datetime
from random import random
from timeseriesgraph import TimeSeriesGraph

class MainWidget(Screen):
    """
        Classe que contrói a interface gráfica do supervisório com imagens,
        botões, caixas de textos, popup e etc...
    """
    _update_thread = None
    _atualiza = True
    _max_points = 20

    def __init__(self,**kwargs):
        """
            Construtor princial da classe MainWidget.
        """
        super().__init__()

        #kwargs será usado para permitir inúmeras passagens de variável de argumentos nomeados,
        #devem ser usados os mesmos nomes para não haver erros ou conflitos
        self._scan_time = kwargs.get('scan_timemain')
        self._ip = kwargs.get('ipmain')
        self._porta = kwargs.get('portamain')
        self._meas = {}
        self._meas['timestamp'] = None
        self._meas['values'] = {}
        self.dic_cores = {}

        #BIBLIOTECA DAS TAGS
        self._tags_importada = Biblioteca_tags().get_tags()
        for tag in self._tags_importada:
            nome = tag['nome']
            addr = tag['address']

            if (nome == 'bc.corrente_r'):
                plot_color = (1, 0, 0, 1)
            else:
                plot_color = (random(), random(), random(), 1)
            self.dic_cores[nome] = {'address': addr, 'color': plot_color}
        

        #Chamada das janelas segundárias (popup) já definido os valores nas linhas 23,24 e 25
        self._j_modbusPopup = Modbus_Popup(ip=self._ip, porta=self._porta)
        self._j_scanPopup = Scan_Popup(scan_time=self._scan_time)
        self._j_atuacao = Atuacao(ipmain=self._ip, portamain=self._porta)
        self._j_medidas = Medicao()
        self._j_graficos = Graficos(self._max_points, self.dic_cores)

        #criando a conexão MODBUS-TCP
        self._modbusCliente = ModbusClient(host=self._ip,port=self._porta, timeout=1)
    

    def abrir_fechar_janela(self,ref):
        """
            Método que abrirá o popup Modbus_Popup e Scan_Popup e fechará a barra lateral
            afim de que não haja poluição visual na tela

            Parâmetro:
            ref (int): Parâmetro que definirá qual janela será popup
        """
        if ref == 1:
            self._j_modbusPopup.open()
            self.ids.nav_drawer.set_state("close")
        elif ref == 2:
            self._j_scanPopup.open()
            self.ids.nav_drawer.set_state("close")

    def encontrar_tag(self,nome_tag):
        """
            Método que buscará as tags
        """
        for tag in self.tags:
            if tag['nome'] == nome_tag:
                return tag['address']

    


    def start_atendimento(self, ip_digitado, porta_digitado):
        """
            Método que inicia a conexão do servidor, configura o endereço de ip
            e a porta de CLP. Além disso inicia uma thread para leitura de dados
            e atualização de imagens da interface gráfica.
        """
        self._ip = ip_digitado
        self._porta = porta_digitado
        self._modbusCliente.host = self._ip
        self._modbusCliente.port = self._porta
        self._j_atuacao = Atuacao(ipmain=self._ip, portamain=self._porta)

        try:
            Window.set_system_cursor('wait')
            self._modbusCliente.open()
            Window.set_system_cursor('arrow')

            if self._modbusCliente.is_open:
                self._atualiza = True
                self.estado_motor = None
                self.ids.img_con.source = "img/con_on.png"
                self.ids.label_con.color = (0, 1, 0, 1)
                self.ids.label_con.text = "[b]CONECTADO[/b]"
                self._j_modbusPopup.dismiss()

                #EVITAR MULTIPLAS THREADS DE MESMO TRABALHO
                if self._update_thread is None or not self._update_thread.is_alive():
                    self._update_thread = Thread(target=self.update)
                    self._update_thread.start()
            else:
                self._j_modbusPopup.set_aviso("Falha na conexão com o servidor.")
        except Exception as erro:
            self._j_modbusPopup.set_aviso(f"ERRO: {erro.args}")


    def update(self):
        """
            Método que fará leitura periódica e atualização da interface
            com base na conectividade com o CLP via Modbus.
        """
        try:
            while self._atualiza:
                try:
                    resultado = self._modbusCliente.read_holding_registers(0, 1)
                    if resultado is None:
                        raise Exception("Sem resposta do servidor")
                    
                    self.read_datas()
                    self.updateGUI()
                    sleep(2)

                except Exception as erro:
                    print("Erro: ",erro.args)
                    self._modbusCliente.close()
                    Clock.schedule_once(lambda dt: setattr(self.ids.img_con, "source", "img/con_off.png"))
                    Clock.schedule_once(lambda dt: setattr(self.ids.label_con, "color", (1, 0, 0, 1)))
                    Clock.schedule_once(lambda dt: setattr(self.ids.label_con, "text", "[b]DESCONECTADO[/b]"))
                    Clock.schedule_once(lambda dt: self._j_modbusPopup.set_aviso("Desconectado do servidor!"))
                    self._atualiza = False                
        except Exception as erro:
            Clock.schedule_once(lambda dt: self._j_modbusPopup.set_aviso(f"ERRO: {erro.args}"))
        finally:
            #SERVIRÁ PARA LIBERÁ O ESPAÇO NA MEMÓRIA PARA CRIA UMA NOVA THREAD PARA CONEXÃO FURURAS
            self._update_thread = None
    
    def read_datas(self):
        """
            Método para leitura no meio do protocolo modbus
        """
        self._meas['timestamp'] = datetime.now()

        for tag in self.dic_cores:
            endereço = self.dic_cores[tag]['address']
            self._meas['values'][tag] = self._modbusCliente.read_holding_registers(endereço,1)[0]
            
            """for dict in self._tags_importada:
                if dict['nome'] == tag:
                    if dict['tipo_modbus'] == '4x':
                        self._meas['values'][tag] = self._modbusCliente.read_holding_registers(endereço,1)[0]
                    if dict['tipo_modbus'] == 'fp':
                        self._meas['values'][tag] = self.leitura_fp(endereço)
                    if dict['tipo_modbus'] == '4x_bit':
                        self._meas['values'][tag] = self.leitura_binario(endereço, dict['bit_pos'])"""
    
    def updateGUI(self):
        """
            Método para atualização da interface gráfica a partir dos dados lidos
        """

        # ATUALIZAÇÃO DAS LABEL
        for tag in self.dic_cores:
            if tag in self._j_medidas.ids:
                if "corrente" in tag:
                    self._j_medidas.ids[tag].text = str(self._meas['values'][tag]) + ' A'
                elif "tensao" in tag:
                    self._j_medidas.ids[tag].text = str(self._meas['values'][tag]) + ' V'
                elif "ativa" in tag:
                    self._j_medidas.ids[tag].text = str(self._meas['values'][tag]) + ' W'
                elif "reativa" in tag:
                    self._j_medidas.ids[tag].text = str(self._meas['values'][tag]) + ' VAr'
                elif "aparente" in tag:
                    self._j_medidas.ids[tag].text = str(self._meas['values'][tag]) + ' VA'
                elif "bc.fp_" in tag:
                    self._j_medidas.ids[tag].text = str(self._meas['values'][tag])
            else:
                continue
        
        # ATUALIZAÇÃO DO GRÁFICO
        tag_types = {
            'current': ['bc.corrente_r', 'bc.corrente_s', 'bc.corrente_n', 'bc.corrente_t', 'bc.corrente_media'],
            'voltage': ['bc.tensao_rs', 'bc.tensao_st', 'bc.tensao_tr'],
            'power': ['bc.ativa_r', 'bc.ativa_s', 'bc.ativa_t', 'bc.ativa_total'],
            'thd': ['bc.thd_tensao_sn', 'bc.thd_tensao_rn', 'bc.thd_tensao_tn', 'bc.thd_tensao_rs', 'bc.thd_tensao_st', 'bc.thd_tensao_tr']
        }
        
        # Determinar qual tipo de dado está ativo
        if self._j_graficos.ids.graph.current_visible:
            tags_to_plot = tag_types['current']
        elif self._j_graficos.ids.graph.voltage_visible:
            tags_to_plot = tag_types['voltage']
        elif self._j_graficos.ids.graph.power_visible:
            tags_to_plot = tag_types['power']
        elif self._j_graficos.ids.graph.thd_visible:
            tags_to_plot = tag_types['thd']
        else:
            tags_to_plot = []

        # Atualizar o gráfico apenas para as tags válidas
        valid_tags = [tag for tag in tags_to_plot if tag in self._meas['values'] and tag in self.dic_cores]
        for i, tag in enumerate(valid_tags):
            self._j_graficos.ids.graph.updateGraph((self._meas['timestamp'], self._meas['values'][tag]), i)
                
    
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
    
    