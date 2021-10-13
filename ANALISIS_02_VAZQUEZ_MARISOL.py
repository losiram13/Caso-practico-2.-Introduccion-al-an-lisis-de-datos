# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# Cargar paquete
import csv

# Asignar una lista vacia para guardar los datos
lista_datos=[]

#Abrir el archivo csv
with open("synergy_logistics_database.csv","r") as archivo:
#Asignar variable del archivo
    lector=csv.DictReader(archivo)  
    for registro in lector: 
        lista_datos.append(registro)       

    
#Opción 1) Rutas de importación y exportación
#creacción de función para conteo de importaciones-exportaciones por ruta
def rutas_exp_import(direccion):
    #conteo de veces que se exporta o importa en una ruta
    contador=0
    #lista de rutas existentes
    rutas_registradas=[]
    #lista de rutas con conteo. 
    conteo_exp_imp_por_ruta=[]
    
    for ruta in lista_datos: #iteración por cada elemento en la lista
        if ruta["direction"] == direccion: #se evalua si pertenece a exportación o importación
            ruta_actual=[ruta["origin"],ruta["destination"]] #asignas tu ruta actual
            
            if ruta_actual not in rutas_registradas: #si no esta registrada esa ruta se prosigue 
                for ruta_bd in lista_datos: #iteración para contar las veces que se utilizó dicha ruta
                    if ruta_actual==[ruta_bd["origin"],ruta_bd["destination"]]:
                        contador+=1
                rutas_registradas.append(ruta_actual) #registro de la ruta
                conteo_exp_imp_por_ruta.append([ruta["origin"],ruta["destination"],contador]) #creación de la nueva tabla
                contador=0 #reinicio contador
    conteo_exp_imp_por_ruta.sort(reverse=True, key=lambda x:x[2]) #ordena la lista de mayor-menor importaciones-exportaciones
    return conteo_exp_imp_por_ruta #regresa la tabla de conteos ordenados

exportaciones_por_ruta=rutas_exp_import("Exports") #correr la función para exportaciones
#imprimir solo las 10 rutas con mayores exportaciones
print("Las 10 rutas [origen=exportador, destino=importador] con mayores exportaciones son: ")
for i in range(0,10):
    print(exportaciones_por_ruta[i])
    
importaciones_por_ruta=rutas_exp_import("Imports") #correr la función para importaciones
#imprimir solo las 10 rutas con mayores importaciones
print("Las 10 rutas [origen=importador, destino=exportador] con mayores importaciones son: ")
for i in range(0,10):
    print(importaciones_por_ruta[i])
 
    
#Inicio del código para opción 2
#Opción 2) Medios de transporte utilizado
def mod_transporte(direccion): #Definir función
    
#Asigna las avriables que se utilizaran después:
    valor=0 #contador para valor total
    transportes_registrados=[] #lista de medios de transporte
    transporte_valor=[] #lista de medios de transporte con dirección y valor total

#iteración sobre lista para elegir solo los que tengan la dirección indicada
    for registro in lista_datos:
        if registro["direction"]==direccion: 
            transporte_actual=[registro["direction"],registro["transport_mode"]] #Modo de transporte a iterar
            
            if transporte_actual not in transportes_registrados: #solo se registran modos de transporte que no se hayan registrado
                for registro_bd in lista_datos: #iteración por cada línea de código 
                       if transporte_actual==[registro_bd["direction"],registro_bd["transport_mode"]]: #sólo se hace el conteo de valor si pertenece al mismo modo de transporte
                           valor+=int(registro_bd["total_value"]) #suma del valor por modo de transporte
                transportes_registrados.append(transporte_actual)  #agregar el modo de transporte 
                transporte_valor.append([registro["direction"],registro["transport_mode"],valor]) #agrega la dirección, el modo de transporte y el valor
                valor=0  #se reinicia el contador
    
    transporte_valor.sort(reverse=True, key=lambda x:x[2]) #ordena la lista de mayores a menores valores por modo de transporte 
    return transporte_valor  #regresa la tabla


modo_transp_exp=mod_transporte("Exports") #Se corre la función para exportaciones
#imprime los 3 modos de transporte con más valor de exportaciones
print("Los tres modos de transporte más importantes de acuerdo con el valor total de exportaciones son: ")
for j in range(0,3):
 print(modo_transp_exp[j])
 
#imprime el modo de transporte con menor valor en exportaciones
print("El modo de transporte con menor valor en exportaciones y que se podría reducir es: "  )
print(modo_transp_exp[-1] )

