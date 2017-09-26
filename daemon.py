import time
from ejecutable import *
from utils import *

def do_something():
    with open("/tmp/current_time.txt", "w") as f:
        f.write("The time is now " + time.ctime())

def run():
    tiempo = getParam("tiempo")
    minutos = int(float(tiempo))
    #Tiempo total en segundos. Se multiplica por 60 para interpretarlo en minutos
    tiempoTotal = minutos * 60
    while True:
        main()
        time.sleep(tiempoTotal)

if __name__ == "__main__":
    run()