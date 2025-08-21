from kivymd.app import MDApp
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.screen import Screen
from kivy.core.window import Window
from kivy.lang.builder import Builder
from popup import Modbus_Popup, Scan_Popup, Atuacao, Medicao, Graficos, HistGraphPopup
from pyModbusTCP.client import ModbusClient
from threading import Thread, Lock
from time import sleep
from kivy.clock import Clock
from biblioteca_tags import Biblioteca_tags
from datetime import datetime
from random import random
from timeseriesgraph import TimeSeriesGraph
from modulopersistencia import ModbusPersistencia
from kivy_garden.graph import LinePlot
from pymodbus.payload import BinaryPayloadBuilder,BinaryPayloadDecoder
from pymodbus.constants import Endian

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
        self._lock = Lock()
        self._scan_time = kwargs.get('scan_timemain')
        self._ip = kwargs.get('ipmain')
        self._porta = kwargs.get('portamain')
        self._meas = {}
        self._meas['timestamp'] = None
        self._meas['values'] = {}
        self.dic_cores = {}
        self.dic_tags_hist = {}
        self._j_medidas = Medicao()
        self._selected_tags = []
        #criando a conexão MODBUS-TCP
        self._modbusCliente = ModbusClient(host=self._ip,port=self._porta, timeout=1)

        #BIBLIOTECA DAS TAGS - FILTRARÁ AS TAGS NECESSÁRIAS QUE SERÃO USADAS
        self._tags_importada = Biblioteca_tags().get_tags()
        for tag in self._tags_importada:
            nome = tag['nome']
            addr = tag['address']
            tipo = tag['tipo_modbus']
            div = tag['Div']
            bit = tag['bit']
            
            if (nome == 'bc.corrente_r'):
                plot_color = (1, 0, 0, 1)
            else:
                plot_color = (random(), random(), random(), 1)
            self.dic_cores[nome] = {    
                                        'address':      addr,
                                        'color':        plot_color,
                                        'tipo_modbus':  tipo,
                                        'Div':          div,
                                        'bit':          bit
                                    }
            tags_historico = [
                'bc.corrente_media', 'bc.ativa_total', 'bc.reativa_total',
                'bc.aparente_total', 'bc.tensao_rs', 'bc.tensao_st', 'bc.tensao_tr'
            ]
            if nome.startswith("bc.temp_") or nome in tags_historico:
                self.dic_tags_hist[nome] = {
                                                'address':      addr, 
                                                'color':        plot_color, 
                                                'tipo_modbus':  tipo
                                            }              

        #Chamada das janelas segundárias (popup) já definido os valores nas linhas 23,24 e 25
        self._j_modbusPopup = Modbus_Popup(ip=self._ip, porta=self._porta)
        self._j_scanPopup = Scan_Popup(scan_time=self._scan_time)
        self._j_atuacao = Atuacao(self._modbusCliente, self._lock)
        self._j_medidas = Medicao()
        self._j_graficos = Graficos(self._max_points, self.dic_cores)
        self._j_histgraph = HistGraphPopup(tags=self.dic_tags_hist)
        self._histdados = ModbusPersistencia(scantime=self._scan_time)

    
    
    #VISTO       
    def desconectar(self):
        """
            Método que desconectará o supervisório da rede MODBUS
        """
        self._modbusCliente.close()
        Clock.schedule_once(lambda dt: setattr(self.ids.img_con, "source", "img/con_off.png"))
        Clock.schedule_once(lambda dt: setattr(self.ids.label_con, "color", (1, 0, 0, 1)))
        Clock.schedule_once(lambda dt: setattr(self.ids.label_con, "text", "[b]DESCONECTADO[/b]"))
        Clock.schedule_once(lambda dt: self._j_modbusPopup.set_aviso("Desconectado do servidor!"))
        self._atualiza = False 

    #VISTO
    def conf_scan_time(self, time):
        """
            Método que configura o tempo de varredura
        """
        self._scan_time = time
        print("Scantime configurado: ",self._scan_time)

    def acionamento_imagem(self):
        self._j_atuacao.acionamento_imagem()   


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
        # self._j_atuacao = Atuacao(ipmain=self._ip, portamain=self._porta)

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
                    #CAPTAÇÃO DE ERRO
                    with self._lock:
                        resultado = self._modbusCliente.read_holding_registers(0, 1)
                        
                    if resultado is None:
                        raise Exception("Sem resposta do servidor")
                    
                    #MUDANÇA DO MOTOR:
                    

                    #CAPTAÇÃO DE DADOS    
                    self.read_datas()
                    self.updateGUI()
                    self._histdados.guardar_dados(self._meas)

                    #TEMPO DE VARREDURA, DIVIDIDO POR 1000 POIS A ENTRADA É EM ms
                    sleep(self._scan_time/1000)

                except Exception as erro:
                    print("Erro: ",erro.args)
                    self._modbusCliente.close()
                    Clock.schedule_once(lambda dt: setattr(self.ids.img_con, "background_normal", "img/con_off.png"))
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
            tipo_modbus = self.dic_cores[tag]['tipo_modbus']
            divisor = self.dic_cores[tag]['Div']        
            
            if tipo_modbus == '4x':                         
                with self._lock:
                    self._meas['values'][tag] = (self._modbusCliente.read_holding_registers(endereço, 1)[0]/divisor)
            elif tipo_modbus == 'FP':
                with self._lock:
                    self._meas['values'][tag] = (self.leitura_fp(endereço)/divisor)
            elif tipo_modbus == '4x_bit':
                with self._lock:
                    self._meas['values'][tag] = (self.leitura_binario(endereço, self.dic_cores[tag]['bit'])/divisor)


    
    def leitura_fp(self, addr):
        #Estudar!!
        puxada = self._modbusCliente.read_holding_registers(addr,2)
        #decode = BinaryPayloadDecoder.fromRegisters(puxada, byteorder=Endian.Big, wordorder=Endian.Big)
        decode = BinaryPayloadDecoder.fromRegisters(puxada,byteorder=Endian.Big,wordorder =Endian.Little) #Concatena os 16bits dos endereços addr e addr+1 para puxar 32bits
        dados = decode.decode_32bit_float()#converte para float
        return dados

    def leitura_binario(self, addr, bit_pos):
        #EStudar!!
        puxada = self._modbusCliente.read_holding_registers(addr)
        decode = BinaryPayloadDecoder.fromRegisters(puxada,byteorder=Endian.Big,wordorder =Endian.Little) #Concatena os 16bits dos endereços addr e addr+1 para puxar 32bits
        dados1 = decode.decode_bits()
        dados2 = decode.decode_bits()

        dados = dados2+dados1
        return dados[bit_pos]    
    
    def updateGUI(self):
        """
            Método para atualização da interface gráfica a partir dos dados lidos
        """
        
        # ATUALIZAÇÃO DAS LABEL
        for tag in self.dic_cores:

            if tag == 'bc.lit01':
                valor = f'{self._meas['values'][tag]:.2f}'
                self.ids.nivel_agua_superior.value = self._meas['values'][tag]
                self.ids.nivel_agua_inferior.value = int(100 - self._meas['values'][tag])
                retro = f'{float(100 - self._meas['values'][tag]):.2f}'
                self.ids.lit01_label.text = "Nível: "+ str(valor) + '%'
                self.ids.lit02_label.text = "Nível: "+ str(retro) + '%'
                print(f'litros %: {self._meas['values'][tag]}')
            
            if tag == "bc.tipo_motor":
                if self._meas['values'][tag] == 1:
                    self.ids.tipo_motor.text = 'Motor 1'
                elif  self._meas['values'][tag] == 2:
                    self.ids.tipo_motor.text = 'Motor 2'
            
            if tag == "bc.pit01":
                valor = f'{self._meas['values'][tag]:.2f}' 
                self.ids.pit_01.text = str(valor) + ' kgf/cm²'
            
            if tag == "bc.fit01":
                valor = f'{self._meas['values'][tag]:.2f}'
                self.ids.fit_01.text = str(valor) + ' m³/h'
            
            if tag == "bc.na_tq_superior":
                if self._meas['values'][tag] == 1:
                    self.ids.reserva_sup.text = 'RESERVATÓRIO CHEIO'
                else:
                    self.ids.reserva_sup.text = ''
            
            if tag == 'bc.habilita':
                if (self._meas['values'][tag] == 1):
                    Clock.schedule_once(lambda dt: setattr(self.ids.img_motor, "background_normal", "img/Motor_on (1).png"))
                    self.ids.how_motor.text = 'ON'
                    self._j_atuacao.est_motor(es = True)
                elif (self._meas['values'][tag] == 0):
                    Clock.schedule_once(lambda dt: setattr(self.ids.img_motor, "background_normal", "img/Motor_off (1).png"))
                    self._j_atuacao.est_motor(es = False)
                    self.ids.how_motor.text = 'OFF'
            
            if tag == 'bc.encoder':
                self.ids.rpm.text = str(self._meas['values'][tag]) + ' rpm'

            if tag == 'bc.torque':
                self.ids.torque.text = str(self._meas['values'][tag]) + ' rpm'               

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
                elif "bc.temp":
                    self._j_medidas.ids[tag].text = str(self._meas['values'][tag]) + ' °C'
                    if tag == "bc.temp_r":
                        self.ids.temp_r.text = 'temp. em R:   ' + str(self._meas['values'][tag]) + ' °C'
                    elif tag == "bc.temp_s":
                        self.ids.temp_s.text = 'temp. em S:   ' + str(self._meas['values'][tag]) + ' °C'
                    elif tag == "bc.temp_t":
                        self.ids.temp_t.text = 'temp. em T:   ' + str(self._meas['values'][tag]) + ' °C'
                    elif tag == "bc.temp_carc":
                        self.ids.temp_carc.text = 'Carcaça          ' + str(self._meas['values'][tag]) + ' °C'
            else:
                continue
        
       
            
        
        # ATUALIZAÇÃO DO GRÁFICO
        tag_types = {
            'current': ['bc.corrente_r', 'bc.corrente_s', 'bc.corrente_n', 'bc.corrente_t', 'bc.corrente_media'],
            'voltage': ['bc.tensao_rs', 'bc.tensao_st', 'bc.tensao_tr'],
            'power': ['bc.ativa_r', 'bc.ativa_s', 'bc.ativa_t', 'bc.ativa_total'],
            'thd': ['bc.thd_tensao_sn', 'bc.thd_tensao_rn', 'bc.thd_tensao_tn', 'bc.thd_tensao_rs', 'bc.thd_tensao_st', 'bc.thd_tensao_tr'],
            'temperature': ['bc.temp_r', 'bc.temp_s', 'bc.temp_t', 'bc.temp_carc']
        }
        
        #DETERMINAR QUAL TIPO DE DADO ESTÁ ATIVO
        if self._j_graficos.ids.graph.current_visible:
            tags_to_plot = tag_types['current']
        elif self._j_graficos.ids.graph.voltage_visible:
            tags_to_plot = tag_types['voltage']
        elif self._j_graficos.ids.graph.power_visible:
            tags_to_plot = tag_types['power']
        elif self._j_graficos.ids.graph.thd_visible:
            tags_to_plot = tag_types['thd']
        elif self._j_graficos.ids.graph.temp_visible:
            tags_to_plot = tag_types['temperature']
        else:
            tags_to_plot = []

        # Atualizar o gráfico apenas para as tags válidas
        valid_tags = [tag for tag in tags_to_plot if tag in self._meas['values'] and tag in self.dic_cores]
        for i, tag in enumerate(valid_tags):
            self._j_graficos.ids.graph.updateGraph((self._meas['timestamp'], self._meas['values'][tag]), i)

    def update_graph_selection(self, tag_id, active):
        """Atualiza a lista de tags selecionadas com base no estado do CheckBox."""
        if active and tag_id not in self._selected_tags:
            self._selected_tags.append(tag_id)
        elif not active and tag_id in self._selected_tags:
            self._selected_tags.remove(tag_id)
        print(f"Tags selecionadas: {self._selected_tags}")


    def read_data(self,a,b):
        """
            Método que coleta as informações da interface fornecidas pelo usuário e requisita a busta no BD
        """
        try:
            init_t = self._histdados.parseDTString(a)
            final_t = self._histdados.parseDTString(b)
            cols = self._selected_tags
            
            if init_t is None or final_t is None or len(cols) == 0:
                return
            cols.append('timestamp')

            dados = self._histdados.acesso_dados_historicos(init_t, final_t, cols)
            print(dados)
            self._j_histgraph.ids.graph.clearPlots()

            for key, value in dados.items():
                if key == 'timestamp':
                    continue
                p = LinePlot(line_width=1.5, color=self.dic_cores.get(key, {'color': (0, 0, 1, 1)})['color'])
                p.points = [(i, value[i]) for i in range(len(value))] 
                self._j_histgraph.ids.graph.add_plot(p)
            
            self._j_histgraph.ids.graph.xmax = len(dados['timestamp']) - 1  
            self._j_histgraph.ids.graph.update_x_labels(dados['timestamp'])

        except Exception as erro:
            print("Erro: ", erro.args)    

          
    
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
    
    