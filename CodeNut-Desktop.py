from logging import disable
import requests
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.text import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

#Global variables acting as cookies
screenx = float(Config.get('graphics', 'width'))
screeny = float(Config.get('graphics', 'height'))

userid = ["userid"]
comment = ["comment"]
password = ["password"]
post = []

ques = ['question']
des = ['description']

nques = ['write a question']
ndes = ['write a description']

idx = [0]

#DOM Root
root = FloatLayout() 

#Components
def button(i, j, text, press):

    def function(event):
        press()

    button = Button()
    button.text = text
    button.pos = (i, j)
    button.size = (100, 30)
    button.background_color = (255, 1, 1, 1)
    button.bind(on_press = function) 
    return button

def send(press):

    def function(event):
        press()

    button = Button()
    button.text = "Send"
    button.font_size = "18sp"
    button.pos = (590, 200)
    button.size = (180, 40)
    button.background_color = (255, 1, 1, 1)
    button.bind(on_press = function) 
    return button

def label(i, j, text):
    label = Label()
    label.font_size = '18sp'
    label.pos = (i, j)
    label.text = text
    return label

def banner_and_background(Screen):
    with Screen.canvas:
        Color(0.4, 0.4, 0.4, 0.3)
        Rectangle(pos=root.pos, size=(screenx, screeny))
        Color(0.2, 0.2, 0.2, 0.7)
        Rectangle(pos=(150,500), size=(500, 100))
    label = Label()
    label.font_size = '36sp'
    label.pos = (350, 500)
    label.text = "CodeNut-Desktop"
    Screen.add_widget(label)

def subhead(Screen, text, i, j):
    label = Label()
    label.font_size = '30sp'
    label.pos = (i, j)
    label.text = text
    Screen.add_widget(label)

def textinput(i, j, var):
    textinput = TextInput()
    textinput.pos = (i, j)
    textinput.font_size = '16sp'
    textinput.size = (150, 30)

    def function(instance, value):
        var[0] = value

    textinput.bind(text = function)
    return textinput

def message(var):
    textinput = TextInput()
    textinput.pos = (590, 255)
    textinput.font_size = '16sp'
    textinput.size = (180, 140)

    def function(instance, value):
        var[0] = value

    textinput.bind(text = function)
    return textinput

def Send():
    data = {'userid': userid[0], 
         'password': password[0],
         'question': post[idx[0]]['question'], 
         'author':  userid[0],
         'comment': comment[0]}
    res = requests.post(url = "https://codenutb.herokuapp.com/createcomment",data=data).json()
    root.clear_widgets()
    root.add_widget(Index())

def CBadge2(votes, k):
    m1 = BoxLayout(orientation='horizontal')
    m1.size_hint = (1, None)

    b1 = Button()
    b2 = Button()
    b3 = Button()
    b4 = Button()

    b1.size_hint = (0.4, 0.25)
    b1.text = "Votes"
    b2.size_hint = (1, 0.25)
    b2.text = votes
    b2.color = "black"
    b3.size_hint = (0.3, 0.25)
    b3.text = "Up"
    b4.size_hint = (0.3, 0.25)
    b4.text = "Down"

    def fun2(event):
        data = {'userid': userid[0], 
         'password': password[0],
         'question': post[idx[0]]['question'], 
         'author': post[idx[0]]['author'],
         'idx': k}
        print(data)

        res = requests.post(url = "https://codenutb.herokuapp.com/upvotec",data=data).json()
        root.clear_widgets()
        root.add_widget(Index())

    b3.bind(on_press = fun2)

    def fun3(event):
        data = {'userid': userid[0], 
         'password': password[0],
         'question': post[idx[0]]['question'], 
         'author': post[idx[0]]['author'],
         'idx': k}
        print(data)

        res = requests.post(url = "https://codenutb.herokuapp.com/downvotec",data=data).json()
        root.clear_widgets()
        root.add_widget(Index())

    b4.bind(on_press = fun3)

    b1.background_color = (255, 1, 1, 1)
    b2.background_color = (255,255,255, 1)
    b3.background_color = (1, 1, 255, 1)
    b4.background_color = (1,1,255, 1)

    m1.add_widget(b1)
    m1.add_widget(b2)
    m1.add_widget(b3)
    m1.add_widget(b4)

    return m1


