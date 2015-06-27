#! /usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import socket
import sys
import time
import datetime
import serial
import logging
#logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-4s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'communications.log')
#logging.basicConfig(format = u'# %(levelname)-4s [%(asctime)s] %(message)s', level = logging.DEBUG)
logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-4s [%(asctime)s] %(message)s', level = logging.DEBUG)


from utils import chSim, udate
from CRC import CRC_M230


	
class DirectChannel(object):
	
	def __init__(self, port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1, writeTimeout=1, ser = serial.Serial(),\
				 whTimeout = 0.1, attempt = 3, whType=0):
		"""
		Открывает прямой канал (как правило по протоколу RS-485) до счетчика.
		whType:
			0 - Меркурий 230
		"""
		self.port = port
		self.ser = ser
		self.ser.port = port
		self.ser.baudrate = baudrate
		self.ser.bytesize = bytesize
		self.ser.parity = parity
		self.ser.stopbits = stopbits
		self.ser.timeout = timeout
		self.ser.writeTimeout = writeTimeout
		self.whTimeout = whTimeout
		self.attempt = attempt
		
		typeCRC = {
			0: CRC_M230(True),
		}
		self.CRC = typeCRC[whType]
		"""
		"""
	
		try:
			self.ser.open()
		except Exception:
			logging.error(u'Не удалось открыть порт: ' + self.port)
		else:
			logging.debug(u'Инициализация порта: ' + self.port)
	
	def TXRX(self, cmd):
		answer = []
		ansHex = []
		ansChr=''
		attempts = self.attempt
		timeO=0
		while attempts>0:
			cmdTX = self.TX(cmd + self.CRC.calculate(cmd))
			logging.debug(u'TX >>> %s [%s]' % (" ".join(cmdTX[0]),  str(cmdTX[1])))
			while timeO < self.whTimeout:
				time.sleep(0.1)
				ansChr += self.RX()
				ansHex += [chSim(hex(ord(x))[2:]) for x in ansChr]
				
				if self.CRC.check(ansChr):
					timeO = self.whTimeout
					cmdRX = [ansHex, len(ansHex)]
					logging.debug(u'RX <<< %s [%s]' % (" ".join(cmdRX[0]), str(cmdRX[1])))
				else:
					timeO += 0.1
			if self.CRC.check(ansChr):
				attempts = 0
				answer = ansHex
			else:
				attempts -= 1
				timeO = 0
				answer = u'Нет ответа от устройства!'
				logging.error(answer)
		return answer
	
	def TX(self, cmd):
		"""
			Метод предназначен для отправки данных в порт
			Принимает в качестве параметров команду
			Возвращает список:
			cmdTX[0] - список, отправленная команда в 16-м представлении
			cmdTX[1] - количество отправленных байт
		"""
		self.ser.write(cmd)
		cmdsend = [chSim(hex(ord(x))[2:]) for x in cmd]
		cmdTX = [cmdsend, len(cmdsend)]
		return cmdTX
		
	def RX(self):	
		return self.ser.read(self.ser.inWaiting())
		
	def terminate(self):
		try:
			self.ser.close()
			logging.debug(u'Порт закрыт: %s' % self.port)
		except:
			logging.error(u'Не удалось закрыть порт: ' + self.port)
	

