#!/usr/bin/python
# -*- coding: utf-8 -*-


import wx
from wx.lib.buttons import GenBitmapButton
import os
import random
import csv
import shutil
import wx.lib.agw.shapedbutton as SB

pwd = os.path.abspath(__file__)[:-len(__file__)]


class Frame(wx.Frame):
    def __init__(self, parent, id, title):
      wx.Frame.__init__(self, parent, id, title, size=(960,700))
      # menu okna głównego ------------------------------------------
      self.CreateStatusBar()
      menuBar = wx.MenuBar()
      menu = wx.Menu()
      pomoc = wx.Menu()
      menu.Append(100,  "&Kalkulator foremek")
      menu.Append(101,  "&Przelicznik kulinarny")
      menu.Append(102,  "&Ulubione")
      menu.Append(99,  "&Zamknij")
      pomoc.Append(103,  "&Aktualizacja")
      pomoc.Append(104,  "&O programie")
      menuBar.Append(menu, "&Menu")
      menuBar.Append(pomoc, "&Pomoc")
      self.SetMenuBar(menuBar)
      self.Bind(wx.EVT_MENU, self.wyjscie, id=99)
      self.Bind(wx.EVT_MENU, self.foremki, id=100)
      self.Bind(wx.EVT_MENU, self.jednostki, id=101)
      self.Bind(wx.EVT_MENU, self.ulubione, id=102)
      self.Bind(wx.EVT_MENU, self.aktualizacja, id=103)
      self.Bind(wx.EVT_MENU, self.about, id=104)
      # -------------------------------------------------------------
      # okno główne - wyszukiwarka + jej wygląd -----------------------
      panel = wx.Panel(self)
      panel.SetBackgroundColour('white')
      self.entrytext = wx.TextCtrl(panel, value="Wpisz frazę, którą chcesz wyszukać")
      self.entrytext.SetForegroundColour((0,0,0))
      button = wx.Button(panel, label="Szukaj")
      radio1 = wx.RadioButton( panel, -1, " po nazwach potraw ", style = wx.RB_GROUP )
      radio2 = wx.RadioButton( panel, -1,  " po składnikach " )
      button1 = wx.Button(panel, label="+ Dodaj przepis")

      button.Bind(wx.EVT_BUTTON, self.Search)
      radio1.Bind(wx.EVT_RADIOBUTTON, self.radiobutton)
      radio2.Bind(wx.EVT_RADIOBUTTON, self.radiobutton)
      button1.Bind(wx.EVT_BUTTON, self.Add)

      radio1.SetForegroundColour('black')
      radio2.SetForegroundColour('black')
      button.SetBackgroundColour((50,50,50))
      button.SetForegroundColour('white')
      button1.SetBackgroundColour((50,50,50))
      button1.SetForegroundColour('white')

      self.sizer = wx.GridBagSizer(5, 5)
      self.sizer.Add(self.entrytext, (7, 10), (1, 12), wx.EXPAND)
      self.sizer.Add(button, (7, 22))
      self.sizer.Add(button1, (0, 0))
      self.sizer.Add(radio1, (8, 11))
      self.sizer.Add(radio2, (8, 15))
      
      # -------------------------------------------------------------
      
      # okno główne - wygląd ----------------------------------------
      logofile = pwd + "logo.png"
      logopng = scale(logofile,200,150)
      wx.StaticBitmap(panel, -1, logopng, (360, 15), (logopng.GetWidth(), logopng.GetHeight()))
      # -------------------------------------------------------------

      # okno główne - inspiracje ----------------------------------------
      names, imagefiles = self.inspiracje()
      imgbuttons = [0]*5
      for i in range(4):
	imagefile = imagefiles[i]
	imagefile = imagefile + ".jpg"
	img = scale(imagefile,175,250)
	h = img.GetHeight()
	imgbutton = GenBitmapButton(panel, -1, img,(50+225*i, 475-h/2))
	imgbuttons[i] = imgbutton
        text = wx.StaticText(panel, -1, names[i], (55+225*i, 495+h/2+10))
	text.SetForegroundColour((0,0,0))
        text.Wrap(175)

      imgbuttons[0].Bind(wx.EVT_BUTTON, lambda event: imgEvent( names[0],self))
      imgbuttons[1].Bind(wx.EVT_BUTTON, lambda event: imgEvent( names[1],self))
      imgbuttons[2].Bind(wx.EVT_BUTTON, lambda event: imgEvent( names[2],self))
      imgbuttons[3].Bind(wx.EVT_BUTTON, lambda event: imgEvent( names[3],self))
      
      text = wx.StaticText(panel, -1, 'Przepisy na dziś', (375,310), style=wx.ALIGN_CENTRE)
      text.SetForegroundColour((0,0,0))
      font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
      text.SetFont(font)
      # -------------------------------------------------------------
      panel.SetSizer(self.sizer)

    #----------------------------------------------------------------------
    # funkcja do menu-kalkulator foremek
    def foremki(self, event):
	global frame4
	frame4 = Frame4(None, -1)
        frame4.CenterOnScreen()
        frame4.Show(True)

    #----------------------------------------------------------------------
    # funkcja do menu-przelicznik kulinarny (jednostek)
    def jednostki(self, event):
	global frame5
	frame5 = Frame5(None, -1)
        frame5.CenterOnScreen()
        frame5.Show(True)

    #----------------------------------------------------------------------
    # funkcja do menu-ulubione
    def ulubione(self, event):
	global frame6
	frame6 = Frame6(None, -1)
        frame6.CenterOnScreen()
        frame6.Show(True)

    #----------------------------------------------------------------------
    # funkcja do menu-aktualizacja
    def aktualizacja(self, event):
	global frame7
	frame7 = Frame7(None, -1)
        frame7.CenterOnScreen()
        frame7.Show(True)
	import update
	frame7.text.SetLabel('\nAktualizacja ukończona!')

    #----------------------------------------------------------------------
    # funkcja do menu-o programie
    def about(self, event):
	global frame8
	frame8 = Frame8(None, -1)
        frame8.CenterOnScreen()
        frame8.Show(True)

    #----------------------------------------------------------------------
    # funkcja do menu-exit
    def wyjscie(self, event):
	self.Close()

    #---------------------------------------------------------------------- 
    # funkcja losująca przepisy do 'Inspiracji'
    def inspiracje(self):
	resultnames = []
	resultfiles = []
	csvfile = open( os.path.join("data", "data.csv"), 'r')
	reader = csv.DictReader(csvfile, delimiter='|')
	randoms = [2,8,9,11]#random.sample(list(xrange( sum(1 for row in reader) ))[:-1] ,  4)
	csvfile.seek(0)
	reader = csv.DictReader(csvfile, delimiter='|')
	k=0
	for row in reader:
		if k in randoms:
			name=row['name']
			imgfile = pwd + "data/images/img_"+ replace(name)
			resultnames.append(name)
			resultfiles.append(imgfile)
			randoms.remove(k)
			if randoms==[]: break
		k=k+1
	csvfile.close()
	return  resultnames, resultfiles


    #----------------------------------------------------------------------
    # funkcja do radio
    def radiobutton(self, event):
	global searchoption
	btn = event.GetEventObject()
	searchoption = btn.GetLabel()

	
    #----------------------------------------------------------------------
    # funkcja do przycisku 'Szukaj'
    def Search(self, event):
        """"""
	global frame2 
	search = (self.entrytext.GetValue()).encode('utf8').lower()
	option = searchoption.encode('utf8')
	csvfile = open( os.path.join("data", "data.csv"), 'r')
	reader = csv.DictReader(csvfile, delimiter='|')
	names = [ row['name'] for row in reader]
	results = []
	if option == " po składnikach " : 
		csvfile.seek(0)
		reader = csv.DictReader(csvfile, delimiter='|')
		for row in reader:
			if search in row['ingredients'].lower():  results.append(row['name'])
	elif option == " po nazwach potraw " :
		for name in names:
			if search in name.lower():
				results.append(name)
	self.Hide() 
	csvfile.close()
	frame2 = Frame2(self, -1, "Wyniki wyszukiwania", results)
        frame2.CenterOnScreen()
        frame2.Show(True)

	
    #----------------------------------------------------------------------
    # funkcja do przycisku '+ Dodaj przepis'
    def Add(self, event):
        """"""
	global frame3
	frame3 = Frame3(None, -1)
        frame3.CenterOnScreen()
        frame3.Show(True)