def Mail(author, message):

    mail = BoxLayout(orientation='horizontal')
    mail.size_hint = (1, None)

    label = Button(disabled=True)
    mess = Button(disabled=True)

    label.text =  author
    mess.text =  message

    mess.color = (0,0,0, 1)
    mess.background_color = (255,255,255, 255)

    mess.size_hint = (6, 1)
    label.size_hint = (1, 1)

    if(author == userid[0]):
        label.background_color = (1,1,255, 1)
    else:
        label.background_color = (255,1,1, 1)  


    if(author == userid[0]):
        mail.add_widget(label)
        mail.add_widget(mess)
    else:
        mail.add_widget(mess)
        mail.add_widget(label)


    return mail

def scrollgridChat(Screen,components,pos, size):
    grid = GridLayout(cols=1, size_hint_y=None)
    grid.bind(minimum_height=grid.setter('height'))
    k = 0
    for i in components:
        grid.add_widget(CBadge2(votes=str(i['votes']), k=k))
        grid.add_widget(Mail(i['author'], i['comment']))
        k = k + 1

    scroll = ScrollView(size_hint=(1, None), pos=pos, size=size)
    scroll.do_scroll_y = True
    scroll.do_scroll_x = False
    scroll.add_widget(grid)
    return scroll

def question():
    textinput = TextInput(text=ques[0])
    textinput.pos = (140, 325)
    textinput.font_size = '16sp'
    textinput.size = (400, 60)

    def function(instance, value):
        ques[0] = value

    textinput.bind(text = function)
    return textinput

def description():
    textinput = TextInput(text=des[0])
    textinput.pos = (140, 385)
    textinput.font_size = '16sp'
    textinput.size = (400, 60)

    def function(instance, value):
        des[0] = value

    textinput.bind(text = function)
    return textinput

