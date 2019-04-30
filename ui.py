from tplight import LB130
import tkinter
from threading import Thread
import time

#   Variaveis
light = LB130("192.168.100.14")
timeVariable = 0.05
startingHue = 0
startingBrightness = 10
startingSaturation = 100
startingTransition = 150
startWithRecycle = 1

#   Funcoes prontas
def setOn():
    light.on()
    
def setOff():
    light.off()
        
def setHue(value):
    light.hue = value
    updateSliderValues()
    
def setColorRed():
    setHue(0)
    
def setColorGreen():
    setHue(100)
    
def setColorBlue():
    setHue(200)
    
#   Funcoes de utilidade 
def getSliderHue(event):
    light.hue = hueSlider.get()
    
def getSliderBrightness(event):
    light.brightness = brightnessSlider.get()
    
def getSliderSaturation(event):
    light.saturation = saturationSlider.get()
    
def getSliderTransition(event):
    light.transition_period = transitionSlider.get()
    
def getSliderTemperature(event):
    light.saturation = 0
    light.temperature = temperatureSlider.get()
    updateSliderValues()
    
def updateSliderValues():
    hueSlider.set(light.hue)
    brightnessSlider.set(light.brightness)
    saturationSlider.set(light.saturation)
    transitionSlider.set(light.transition_period)
    temperatureSlider.set(light.temperature)
    
def initializeValues():
    hueSlider.set(startingHue)
    brightnessSlider.set(startingBrightness)
    saturationSlider.set(startingSaturation)
    transitionSlider.set(startingTransition)
    recycleCheckBoxVariable.set(startWithRecycle)
    if(recycleCheckBoxVariable.get()):
        initRecycle()
    
#   Funcoes de modo
def initRecycle():
    t = Thread(target = Recycle)
    t.start()
    
def Recycle():
    while(recycleCheckBoxVariable.get()):
        for i in range(0, 360):
            #sera que é melhor um if assim, que quando entrar da ja um break e nem vai pras linhas de baixo
            if(recycleCheckBoxVariable.get() == 0):
                break
            light.hue = i
            time.sleep(light.transition_period/1000)
            updateSliderValues()
        for i in range(0, 360):
            #ou um assim que fica mais "legivel friendly" ?
            if(recycleCheckBoxVariable.get() == 0):
                break
            else:
                light.hue = 360 - i
                time.sleep(light.transition_period/1000)
                updateSliderValues()
            
def initBreathe():
    t = Thread(target = Breathe)
    t.start()
    
def Breathe():
    while(breatheCheckBoxVariable.get()):
        for i in range(1, 100):
            if(breatheCheckBoxVariable.get() == 0):
                break
            light.brightness = i
            if(recycleCheckBoxVariable.get() == 1):
                time.sleep(light.transition_period/1000)
            else:
                time.sleep(0.05/2)
            updateSliderValues()
        for i in range(1, 100):
            if(breatheCheckBoxVariable.get() == 0):
                break
            light.brightness = 100 - i
            if(recycleCheckBoxVariable.get() == 1):
                time.sleep(light.transition_period/1000)
            else:
                time.sleep(0.05/2)
            updateSliderValues()
            
#   Inicializa a janela, coloca um titulo e uma resolução
window = tkinter.Tk()
window.title("Burca's awesome light controler")
window.geometry('800x600')

#   Cria os elementos da janela

buttonOn = tkinter.Button(window, text = 'On', command = setOn)
buttonOff = tkinter.Button(window, text = 'Off', command = setOff)

colorsLabel = tkinter.Label(window, text = 'Colors !')

buttonRed = tkinter.Button(window, text = 'Red', command = setColorRed, bg = 'red')
buttonBlue = tkinter.Button(window, text = 'Green', command = setColorGreen, bg = 'green')
buttonGreen = tkinter.Button(window, text = 'Blue', command = setColorBlue, bg = 'blue')

hueSlider = tkinter.Scale(window, from_ = 0, to = 360, orient = tkinter.HORIZONTAL, label = 'Hue(Rainbow): ', length = 300, command = getSliderHue)
brightnessSlider = tkinter.Scale(window, from_ = 0, to = 100, orient = tkinter.HORIZONTAL, label = 'Brightness:(%) ', length = 300, command = getSliderBrightness)
saturationSlider = tkinter.Scale(window, from_ = 0, to = 100, orient = tkinter.HORIZONTAL, label = 'Saturation(%): ', length = 300, command = getSliderSaturation)
transitionSlider = tkinter.Scale(window, from_ = 0, to = 1000, orient = tkinter.HORIZONTAL, label = 'Transition Period(ms): ', length = 300, command = getSliderTransition)
temperatureSlider = tkinter.Scale(window, from_ = 3200, to = 7000, orient = tkinter.HORIZONTAL, label = 'Temperature(K): ', length = 300, command = getSliderTemperature)

recycleCheckBoxVariable = tkinter.IntVar()
recycleCheckBox = tkinter.Checkbutton(window, text = "Recycle", variable = recycleCheckBoxVariable, onvalue = 1, offvalue = 0, height=5, width = 20, command = initRecycle)

breatheCheckBoxVariable = tkinter.IntVar()
breatheCheckBox = tkinter.Checkbutton(window, text = "Breathe", variable = breatheCheckBoxVariable, onvalue = 1, offvalue = 0, height=5, width = 20, command = initBreathe)

#   Coloca os valores atuais nos sliders
initializeValues()

#   Adiciona os elementos a janela para serem exibidos
#buttonOn.pack()
#buttonOff.pack()
colorsLabel.pack()
buttonRed.pack()
buttonBlue.pack()
buttonGreen.pack()
hueSlider.pack()
brightnessSlider.pack()
saturationSlider.pack()
transitionSlider.pack()
temperatureSlider.pack()
recycleCheckBox.pack()
breatheCheckBox.pack()
    
#   Mostra a janela
window.mainloop()
