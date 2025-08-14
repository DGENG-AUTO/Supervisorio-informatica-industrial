from db import Base
from sqlalchemy import Column, Integer, DateTime

class DadoCLP(Base):
    """
    Modelo dos dados do CLP
    """
    __tablename__ = 'dadoclp'
    id = Column(Integer, primary_key=True,autoincrement=True)
    timestamp = Column(DateTime)
    corrente = Column(Integer)
    tensao = Column(Integer)
    potencia = Column(Integer)
    thd = Column(Integer)

    def get_attr_printable_list(self):
        return [self.id,
                self.timestamp.strftime('%d/%m/%Y %H:%M:%S.%f'),
                self.corrente,
                self.tensao,
                self.potencia,
                self.thd]

   