def Chat():
    Chat = Widget()
    banner_and_background(Chat)

    with Chat.canvas:

        Color(0.3, 0.3, 0.3, 0.9)
        Rectangle(pos=(580,250), size=(200, 200))
        Color(0.2, 0.2, 0.2, 1)
        Rectangle(pos=(590, 255), size=(180, 140))

        Color(0.3, 0.3, 0.3, 0.9)
        Rectangle(pos=(40,50), size=(500, 220))
        Color(0.2, 0.2, 0.2, 1)
        Rectangle(pos=(60,50), size=(480, 180))
    
    btn = Button()
    btn.pos = (60, 325)
    btn.size = (82, 60)
    btn.text = "Description"
    btn.background_color = (255, 1, 1, 1)
    Chat.add_widget(btn)

    btn = Button()
    btn.pos = (60, 385)
    btn.size = (82, 60)
    btn.text = "Question"
    btn.background_color = (255, 1, 1, 1)
    Chat.add_widget(btn)

    b1 = Button()
    b2 = Button()
    b3 = Button()
    b4 = Button()
    b5 = Button()
    b6 = Button()
    b7 = Button()
    b8 = Button()

    ques[0] = post[idx[0]]['question']
    des[0] = post[idx[0]]['description']

    b1.size = (100, 20)
    b1.pos = (60, 445)
    b1.text = "Votes"
    b2.text = post[idx[0]]['votes']
    b2.size = (100, 20)
    b2.pos = (159, 445)
    b2.color = "black"
    b3.size = (100, 20)
    b3.pos = (341, 445)
    b3.text = "Author"
    b4.text = post[idx[0]]['author']
    b4.size = (100, 20)
    b4.pos = (440, 445)
    b4.color = "black"

    def fun4(instance):
         data = {'userid': userid[0], 
         'password': password[0],
         'question': post[idx[0]]['question'], 
         'author':  post[idx[0]]['author']}
         res = requests.post(url = "https://codenutb.herokuapp.com/upvoteq",data=data).json()
         root.clear_widgets()
         root.add_widget(Index())

    b7.bind(on_press = fun4)

    b7.size = (45, 20)
    b7.pos = (257, 445)
    b7.text = "Up"

    def fun5(instance):
         data = {'userid': userid[0], 
         'password': password[0],
         'question': post[idx[0]]['question'], 
         'author':  post[idx[0]]['author']}
         res = requests.post(url = "https://codenutb.herokuapp.com/downvoteq",data=data).json()
         root.clear_widgets()
         root.add_widget(Index())

    b8.bind(on_press = fun5)

    b8.size = (45, 20)
    b8.pos = (300, 445)
    b8.text = "Down"

    b5.size = (200, 35)
    b5.pos = (300, 285)
    b5.text = "Delete"
    def fun3(instance):
         data = {'userid': userid[0], 
         'password': password[0],
         'question': post[idx[0]]['question'], 
         'author':  post[idx[0]]['author']}
         res = requests.post(url = "https://codenutb.herokuapp.com/deletepost",data=data).json()
         root.clear_widgets()
         root.add_widget(Index())

    b5.bind(on_press = fun3)

    b6.size = (200, 35)
    b6.pos = (100, 285)
    b6.text = "Update"

    def fun3(instance):
         data = {'userid': userid[0], 
         'password': password[0],
         'question': post[idx[0]]['question'],
         'description': post[idx[0]]['description'], 
         'author':  post[idx[0]]['author'],
         'newquestion': ques[0], 
         'newdescription': des[0],}
         print(data)
         res = requests.post(url = "https://codenutb.herokuapp.com/updatepost",data=data).json()
         print(res)
         root.clear_widgets()
         root.add_widget(Index())

    b6.bind(on_press = fun3)


    b1.background_color = (255, 1, 1, 1)
    b2.background_color = (255,255,255, 1)
    b3.background_color = (255, 1, 1, 1)
    b4.background_color = (255,255,255, 1)
    b5.background_color = (1, 1, 255, 1)
    b6.background_color = (1, 1, 255, 1)
    b7.background_color = (1, 1, 255, 1)
    b8.background_color = (1, 1, 255, 1)

    Chat.add_widget(b1)
    Chat.add_widget(b2)
    Chat.add_widget(b3)
    Chat.add_widget(b4)
    Chat.add_widget(b5)
    Chat.add_widget(b6)
    Chat.add_widget(b7)
    Chat.add_widget(b8)

    subhead(Chat,"Comment", 630, 375)
    subhead(Chat,"All Comments", 230, 200)
    Chat.add_widget(message(comment))
    Chat.add_widget(question())
    Chat.add_widget(description())
    Chat.add_widget((send(Send)))

    Chat.add_widget(button(630, 150, "GO Back", Login))

    if(type(post[idx[0]]['comments']) != str):
        Chat.add_widget(scrollgridChat(Chat, post[idx[0]]['comments'], pos=(60,50), size=(480, 180)))

    return Chat