#----------------------------------------------------------------------
# okno z przepisem
class Frame1(wx.Frame): 
    def __init__(self, parent, id, title):
      wx.Frame.__init__(self, parent, id, title, size=(600,600))
      #panel = wx.Panel(self)
      panel = wx.PyScrolledWindow( self, -1 )
      panel.SetBackgroundColour('white')
      logofile = pwd + "logo.png"
      logopng = scale(logofile,120,90)
      wx.StaticBitmap(panel, -1, logopng, (40, 10), (logopng.GetWidth(), logopng.GetHeight()))
      fotofile = pwd + "data/images/img_" + replace(title) +".jpg"
      fotopng = scale(fotofile,200,200)
      h = fotopng.GetHeight()
      wx.StaticBitmap(panel, -1, fotopng, (20, 110), (fotopng.GetWidth(), h))
      lista = wx.StaticText(panel, -1, 'Lista składników:', (45,130+h), style=wx.ALIGN_CENTRE)
      lista.SetForegroundColour((0,0,0))
      csvfile = open( os.path.join("data", "data.csv"), 'r')
      reader = csv.DictReader(csvfile, delimiter='|')
      for row in reader: 
	if row['name']==title : ingred = row['ingredients'] ; recipe = row['recipe'] 
      csvfile.close()
      line=0
      for ing in ingred.split("\n") :
	line = line + 1
	if len(ing) > 25 : 
		line = line +1
      h_ing = line*10
      ingred = wx.StaticText(panel, -1, ingred, (20,160+h), style=wx.ALIGN_LEFT)
      ingred.SetForegroundColour((0,0,0))
      ingred.Wrap(170)	
      text = wx.StaticText(panel, -1, title, (230,70), (500, 40), style=wx.ALIGN_CENTER)
      text.SetForegroundColour((0,0,0))
      text.Wrap(250)
      font = wx.Font(14, wx.NORMAL, wx.NORMAL, wx.NORMAL)
      text.SetFont(font)
      text = wx.StaticText(panel, -1, 'Wykonanie:', (240,130), style=wx.ALIGN_LEFT)
      text.SetForegroundColour((0,0,0))
      font = wx.Font(11, wx.NORMAL, wx.NORMAL, wx.NORMAL)
      text.SetFont(font)
      self.ulub = wx.StaticText(panel, -1, 'Dodano do ulubionych!', (440,40), style=wx.ALIGN_RIGHT)
      self.ulub.SetForegroundColour((10,150,10))
      self.ulub.Hide()
      line1=0
      for rec in recipe.split("\n") :
	line1 = line1 + 1
	if len(rec) > 50 : 
		line1 = line1 +1
      h_rec = line1*15
      recipe = wx.StaticText(panel, -1, recipe, (240,160), style=wx.ALIGN_LEFT)
      recipe.SetForegroundColour((0,0,0))
      recipe.Wrap(350)
      button1 = wx.Button(panel, -1, "Wstecz", (350	, 5))
      button1.SetBackgroundColour((50,50,50))
      button1.SetForegroundColour('white')
      button1.Bind(wx.EVT_BUTTON, lambda event: Back(parent))
      button2 = wx.Button(panel, -1, "Dodaj do ulubionych", (440, 5))
      button2.SetBackgroundColour((50,50,50))
      button2.SetForegroundColour('white')
      button2.Bind(wx.EVT_BUTTON, lambda event: self.Favorite(title))
      if h_ing > 440-h or h_rec > 480 :
	y = 150 + h_rec
      	panel.SetScrollbars( 0, 50,  0, y/50+1 )
      	panel.SetScrollRate( 1, 1 )


    def Favorite(self,name):
      favpath = pwd+"data/favorite.dat"
      mode = 'a+'
      favfile = open( favpath, mode)
      if (name+"\n") not in favfile.readlines(): favfile.write(name+"\n")
      self.ulub.Show()

