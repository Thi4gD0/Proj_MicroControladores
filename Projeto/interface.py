import tkinter as tk
from datetime import datetime, timedelta

from fisica.corpos import cria_planeta, cria_foguete, cria_alvo
from fisica.simulacao import valida_parametros
from execucao_da_cnc import executa_na_cnc

# SETAR PARAMETROS GLBOAIS
global state
state= False
global acabou
acabou = False
global ganhou
ganhou = False
global tempc
global cont
cont = 100
global qnt
qnt = "COMBUSTIVEL RESTANTE: XXXXXXXXXX"
global segurarcima
global seguraresq
global segurardir
segurarcima = False
seguraresq = False
segurardir = False
global ang
ang = 0

janela = tk.Tk()
janela.title("Interface Gráfica")
janela.geometry("650x300")

labelcomeco = tk.Label(
    janela,
    text="Começando o jogo",
    fg="black"
)

def comecar():
  global state
  global tempc
  tempc = datetime.now()
  print("Começando o jogo.")
  labelcomeco.place(x=130, y=130)
  state = True
  

def apertarcima(event):
  if state == True:
    global segurarcima
    segurarcima = True

def soltarcima(event):
  global segurarcima
  global state
  if state == True:
    segurarcima = False

def apertaresquerda(event):
  global seguraresq
  global state
  if state == True:
    seguraresq = True

def soltaresquerda(event):
  global seguraresq
  global state
  if state == True:
    seguraresq = False
  
def apertardireita(event):
  global segurardir
  global state
  if state == True:
    segurardir = True

def soltardireita(event):
  global segurardir
  global state
  if state == True:
    segurardir = False

def checagem():
  global segurarcima
  global seguraresq
  global segurardir
  global state
  global tempc
  if state == True:
    tempag = datetime.now()
    inter = tempag-tempc
    segs = (inter.total_seconds())
    if (segs>=3):
        labelcomeco.place_forget()
    if segurarcima == True and state == True:
      atualizar_comb()
    elif seguraresq == True and state == True:
      angesq()
    elif segurardir == True and state == True:
      angdir()
  janela.after(100,checagem)

checagem()

def angesq():
  global ang
  ang -=1
  if (ang == -360):
    ang = 0
  print(ang)


def angdir():
  global ang
  ang +=1
  if (ang == 360):
    ang = 0
  print(ang)

hello = tk.StringVar()
comb = tk.Label(janela, textvariable=hello)
comb.place(x=0,y=0)
hello.set(qnt)

def atualizar_comb():
  global cont
  global qnt
  global state
  global acabou
  cont -=1
  if cont <0:
    cont=0
  if (cont >0 and cont%10==0 and cont<100):
    qnt = "COMBUSTIVEL RESTANTE: " + "X"*(int(cont/10))
    hello.set(qnt)
  elif(cont==0): 
    qnt ="ACABOU O COMBUSTIVEL"
    hello.set(qnt)
    acabou = True
    print("FIM DE JOGO")

labelfim = tk.Label(
    janela,
    text="FIM DE JOGO",
    fg="black"
)

labelganhou = tk.Label(
    janela,
    text="VOCÊ GANHOU",
    fg="black"
)

def fim():
  global acabou
  global ganhou
  if(acabou == True and ganhou == False):
    labelfim.place(x=150, y=150)
  elif(acabou == True and ganhou == True):
    labelganhou.place(x=150,y=150)
  janela.after(100,fim)

fim()

botao1 = tk.Button(janela, text="COMEÇAR", command=comecar)
botao1.place(x=250, y=250)

botao2 = tk.Button(janela, text="CIMA")
botao2.place(x=500, y=150)
botao2.bind('<ButtonPress-1>',apertarcima)
botao2.bind('<ButtonRelease-1>',soltarcima)

botao4 = tk.Button(janela, text="ESQUERDA")
botao4.place(x=400, y=200)
botao4.bind('<ButtonPress-1>',apertaresquerda)
botao4.bind('<ButtonRelease-1>',soltaresquerda)

botao5 = tk.Button(janela, text="DIREITA")
botao5.place(x=550, y=200)
botao5.bind('<ButtonPress-1>',apertardireita)
botao5.bind('<ButtonRelease-1>',soltardireita)

labelparametro = tk.Label(
    janela,
    text="PARAMETRO",
    fg="black"
)

labelparametro.place(x=250, y=150)

slider = tk.Scale(janela, from_=0, to=100, orient=tk.HORIZONTAL)
slider.place(x=250, y=170)


janela.mainloop()

