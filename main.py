from kivy.app import App
from kivy.uix.label import Label

class AndroidRDP(App):
    def build(self):
        return Label(text="Version for RDP also works on Android")

AndroidRDP().run()
