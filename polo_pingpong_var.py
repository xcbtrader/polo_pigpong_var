__author__ = 'xcbtrader'
# -*- coding: utf-8 -*-

import poloniex
import time
import sys

def leer_operativa():
	fOperativa = open('polo_pingpong_var_operativa.txt', 'r')
	op = fOperativa.readline()
	op = int(fOperativa.readline())
	fOperativa.close()
	return op

def leer_ordenes():
	global polo
	try:
		openOrders = polo.returnOpenOrders('USDT_BTC')
		return openOrders
	except KeyboardInterrupt:
		exit()	
	except Exception:
		print('### ERROR AL LEER LAS ORDENES ABIERTAS ###')
		print('### ESPERANDO 30 SEGUNDOS ###')
		time.sleep(30)

def realizar_compra(last,margen, saldoUSDTinv):
	global polo

	precio_compra = last - (last * margen)	
	try:
		make_order_buy = polo.buy('USDT_BTC',precio_compra,saldoUSDTinv/precio_compra)
		print('-------------------------------------------------------')
		print('*** CREADA ORDEN DE COMPRA NUM ' + make_order_buy['orderNumber'] + ' - PRECIO: ' + str(precio_compra) + ' $ - IVERSION: ' + str(saldoUSDTinv) + ' - BTC: ' + str(saldoUSDTinv/precio_compra) + ' ***')
	except KeyboardInterrupt:
		exit()	
	except Exception:
		print('### ERROR AL CREAR ORDEN DE COMPRA ###')
		print('### ESPERANDO 30 SEGUNDOS ###')
		time.sleep(30)	
	
def realizar_venta(last, margen, saldoBTCinv):
	global polo
	
	precio_venta = last + (last * margen)
	try:
		make_order_sell = polo.sell('USDT_BTC', precio_venta, saldoBTCinv)
		print('*** CREADA ORDEN DE VENTA NUM ' + make_order_sell['orderNumber'] + ' - PRECIO: ' + str(precio_venta) + ' $ - IVERSION: ' + str(saldoBTCinv) + ' - USD: ' + str(saldoBTCinv * precio_venta) + ' ***')
		print('-------------------------------------------------------')	
	except KeyboardInterrupt:
		exit()	
	except Exception:
		print('### ERROR AL CREAR ORDEN DE VENTA ###')
		print('### ESPERANDO 30 SEGUNDOS ###')
		time.sleep(30)
			
def realizar_ordenes(margen, saldoUSDT, saldoUSDTinv, saldoBTC, saldoBTCinv):
	global polo

	try:
		ticker = polo.returnTicker()
		t = ticker['USDT_BTC']
		last = float(t['last'])
		
		if last > 100:
			realizar_compra(last,margen, saldoUSDTinv)
			time.sleep(15)
			realizar_venta(last, margen, saldoBTCinv)
			print('### ORDENES REALIZADAS CORRECTAMENTE - ESPERANDO 5 MINUTOS ###')
			time.sleep(300)
		else:
			print('### ERROR AL LEER VALOR ACTUAL btc ###')
			print('### ESPERANDO 30 SEGUNDOS ###')
			time.sleep(30)	
	except KeyboardInterrupt:
		exit()	
	except Exception:
		print('### ERROR AL LEER VALOR ACTUAL btc ###')
		print('### ESPERANDO 30 SEGUNDOS ###')
		time.sleep(30)	

def leer_balance():
	global polo

	err = True
	while err:
		try:
			balance = polo.returnBalances()
			saldoUSDT = float(balance['USDT'])
			saldoBTC = float(balance['BTC'])
			return saldoUSDT, saldoBTC
		except KeyboardInterrupt:
			exit()	
		except Exception:
			print('### ERROR AL LEER SALDOS DE LA CUENTA ###')
			print('### ESPERANDO 30 SEGUNDOS ###')
			time.sleep(30)	
		
def crear_ordenes(margen):
	
	saldoUSDT, saldoBTC = leer_balance()
	saldoUSDTinv = saldoUSDT/2
	saldoBTCinv = saldoBTC/2
		
	if saldoBTC < 0.0005 or saldoUSDT < 1:
		print('### ERROR SALDO INSUFICIENTE PARA REALIZAR ORDEN ###')
		print('### ESPERANDO NUEVO SALDO ###')
		time.sleep(300)
	else:
		realizar_ordenes(margen, saldoUSDT, saldoUSDTinv, saldoBTC, saldoBTCinv)	