#---------------------------------------------------------------------- 
# okno z listą wyników
class Frame2(wx.Frame): 
    def __init__(self, parent, id, title, names):
      wx.Frame.__init__(self, parent, id, title, size=(600,700))
      window = wx.PyScrolledWindow( self, -1 )
      window.SetBackgroundColour('white')
      logofile = pwd + "logo.png"
      logopng = scale(logofile,120,100)
      wx.StaticBitmap(window, -1, logopng, (40, 10), (logopng.GetWidth(), logopng.GetHeight()))
      text = wx.StaticText(window, -1, 'Lista wyników:', (230,80))
      text.SetForegroundColour((0,0,0))
      font = wx.Font(14, wx.NORMAL, wx.NORMAL, wx.NORMAL)
      text.SetFont(font)
      buttons = []
      i=-1
      for name in names:
	i = names.index(name)
	fotofile = pwd + "data/images/img_" + replace(name) + ".jpg"
      	img = scale(fotofile,180,150)
	wx.StaticBitmap(window, -1, img,(50, 140+110*i), (logopng.GetWidth(), logopng.GetHeight()))
	text = wx.StaticText(window, -1, name, (180,160+110*i), style=wx.ALIGN_LEFT)
	text.SetForegroundColour((0,0,0))
	text.Wrap(300)
	button = wx.Button(window, -1, "Zobacz przepis", (470, 200+110*i))
        button.SetBackgroundColour((50,50,50))
        button.SetForegroundColour('white')
	buttons.append(button)
	buttons[i].Bind(wx.EVT_BUTTON, lambda event, i=i: imgEvent( names[i], self))
      if i>=0:
	y = 250+110*i
      	window.SetScrollbars( 0, 50,  0, y/50+1 )
      	window.SetScrollRate( 1, 1 )
      button1 = wx.Button(window, -1, "Wstecz", (500, 2))
      button1.SetBackgroundColour((50,50,50))
      button1.SetForegroundColour('white')
      button1.Bind(wx.EVT_BUTTON, lambda event: Back(parent))
   

