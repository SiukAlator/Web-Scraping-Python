# -*- coding: utf-8 -*-
#Autor: Cesar Delgado Arcos
#version: 1.0

from utils import *
from bs4 import BeautifulSoup
import requests
import time

def main():
    codigos = ""
    FechaIni = ""
    HoraIni = ""
    FechaFin = ""
    HoraFin = ""
    HoraActual = ""

    HoraActual = time.strftime("%H:%M")
    codigos = getParam("codigos")
    FechaIni = time.strftime("%d-%m-%Y")
    HoraIni = "00:00"
    FechaFin = time.strftime("%d-%m-%Y")
    HoraFin = "23:59"

    Ema_IDs = codigos.split(", ")

    escribeLog("Comienza proceso de ejecucion")
    #Se realiza la peticion web tantos codigos existan
    for codigo in Ema_IDs:

        #http://www.agromet.cl/stationGraphics.php?ema_ia_id=32&dateFrom=26-08-201600:00&dateTo=26-08-201623:59
        url = "http://www.agromet.cl/stationGraphics.php?ema_ia_id=%s&dateFrom=%s%s&dateTo=%s%s" %(codigo, FechaIni, HoraIni, FechaFin, HoraFin)

        # Realizamos la petición a la web
        req = requests.get(url)
        # Comprobamos que la petición nos devuelve un Status Code = 200
        statusCode = req.status_code
        if statusCode == 200:

            # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
            html = BeautifulSoup(req.text, "lxml")

            # Obtenemos todos los divs donde estan las entradas
            #entradas = html.findAll('estacion')

            #print "HTML: %s" %(html)
            estacion = getParseHTML("<estacion id='%s'><dato>" %(codigo), "</estacion>", html)
            #print "estacion: %s" %(estacion)
            if estacion == "-1" or estacion == "-2":
                escribeLog ("No se encuentran datos en WEB para codigo %s" %(codigo))
            else:

                datos = estacion.split("<dato>")

                totalDatos = len(datos)
                ultimoDato = ultimoDatoIngresado(codigo)
                if ultimoDato != "0":
                    #Se evalua si el registro obtenido ya se encuentra en BBDD
                    fecha_horaUD = ultimoDato.split(" ")
                    fechaUD = fecha_horaUD[0]
                    horaUD = fecha_horaUD[1]

                    valores = datos[totalDatos-1].split("|")
                    fecha_hora = valores[1].split(" ")
                    '''
                    print "Fecha: %s" %(fecha_hora[0])
                    print "Hora: %s" %(fecha_hora[1])
                    print "TemperaturaAmbiente: %s" %(getTag('1', datos[totalDatos-1]))
                    print "Precipitacion: %s" %(getTag('2', datos[totalDatos-1]))
                    print "HumedadAmbiente: %s" %(getTag('3', datos[totalDatos-1]))
                    print "PresionAtomosferica: %s" %(getTag('4', datos[totalDatos-1]))
                    print "RadiacionSolar: %s" %(getTag('5', datos[totalDatos-1]))
                    print "VelocidadViento: %s" %(getTag('6', datos[totalDatos-1]))
                    print "DireccionViento: %s" %(getTag('9', datos[totalDatos-1]))
                    print ""
                    '''
                    #Se evalua que los datos no se encuentre ingresados
                    if fechaUD!= fecha_hora[0] or horaUD != fecha_hora[1]:
                        #Si la fecha actual es distinta con la ultima ingresada, significa que no se han ingresado datos en el dia.
                        if fechaUD!= fecha_hora[0]:
                            for dato in datos:
                                valores = dato.split("|")
                                fecha_hora = valores[1].split(" ")

                                ingresarDatosBBDD(codigo, fecha_hora[0], fecha_hora[1], getTag('1', dato), getTag('2', dato), getTag('3', dato), getTag('4', dato), getTag('5', dato), getTag('6', dato), getTag('9', dato), FechaFin, HoraActual)
                        else:
                            #Si no, solo se ingresa se evalua a partir de que hora se debe ingresar
                            for dato in datos:
                                valores = dato.split("|")
                                fecha_hora = valores[1].split(" ")
                                rComparacion = compararHoras(fecha_hora[1], horaUD)
                                if rComparacion == "1":
                                    ingresarDatosBBDD(codigo, fecha_hora[0], fecha_hora[1], getTag('1', dato), getTag('2', dato), getTag('3', dato), getTag('4', dato), getTag('5', dato), getTag('6', dato), getTag('9', dato), FechaFin, HoraActual)
                                    #ingresarDatosBBDD(codigo, fecha_hora[0], fecha_hora[1], getTag('1', datos[totalDatos-1]), getTag('2', datos[totalDatos-1]), getTag('3', datos[totalDatos-1]), getTag('4', datos[totalDatos-1]), getTag('5', datos[totalDatos-1]), getTag('6', datos[totalDatos-1]), getTag('9', datos[totalDatos-1]), FechaFin, HoraActual)
                    else:
                        escribeLog("No existe actualizacion nueva en web para codigo: %s" %(codigo))
                else:
                    #En caso de que no existan registros, se ingresa todos lo datos recolectados del dia
                    for dato in datos:
                        valores = dato.split("|")

                        fecha_hora = valores[1].split(" ")

                        ingresarDatosBBDD(codigo, fecha_hora[0], fecha_hora[1], getTag('1', dato), getTag('2', dato), getTag('3', dato), getTag('4', dato), getTag('5', dato), getTag('6', dato), getTag('9', dato), FechaFin, HoraActual)
        else:
            escribeLog("ERROR: Web no encontrada")
    escribeLog("--- Fin de lectura de datos ---")

