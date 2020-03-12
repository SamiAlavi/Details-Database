import kivy
kivy.require('1.9.1')

# add the following 2 lines to solve OpenGL 2.0 bug
from kivy import Config
Config.set('graphics', 'multisamples', '1')

Config.set('kivy','exit_on_escape','0')
Config.set('graphics','window_state','maximized')
Config.set('graphics','minimum_width','1366')
Config.set('graphics','minimum_height','740')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.graphics import Color, Rectangle
from kivy.core.audio import SoundLoader

import sqlite3

################################################################################################################################################################################################################################

conn = sqlite3.connect('Data.db')
c = conn.cursor()

Personal=['','','','','','','']
CreditCard=['','','','','',]
Passport=['','','','','','','','','',]
Car=['','','','','','']
Notee=['']
length=0
n=-2
sound=SoundLoader.load('audio/blacknoise.mp3')
sound.play()
popup=''

################################################################################################################################################################################################################################

def FindLength(key):
    if 1<len(key)<26:
        return len(key)
    else:
        return 13
        
def CaesarCipherishEncryption(data):
    global length
    e=''
    for i in data:
        i=ord(i)
        i=chr(i+length)
        e+=str(i)
    #print(e)
    return e

def CaesarCipherishDecryption(data):
    global length
    d=''
    for i in data:
        i=ord(i)
        i=chr(i-length)
        d+=str(i)
    #print(d)
    return d
    
################################################################################################################################################################################################################################

class Main(Screen):
    def on_enter(self):
        global sound, popup

        if popup!='':
            popup.dismiss()
        sound.stop()
        sound=SoundLoader.load('audio/animation.mp3')
        sound.play()
        

class SignUpScreen(Screen):
    def signup(self, *args):
        
        global length, popup
        
        c.execute("CREATE TABLE IF NOT EXISTS SignUp(id INTEGER, Username TEXT, Password TEXT)")
        c.execute("INSERT INTO SignUp VALUES(1,'','')")
        
        username = self.ids.username_input
        username_text = username.text
        password = self.ids.password_input
        password_text = password.text
        #print(password_text)
        
        length=FindLength(password_text)
        
        if username_text.isalnum() and len(password_text)>=8 and password_text.isalnum():
            
            popup = Popup(title='', content=Label(text='Signing up...'),pos=(300, 230), size_hint=(None,None) ,size=(300, 150))
            popup.open()
            
            UN=CaesarCipherishEncryption(username_text)
            PW=CaesarCipherishEncryption(password_text)

            c.execute("UPDATE SignUp SET Username = ? WHERE id = ?",(UN, 1))
            c.execute("UPDATE SignUp SET Password = ? WHERE id = ?",(PW, 1))
            conn.commit()
            
            self.manager.current = 'Main'

        else:
            popup = Popup(title='ERROR',title_align='center',title_color=[1,0,0,1],title_size=30,
                          content=Label(text='• Username and Password must be alphanumeric \n• Greater than 7 characters'),pos=(250, 230), size_hint=(None,None) ,size=(350, 150))
            popup.open()
################################################################################################################################################################################################################################