#---------------------------------------------------------------------- 
# okno z opcja dodania przepisu
class Frame3(wx.Frame): 
    def __init__(self, parent, id):
      wx.Frame.__init__(self, parent, id, size=(600,700))
      panel = wx.Panel(self)
      panel.SetBackgroundColour('white')
      logofile = pwd + "logo.png"
      logopng = scale(logofile,120,100)
      wx.StaticBitmap(panel, -1, logopng, (230, 10), (logopng.GetWidth(), logopng.GetHeight()))
      global fotopath
      fotopath = pwd + "data/images/brak.jpg" 
      self.nazwa = wx.TextCtrl(panel, value="Wpisz nazwę potrawy")
      self.nazwa.SetForegroundColour('black')
      self.skladniki = wx.TextCtrl(panel, -1, value="Wpisz składniki", style=wx.TE_MULTILINE)
      self.skladniki.SetForegroundColour('black')
      self.przepis = wx.TextCtrl(panel, -1, value="Wpisz treść przepisu", style=wx.TE_MULTILINE)
      self.przepis.SetForegroundColour('black')
      self.button = wx.Button(panel, label="Dodaj")
      self.button1 = wx.Button(panel, label="Dodaj zdjęcie")
      self.text = wx.StaticText(panel, -1, ' Nie dodano zdjęcia.', style=wx.ALIGN_LEFT)
      self.text.SetForegroundColour((255,0,0))

      self.button1.SetBackgroundColour((50,50,50))
      self.button1.SetForegroundColour('white')
      self.button.SetBackgroundColour((50,50,50))
      self.button.SetForegroundColour('white')

      self.button.Bind(wx.EVT_BUTTON, self.Add1)
      self.button1.Bind(wx.EVT_BUTTON, self.Open)
      self.skladniki.SetInsertionPoint(0)
      self.przepis.SetInsertionPoint(0)

      self.sizer = wx.GridBagSizer(5, 5)
      self.sizer.Add(self.nazwa, (5, 5), (1, 20), wx.EXPAND)
      self.sizer.Add(self.skladniki, (6, 5), (7, 20), wx.EXPAND)
      self.sizer.Add(self.przepis, (13, 5), (12, 20), wx.EXPAND)
      self.sizer.Add(self.button1, (25, 5))
      self.sizer.Add(self.button, (26, 23))
      self.sizer.Add(self.text, (26, 5))
      panel.SetSizer(self.sizer)

    #----------------------------------------------------------------------
    # funkcja do przycisku 'Dodaj'
    def Add1(self, event):
        """"""
	nazwa = (self.nazwa.GetValue()).encode('utf8')
	skladniki = (self.skladniki.GetValue()).encode('utf8')
	przepis = (self.przepis.GetValue()).encode('utf8')
	csvfile = open(os.path.join("data", "data.csv"), 'a')
	fieldnames = ['name', 'link', 'ingredients', 'recipe']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="|")
	writer.writerow({'name': nazwa, 'link': 'brak', 'ingredients': skladniki, 'recipe': przepis})
	file_path = pwd +"data/images/" + "img_" + replace(nazwa) + ".jpg"
	shutil.copy2(fotopath, file_path)
	self.Destroy()

    #----------------------------------------------------------------------
    # funkcja do przycisku 'Dodaj zdjęcie'
    def Open(self, event):
       """"""
       dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.*", wx.OPEN)
       global fotopath
       if dlg.ShowModal() == wx.ID_OK:
                fotopath = dlg.GetPath()
		self.text.SetLabel('Zdjęcie dodano!')
		self.text.SetForegroundColour((10,150,10))
		self.sizer.Layout()
       dlg.Destroy()   


