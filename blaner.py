import kivy
from kivy.app import App
from kivy.uix.label import Label

class BlanerUI(App):

  def build(self):
    return Label(text='Blaner')

if __name__ == '__main__':
  BlanerUI().run()