def Create():
    Create = Widget()
    banner_and_background(Create)

    textinput1 = TextInput()
    textinput1.pos = (200, 400)
    textinput1.font_size = '16sp'
    textinput1.size = (450, 60)
    textinput1.text = nques[0]

    def function(instance, value):
        nques[0] = value
    textinput1.bind(text = function)

    textinput2 = TextInput()
    textinput2.pos = (200, 300)
    textinput2.font_size = '16sp'
    textinput2.size = (450, 60)
    textinput2.text = ndes[0]

    def function(instance, value):
        ndes[0] = value
    textinput2.bind(text = function)

    btn1 = Button()
    btn1.size = (100, 60)
    btn1.pos = (100, 400)
    btn1.text = "Question"

    btn2 = Button()
    btn2.size = (100, 60)
    btn2.pos = (100, 300)
    btn2.text = "Description"

    def fun2(event):
        data = {'userid': userid[0], 
         'password': password[0],
         'question': nques[0], 
         'description': ndes[0],
         'author': userid[0]}
        print(data)

        res = requests.post(url = "https://codenutb.herokuapp.com/createpost",data=data).json()
        nques[0] = 'write a question'
        ndes[0] = 'write a description'
        root.clear_widgets()
        root.add_widget(Index())

    btn3 = Button()
    btn3.size = (150, 50)
    btn3.pos = (200, 200)
    btn3.text = "Create"
    btn3.background_color = (255, 1, 1, 1)
    btn3.bind(on_press = fun2) 

    btn4 = Button()
    btn4.size = (150, 50)
    btn4.pos = (350, 200)
    btn4.text = "Go Back"
    btn4.background_color = (255, 1, 1, 1)

    def fun1(event):
        root.clear_widgets()
        root.add_widget(Index())
    btn4.bind(on_press = fun1) 


    Create.add_widget(btn1)
    Create.add_widget(btn2)
    Create.add_widget(btn3)
    Create.add_widget(btn4)

    Create.add_widget(textinput1)
    Create.add_widget(textinput2)
    
    return Create

def scrollgrid(Screen,components,pos, size):
    grid = GridLayout(cols=1, size_hint_y=None)
    grid.bind(minimum_height=grid.setter('height'))
    for i in components:
        grid.add_widget(i)

    scroll = ScrollView(size_hint=(1, None), pos=pos, size=size)
    scroll.do_scroll_y = True
    scroll.do_scroll_x = False
    scroll.add_widget(grid)

    return scroll

def scrollgrid2(Screen,components,pos, size):
    grid = GridLayout(cols=2, size_hint_y=None)
    grid.bind(minimum_height=grid.setter('height'))
    for i in components:
        grid.add_widget(i)

    scroll = ScrollView(size_hint=(1, None), pos=pos, size=size)
    scroll.do_scroll_y = True
    scroll.do_scroll_x = False
    scroll.add_widget(grid)

    return scroll

def Badge(text):
    button = Button()
    button.size_hint = (None, None)
    button.text = text
    button.size = (120, 30)
    button.background_color = (255, 1, 1, 1)
    return button

def Badge2(exp):
    button = Button()
    button.size_hint = (None, None)
    button.text = exp
    button.size = (60, 30)
    button.background_color = (1, 1, 255, 1)
    return button

def CBadge(votes,author):
    m1 = BoxLayout(orientation='horizontal')
    m1.size_hint = (1, None)

    b1 = Button()
    b2 = Button()
    b3 = Button()
    b4 = Button()

    b1.size_hint = (0.4, 0.25)
    b1.text = "Author"
    b2.size_hint = (1, 0.25)
    b2.text = author
    b2.color = "black"
    b3.size_hint = (0.4, 0.25)
    b3.text = "Votes"
    b4.text = votes
    b4.color = "black"
    b4.size_hint = (1, 0.25)

    b1.background_color = (255, 1, 1, 1)
    b2.background_color = (255,255,255, 1)
    b3.background_color = (255, 1, 1, 1)
    b4.background_color = (255,255,255, 1)

    m1.add_widget(b1)
    m1.add_widget(b2)
    m1.add_widget(b3)
    m1.add_widget(b4)

    return m1

def Card(message, x):

    def  function (event):
        idx[0] = x
        print(post[x])
        root.clear_widgets()
        root.add_widget(Chat())

    mail = BoxLayout(orientation='horizontal')
    mail.size_hint = (1, None)

    label = Button()
    mess = Button()

    label.text =  "Question"
    mess.text =  message

    mess.color = (0,0,0, 1)
    mess.background_color = (255,255,255, 255)

    mess.size_hint = (6, 1)
    label.size_hint = (1, 1)

    label.background_color = (1,1,255, 1)
    mail.add_widget(label)
    mail.add_widget(mess)

    label.bind(on_press = function) 
    mess.bind(on_press = function) 

    return mail

