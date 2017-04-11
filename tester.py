from gensim import utils
from gensim.models import doc2vec
from collections import namedtuple
from gensim.models import Doc2Vec
import numpy,sys

check = False
verbose = False
factotum = False

if len(sys.argv) >= 7:
		if sys.argv[1] != "-ficheroProcesadoTest" and sys.argv[1] != "-fpt":
			print "El primer parametro debe ser -ficheroProcesadoTest (o -fpt) seguido del path al fichero."
			sys.exit(0)
		else:
			ficheroProcesadoTest = sys.argv[2]
			if sys.argv[3] != "-dominio" and sys.argv[3] != "-d":
				print "El segundo parametro debe ser -dominio (o -d) seguido del path al fichero de dominios."
				sys.exit(0)
			else:
				dominio = sys.argv[4]
				if sys.argv[5] != "-modelo" and sys.argv[5] != "-m":
					print "El tercer parametro debe ser -modelo (o -m) seguido del path al fichero de modelo."
					sys.exit(0)
				else:
					modelo = sys.argv[6]
					i=7
					while i < len(sys.argv):
						if sys.argv[i] == "-check" or sys.argv[i] == "-c":
							check = True
						if sys.argv[i] == "-verbose" or sys.argv[i] == "-v":
							verbose = True
						if sys.argv[i] == "-factotum" or sys.argv[i] == "-f":
							factotum = True
						i += 1


else:
    print "Este programa necesita los parametros -ficheroProcesadoTest -dominio -modelo, en ese orden. Ademas se podran anadir -verbose, -factotum y -check. Se recomienda tener cuidado con los permisos de acceso a carpetas"
    sys.exit(0)

def checkDomain(dom1, dom2):

	for x in domains:
		if (x.split('\t')[0] == dom1 and x.split('\t')[1] == dom2) or dom1 == dom2:
			return True
		elif x.split('\t')[0] == dom1:
			if checkDomain(x.split('\t')[1], dom2):
				return True
	return False


with open(dominio) as f:
    domains = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
domains = [x.strip('\n') for x in domains]

with open(ficheroProcesadoTest) as f:
    test = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
test = [x.strip('\n') for x in test] 


clasified = []

for x in test:
	listapalabras = []
	if "(" in x:
		try:
			tema = x.split("#")[4]
		except:
			tema = 'UNKNOWN'
	elif len(x) > 0 and not("(" in x):
		for y in x.split(" "):
			listapalabras.append(unicode(y.split("#")[0]))
		if not((tema == "factotum" or tema == "UNKNOWN") and factotum == False): 
			clasified.append([unicode(tema), listapalabras])
model = Doc2Vec.load(modelo)

lista = []

for x in clasified:
	words = x[1]
	finished = False
	while not(finished) and len(words) > 0 :
		try:
			esperado = x[0]
			if (model.docvecs.most_similar(model[words])[0][0]) != None:
				estimacion = (model.docvecs.most_similar(model[words]))
			finished = True
		except Exception, e:
			words.remove(str(str(e).split('\' not in vocabulary')[0]).split("u\"word '")[1])
	#if estimacion != None and esperado != None:
	lista.append((esperado.upper(),estimacion))

total = len(lista)
acertados = 0
fallados = 0

for x in lista:
	res = False
	if verbose:
		print "* "+x[0]+" *"
	if check:
		for est in x[1]:
			if (res or checkDomain(x[0], est[0])):
				if checkDomain(x[0], est[0]):
					res = True
					if verbose:
						print '\033[1m' + est[0] + " , " + str(est[1])
				else:
					if verbose:
						print '\033[0m' + est[0]  + " , " + str(est[1])
			else:
				if verbose:
					print '\033[0m' + est[0] + " , " + str(est[1])
	else:
		if (res or checkDomain(x[0], x[1][0][0])):
			res = True
	if res:
		acertados += 1
	else:
		fallados += 1
	if verbose:	
		print "---------------------------"
		
print "Resultados del programa de clasificacion"
print "--------------------------------"
print "Acertados: " + str(acertados)
print "Fallados: " + str(fallados)
print "Total: " + str(acertados + fallados)
print "--------------------------------"
print "Porcentaje acertados: " + str(acertados * 100.0 / total) + "%"
print "Porcentaje fallados: " + str(fallados * 100.0 / total) + "%"