class GSMChannel(object):
	
	def __init__(self, port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1, writeTimeout=1, ser = serial.Serial(),\
				 whTimeout = 5, attempt = 3, whType=0, phone_number='', call_attempt=3):
		"""
		Открывает прямой канал (как правило по протоколу RS-485) до счетчика.
		whType:
			0 - Меркурий 230
		"""
		self.port = port
		self.ser = ser
		self.ser.port = port
		self.ser.baudrate = baudrate
		self.ser.bytesize = bytesize
		self.ser.parity = parity
		self.ser.stopbits = stopbits
		self.ser.timeout = timeout
		self.ser.writeTimeout = writeTimeout
		self.whTimeout = whTimeout
		self.attempt = attempt
		self.phone_number = phone_number
		self.call_attempt = call_attempt
		
		typeCRC = {
			0: CRC_M230(True),
		}
		self.CRC = typeCRC[whType]
		"""
		"""
	
		try:
			self.ser.open()
		except Exception:
			logging.error(u'Не удалось открыть порт модема: ' + self.port)
		else:
			logging.debug(u'Инициализация порта модема: ' + self.port)
			
		try:
			self.call(self.phone_number, self.call_attempt)
		except Exception:
			logging.error(u'Не удалось установить соединение, завершаем работу скрипта!')
			self.terminate()
		
		
	def call(self, phone_number = '', call_attempt = 3):
		callCmd = 'ATD'+phone_number+'\r'
		
		while call_attempt>0:
			logging.debug(u'Звоним на номер: ' + phone_number)
			callAns = self.modemTXRX(callCmd, 15)
			if 'CONNECT 9600' in callAns[1]:
				logging.debug(u'Соединение с модемом установлено')
				call_attempt = 0
				return True
			elif 'NO CARRIER' in callAns[1]:
				logging.error(u'Соединение с модемом не установлено')
				call_attempt -= 1
	
	def terminate(self):
		self.modemTXRX('+++', 1)
		time.sleep(0.5)
		self.modemTXRX('ATH\r', 1)
		return True
	
	def modemTXRX(self, cmd, modemTimeout=5):
		
		ansHex = []
		answer = []
		ansChr=''
		cmdTX = self.modemTX(cmd)
		logging.debug(u'TX >>> ' + " ".join(cmdTX[0]) + ' <<<>>> ' + cmdTX[1] + ' [' + str(cmdTX[2]) +'] ')
		time.sleep(modemTimeout)
		ansChr += self.modemRX()
		ansHex += [chSim(hex(ord(x))[2:]) for x in ansChr]
		cmdRX = [ansHex, ansChr, len(ansHex)]
		logging.debug(u'RX <<< ' + " ".join(cmdRX[0]) + ' <<<>>> ' + cmdRX[1] + ' [' + str(cmdRX[2]) +'] ')
		answer = [ansHex, ansChr]

		return answer
	
	def modemTX(self, cmd):
		"""
			Метод предназначен для отправки данных в порт
			Принимает в качестве параметров команду
			Возвращает список:
			cmdTX[0] - список, отправленная команда в 16-м представлении
			cmdTX[1] - количество отправленных байт
		"""
		self.ser.write(cmd)
		cmdsend = [chSim(hex(ord(x))[2:]) for x in cmd]
		cmdTX = [cmdsend, cmd, len(cmdsend)]
		return cmdTX
		
	def modemRX(self):		
		return self.ser.read(self.ser.inWaiting())
		
	
	def TXRX(self, cmd, byteExpected=0):
		answer = []
		ansHex = []
		answer = []
		ansChr=''
		timeO=0
		attempts = self.attempt
		while attempts>0:
			cmdTX = self.TX(cmd + self.CRC.calculate(cmd))
			logging.debug(u'TX >>> ' + " ".join(cmdTX[0]) + ' [' + str(cmdTX[1]) +'] ')
		
			
			while timeO < self.whTimeout:
				time.sleep(0.1)
				ansChr += self.RX()
				ansHex += [chSim(hex(ord(x))[2:]) for x in ansChr]
				
				if self.CRC.check(ansChr):
					timeO = self.whTimeout
					cmdRX = [ansHex, len(ansHex)]
					logging.debug(u'RX <<< ' + " ".join(cmdRX[0]) + ' [' + str(cmdRX[1]) +'] ')
				
				else:
					timeO += 0.1
			if self.CRC.check(ansChr):
				attempts = 0
				answer = ansHex
			else:
				attempts -= 1
				timeO = 0
				answer = u'Нет ответа от устройства!'
				logging.error(answer)
		return answer
	
	
	
	def TX(self, cmd):
		"""
			Метод предназначен для отправки данных в порт
			Принимает в качестве параметров команду
			Возвращает список:
			cmdTX[0] - список, отправленная команда в 16-м представлении
			cmdTX[1] - количество отправленных байт
		"""
		self.ser.write(cmd)
		cmdsend = [chSim(hex(ord(x))[2:]) for x in cmd]
		cmdTX = [cmdsend, len(cmdsend)]
		return cmdTX
		
	def RX(self):	   
		return self.ser.read(self.ser.inWaiting())
	
	
