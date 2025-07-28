from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from rdpy.protocol.rdp import RDPClientFactory
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint

class RDPClient(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="🔌 Подключение к RDP..."))
        self.connect_rdp("192.168.130.39", 3389)

    def connect_rdp(self, ip, port):
        factory = RDPClientFactory()
        endpoint = TCP4ClientEndpoint(reactor, ip, port)
        d = endpoint.connect(factory)
        d.addCallback(lambda _: print("✅ Подключено"))
        d.addErrback(lambda e: print(f"❌ Ошибка: {e}"))
        reactor.run()

class RDPApp(App):
    def build(self):
        return RDPClient()

if __name__ == "__main__":
    RDPApp().run()
