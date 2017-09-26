# -*- coding: utf-8 -*-

import MySQLdb
import time

def getParam( parametro):
    archivo = open("parametros.conf")
    linea = ""
    retorno = ""
    largoParam = len(parametro)
    linea = archivo.readline()
    while linea != '':
        # procesar línea
        linea = archivo.readline()
        finLinea = len(linea)
        var = linea[:largoParam]
        if var == parametro:
            retorno = linea[largoParam+3:finLinea-1]
    return retorno

def getParseHTML(ParamIni, ParamFin, Texto2):
    largoParamIni = len(ParamIni)
    Texto = ""
    Texto = Texto2.getText()
    PosIni = Texto.find(ParamIni)
    if PosIni == -1:
        #Valor no encontrado
        return "-1"
    else:
        PosFin = Texto.find(ParamFin)
        if PosFin == -1:
            #No se encuentra tag fin, XML mal formado
            return "-2"
        else:
            return Texto[PosIni+largoParamIni:PosFin]

def getParseTexto(ParamIni, ParamFin, Texto):
    largoParamIni = len(ParamIni)
    PosIni = Texto.find(ParamIni)
    if PosIni == -1:
        #Valor no encontrado
        return "-1"
    else:
        PosFin = Texto.find(ParamFin)
        if PosFin == -1:
            #No se encuentra tag fin, XML mal formado
            return "-2"
        else:
            return Texto[PosIni+largoParamIni:PosFin]


def ingresarDatosBBDD(var1, var2,var3,var4, var5,var6, var7, var8, var9, var10, var11, var12):
    # Establecemos la conexión con la base de datos
    host = ""
    usuario = ""
    password = ""
    bbdd = ""
    host = getParam("host")
    usuario = getParam("usuario")
    password = getParam("password")
    bbdd = getParam("bbdd")
    bd = MySQLdb.connect(host,usuario,password,bbdd )
    # Preparamos el cursor que nos va a ayudar a realizar las operaciones con la base de datos
    cursor = bd.cursor()
    # Preparamos el query SQL para insertar un registro en la BD
    sql = "INSERT INTO sitio1_agromet (cod_agromet, fecha_agromet, hora_agromet, temperaturaAmbiente, precipitacion, humedadAmbiente, presionAtmosferica, radiacionSolar, velocidadViento, direccionViento, fecha_sys, hora_sys ) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(var1, var2,var3,var4, var5,var6, var7, var8, var9, var10, var11, var12)

    try:
        # Ejecutamos el comando
        cursor.execute(sql)
        escribeLog("Datos ingresados correctamente. Codigo: %s; Fecha Agromet: %s; Hora Agromet: %s" %(var1, var2, var3))
        # Efectuamos los cambios en la base de datos
        bd.commit()
    except:
        escribeLog("ERROR: Ingreso de datos. Codigo: %s; Fecha Agromet: %s; Hora Agromet: %s" %(var1, var2, var3))
        # Si se genero algún error revertamos la operación
        bd.rollback()
    # Nos desconectamos de la base de datos
    bd.close()

def ultimoDatoIngresado(ID):
    # Establecemos la conexión con la base de datos
    host = ""
    usuario = ""
    password = ""
    bbdd = ""
    host = getParam("host")
    usuario = getParam("usuario")
    password = getParam("password")
    bbdd = getParam("bbdd")
    bd = MySQLdb.connect(host,usuario,password,bbdd )
    # Preparamos el cursor que nos va a ayudar a realizar las operaciones con la base de datos
    cursor = bd.cursor()
    # Preparamos el query SQL para insertar un registro en la BD
    sql = "select fecha_agromet, hora_agromet from sitio1_agromet where cod_agromet = '%s' order by id DESC limit 1;" %(ID)

    try:
        # Ejecutamos el comando
        cursor.execute(sql)
        flag_ingreso = 0
        fecha_hora = ""

        for (fecha_agromet, hora_agromet) in cursor:
            flag_ingreso = 1
            fecha_hora = "%s %s" %(fecha_agromet, hora_agromet)

        cursor.close()

        if flag_ingreso == 1:
            return fecha_hora
        else:
            #En caso de que no se encuentre, retorna 0
            return "0"
    except:
        escribeLog("Error en consulta codigo: %s" %(ID))
        return "0"
    bd.close()

def getTag(digitoVerificador, fila):
    texto = getParseTexto("fecha|", "</dato>", fila)
    digito = "|%s|" %(digitoVerificador)
    largoDigito = len(digito)
    posDigito = texto.find(digito)

    if posDigito != -1:
        nuevoTexto = texto[posDigito+largoDigito:]
        posDigito = nuevoTexto.find("|")
        if posDigito != -1:
            valor_retorno = nuevoTexto[:posDigito]
            return valor_retorno
        else:
            valor_retorno = nuevoTexto
            return nuevoTexto
    else:
        return ""

def escribeLog(texto):
    dirLog = getParam("dirLog")
    EjecucionLog = getParam("EjecucionLog")

    if EjecucionLog == "1":
        nomArchivo = "%slogSitio1_%s.log" %(dirLog, time.strftime("%d-%m-%Y"))
        f = open (nomArchivo, "a+")
        f.write("%s:   %s\n" %(time.strftime("%H:%M:%S"), texto))
        f.close()
    else:
        print "%s" %(texto)

#Se compara horas
#retorna 0 en caso de ser iguales
#retorna 1 en caso de que hora1 sea mayor a hora2
#retorna 2 en caso de que hora1 sea menor a hora2
def compararHoras(hora1, hora2):
    #Hora de Web
    horaWeb = hora1.split(":")
    horaOW = horaWeb[0]
    minutosOW = horaWeb[1]
    #Hora de BBDD
    horaBBDD = hora2.split(":")
    horaOBD = horaBBDD[0]
    minutosOBD = horaBBDD[1]

    if hora1 != hora2:
        if horaOW > horaOBD:
            return "1"
        elif horaOW < horaOBD:
            return "2"
        else:
            if minutosOW > minutosOBD:
                return "1"
            elif minutosOW < minutosOBD:
                return "2"
            else:
                return "0"
    else:
        return "0"


