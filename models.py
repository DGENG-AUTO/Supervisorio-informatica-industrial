from db import Base
from sqlalchemy import Column, Integer, DateTime

class DadoCLP(Base):
    """
    Modelo dos dados do CLP
    """
    __tablename__ = 'dadoclp'
    id = Column(Integer, primary_key=True,autoincrement=True)
    timestamp = Column(DateTime)
    corrente_media = Column(Integer)
    tensao_rs = Column(Integer)
    tensao_st = Column(Integer)
    tensao_tr = Column(Integer)
    potencia_ativa = Column(Integer)
    potencia_reativa = Column(Integer)
    potencia_aparente = Column(Integer)
    temperatura_r = Column(Integer)
    temperatura_s = Column(Integer)
    temperatura_t = Column(Integer)
    temperatura_superficie = Column(Integer)

    def get_attr_printable_list(self):
        return [self.id,
                self.timestamp.strftime('%d/%m/%Y %H:%M:%S.%f'),
                self.corrente_media,
                self.tensao_rs,
                self.tensao_tr,
                self.tensao_st,
                self.potencia_ativa,
                self.potencia_reativa,
                self.potencia_aparente,
                self.temperatura_r,
                self.temperatura_s,
                self.temperatura_t,
                self.temperatura_superficie]

   