#---------------------------------------------------------------------- 
# okno kalkulatora foremek
class Frame4(wx.Frame): 
    def __init__(self, parent, id):
      wx.Frame.__init__(self, parent, id, size=(560,600))
      panel = wx.Panel(self)
      panel.SetBackgroundColour('white')
      logofile = pwd + "logo.png"
      logopng = scale(logofile,120,100)
      wx.StaticBitmap(panel, -1, logopng, (60, 10), (logopng.GetWidth(), logopng.GetHeight()))
      text = wx.StaticText(panel, -1, 'Kalkulator foremek', (230,50))
      text.SetForegroundColour((0,0,0))
      font = wx.Font(14, wx.NORMAL, wx.NORMAL, wx.NORMAL)
      text.SetFont(font)
      text01 = wx.StaticText(panel, -1, 'Przelicz z (forma z przepisu):', (30,120))
      text01.SetForegroundColour((0,0,0))
      text02 = wx.StaticText(panel, -1, 'Przelicz na (Twoja forma):', (330,120))
      text02.SetForegroundColour((0,0,0))

      radio1 = wx.RadioButton( panel, -1, " blachy ", style = wx.RB_GROUP)
      radio2 = wx.RadioButton( panel, -1, " tortownicy " )
      radio3 = wx.RadioButton( panel, -1, " blachę ", style = wx.RB_GROUP )
      radio4 = wx.RadioButton( panel, -1, " tortownicę " )
      radio1.SetForegroundColour('black')
      radio2.SetForegroundColour('black')
      radio3.SetForegroundColour('black')
      radio4.SetForegroundColour('black')

      self.text1 = wx.StaticText(panel, -1, 'Wymiary:			x', (60,210))
      self.text2 = wx.StaticText(panel, -1, 'Wymiary:			x', (350,210))
      self.text1.SetForegroundColour('black')
      self.text2.SetForegroundColour('black')

      self.wymiar1 = wx.TextCtrl(panel, value="", pos = (135,205), size = (40,30))
      self.wymiar2 = wx.TextCtrl(panel, value="", pos = (190,205), size = (40,30))
      self.wymiar3 = wx.TextCtrl(panel, value="", pos = (425,205), size = (40,30))
      self.wymiar4 = wx.TextCtrl(panel, value="", pos = (480,205), size = (40,30))

      text3 = wx.StaticText(panel, -1, 'Lista składników:', (80,260))
      text3.SetForegroundColour('black')

      self.skladnik1 = wx.TextCtrl(panel, value="", pos = (70,283), size = (170,30))
      self.skladnik2 = wx.TextCtrl(panel, value="", pos = (70,317), size = (170,30))
      self.skladnik3 = wx.TextCtrl(panel, value="", pos = (70,351), size = (170,30))
      self.skladnik4 = wx.TextCtrl(panel, value="", pos = (70,385), size = (170,30))

      il = wx.StaticText(panel, -1, 'Ilość:', (260,288))
      il.SetForegroundColour('black')
      il = wx.StaticText(panel, -1, 'Ilość:', (260,322))
      il.SetForegroundColour('black')
      il = wx.StaticText(panel, -1, 'Ilość:', (260,356))
      il.SetForegroundColour('black')
      il = wx.StaticText(panel, -1, 'Ilość:', (260,390))
      il.SetForegroundColour('black')

      self.ilosc1 = wx.TextCtrl(panel, value="", pos = (300,283), size = (50,30))
      self.ilosc2 = wx.TextCtrl(panel, value="", pos = (300,317), size = (50,30))
      self.ilosc3 = wx.TextCtrl(panel, value="", pos = (300,351), size = (50,30))
      self.ilosc4 = wx.TextCtrl(panel, value="", pos = (300,385), size = (50,30))

      jednostki = ['ml','l','g','kg','szkl.','łyż.','łyżecz.','szt.']
      self.jednostka1 = wx.Choice(panel,choices = jednostki) 
      self.jednostka2 = wx.Choice(panel,choices = jednostki) 
      self.jednostka3 = wx.Choice(panel,choices = jednostki) 
      self.jednostka4 = wx.Choice(panel,choices = jednostki) 
      self.jednostka1.SetForegroundColour('black')
      self.jednostka2.SetForegroundColour('black')
      self.jednostka3.SetForegroundColour('black')
      self.jednostka4.SetForegroundColour('black')


      self.hidden0 = wx.StaticText(panel, -1, 'Lista składników po przeliczeniu:', (80,450))
      self.hidden0.SetForegroundColour('black')
      self.hidden1 = wx.StaticText(panel, -1, 'Składnik1', (80,480))   
      self.hidden1.SetForegroundColour('black')   
      self.hidden2 = wx.StaticText(panel, -1, 'Składnik2', (80,500))
      self.hidden2.SetForegroundColour('black')
      self.hidden3 = wx.StaticText(panel, -1, 'Składnik3', (80,520))  
      self.hidden3.SetForegroundColour('black')    
      self.hidden4 = wx.StaticText(panel, -1, 'Składnik4', (80,540))
      self.hidden4.SetForegroundColour('black')
      self.hidden0.Hide()
      self.hidden1.Hide()
      self.hidden2.Hide()
      self.hidden3.Hide()
      self.hidden4.Hide()

      self.button = wx.Button(panel, label="Przelicz")
      self.button.SetBackgroundColour((50,50,50))
      self.button.SetForegroundColour('white')
      radio1.Bind(wx.EVT_RADIOBUTTON, self.radiobutton1)
      radio2.Bind(wx.EVT_RADIOBUTTON, self.radiobutton1)
      radio3.Bind(wx.EVT_RADIOBUTTON, self.radiobutton2)
      radio4.Bind(wx.EVT_RADIOBUTTON, self.radiobutton2)
      self.button.Bind(wx.EVT_BUTTON, self.Przelicz)

      self.sizer = wx.GridBagSizer(5, 5)
      #self.sizer.Add(self.entrytext, (7, 16), (1, 12), wx.EXPAND)
      #self.sizer.Add(button, (7, 28))
      #self.sizer.Add(text1, (8, 4))
      self.sizer.Add(radio1, (6, 4))
      self.sizer.Add(radio2, (7, 4))
      self.sizer.Add(radio3, (6, 17))
      self.sizer.Add(radio4, (7, 17))
      self.sizer.Add(self.button, (14, 18))
      self.sizer.Add(self.jednostka1, (11, 17))
      self.sizer.Add(self.jednostka2, (12, 17))
      self.sizer.Add(self.jednostka3, (13, 17))
      self.sizer.Add(self.jednostka4, (14, 17))
      panel.SetSizer(self.sizer)


    #----------------------------------------------------------------------
    # funkcja do radio 'z'

    def radiobutton1(self, event):
	#self.sizer.Layout()
	global fromoption
	fromoption = 1
	btn = event.GetEventObject()
	if btn.GetLabel() == " blachy " : 
		self.text1.SetLabel('Wymiary:			x')
		self.wymiar2.Show()
		fromoption = 1
	elif btn.GetLabel() == " tortownicy " : 
		self.text1.SetLabel('Średnica:')
		self.wymiar2.Hide()
		fromoption = 2
	
    #----------------------------------------------------------------------
    # funkcja do radio 'na'
    def radiobutton2(self, event):
	global tooption
	tooption = 1
	btn = event.GetEventObject()
	label = (btn.GetLabel()).encode('utf8')
	if label == " blachę " : 
		self.text2.SetLabel('Wymiary:			x')
		self.wymiar4.Show()
		tooption = 1
	elif label == " tortownicę " : 
		self.text2.SetLabel('Średnica:')
		self.wymiar4.Hide()
		tooption = 2
	
    #----------------------------------------------------------------------
    # funkcja do przycisku 'Przelicz'
    def Przelicz(self, event):
	skala = self.Skala()
	self.hidden0.Show()
	skladniki = [self.skladnik1, self.skladnik2, self.skladnik3, self.skladnik4]
	ilosci = [self.ilosc1, self.ilosc2, self.ilosc3, self.ilosc4]
	jednostki = [self.jednostka1, self.jednostka2, self.jednostka3, self.jednostka4]
	hiddeny = [self.hidden1, self.hidden2, self.hidden3, self.hidden4]
	for i in [1,2,3,4] : 
		skladnik = skladniki[i-1]
		skladnik = (skladnik.GetValue()).encode('utf8')
		if skladnik != '' :
			ilosc = ilosci[i-1]
			ilosc = float(ilosc.GetValue())
			ilosc = ilosc * skala
			jednostka = jednostki[i-1]
			jednostka = jednostka.GetString(jednostka.GetSelection())
			tekst = skladnik + '    ' + str("%.2f" % ilosc) + '  ' + jednostka.encode('utf8')
			hiddeny[i-1].SetLabel(tekst)
			hiddeny[i-1].Show()

    #----------------------------------------------------------------------
    # funkcja wyliczająca skalę do przeliczenia ilosci potrzebnych skladnikow
    def Skala(self):
	wymiar1 = float(self.wymiar1.GetValue())
	wymiar3 = float(self.wymiar3.GetValue())
	if fromoption == 1 :
		wymiar2 = float(self.wymiar2.GetValue())
		P1 = wymiar1 * wymiar2
		if tooption == 1 :
		 	wymiar4 = float(self.wymiar4.GetValue())
			P2 = wymiar3 * wymiar4
		else : 
			P2 = (wymiar3/2.0)**2 * 3.14159
	elif fromoption == 2 :
		P1 = (wymiar1/2.0)**2 * 3.14159
		if tooption == 1 :
		 	wymiar4 = float(self.wymiar4.GetValue())
			P2 = wymiar3 * wymiar4
		else : 
			P2 = (wymiar3/2.0)**2 * 3.14159
	skala = P2/P1
	return skala