class LoginScreen(Screen):
    def login(self, *args):
        
        global length, popup
        
        c.execute("CREATE TABLE IF NOT EXISTS SignUp(id INTEGER, Username TEXT, Password TEXT)")
        c.execute("INSERT INTO SignUp VALUES(1,'','')")
        
        username = self.ids.username_input
        username_text = username.text
        password = self.ids.password_input
        password_text = password.text

        length=FindLength(password_text)
        
        c.execute('SELECT Username FROM SignUp WHERE id=1')
        data=c.fetchone()
        UN=CaesarCipherishDecryption(data[0])
        #print(UN)
        
        c.execute('SELECT Password FROM SignUp WHERE id=1')
        data=c.fetchone()
        PW=CaesarCipherishDecryption(data[0])
        #print(PW)
        
        if username_text != '' and password_text != '' and username_text == UN and password_text == PW :
            popup = Popup(title='', content=Label(text='Logging in...'),pos=(300, 230), size_hint=(None,None) ,size=(300, 150))
            popup.open()
            self.manager.current = 'Database'

        elif username_text == '' and password_text == '':
            popup = Popup(title='ERROR',title_align='center',title_color=[1,0,0,1],title_size=30,
                          content=Label(text='• Username and Password not given'),pos=(250, 230), size_hint=(None,None) ,size=(350, 150))
            popup.open()

        elif username_text == '' and password_text != '':
            popup = Popup(title='ERROR',title_align='center',title_color=[1,0,0,1],title_size=30,
                          content=Label(text='• Username not given'),pos=(350, 230), size_hint=(None,None) ,size=(250, 150))
            popup.open()

        elif username_text != '' and password_text == '':
            popup = Popup(title='ERROR',title_align='center',title_color=[1,0,0,1],title_size=30,
                          content=Label(text='• Password not given'),pos=(250, 230), size_hint=(None,None) ,size=(250, 150))
            popup.open()

        else:
            popup = Popup(title='ERROR',title_align='center',title_color=[1,0,0,1],title_size=30,
                          content=Label(text='• Wrong Username and/or Password'),pos=(250, 230), size_hint=(None,None) ,size=(350, 150))
            popup.open()
################################################################################################################################################################################################################################

class Database(Screen):

    def on_enter(self):
        popup.dismiss()

    def logout(self):
        global popup
        popup = Popup(title='', content=Label(text='Logging out...'),pos=(300, 230), size_hint=(None,None) ,size=(300, 150))
        popup.open()
    
    def play(self, *args):
        
        global n,sound
        
        n+=1
        if -1<n<31:
            sound.stop()
            sound = SoundLoader.load('audio/Trap Nation 2018 Best Trap_%s.mp3'%n)
            if sound:                
                #print(n)
                sound.play()
                if 0<n<30:
                    popup = Popup(title='Music Player',title_align='center',title_color=[1,1,1,1],title_size=30,
                                  content=Label(text='Trap Nation 2018 Best Trap_%s.mp3'%n),pos=(300, 230), size_hint=(None,None) ,size=(300, 150))
                    popup.open('Trap Nation 2018 Best Trap_%s.mp3'%n)
                elif n==0:
                    popup = Popup(title='Music Player',title_align='center',title_color=[1,1,1,1],title_size=30,
                                  content=Label(text='BTS - Blood, Sweat and Tears.mp3'),pos=(300, 230), size_hint=(None,None) ,size=(300, 150))
                    popup.open()
                else:
                    popup = Popup(title='Music Player',title_align='center',title_color=[1,1,1,1],title_size=30,
                                  content=Label(text='Aqua - Barbie Girl'),pos=(300, 230), size_hint=(None,None) ,size=(300, 150))
                    popup.open()
                                    
        elif n==-1 or n==31:
            n=-1
            sound.stop()
            sound = SoundLoader.load('audio/Pokémon - Theme.mp3')
            if sound:   
                sound.play()
                popup = Popup(title='Music Player',title_align='center',title_color=[1,1,1,1],title_size=30,
                              content=Label(text='Pokémon - Theme.mp3'),pos=(300,230), size_hint=(None,None) ,size=(300, 150))
                popup.open()
        #print(n)



    def back(self, *args):
        
        global n,sound
        
        n-=1
        if n==-2:
            n=30
        if -1<n<31:
            sound.stop()
            sound = SoundLoader.load('audio/Trap Nation 2018 Best Trap_%s.mp3'%n)
            if sound:
                sound.play()
                if 0<n<30:
                    popup = Popup(title='Music Player',title_align='center',title_color=[1,1,1,1],title_size=30,
                                  content=Label(text='Trap Nation 2018 Best Trap_%s.mp3'%n),pos=(300, 230), size_hint=(None,None) ,size=(300, 150))
                    popup.open('Trap Nation 2018 Best Trap_%s.mp3'%n)
                elif n==0:
                    popup = Popup(title='Music Player',title_align='center',title_color=[1,1,1,1],title_size=30,
                                  content=Label(text='BTS - Blood, Sweat and Tears.mp3'),pos=(300, 230), size_hint=(None,None) ,size=(300, 150))
                    popup.open()
                else:
                    popup = Popup(title='Music Player',title_align='center',title_color=[1,1,1,1],title_size=30,
                                  content=Label(text='Aqua - Barbie Girl'),pos=(300, 230), size_hint=(None,None) ,size=(300, 150))
                    popup.open()
                                    
        elif n==-1 or n==31:
            n=-1
            sound.stop()
            sound = SoundLoader.load('audio/Pokémon - Theme.mp3')
            if sound:                
                sound.play()
                popup = Popup(title='Music Player',title_align='center',title_color=[1,1,1,1],title_size=30,
                              content=Label(text='Pokémon - Theme.mp3'),pos=(300,230), size_hint=(None,None) ,size=(300, 150))
                popup.open()
        #print(n)
    
    def stop(self, *args):        
        global sound
        sound.stop()
    
        