def cbutton():

    def function(event):
        root.clear_widgets()
        root.add_widget(Create())

    create = Button()
    create.font_size = "20sp"
    create.pos = (605,80)
    create.size = (150, 50)
    create.text = "Create"
    create.background_color = (255, 1, 1, 1)
    create.bind(on_press = function)
    return create

def Index():
    Index = Widget()
    banner_and_background(Index)
    with Index.canvas:
        Color(0.3, 0.3, 0.3, 0.9)
        Rectangle(pos=(40,50), size=(500, 400))
        Color(0.2, 0.2, 0.2, 1)
        Rectangle(pos=(60,50), size=(480, 400))
        Color(0.3, 0.3, 0.3, 0.9)
        Rectangle(pos=(580,150), size=(200, 300))
        Color(0.2, 0.2, 0.2, 1)
        Rectangle(pos=(590,160), size=(180, 240))
    subhead(Index,"Users", 630, 375)
    subhead(Index,"All Posts", 250, 375)

    res = requests.get(url = "https://codenutb.herokuapp.com/getalluser").json()

    set = []

    for i in res['data']:
        set.append(Badge(i['userid']))
        set.append(Badge2(i['exp']))
            
    
    Index.add_widget(scrollgrid2(Index, set, pos=(590,60), size=(180, 340)))

    set = []
    post.clear()
    res = requests.get(url = "https://codenutb.herokuapp.com/getallpost").json()
    k = 0

    for i in res['data']:
        post.append(i)
        set.append(CBadge(author=str(i['author']),votes=str(i['votes'])))
        set.append(Card(message=str(i['question']), x = k))
        k = k + 1
    
    Index.add_widget(scrollgrid(Index, set, pos=(60, 60), size=(480, 340)))
    Index.add_widget(cbutton())

    return Index

def gsync():

    post = []
    res = requests.get(url = "https://codenutb.herokuapp.com/getallpost").json()
    k = 0

    for i in res['data']:
        post.append(i)
        k = k + 1

def Login():
    data = {'userid':userid[0], 'password': password[0]}
    res = requests.post(url = "https://codenutb.herokuapp.com/isauth",data=data).json()
    if(res['success'] == "True"):
        root.clear_widgets()
        root.add_widget(Index())
    else:
        root.clear_widgets()
        root.add_widget(Account())

def Register():
    data = {'userid':userid[0], 'password': password[0]}
    res = requests.post(url = "https://codenutb.herokuapp.com/adduser",data=data).json()
    if(res['success'] == "True"):
        root.clear_widgets()
        root.add_widget(Index())
        Clock.schedule_interval(gsync, 20)
    else:
        root.clear_widgets()
        root.add_widget(Account())
    
def Account():
    Account = Widget()
    banner_and_background(Account)
    with Account.canvas:
        Color(0.3, 0.3, 0.3, 0.9)
        Rectangle(pos=(60,150), size=(250, 320))
        Color(0.2, 0.2, 0.2, 1)
        Rectangle(pos=(150,150), size=(160, 320))
        Color(0.3, 0.3, 0.3, 0.9)
        Rectangle(pos=(415,150), size=(250, 320))
        Color(0.2, 0.2, 0.2, 1)
        Rectangle(pos=(505,150), size=(160, 320))
    Account.add_widget(label(50, 400, "Userid"))
    Account.add_widget(label(65, 320, "Password"))
    Account.add_widget(label(405, 400, "Userid"))
    Account.add_widget(label(420, 320, "Password"))
    Account.add_widget(label(455, 240, "Re-Enter Password"))
    Account.add_widget(textinput(440, 235, password))
    Account.add_widget(textinput(80, 400, userid))
    Account.add_widget(textinput(80, 320, password))
    Account.add_widget(textinput(440, 400, userid))
    Account.add_widget(textinput(440, 320, password))
    Account.add_widget(button(180, 250, "Login", Login))
    Account.add_widget(button(550, 165, "Register", Register))
    return Account

root.add_widget(Account())

class App(App):
    def build(self):
        return root

if __name__ == "__main__":
    App().run()