modo_transp_imp=mod_transporte("Imports") #Se corre la función para importaciones
#imprime los 3 modos de transporte con más valor de importaciones
print("Los tres modos de transporte más importantes de acuerdo con el valor total de importaciones son: ")
for j in range(0,3):
 print(modo_transp_imp[j])
 
 #imprime el modo de transporte con menor valor en importaciones
print("El modo de transporte con menor valor en importaciones y que se podría reducir es: "  )
print(modo_transp_imp[-1] )


#Inicio del código para opción 3
#Opción 3) Valor total de importaciones y exportaciones (80% de ellas)

def valor_pais_exp_imp(direccion): #Definir función
    #Asignar las variables y listas a utilizar
    valor_pais=0 #variable para asignar el valor de importación-exportación por país
    no_movimiento=0 #variable para asignar el número de exp.-imp. por país
    paises_contados=[]  #lista de países
    valor_total_paises=[] #lista de países con el valor de exp.-impor.
   
    for linea in lista_datos: #iteración por cada línea de la tabla
        pais_actual=[direccion,linea["origin"]]  #asignar el país y dirección a contar
        if pais_actual in paises_contados: #evalua si ya se registro dicho pais de ser así continua.
            continue
        
        for movimiento in lista_datos: #iteración para calcular el valor por país
            if pais_actual==[movimiento["direction"],movimiento["origin"]]: #verifica si es el mismo país y dirección para sumar
                valor_pais+=int(movimiento["total_value"]) #suma el valor de impor.-export.
                no_movimiento+=1 #suma el numero de import.-export.
                
        paises_contados.append(pais_actual) #lista de paises contados
        valor_total_paises.append([direccion,linea["origin"],no_movimiento,valor_pais]) #agrega el pais,#de import.-export., valor de dichas import.-export.
        valor_pais=0 #reinicia el contador para el siguiente país
        no_movimiento=0 #reinicia el contador para el siguiente país
    
    valor_total_paises.sort(reverse=True,key=lambda x:x[3]) # ordena tabla de países de mayor-menor valor de importaciones-exportaciones
    return valor_total_paises # regresa el valor de la función

#print(valores_paises)

#crea la función para elegir los países que aporten el % deseado
def porcentajes_pais(direccion,porcentaje=0.8):
    
    #asignar variables y listas
    valores_paises=valor_pais_exp_imp(direccion) #carga la función que ordena países de menor a mayor valor
    valor_total=0 # variable para sumar el valor total de todas las import.-export.
    
    #ciclo para contar el valor total de todas las import.-export.  
    for pais in valores_paises:
        valor_total+=int(pais[3]) #suma el valor por cada país
    #print(valor_total)
   
    #asigna las variables y valores 
    valor_pais=0 #variable para sumar el valor de cada país
    porcentaje_pais=0 #variable para calcular el % de aportacion de cada país
    porcentaje_actual=0 #variable para sumar porcentaje de países
    porcentajes_calculados=[] #lista de porcentajes por país
    porcentajes=[] #lista de porcentajes
    
    #ciclo para sumar porcentaje de cada país
    for pais in valores_paises:  
        valor_pais=int(pais[3]) #asigna el valor de cada país
        porcentaje_pais=round(valor_pais/valor_total,3) #saca el % del país
        #print(porcentaje_pais)
        porcentaje_actual+=round(porcentaje_pais,3) #suma el de los países registrados
        porcentajes.append(porcentaje_actual) #agrega el porcentaje de la suma actual
        #agrega a la tabla la dirección, el país de origen, el # de importaciones-esportaciones, el valor total por país, % del país, suma del %
        porcentajes_calculados.append([pais[0],pais[1],pais[2],pais[3],porcentaje_pais,porcentaje_actual])
        
        #función condicional para que solo asigne los países que generen el % solicitado
        if porcentaje_actual<=porcentaje:
            continue
        else:
            if porcentaje_actual-porcentaje>=porcentajes[-2]-porcentaje:
                break
            else:
                porcentajes_calculados.pop(-1)
                break
    return porcentajes_calculados # regresa la tabla de países

print("Los países que aportan el 80% del valor de las exportaciones son: \n [Exports,origen,# Movimientos, valor total,% de aportación por país, %acumulado]")       
porcentaje_paises=porcentajes_pais("Exports",0.8) #corre la función  
print(porcentaje_paises) #imprime las exportaciónes que aportan el %


print("Los países que aportan el 80% del valor de las importaciones son: \n [Imports,origen(país que importa),# Movimientos, valor total,% de aportación por país, %acumulado]")       
porcentaje_paises=porcentajes_pais("Imports",0.8)  #corre la función     
print(porcentaje_paises) #imprime las importaciónes que aportan el %
