import tkinter as tk
from tkinter.ttk import Combobox, Frame, Scale, Style
from tkinter import StringVar, IntVar

from testsFunctions import Spherical, Rastrigin, Ackley, Beale, Booth, Bukin, Three_humpCamel, Holder_table, McCormick, Shaffer
from methodsCrossingovers import OnePointCrossingover, TwoPointCrossingover, GenCrossovering
from methodsMutation import SingleBitAbsoluteMutation, InverisonBits, RandomBits, FlipBit

from main import Evolution

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Settings():
    def __init__(self):
        self.testFunction = Spherical()
        self.crossovering = OnePointCrossingover()
        self.mutations = SingleBitAbsoluteMutation()
        self.populationSize = 100
        self.iteration = 80


class InitGuiVar():
    def __init__(self, settings):
        self.settings = settings
        self.initGuiVar()

    def initGuiVar(self):
        self.varSelectTestFunction = StringVar()
        self.varSelectTestFunction.trace_add("write", self.changeTestFunction)

        self.varSelectMethodCrossingover = StringVar()
        self.varSelectMethodCrossingover.trace_add("write", self.changeMethodCrossingover)

        self.varSelectMethodMutations = StringVar()
        self.varSelectMethodMutations.trace_add("write", self.changeMethodMutations)
        
        self.varPopulationSize = IntVar()
        self.varPopulationSize.set(self.settings.populationSize)
        self.varPopulationSize.trace_add("write", self.changePopulationSize)

        self.varIteration = IntVar()
        self.varIteration.set(self.settings.iteration)
        self.varIteration.trace_add("write", self.changeIteration)

        self.varSliderEra = StringVar()
        self.varSliderEra.set("Поколение: ")



    def changeTestFunction(self, v, i, m):
        value = self.varSelectTestFunction.get()
        print(value)

        if value == "Сферическая":
            self.settings.testFunction = Spherical()
            print("Выбрана функция сферическая")
        if value == "Растригина":
            self.settings.testFunction = Rastrigin()
            print("Выбрана функция растригина")
        if value == "Экли":
            self.settings.testFunction = Ackley()
        if value == "Била":
            self.settings.testFunction = Beale()
        if value == "Стенда":
            self.settings.testFunction = Booth()
        if value == "Букина":
            self.settings.testFunction = Bukin()
        if value == "Три горба":
            self.settings.testFunction = Three_humpCamel()
        if value == "Таблица Холдера":
            self.settings.testFunction = Holder_table()
        if value == "Кормика":
            self.settings.testFunction = McCormick()
        if value == "Шафера":
            self.settings.testFunction = Shaffer()
        
        self.updateEvolution()
        try:
            drawStartArea()
        except NameError:
            pass

    def changeMethodCrossingover(self, v, i, m):
        value = self.varSelectMethodCrossingover.get()
        print(value)
        if value == "Одноточечный":
            self.settings.crossovering = OnePointCrossingover()
        if value == "Двухточечный":
            self.settings.crossovering = TwoPointCrossingover()
        if value == "Обмен генами":
            self.settings.crossovering = GenCrossovering()
        self.updateEvolution()
        
    def changeMethodMutations(self, v, i, m):
        value = self.varSelectMethodMutations.get()
        print(value)
        if value == "Инвертировать один из битов":
            self.settings.mutations = SingleBitAbsoluteMutation()
        if value == "Инвертировать каждый бить с вероятностью":
            self.settings.mutations = InverisonBits()
        if value == "Устаналивать случайно каждый бит с вероятностью":
            self.settings.mutations = RandomBits()
        if value == "Менять местами 2 бита":
            self.settings.mutations = FlipBit()
        self.updateEvolution()
        
    def changePopulationSize(self, v, i, m):
        self.settings.populationSize = self.varPopulationSize.get()
        print(self.settings.populationSize)
        self.updateEvolution()

    def changeIteration(self, v, i, m):
        self.settings.iteration = self.varIteration.get()
        print(self.settings.iteration)
        self.updateEvolution()

    
    def updateEvolution(self):
        global e
        e = Evolution(ss)



window = tk.Tk()
ss = Settings()
e = Evolution(ss)
s = InitGuiVar(ss)

