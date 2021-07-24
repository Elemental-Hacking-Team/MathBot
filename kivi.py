# import functions from kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

Window.clearcolor = get_color_from_hex("#86a2ec")

# import of functions
from backend import frac2float, maxfraction, findbestanswer, printfraction
import pandas as pd
import re
from playsound import playsound

dfconcepts = pd.read_csv('concepts.csv', index_col=None, header=None)
dfconcepts.columns = ["Questions", "Answers"]

# defition of different screens
class Button1(Button):
    pass

class FractionExplanation(Popup):
    pass

class ComparisonExplanation(Popup):
    pass

class MainWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class ConceptsWindow(Screen):
    def cleartext(self):
        self.message.text = ''

    def answer(self):
        user_message = self.message.text

        if type(user_message) == str and bool(user_message.strip()) == True:
            message, qtag = findbestanswer(user_message, dfconcepts)
            playsound("concept%s.mp3" % qtag)
        else:
            content = Button(text="Please introduce a valid concept", font_size=15)
            popup = Popup(title="Error", content=content, size_hint=(0.5, 0.3), auto_dismiss=True)
            content.bind(on_press=popup.dismiss)
            popup.open()

class ExplanationWindow(Screen):
    def cleartext(self):
        self.fraction.text = ''

    def open_popup(self):
        frac_txt = self.fraction.text

        if len(re.findall(r'/+', frac_txt)) == 1:

            if len(re.findall(r'[0-9]{1,}/+[0-9]{1,}', frac_txt)) > 0:

                num, den, frac_float = frac2float(frac_txt)

                if num == 1:
                    message = "The fraction %d/%d means that a unit is\ndivided by %d and %d is selected.\nThis fraction as decimal is %0.4f " % (num, den, den, num, frac_float)
                else:
                    message = "The fraction %d/%d means that a unit is\ndivided by %d and %d are selected.\nThis fraction as decimal is %0.4f " % (num, den, den, num, frac_float)

                # the popup
                content = Button(text=message, font_size=20)
                popup = Popup(title="Fraction explanation", content=content, size_hint=(0.8, 0.5), auto_dismiss=False)
                content.bind(on_press=popup.dismiss)
                popup.open()
            else:
                content = Button(text="Please introduce a fraction.\nUsing number/number.", font_size=15)
                popup = Popup(title="Error", content=content, size_hint=(0.5, 0.3), auto_dismiss=True)
                content.bind(on_press=popup.dismiss)
                popup.open()
        else:
            content = Button(text="Please introduce a fraction.\nUsing number/number.", font_size=15)
            popup = Popup(title="Error", content=content, size_hint=(0.5, 0.3), auto_dismiss=True)
            content.bind(on_press=popup.dismiss)
            popup.open()

    def open_popup2(self):
        frac_txt = self.fraction.text

        if len(re.findall(r'/+', frac_txt)) > 0:
            num, den, frac_float = frac2float(frac_txt)
            printfraction(num,den)

            # the popup
            content = Image(source='fraction%d-%d.png' % (num, den))
            popup = Popup(title="Fraction " + frac_txt, content=content, size_hint=(0.8, 0.8), auto_dismiss=True)
            content.bind(on_press=popup.dismiss)
            popup.open()
        else:
            content = Button(text="Please introduce a fraction.\nSeparated with slash (/).", font_size=15)
            popup = Popup(title="Error", content=content, size_hint=(0.5, 0.3), auto_dismiss=True)
            content.bind(on_press=popup.dismiss)
            popup.open()


class ComparisonWindow(Screen):
    def cleartext(self):
        self.fraction1.text = ''
        self.fraction2.text = ''
    def open_popup(self):
        frac_txt1 = self.fraction1.text
        frac_txt2 = self.fraction2.text

        if len(re.findall(r'/+', frac_txt1)) > 0 and len(re.findall(r'/+', frac_txt2)) > 0:
            num1, den2, frac_float1 = frac2float(frac_txt1)
            num1, den2, frac_float2 = frac2float(frac_txt2)

            great, less = maxfraction(frac_float1, frac_float2)

            if great == frac_float1:
                greatfrac = frac_txt1
                lessfrac = frac_txt2
            else:
                greatfrac = frac_txt2
                lessfrac = frac_txt1

            message = "The fraction %s is greater than %s.\nThe fraction %s as decimal is %0.4f\nand  %s is %0.4f" % (greatfrac, lessfrac, greatfrac, great, lessfrac, less)

            # the popup
            content = Button(text=message, font_size=20)
            popup = Popup(title="Fraction comparison", content=content, size_hint=(0.8, 0.5), auto_dismiss=False)
            content.bind(on_press=popup.dismiss)
            popup.open()

        else:
            content = Button(text="Please introduce two fractions.\nUsing number/number.", font_size=15)
            popup = Popup(title="Error", content=content, size_hint=(0.5, 0.3), auto_dismiss=True)
            content.bind(on_press=popup.dismiss)
            popup.open()

# builds the app using the structure and dato from my.kv
kv = Builder.load_file("my.kv")

# main class for the app
class MathBot(App):
    def build(self):
        Window.size = (576, 720)
        return kv

# executes the main class
if __name__ == "__main__":
    MathBot().run()