#---------------------------------------------------------------------- 
# okno przelicznika jednostek
class Frame5(wx.Frame): 
    def __init__(self, parent, id):
      wx.Frame.__init__(self, parent, id, size=(420,250))
      panel = wx.Panel(self)
      panel.SetBackgroundColour('white')
      logofile = pwd + "logo.png"
      logopng = scale(logofile,120,100)
      wx.StaticBitmap(panel, -1, logopng, (10, 10), (logopng.GetWidth(), logopng.GetHeight()))
      text = wx.StaticText(panel, -1, 'Przelicznik kulinarny', (170,50))
      text.SetForegroundColour('black')
      font = wx.Font(14, wx.NORMAL, wx.NORMAL, wx.NORMAL)
      text.SetFont(font)

      #skladniki = ['mąka pszenna','mąka ziemniaczana','mąka krupczatka','mąka kukurydziana','cukier','cukier puder','cukier brązowy','kakao','mak','olej','miód','płatki owsiane','mleko/woda','masło','ryż sypki','śmietana kremówka', 'śmietana kwaśna','wiórki kokosowe']
      skladniki = ['mąka pszenna', 'mąka ziemniaczana', 'cukier', 'cukier puder', 'olej', 'miód', 'mleko/woda']
      self.skladnik = wx.Choice(panel,choices = skladniki)      
      self.skladnik.SetForegroundColour('black')
      #jednostki = ['ml','l','g','kg','szkl.','łyż.','łyżecz.']
      jednostki = ['ml','g','szkl.']
      self.jednostka1 = wx.Choice(panel,choices = jednostki) 
      self.jednostka2 = wx.Choice(panel,choices = jednostki) 
      self.jednostka1.SetForegroundColour('black')
      self.jednostka2.SetForegroundColour('black')

      text = wx.StaticText(panel, -1, 'Ilość:', (30,165))
      text.SetForegroundColour('black')
      self.ilosc1 = wx.TextCtrl(panel, value="", pos = (80,160), size = (60,30))
      text = wx.StaticText(panel, -1, 'na', (250,140))
      text.SetForegroundColour('black')
      self.wynik = wx.StaticText(panel, -1, 'Wynik', (300,165))
      self.wynik.SetForegroundColour('black')
      font = wx.Font(12, wx.NORMAL, wx.NORMAL, wx.NORMAL)
      self.wynik.SetFont(font)
      self.wynik.Hide()

      self.button = wx.Button(panel, label="Przelicz")
      self.button.Bind(wx.EVT_BUTTON, self.Przelicz1)
      self.button.SetBackgroundColour((50,50,50))
      self.button.SetForegroundColour('white')

      self.sizer = wx.GridBagSizer(10, 10)
      self.sizer.Add(self.skladnik, (4, 3), span=(1,2))
      self.sizer.Add(self.jednostka1, (5, 4))
      self.sizer.Add(self.jednostka2, (4, 7))
      self.sizer.Add(self.button, (6, 4))
      panel.SetSizer(self.sizer)	


    #----------------------------------------------------------------------
    # funkcja do przycisku 'Przelicz'
    def Przelicz1(self, event):
	gestosci = {'mąka pszenna':0.68, 'mąka ziemniaczana':0.76, 'cukier':0.88, 'cukier puder':0.68, 'olej':0.92, 'miód':1.44, 'mleko/woda':1.00 } #[g/ml]
	jednostki = [self.jednostka1, self.jednostka2]
	skladnik = self.skladnik.GetString(self.skladnik.GetSelection())
	jednostka1 = self.jednostka1.GetString(self.jednostka1.GetSelection())
	jednostka2 = self.jednostka2.GetString(self.jednostka2.GetSelection())
	ilosc = float(self.ilosc1.GetValue())
	skladnik = skladnik.encode('utf8')
	gestosc = gestosci[skladnik]
	if jednostka2 == 'ml' : 
		if jednostka1 == 'szkl.' :  
			wynik = 200 * ilosc
		elif jednostka1 == 'g' : 
			wynik = ilosc / gestosc
		else : 
			wynik = ilosc
	elif jednostka2 == 'szkl.' : 
		if jednostka1 == 'ml' : 
			wynik = ilosc / 200
		elif jednostka1 == 'g' : 
			wynik = ilosc / (200 * gestosc)
		else : 
			wynik = ilosc
	elif jednostka2 == 'g' : 
		if jednostka1 == 'ml' : 
			wynik = ilosc * gestosc
		elif jednostka1 == 'szkl.' : 
			wynik = 200 * ilosc * gestosc
		else : 
			wynik = ilosc
	self.wynik.SetLabel(str("%.2f" % wynik))
	self.wynik.Show()	