window.style = Style()
#window.style.theme_use("alt")
window.option_add( "*font", "clearlyu 12" )
window.title("Лабораторная работа Сиренко В. Н. ИИС-Tg11 2022")
window.geometry('1010x850')


titleFrame = Frame(window)
canvasFrame = Frame(window)
frame = Frame(titleFrame)

# Выбор тестовой функции
label = tk.Label(frame, text="Тестовая функция: ")
label.grid(column=0, row=0)


combo1 = Combobox(frame, textvariable=s.varSelectTestFunction)
combo1['values'] = ["Сферическая", "Растригина", "Экли", "Била", "Стенда", "Букина", "Три горба", "Таблица Холдера", "Кормика", "Шафера"]
combo1.current(0)
combo1.grid(column=1, row=0)

# Выбор метода кроссоверинга
label1 = tk.Label(frame, text="Метод кроссинговера: ")
label1.grid(column=0, row=1, pady=5)

combo2 = Combobox(frame, textvariable=s.varSelectMethodCrossingover)
combo2['values'] = ["Одноточечный", "Двухточечный", "Обмен генами"]
combo2.current(0)
combo2.grid(column=1, row=1, pady=5)

# Размер популяции
label2 = tk.Label(frame, text="Размер популяции: ")
label2.grid(column=3, row=0, padx=5)

ePopulationSize = tk.Entry(frame, width=30, textvariable=s.varPopulationSize)
ePopulationSize.grid(column=4, row=0)

# Итераций
label3 = tk.Label(frame, text="Поколение: ")
label3.grid(column=3, row=1, padx=5)

eIteration = tk.Entry(frame, width=30, textvariable=s.varIteration)
eIteration.grid(column=4, row=1)


# Выбор метода мутации
mutationFrame = Frame(titleFrame)

label4 = tk.Label(mutationFrame, text="Метод мутации: ")
label4.grid(column=0, row=0, pady=5)

combo3 = Combobox(mutationFrame,width=50, textvariable=s.varSelectMethodMutations)
combo3['values'] = ["Инвертировать один из битов", 
                    "Инвертировать каждый бить с вероятностью", 
                    "Устаналивать случайно каждый бит с вероятностью", 
                    "Менять местами 2 бита"]
combo3.current(0)
combo3.grid(column=1, row=0, pady=5)

label5 = tk.Label(mutationFrame, textvariable=s.varSliderEra)
label5.grid(column=2, row=0, pady=5)

frame.grid(column=0, row=0, pady=5)

##########


##### код эволюции
def runEvolution():
    global e
    print("Старт эволюции!")
    e.run()

canvas = None
def drawStartArea():
    global canvas
    if canvas:
        canvas.get_tk_widget().pack_forget()
    # canvas = FigureCanvasTkAgg(e.drawHromoByStep(), canvasFrame)
    canvas = FigureCanvasTkAgg(e.drawInitArea(), canvasFrame)
    canvas.get_tk_widget().pack()

def updateSlider(arg):
    #print(arg)
    step = int((ss.iteration / 100)  * float(arg))
    #print(f"Slider! {step}")
    s.varSliderEra.set("Поколение: "+str(step))
    global canvas
    if canvas:
        canvas.get_tk_widget().pack_forget()
    canvas = FigureCanvasTkAgg(e.drawHromoByStep(
        step
    ), canvasFrame)
    canvas.get_tk_widget().pack()

btnStartEvolution = tk.Button(titleFrame,
                              text="Запустить эволюцию",
                              command=runEvolution)
btnStartEvolution.grid(column=1, row=0, padx=20)

frameSlider=Frame(titleFrame)
slider=Scale(frameSlider, from_=0, to=100, orient='horizontal', length = 980,
             command=updateSlider)
slider.grid(column=0, row=0)
lSlider=tk.Label(frameSlider, text="0..100")

mutationFrame.grid(column=0, row=1, sticky=tk.W+tk.E, columnspan=3)
frameSlider.grid(column=0, row=2, sticky=tk.W+tk.E, columnspan=3)

titleFrame.grid(column=0, row=0)
canvasFrame.grid(column=0, row=1)

# AFter-init
drawStartArea()
window.mainloop()