import json
from kivymd.app import MDApp 
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.button import Button
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp

from parsing import convert_scraping
Window.size = (400, 500)

kv = """
MDFloatLayout:
    md_bg_color: 1, 1, 1, 1
    MDLabel:
        text: "Currency Converter"
        pos_hint: {"center_x": .5, "center_y": .9}
        halign: "center"
        font_name: "Poppins/Poppins-SemiBold.ttf"
        font_size: "26sp"
    MDFloatLayout:
        size_hint: .85, .2
        pos_hint: {"center_x": .5, "center_y": .7}
        MDLabel:
            text: "Enter Amount"
            pos_hint: {"center_x": .5, "center_y": .85}
            font_name: "Poppins/Poppins-Medium.ttf"
            font_size: "18sp"
        MDFloatLayout:
            size_hint_y: .5
            pos_hint: {"center_x": .5, "center_y": .38}
            canvas.before: 
                Color:
                    rgb: 210/255, 210/255, 210/255, 1
                Line:
                    width: 1.2
                    rounded_rectangle: self.x, self.y, self.width, self.height, 6, 6, 6, 6, 100 
            TextInput:
                id: amount
                size_hint: 1, None
                pos_hint: {"center_x": .5, "center_y": .5}
                height: self.minimum_height
                font_name: "Poppins/Poppins-Regular.ttf"
                font_size: "18sp"
                hint_text_color: 170/255, 170/255, 170/255, 1
                background_color: 1, 1, 1, 0
                padding: 13
                cursor_color: 0, 0, 0, 1
                multiline: False

    MDFloatLayout:
        size_hint: .85, .2
        pos_hint: {"center_x": .5, "center_y": .46}
        MDFloatLayout:
            pos_hint: {"center_x": .6, "center_y": .5}
            MDLabel:
                text: "From"
                pos_hint: {"center_x": .5, "center_y": .85}
                font_name: "Poppins/Poppins-Medium.ttf"
                font_size: "18sp"
            DropDownButton:
                id: from_currency
                text: "USD"
                size_hint: .25, .5
                pos_hint: {"center_x": .125, "center_y": .38}
                background_color: 0, 0, 0, 0
                color: 0, 0, 0, 1
                font_size: "20sp"
                font_name: "Poppins/Poppins-Regular.ttf"
                on_release: app.from_menu.open()
                canvas.before: 
                    Color:
                        rgb: 210/255, 210/255, 210/255, 1
                    Line:
                        width: 1.2
                        rounded_rectangle: self.x, self.y, self.width, self.height, 6, 6, 6, 6, 100
        Image:
            source: "arrow.png"
            size_hint: .35, .35
            pos_hint: {"center_x": .5, "center_y": .38}

        MDFloatLayout:
            pos_hint: {"center_x": 1.15, "center_y": .5}
            MDLabel:
                text: "To"
                pos_hint: {"center_x": .5, "center_y": .85}
                font_name: "Poppins/Poppins-Medium.ttf"
                font_size: "18sp"
            DropDownButton:
                id: to_currency
                text: "RUB"
                size_hint: .25, .5
                pos_hint: {"center_x": .125, "center_y": .38}
                background_color: 0, 0, 0, 0
                color: 0, 0, 0, 1
                font_size: "20sp"
                font_name: "Poppins/Poppins-Regular.ttf"
                on_release: app.to_menu.open()
                canvas.before: 
                    Color:
                        rgb: 210/255, 210/255, 210/255, 1
                    Line:
                        width: 1.2
                        rounded_rectangle: self.x, self.y, self.width, self.height, 6, 6, 6, 6, 100
    MDLabel:
        id: result
        text: 
        pos_hint: {"center_x": .5, "center_y": .3}
        halign: "center"
        font_name: "Poppins/Poppins-Regular.ttf"
        font_size: "18sp"

    Button:
        text: "Get Exchange Rate"
        font_name: "Poppins/Poppins-Regular.ttf"
        size_hint: .85, .12
        font_size: "18sp"
        pos_hint: {"center_x": .5, "center_y": .15}
        background_color: 1, 1, 1, 0
        color: 1, 1, 1, 1
        on_release: app.convert()
        canvas.before:
            Color:
                rgb: 71/255, 104/255, 237/255, 1
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [6]
"""

class DropDownButton(MDFloatLayout, Button):
    pass

class CurrencyConverter(MDApp):
    
    with open('ratealerts.json', 'r') as file:
        data = json.load(file)

    currencies = data.get("commonI18nResources", {}).get("currencies", {}).get('en', {})
    currency_dict = {currency_code: currency_data.get("name", "") for currency_code, currency_data in currencies.items()}

    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(kv)
        from_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{k} - {v}",
                "height": dp(56),
                "on_release": lambda x=f"{k}": self.set_from(x),
            } for k,v in self.currency_dict.items()
        ]
        self.from_menu = MDDropdownMenu(
            caller=self.screen.ids.from_currency,
            items=from_items,
            position="auto",
            width_mult=4
        )
        self.from_menu.bind()
        
        to_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{k} - {v}",
                "height": dp(56),
                "on_release": lambda x=f"{k}": self.set_to(x),
            } for k,v in self.currency_dict.items()
        ]
        self.to_menu = MDDropdownMenu(
            caller=self.screen.ids.to_currency,
            items=to_items,
            position="auto",
            width_mult=4
        )
        self.to_menu.bind()

    def set_from(self, text_item):
        if text_item != self.screen.ids.to_currency.text:
            self.screen.ids.from_currency.text = text_item
            self.from_menu.dismiss()

    def set_to(self, text_item):
        if text_item != self.screen.ids.from_currency.text:
            self.screen.ids.to_currency.text = text_item
            self.to_menu.dismiss()

    def build(self):
        return self.screen
    

    def convert(self):
        amount_text = self.screen.ids.amount.text

        if not amount_text.strip():
            self.root.ids.result.text = "Amount is empty. Please enter a value."
            return

        try:
            amount = float(amount_text)
        except ValueError:
            self.root.ids.result.text = "Amount must be a number."
            return

        from_currency = self.screen.ids.from_currency.text
        to_currency = self.screen.ids.to_currency.text
        url = f"https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={from_currency}&To={to_currency}"
        result = convert_scraping(url)
        print(result)
        self.root.ids.result.text = f"{result['amount_and_from']} {result['result_convert']}"
        
CurrencyConverter().run()