#---------------------------------------------------------------------- 
# okno z listą ulubionych przepisów
class Frame6(wx.Frame): 
    def __init__(self, parent, id):
      wx.Frame.__init__(self, parent, id, "Ulubione", size=(600,700))
      window = wx.PyScrolledWindow( self, -1 )
      window.SetBackgroundColour('white')
      logofile = pwd + "logo.png"
      logopng = scale(logofile,120,100)
      wx.StaticBitmap(window, -1, logopng, (40, 10), (logopng.GetWidth(), logopng.GetHeight()))
      text = wx.StaticText(window, -1, 'Ulubione przepisy', (230,80))
      text.SetForegroundColour((0,0,0))
      font = wx.Font(14, wx.NORMAL, wx.NORMAL, wx.NORMAL)
      text.SetFont(font)
      buttons = []
      try:
	favpath = pwd+"data/favorite.dat"
	favfile = open( favpath, 'r')
	names = favfile.readlines()   
      	i=-1
      	for name in names:
		i = names.index(name)
		fotofile = pwd + "data/images/img_" + replace(name[:-1]) + ".jpg"
	      	img = scale(fotofile,180,150)
		wx.StaticBitmap(window, -1, img,(50, 140+110*i), (logopng.GetWidth(), logopng.GetHeight()))
		text = wx.StaticText(window, -1, name[:-1], (180,160+110*i), style=wx.ALIGN_LEFT)
		text.SetForegroundColour((0,0,0))
		text.Wrap(300)
		button = wx.Button(window, -1, "Zobacz przepis", (470, 200+110*i))
		button.SetBackgroundColour((50,50,50))
		button.SetForegroundColour('white')
		buttons.append(button)
		buttons[i].Bind(wx.EVT_BUTTON, lambda event, i=i: imgEvent( (names[i])[:-1], self))
      	if i>=0:
		y = 250+110*i
	      	window.SetScrollbars( 0, 50,  0, y/50+1 )
	      	window.SetScrollRate( 1, 1 )
      except IOError:
	text = wx.StaticText(window, -1, 'Brak przepisów', (230,150))
      	text.SetForegroundColour((0,0,0))


