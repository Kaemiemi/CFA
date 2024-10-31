from machine import ADC, Pin
import time

led = Pin(13, Pin.OUT)

class LDR:
    """This class read a value from a light dependent resistor (LDR)"""

    def __init__(self, pin, min_value=0, max_value=100):
        """
        Initializes a new instance.
        :parameter pin A pin that's connected to an LDR.
        :parameter min_value A min value that can be returned by value() method.
        :parameter max_value A max value that can be returned by value() method.
        """

        if min_value >= max_value:
            raise Exception('Min value is greater or equal to max value')

        # initialize ADC (analog to digital conversion)
        self.adc = ADC(Pin(pin))

        # set 11dB input attenuation (voltage range roughly 0.0v - 3.6v)
        self.adc.atten(ADC.ATTN_11DB)

        self.min_value = min_value
        self.max_value = max_value

    def read(self):
        """
        Read a raw value from the LDR.
        :return A value from 0 to 4095.
        """
        return self.adc.read()

    def value(self):
        """
        Read a value from the LDR in the specified range.
        :return A value from the specified [min, max] range.
        """
        return (self.max_value - self.min_value) * self.read() / 4095


# inicializa o LDR
ldr = LDR(32)

class DadosLuminosidadeUltimaHora:
    def __init__(self):
        self.lista = []
        
    def adicionar(self, valor):
        # Limita a lista a 60 valores
        if len(self.lista) < 60:
            self.lista.append(valor)
        else:
            self.lista.pop(0)
            self.lista.append(valor)
    
    def mostrar(self):
        print(self.lista)

dados = DadosLuminosidadeUltimaHora()

while True:
    
    # lê o valor do LDR
    value = ldr.value()
    
    # adiciona 
    dados.adicionar(value)
    
    print('luminosidade = {:.0f} de 100'.format(value))
    
    # faz o led piscar em caso de alta luminosidade
    if(value >= 70):
        led.value(1)
        time.sleep(0.5)
        led.value(0)
        
    dados.mostrar()

    # delay entre medições
    time.sleep(1)