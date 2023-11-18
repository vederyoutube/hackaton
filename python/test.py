from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class PositioningApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Создаем кнопку
        button = Button(text='Кнопка по координатам', size_hint=(None, None), size=(1366, 150))

        # Устанавливаем координаты (x, y) кнопки
        button.pos = (817, 300)

        layout.add_widget(button)
        return layout

if __name__ == '__main__':
    PositioningApp().run()