# PROGRAMA PRINCIPAL ##################################################################
global polo

print('')
print('**************************************************************')
print('   INICIANDO BOT POLONIEX PingPong VARIABLE')
print('**************************************************************')
print('')

API_key = 'AQUI PONER NUESTRA API key'
Secret = 'AQUI PONER EL SECRET DE NUESTRA API key'

err = True
while err:
	try:
		polo = poloniex.Poloniex(API_key,Secret)
		err = False
		print('### CONECTADO CORRECTAMENTE A LA API DE POLONIEX ###')
	except KeyboardInterrupt:
		exit()
	except Exception:
		print('### ERROR AL CONECTAR CON API POLONEX ###')
		print('### ESPERANDO 30 SEGUNDOS ###')
		time.sleep(30)
		

tot_buy = 0
tot_sell= 0

margen = 0.0
while margen <0.5:
	m = str(input('Entra margen de beneficio (>=0.5) :? '))
	margen = float(m.replace(',','.'))

margen = margen/100
n = 1

while True:
	
	openOrders = leer_ordenes()
	nOrdenes = len(openOrders)
	
	operativa = leer_operativa()
	
	if operativa == 1 or operativa == 2:
		if nOrdenes == 0 : #Escenario sin inversion. Poner 2 ordenes
			crear_ordenes(margen)
			
		elif nOrdenes == 1: 	#Escenario Con una orden cerrada y una orden abierta. Hay que cerrarla si hay suficiente saldo para nueva inversion
			
			for no in openOrders:
				num_orden_cerrar = no['orderNumber']
				tipo_orden_cerrar = no['type']
			try:
				if tipo_orden_cerrar == 'sell':
					tot_buy +=1
				elif tipo_orden_cerrar == 'buy':
					tot_sell +=1
				
				saldoUSDT, saldoBTC = leer_balance()
			
				if saldoBTC < 0.0005 or saldoUSDT < 1:
					print('### ERROR SALDO INSUFICIENTE PARA CANCELAR ORDEN ###')
					print('### ESPERANDO QUE SE CIERRE ORDEN PENDIENTE ###')
					time.sleep(300)
				else:
					cancelar_orden = polo.cancelOrder(num_orden_cerrar)
					print('### CANCELADA ORDEN: ' + str(num_orden_cerrar))
					print('### ESPERANDO 2 MINUTOS PARA CONTINUAR ###')
					time.sleep(120)
			except KeyboardInterrupt:
				exit()	
			except Exception:
				print('### ERROR AL CANCELAR ORDEN ###')
				print('### ESPERANDO 30 SEGUNDOS ###')
				time.sleep(30)
				
		elif nOrdenes == 2: # Escenario con toda la inversion aun abierta. No hacer nada
			ticker = polo.returnTicker()
			t = ticker['USDT_BTC']
			last = float(t['last'])
			print('-------------------------------------------------------')
			print(str(n) + ') Buy Ord: ' + str(tot_buy) + ' - Sell Ord: ' + str(tot_sell) + ' - btc = ' + str(last) + ' $')
			n +=1
			for orde in openOrders:
				print(orde['type'] + ' - ' + orde['date'] + ' - ' + orde['rate'] + ' $ - ' + orde['amount'] + ' btc')
			print('-------------------------------------------------------')
			print('### ESPERANDO 5 MINUTOS PARA CONTINUAR ###')
			time.sleep(300)
		elif nOrdenes > 2: # Escenario ERROR demasiadas ordenes abiertas
			print('### ERROR - DEMASIADAS ORDENES ABIERTAS - Max 2 ORDENES. Act. ' + str(nOrdenes) + ' ABIERTAS ###')
			print('### ESPERANDO A QUE SE CIERREN ###')
			time.sleep(300)		


	else:
		print ('### PROCESO CANCELADO ###')
		exit()
	if operativa == 2:
		print ('### PROCESO FINALIZADO ###')
		exit()		
