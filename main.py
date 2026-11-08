from mainwidget import MainWidgetApp
from kivy.lang.builder import Builder

if __name__ =='__main__':
    ativa = MainWidgetApp()
    Builder.load_string(open("mainwidget.kv",encoding="utf-8").read(),rulesonly=True)
    Builder.load_string(open("popup.kv",encoding="utf-8").read(),rulesonly=True)
    ativa.run()