################################################################################################################################################################################################################################

class PersonalDetails(Screen):
    
    global Personal

    c.execute("CREATE TABLE IF NOT EXISTS PersonalDetails(id INTEGER,FirstName TEXT, MiddleName TEXT, LastName TEXT, Address TEXT, PostalCode TEXT, Phone TEXT, Birthday TEXT)")
    c.execute("INSERT INTO PersonalDetails VALUES(1,'','','','','','','')")

    def helpp(self, *args):
        popup = Popup(title='Help',title_align='center',title_color=[0,0.74901960784,1,1],title_size=30,
                              content=Label(text='• Enter the details in the spaces provided\n• Remember to press done after updating the details \n  or else they will not be saved'),
                      pos=(240,230), size_hint=(None,None) ,size=(360, 150))
        popup.open()
    
    def FirstName(self,text):
        Personal[0]=text
        #print(Personal)
        e=CaesarCipherishEncryption(Personal[0])
        
        c.execute("UPDATE PersonalDetails SET FirstName = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
    def MiddleName(self,text):
        Personal[1]=text
        #print(Personal)
        e=CaesarCipherishEncryption(Personal[1])
        
        c.execute("UPDATE PersonalDetails SET MiddleName = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
    def LastName(self,text):
        Personal[2]=text
        #print(Personal)
        e=CaesarCipherishEncryption(Personal[2])
        
        c.execute("UPDATE PersonalDetails SET LastName = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
    def Address(self,text):
        Personal[3]=text
        #print(Personal)
        e=CaesarCipherishEncryption(Personal[3])
        
        c.execute("UPDATE PersonalDetails SET Address = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
    def PostalCode(self,text):
        Personal[4]=text
        #print(Personal)
        e=CaesarCipherishEncryption(Personal[4])
        
        c.execute("UPDATE PersonalDetails SET PostalCode = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
    def Phone(self,text):
        Personal[5]=text
        #print(Personal)
        e=CaesarCipherishEncryption(Personal[5])
        
        c.execute("UPDATE PersonalDetails SET Phone = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
    def Birthday(self,text):
        Personal[6]=text
        #print(Personal)
        e=CaesarCipherishEncryption(Personal[6])
        
        c.execute("UPDATE PersonalDetails SET Birthday = ? WHERE id = ?",
                  (e,1))
        conn.commit()

class ViewPersonalDetails(Screen):
    def on_pre_enter(self):
        global popup
        popup = Popup(title='Personal Details',title_align='center',title_color=[1,1,1,1],title_size=30,
                      content=Label(text='Opening...'),pos=(300, 230), size_hint=(None,None) ,size=(300, 150))
        popup.open()
        
    def on_enter(self):
        global popup
        popup.dismiss()
        with self.canvas:
            Color(0, 0, 0)
            Rectangle(pos=(0,100), size=(1366,800))
        
        c.execute('SELECT * FROM PersonalDetails WHERE id=1')
        data=c.fetchone()
        data=list(data)
    
        i,x,top=1,0,0.7
        while i!=8:
            d=CaesarCipherishDecryption(data[i])
            label=Label(text=str(i)+') '+str(d),pos_hint={'x':x,'top':top},size_hint=(0.5,0.1))
            self.add_widget(label)
            
            if x%2==0:
                x=0.5
            else:
                x=0
                top-=0.1
            i+=1

################################################################################################################################################################################################################################

class CreditCardDetails(Screen):
    
    global CreditCard
    
    c.execute("CREATE TABLE IF NOT EXISTS CreditCardDetails(id INTEGER, CardholderName TEXT, CardType TEXT, CardNumber TEXT, ExpirationDate TEXT, CVC TEXT)")
    c.execute("INSERT INTO CreditCardDetails VALUES(1,'','','','','')")
    
    def helpp(self, *args):
        popup = Popup(title='Help',title_align='center',title_color=[0,0.74901960784,1,1],title_size=30,
                              content=Label(text='• Enter the details in the spaces provided\n• Remember to press done after updating the details \n  or else they will not be saved'),
                      pos=(240,230), size_hint=(None,None) ,size=(360, 150))
        popup.open()
        
    def CardholderName(self,text):
        CreditCard[0]=text
        #print(CreditCard)
        e=CaesarCipherishEncryption(CreditCard[0])
        
        c.execute("UPDATE CreditCardDetails SET CardholderName = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
    def CardType(self,text):
        CreditCard[1]=text
        #print(CreditCard)
        e=CaesarCipherishEncryption(CreditCard[1])
        
        c.execute("UPDATE CreditCardDetails SET CardType = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
    def CardNumber(self,text):
        CreditCard[2]=text
        #print(CreditCard)
        e=CaesarCipherishEncryption(CreditCard[2])
        
        c.execute("UPDATE CreditCardDetails SET CardNumber = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
    def ExpirationDate(self,text):
        CreditCard[3]=text
        #print(CreditCard)
        e=CaesarCipherishEncryption(CreditCard[3])
        
        c.execute("UPDATE CreditCardDetails SET ExpirationDate = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
    def CVC(self,text):
        CreditCard[4]=text
        #print(CreditCard)
        e=CaesarCipherishEncryption(CreditCard[4])
        
        c.execute("UPDATE CreditCardDetails SET CVC = ? WHERE id = ?",
                  (e,1))
        conn.commit()

class ViewCreditCardDetails(Screen):
    def on_pre_enter(self):
        global popup
        popup = Popup(title='Credit Card Details',title_align='center',title_color=[1,1,1,1],title_size=30,
                      content=Label(text='Opening...'),pos=(300, 230), size_hint=(None,None) ,size=(300, 150))
        popup.open()
        
    def on_enter(self):
        global popup
        popup.dismiss()
        
        with self.canvas:
            Color(0, 0, 0)
            Rectangle(pos=(0,100), size=(1366,800))
            
            c.execute('SELECT * FROM CreditCardDetails WHERE id=1')
            data=c.fetchone()
            data=list(data)
        
            i,x,top=1,0,0.7
            while i!=6:
                d=CaesarCipherishDecryption(data[i])
                label=Label(text=str(i)+') '+str(d),pos_hint={'x':x,'top':top},size_hint=(0.5,0.1))
                self.add_widget(label)
                
                if x%2==0:
                    x=0.5
                else:
                    x=0
                    top-=0.1
                i+=1

################################################################################################################################################################################################################################

class PassportDetails(Screen):
    
    global Passport
    
    c.execute("CREATE TABLE IF NOT EXISTS PassportDetails(id INTEGER, FirstName TEXT, MiddleName TEXT, LastName TEXT, Address TEXT, IssuingCountry TEXT, City TEXT, Expiration TEXT, MobileNumber TEXT, Birthday TEXT)")
    c.execute("INSERT INTO PassportDetails VALUES(1,'','','','','','','','','')")
    
    def helpp(self, *args):
        popup = Popup(title='Help',title_align='center',title_color=[0,0.74901960784,1,1],title_size=30,
                              content=Label(text='• Enter the details in the spaces provided\n• Remember to press done after updating the details \n  or else they will not be saved'),
                      pos=(240,230), size_hint=(None,None) ,size=(360, 150))
        popup.open()
            
    def FirstName(self,text):
        Passport[0]=text
        #print(Passport)
        e=CaesarCipherishEncryption(Passport[0])
        
        c.execute("UPDATE PassportDetails SET FirstName = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
    def MiddleName(self,text):
        Passport[1]=text
        #print(Passport)
        e=CaesarCipherishEncryption(Passport[1])
        
        c.execute("UPDATE PassportDetails SET MiddleName = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
    def LastName(self,text):
        Passport[2]=text
        #print(Passport)
        e=CaesarCipherishEncryption(Passport[2])
        
        c.execute("UPDATE PassportDetails SET LastName = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
    def Address(self,text):
        Passport[3]=text
        #print(Passport)
        e=CaesarCipherishEncryption(Passport[3])
        
        c.execute("UPDATE PassportDetails SET Address = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
    def IssuingCountry(self,text):
        Passport[4]=text
        #print(Passport)
        e=CaesarCipherishEncryption(Passport[4])
        
        c.execute("UPDATE PassportDetails SET IssuingCountry = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
    def City(self,text):
        Passport[5]=text
        #print(Passport)
        e=CaesarCipherishEncryption(Passport[5])
        
        c.execute("UPDATE PassportDetails SET City = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
    def Expiration(self,text):
        Passport[6]=text
        #print(Passport)
        e=CaesarCipherishEncryption(Passport[6])
        
        c.execute("UPDATE PassportDetails SET Expiration = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
    def MobileNumber(self,text):
        Passport[7]=text
        #print(Passport)
        e=CaesarCipherishEncryption(Passport[7])
        
        c.execute("UPDATE PassportDetails SET MobileNumber = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
    def Birthday(self,text):
        Passport[8]=text
        #print(Passport)
        e=CaesarCipherishEncryption(Passport[8])
        
        c.execute("UPDATE PassportDetails SET Birthday = ? WHERE id = ?",
                  (e,1))    
        conn.commit()

class ViewPassportDetails(Screen):
        
    def on_pre_enter(self):
        global popup
        popup = Popup(title='Passport Details',title_align='center',title_color=[1,1,1,1],title_size=30,
                      content=Label(text='Opening...'),pos=(300, 230), size_hint=(None,None) ,size=(300, 150))
        popup.open()
        
    def on_enter(self):
        global popup
        popup.dismiss()
        with self.canvas:
            Color(0, 0, 0)
            Rectangle(pos=(0,100), size=(1366,800))
            
        c.execute('SELECT * FROM PassportDetails WHERE id=1')
        data=c.fetchone()
        data=list(data)
        
        i,x,top=1,0,0.7
        while i!=10:
            d=CaesarCipherishDecryption(data[i])
            label=Label(text=str(i)+') '+str(d),pos_hint={'x':x,'top':top},size_hint=(0.5,0.1))
            self.add_widget(label)
            
            if x%2==0:
                x=0.5
            else:
                x=0
                top-=0.1
            i+=1

################################################################################################################################################################################################################################
        
class CarDetails(Screen):
    
    global Car
    
    c.execute("CREATE TABLE IF NOT EXISTS CarDetails(id INTEGER, Manufacturer TEXT, Model TEXT, EngineCapacity TEXT, Oil TEXT, FuelType TEXT, CarNumber TEXT)")
    c.execute("INSERT INTO CarDetails VALUES(1,'','','','','','')")
    
    def helpp(self, *args):
        popup = Popup(title='Help',title_align='center',title_color=[0,0.74901960784,1,1],title_size=30,
                              content=Label(text='• Enter the details in the spaces provided\n• Remember to press done after updating the details \n  or else they will not be saved'),
                      pos=(240,230), size_hint=(None,None) ,size=(360, 150))
        popup.open()
            
    def Manufacturer(self,text):
        Car[0]=text
        #print(Car)
        e=CaesarCipherishEncryption(Car[0])
        
        c.execute("UPDATE CarDetails SET Manufacturer = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
    def Model(self,text):
        Car[1]=text
        #print(Car)
        e=CaesarCipherishEncryption(Car[1])
        
        c.execute("UPDATE CarDetails SET Model = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
    def EngineCapacity(self,text):
        Car[2]=text
        #print(Car)
        e=CaesarCipherishEncryption(Car[2])
        
        c.execute("UPDATE CarDetails SET EngineCapacity = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
    def Oil(self,text):
        Car[3]=text
        #print(Car)
        e=CaesarCipherishEncryption(Car[3])
        
        c.execute("UPDATE CarDetails SET Oil = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
    def FuelType(self,text):
        Car[4]=text
        #print(Car)
        e=CaesarCipherishEncryption(Car[4])
        
        c.execute("UPDATE CarDetails SET FuelType = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
    def CarNumber(self,text):
        Car[5]=text
        #print(Car)
        e=CaesarCipherishEncryption(Car[5])
        
        c.execute("UPDATE CarDetails SET CarNumber = ? WHERE id = ?",
                  (e,1))
        conn.commit()

class ViewCarDetails(Screen):
    def on_pre_enter(self):
        global popup
        popup = Popup(title='Car Details',title_align='center',title_color=[1,1,1,1],title_size=30,
                      content=Label(text='Opening...'),pos=(300, 230), size_hint=(None,None) ,size=(300, 150))
        popup.open()
        
    def on_enter(self):
        popup.dismiss()
        with self.canvas:
            Color(0, 0, 0)
            Rectangle(pos=(0,100), size=(1366,800))
        
        c.execute('SELECT * FROM CarDetails WHERE id=1')
        data=c.fetchone()
        data=list(data)
        
        i,x,top=1,0,0.7
        while i!=7:
            d=CaesarCipherishDecryption(data[i])
            label=Label(text=str(i)+') '+str(d),pos_hint={'x':x,'top':top},size_hint=(0.5,0.1))
            self.add_widget(label)
            
            if x%2==0:
                x=0.5
            else:
                x=0
                top-=0.1
            i+=1

################################################################################################################################################################################################################################
        
class Notes(Screen):
    
    global Notee
    
    c.execute("CREATE TABLE IF NOT EXISTS Notes(id INTEGER, Note TEXT)")
    c.execute("INSERT INTO Notes VALUES(1,'')")
    
    def helpp(self, *args):
        popup = Popup(title='Help',title_align='center',title_color=[0,0.74901960784,1,1],title_size=30,
                              content=Label(text='• Enter the details in the space provided'),pos=(240,230), size_hint=(None,None) ,size=(360, 150))
        popup.open()
            
    def Note(self,text):
        Notee[0]=text
        e=CaesarCipherishEncryption(Notee[0])
        #print(Notee)
        
        c.execute("UPDATE Notes SET Note = ? WHERE id = ?",
                  (e,1))
        conn.commit()
        
class ViewNotes(Screen):
    def on_pre_enter(self):
        global popup
        popup = Popup(title='Notes',title_align='center',title_color=[1,1,1,1],title_size=30,
                      content=Label(text='Opening...'),pos=(300, 230), size_hint=(None,None) ,size=(300, 150))
        popup.open()
    
    def on_enter(self):
        global popup
        popup.dismiss()
        with self.canvas:
            Color(0, 0, 0)
            Rectangle(pos=(0,100), size=(1366,800))
            
        c.execute('SELECT Note FROM Notes WHERE id=1')
        data=c.fetchone()
        data=CaesarCipherishDecryption(data[0])
        
        label=Label(text=str(data), pos=(10,100), size=(770,490),text_size=(1300,self.height))
        self.add_widget(label)

################################################################################################################################################################################################################################

class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file('main.kv')

    
class Walletz(App):

    def build(self):
        return presentation


if __name__ == '__main__':
    Walletz().run()
