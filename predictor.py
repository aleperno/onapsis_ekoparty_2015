#!/usr/bin python
# -*- coding: utf-8 -*-
class LfsrPredictor():

	def __init__(self, code_list=None, config=None):
		self.code_list = code_list
		self.config = config
		self.seed = None

	def _can_predict(self):
		if self.config is None:
			return False
		else:
			return True

	def _coord_to_bin(self,code):
		"""
		Coordenadas a binario, recibe las 4 coordenadas y las 
		expresa en binario. 
		Rango de las coordenadas 0..3 > 2 bits.
		"""
		binary = ""
		for num in code:
			binary += '{0:02b}'.format(int(num))
		assert ( len(binary) == 16 )
		return binary
	
	def _bin_to_coord(self,binary):
		res = ""
		for i in xrange(0,16,2):
			bin_num = binary[i:i+2]
			num = int(bin_num,2)
			res += str(num)
		return res
	
	def _config_generator(self):
		#16 bits
		MAX = (2**16)
		res = []
		for i in xrange(MAX):
			conf = '{0:016b}'.format(i)
			assert ( len(conf) == 16 )
			res.append(conf)
		return res
	
	def _lfsr(self,code,config):
		binary = self._coord_to_bin(code)
		assert len(binary) == 16
		assert len(config) == 16
		for loop in xrange(16):
			#Requiero 16 loops para cambiar todo el binario	
			xor = 0
			for i in xrange(0,16,1):
				if (config[i]=="1"):
					bit = int(binary[i])
					if xor == bit:
						xor = 0
					else:
						xor = 1
	
			binary = binary[1:] + str(xor)
		return self._bin_to_coord(binary)
	
	def predict_conf(self):
		possibles = self._config_generator()
		for i in xrange(len(self.code_list)-1):
			"""
			Tengo X-1 datos para comparar (uno lo uso como seed)
			"""
			hits = []
			seed = self.code_list[i]
			next_code = self.code_list[i+1]
			for conf in possibles:
				prediction = self._lfsr(seed,conf)
				if prediction == next_code:
					#print "Una configuracion posible es %s" % conf
					hits.append(conf)
			#print "Fin del test %d, hay %d configuraciones posibles" % (i+1,len(hits))
			possibles = hits
		if len(possibles) == 1:
			#Es determinista, solo puede haber una configuracion
			print "Prediccion exitosa"
			self.config = possibles[0]
			return True
		else:
			print "Prediccion no exitosa"
			return False

	def set_seed(self,seed):
		self.seed = seed

	def next(self,seed=None):
		if not self.config:
			print "No hay configuracion con cual predecir"
			return
		if not seed and not self.seed:
			print "No hay semilla con la cual predecir"
			return
		next_cheat = self._lfsr(self.seed,self.config)
		self.seed = next_cheat
		return next_cheat 


"""
Obtenidos de los .wav
"""
code1 = "22231100"
code2 = "02131111"
code3 = "13300330"
code4 = "01212233"
code5 = "11331200"

CODES = [code1,code2,code3,code4,code5]

predictor = LfsrPredictor(code_list=CODES)
predictor.predict_conf()
predictor.set_seed(code1)

print "Press enter to continue or CTRL-C to exit"
cont = True
print code1
while cont:
	try:
		raw_input()
		print predictor.next()
	except KeyboardInterrupt:
		cont = False
		print ""
