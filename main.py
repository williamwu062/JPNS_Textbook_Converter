from urllib.parse import non_hierarchical
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
import sheets


class Scrape:
  CSV_PATH = Path('japanese_quizlets/')

  def __init__(self, html):
    self.soup = BeautifulSoup(html, 'html.parser')
    self.frame = None

  
  def start(self):
    # check for ATTRIBUTE ERROR 'NoneType' object has no attribute 'string'

    temp_frame = []

    unit = self.soup.title.string
    AND_PERSAND = '&amp;'
    headings = self.soup.find_all('h2')
    tables = self.soup.find_all('tbody')
    flashcards = []
    for table in tables:
      tb_row = table.find_all('tr')
      for tr in tb_row[0:]:
        flashcard_data = tr.find_all('td')
        def getFlashcard(flashcard_data, length):
          trans_loc = 3 if length == 4 else 2
          non_breakspace = u'\xa0'
          if flashcard_data[1].text == non_breakspace or len(flashcard_data[1].text) == 0:
            japanese_word = '{}'.format(flashcard_data[0].text)
          else:
            #print('yo', flashcard_data[1].text)
            japanese_word = '{} ({})'.format(flashcard_data[0].text, flashcard_data[1].text)
          english_trans = flashcard_data[trans_loc].text
          return [english_trans, japanese_word]

        flashcards.append(getFlashcard(flashcard_data, len(flashcard_data)))

    self.frame = pd.DataFrame(columns=['English', 'Japanese'], data=flashcards)
    Scrape.CSV_PATH.mkdir(parents=True, exist_ok=True)
    csv_file = unit + '.csv'
    path = Scrape.CSV_PATH / csv_file

    self.frame.to_csv(path, index=False, encoding='utf-8-sig')
    #print('success')

    return path
  
  def __convert__(self):
    pass
    

class MyGrid(GridLayout):
  def __init__(self, **kwargs):
    super(MyGrid, self).__init__(**kwargs)
    self.rows = 2
    self.html = TextInput(multiline=True)
    self.add_widget(self.html)
    
    self.submit = Button(text="Enter", font_size=30)
    self.submit.bind(on_press=self.pressed)
    self.add_widget(self.submit)

  def pressed(self, instance):
    html = self.html.text
    if html == '':
      return
    self.html.text = ''
    scraper = Scrape(html)
    try:
      csv_path = scraper.start()
    except AttributeError as ae:
      return
    sheets.addToSheet(csv_path)
    


class MyApp(App):
  def build(self):
    return MyGrid()


if __name__ == '__main__':
  MyApp().run()