class TCPChannel(object):
	
	def __init__(self, address, port, whTimeout = 5, attempt = 3, whType=0, connect_attempt=3):
		"""
		Открывает канал TCP до счетчика.
		whType:
			0 - Меркурий 230
		"""
		
		self.address = address
		self.port = port
		self.whTimeout = whTimeout
		self.attempt = attempt
		self.connect_attempt = connect_attempt
		
		typeCRC = {0: CRC_M230(True),}
		self.CRC = typeCRC[whType]
		
			
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error, e:
			logging.error(u'Не удалось создать сокет! %s' % e)
			self.terminate()
		
		try:
			self.connect(self.address, self.port, self.connect_attempt)
		except socket.error, msg:
			logging.error(u'Не удалось подключиться к хосту %s:%s. Причина: %s' % (self.address, self.port, e))
			sys.exit()
		else:
			logging.debug(u'Соединение установлено!')
		
				
	def connect(self, address, port, connect_attempt):
		
		while connect_attempt>0:
			logging.debug(u'Устанавливаем соединение: %s:%s' % (address, port))
			try:
				connection = self.sock.connect((address, port))
				connect_attempt = 0
				return True
			except socket.error, e:
				connect_attempt -= 1
				logging.error(u'Соединение не установлено. Причина: ' % e)


	
	def terminate(self):
		try:
			self.sock.close()
			logging.debug(u'Разрываем соединение: %s:%s' % (self.address, self.port))
			return True
		except socket.error, e:
			logging.error(u'Соединение не разорвано. Причина: ' % e)
			return False
	
	  
	
	def TXRX(self, cmd, byteExpected=0):
		answer = []
		ansHex = []
		answer = []
		ansChr=''
		timeO=0
		attempts = self.attempt
		while attempts>0:
			cmdTX = self.TX(cmd + self.CRC.calculate(cmd))
			logging.debug(u'TX >>> ' + " ".join(cmdTX[0]) + ' [' + str(cmdTX[1]) +'] ')
			
			ansChr += self.RX()
			ansHex += [chSim(hex(ord(x))[2:]) for x in ansChr]
				
			
			
			""""
			while timeO < self.whTimeout:
				print timeO
				time.sleep(0.1)
				ansChr += self.RX()
				ansHex += [chSim(hex(ord(x))[2:]) for x in ansChr]
				
				if self.CRC.check(ansChr):
					timeO = self.whTimeout
					cmdRX = [ansHex, len(ansHex)]
					logging.debug(u'RX <<< ' + " ".join(cmdRX[0]) + ' [' + str(cmdRX[1]) +'] ')
				
				else:
					timeO += 0.1
			"""
			if self.CRC.check(ansChr):
				attempts = 0
				answer = ansHex
				#######
				cmdRX = [ansHex, len(ansHex)]
				logging.debug(u'RX <<< ' + " ".join(cmdRX[0]) + ' [' + str(cmdRX[1]) +'] ')
				#######
			else:
				attempts -= 1
				timeO = 0
				answer = False
				if attempts>0:
					logging.error(u'Осталось попыток запроса: %d' % attempts)
				else:
					logging.error(u'Количество попыток запроса исчерпано!')
		return answer
	
	
	
	def TX(self, cmd):
		"""
			Метод предназначен для отправки данных в порт
			Принимает в качестве параметров команду
			Возвращает список:
			cmdTX[0] - список, отправленная команда в 16-м представлении
			cmdTX[1] - количество отправленных байт
		"""
		totalsent = 0
		while totalsent < len(cmd):
			#print len(cmd)
			sent = self.sock.send(cmd[totalsent:])
			if sent == 0:
				raise RuntimeError("socket connection broken")
			totalsent = totalsent + sent
		cmdsend = [chSim(hex(ord(x))[2:]) for x in cmd]
		cmdTX = [cmdsend, len(cmdsend)]
		return cmdTX
	
		"""
		try:
			self.sock.send(cmd)
		except socket.error, msg:
			logging.error(u'Ошибка отправки данных: %s. Причина: %s' % (cmd, msg))			  
		cmdsend = [chSim(hex(ord(x))[2:]) for x in cmd]
		cmdTX = [cmdsend, len(cmdsend)]
		return cmdTX
		"""
		
	def RX(self):
		chunk = ''
		try:
			self.sock.settimeout(self.whTimeout)
			chunk = self.sock.recv(1024)
			self.sock.settimeout(None)
		except socket.error, e:
			logging.error(u'Нет ответа на запрос! Причина: %s' % e)
		"""
		chunks = ''
		bytes_recd = 0
		MSGLEN = 4
		while bytes_recd < MSGLEN:
			chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
			if chunk == '':
				raise RuntimeError("socket connection broken")
			chunks += chunk
			bytes_recd = bytes_recd + len(chunk)
		"""
		return chunk

