from time import sleep
from datetime import datetime
from threading import Thread, Lock
from tabulate import tabulate
from db import Session, Base, engine
from models import DadoCLP


class ModbusPersistencia(object):
    """
    Classe que implementa funcionalidade de persistência de dados 
    lidos a partir do protocolo Modbus e também permite a busca de dados históricos
    """
    def __init__(self,**kwargs):
        """
        Construtor
        """
        super().__init__()
       
        self._tags_addrs = {}
        self._scan_time = kwargs.get('scantime')
        self.session = Session()
        Base.metadata.create_all(engine)
        self.lock = Lock()


    def guardar_dados(self,meas):
        """
        Método para leitura de um dado da tabela MODBUS
        """
        self._tags_addrs = meas
        data = {}
        data['timestamp'] = self._tags_addrs['timestamp']
        TAG_TO_DB = {'bc.corrente_media': 'corrente_media', 
                     'bc.tensao_rs':'tensao_rs',
                     'bc.tensao_st':'tensao_st',
                     'bc.tensao_tr':'tensao_tr',
                     'bc.ativa_total':'potencia_ativa',
                     'bc.reativa_total':'potencia_reativa',
                     'bc.aparente_total':'potencia_aparente',
                     'bc.temp_r':'temperatura_r',   
                     'bc.temp_s':'temperatura_s',   
                     'bc.temp_t':'temperatura_t',   
                     'bc.temp_carc':'temperatura_superficie',
                     }

        for tag, valor in self._tags_addrs['values'].items():
            if tag in TAG_TO_DB:
                coluna = TAG_TO_DB[tag]
                data[coluna] = valor

        dado = DadoCLP(**data)
        self.lock.acquire()
        self.session.add(dado)
        self.session.commit()
        self.lock.release()
        


    def acesso_dados_historicos(self, a, b, cols):
        """
            Método que permite ao usuário acessar dados históricos
            Retorna um dicionário no formato:
            {
                'timestamp': [datetime1, datetime2, ...],
                'corrente': [valor1, valor2, ...],
                'tensao': [valor1, valor2, ...],
                'potencia': [valor1, valor2, ...],
                'thd': [valor1, valor2, ...]
            }
        """
        lock_acquired = False  # Flag para rastrear se o lock foi adquirido
        try:
            print("Bem vindo ao sistema de busca de dados históricos")
            print(f"Intervalo de busca: {a} a {b}, colunas: {cols}")  # Depuração

            init = a
            final = b
            
            self.lock.acquire()
            lock_acquired = True
            result = self.session.query(DadoCLP).filter(DadoCLP.timestamp.between(init, final)).all()
            print(f"Resultados brutos: {[obj.__dict__ for obj in result]}")  # Depuração

            # Criar lista de dados formatados
            result_fmt_list = [obj.get_attr_printable_list() for obj in result]
            print(f"Resultados formatados: {result_fmt_list}")  # Depuração

            # Exibir dados formatados (opcional)
            print(tabulate(result_fmt_list, headers=['id', 'timestamp', 'corrente_media', 'tensao_rs', 
                                                     'tensao_st','tensao_tr', 'potencia_ativa', 'potencia_reativa',
                                                     'potencia_aparente','temperatura_r', 'temperatura_s', 'temperatura_t',
                                                     'temperatura_superficie']))

            # Converter para dicionário
            dados = {
                'timestamp': [datetime.strptime(row[1], '%d/%m/%Y %H:%M:%S.%f') for row in result_fmt_list],
                'corrente_media': [row[2] if row[2] is not None else None for row in result_fmt_list],
                'tensao_rs': [row[3] if row[3] is not None else None for row in result_fmt_list],
                'tensao_st': [row[4] if row[4] is not None else None for row in result_fmt_list],
                'tensao_tr': [row[5] if row[5] is not None else None for row in result_fmt_list],
                'potencia_ativa':[row[6] if row[6] is not None else None for row in result_fmt_list], 
                'potencia_reativa': [row[7] if row[7] is not None else None for row in result_fmt_list],
                'potencia_aparente': [row[8] if row[8] is not None else None for row in result_fmt_list],
                'temperatura_r': [row[9] if row[9] is not None else None for row in result_fmt_list], 
                'temperatura_s': [row[10] if row[10] is not None else None for row in result_fmt_list], 
                'temperatura_t': [row[11] if row[11] is not None else None for row in result_fmt_list],
                'temperatura_superficie': [row[12] if row[12] is not None else None for row in result_fmt_list]
            }
            print(f"Dados antes do filtro: {dados}")  # Depuração

            # Mapeamento de tags para colunas
            tag_to_column = {
                'bc.corrente_media': 'corrente_media', 
                'bc.tensao_rs':'tensao_rs',
                'bc.tensao_st':'tensao_st',
                'bc.tensao_tr':'tensao_tr',
                'bc.ativa_total':'potencia_ativa',
                'bc.reativa_total':'potencia_reativa',
                'bc.aparente_total':'potencia_aparente',
                'bc.temp_r':'temperatura_r',   
                'bc.temp_s':'temperatura_s',   
                'bc.temp_t':'temperatura_t',   
                'bc.temp_carc':'temperatura_superficie'
            }

            # Filtrar apenas as colunas solicitadas, mapeando as tags
            if cols:
                filtered_cols = ['timestamp']  # Sempre incluir timestamp
                for tag in cols:
                    if tag in tag_to_column:
                        filtered_cols.append(tag_to_column[tag])
                return {key: dados[key] for key in filtered_cols if key in dados}
            return dados

        except Exception as e:
            print("Erro durante a execução:", e.args)
            return {'timestamp': [], 'corrente_media' : [], 'tensao_rs':[], 'tensao_st':[],
                    'tensao_tr':[], 'potencia_ativa':[], 'potencia_reativa':[],
                    'potencia_aparente':[],'temperatura_r':[], 'temperatura_s':[],
                    'temperatura_t':[], 'temperatura_superficie':[]}

        finally:
            if lock_acquired:
                self.lock.release()
                print("Lock liberado com sucesso")

    def parseDTString(self,datetime_str):
        """
        Método que converte as strings inseridas pelos usuários para um objeto datetime
        """
        try:
            return datetime.strptime(datetime_str, '%d/%m/%Y %H:%M:%S')
        except ValueError as erro:
            print("Erro ao parser data:", erro)
            return None 
       

    

  
   

    
