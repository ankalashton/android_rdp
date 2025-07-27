from kivy.app import App
from kivy.uix.label import Label

# main.py
# This is a simple Kivy application that displays a label with a success message.
class AndroidRDP(App):
    def build(self):
        return Label(text="✅ It works!")

if __name__ == "__main__":
    AndroidRDP().run()