#---------------------------------------------------------------------- 
# okno podczas aktualizacji
class Frame7(wx.Frame): 
    def __init__(self, parent, id):
      wx.Frame.__init__(self, parent, id, "Aktualizacja", size=(250,170))
      panel = wx.Panel(self)
      panel.SetBackgroundColour('white')
      logofile = pwd + "logo.png"
      logopng = scale(logofile,100,100)
      wx.StaticBitmap(panel, -1, logopng, (70, 10), (logopng.GetWidth(), logopng.GetHeight()))
      self.text = wx.StaticText(panel, -1, 'Trwa aktualizacja. \nMoże potrwać kilka minut.', (30,100), style=wx.ALIGN_CENTRE)
      self.text.SetForegroundColour((0,0,0))

#---------------------------------------------------------------------- 
# okno 'o programie'
class Frame8(wx.Frame): 
    def __init__(self, parent, id):
      wx.Frame.__init__(self, parent, id, "O programie", size=(300,250))
      panel = wx.Panel(self)
      panel.SetBackgroundColour('white')
      logofile = pwd + "logo.png"
      logopng = scale(logofile,100,100)
      wx.StaticBitmap(panel, -1, logopng, (100, 10), (logopng.GetWidth(), logopng.GetHeight()))
      self.text = wx.StaticText(panel, -1, 'Wersja 1.0 \n\nProgram jest komputerową książką kucharską zawierającą wybrane przepisy ze strony internetowej  \n                           . \n\n2016  Kamila Smyrgała', (30,100), style=wx.ALIGN_CENTRE)
      self.text1 = wx.StaticText(panel, -1, 'pychotka.pl', (110,186), style=wx.ALIGN_CENTRE)
      self.text.SetForegroundColour((0,0,0))
      self.text1.SetForegroundColour((0,0,0))
      self.text.Wrap(250)
      font = wx.Font(10, wx.NORMAL, wx.ITALIC, wx.NORMAL)
      self.text1.SetFont(font)

#---------------------------------------------------------------------- 


class MyApp(wx.App):
    def OnInit(self):
        global frame
	frame = Frame(None, -1, "Przepiśnik")
        frame.CenterOnScreen()
        frame.Show(True)
        return True

#----------------------------------------------------------------------
# funkcja otwierająca okno z przepisem - globalna
def imgEvent(name,parent):
        imgfile = pwd + "data/images/img_" + replace(name) + ".jpg"
	parent.Hide() 
	global frame1
	frame1 = Frame1(parent, -1, name)
        frame1.CenterOnScreen()
        frame1.Show(True)
        return True


#----------------------------------------------------------------------
# funkcja powracająca do poprzedniego okna - globalna
def Back(parent):
	if str(parent)[10:16]=="Frame;" : 
		try:
		     frame2.Destroy()
        	     frame.Show()
        	except:
        	     frame1.Destroy()
		     frame.Show()
	elif str(parent)[10:16]=="Frame2" : 
		frame1.Destroy()	
		frame2.Show()
	elif str(parent)[10:16]=="Frame6" :
		frame1.Destroy()	
		frame6.Show()
        return True
	
	
#---------------------------------------------------------------------- 
# funkcja skalująca obrazy - globalna

def scale(imgfile,a,b):
	img = wx.Image(imgfile, wx.BITMAP_TYPE_ANY)
	x = img.GetWidth()
	y = img.GetHeight()
      	sx = float(a)/x
      	sy = float(b)/y
       	if sx < 1 and sx <= sy:
	   newx = x*sx
	   newy = y*sx
	   img = img.Rescale(newx, newy, wx.IMAGE_QUALITY_HIGH)
	   #img = img.Resize((a,b),((a-newx)/2, (b-newy)/2),r=-1,g=-1,b=-1)
      	elif sy < 1 and sy < sx:
	   newx = x*sy
	   newy = y*sy
	   img = img.Rescale(newx, newy, wx.IMAGE_QUALITY_HIGH)
	   #img = img.Resize((a,b),((a-newx)/2, (b-newy)/2),r=-1,g=-1,b=-1)
      	else:
	   img = img.Resize((a,b),((a-x)/2, (b-y)/2),r=-1,g=-1,b=-1)
	img = wx.BitmapFromImage(img)
	return img
#---------------------

def replace(text):	
	dic = {"ż":"z", "ź":"z", "ć":"c", "ś":"s", "ą":"a", "ę":"e", "ó":"o", "ł":"l", "ń":"n", "Ż":"Z", "Ź":"Z", "Ć":"C", "Ą":"A", "Ę":"E", "Ś":"S", "Ó":"O", "Ł":"L", "Ń":"N", " ":"-"}
	for i, j in dic.iteritems():
		text = text.replace(i, j)
	return text

#------------------------------------------------- 

app = MyApp(0)
app.MainLoop()


