import sys

if len(sys.argv) >= 9:
		if sys.argv[1] != "-ficheroContextInput" and sys.argv[1] != "-fci":
			print "El primer parametro debe ser -ficheroContextInput (o -fci) seguido del path al fichero de contexto."
			sys.exit(0)
		else:
			ficheroContextInput = sys.argv[2]
			if sys.argv[3] != "-variant" and sys.argv[3] != "-v":
				print "El segundo parametro debe ser -variant (o -v) seguido del path al fichero de variantes."
				sys.exit(0)
			else:
				ficheroVariant = sys.argv[4]
				if sys.argv[5] != "-domains" and sys.argv[5] != "-d":
					print "El tercer parametro debe ser -domains (o -d) seguido del path al fichero de dominios."
					sys.exit(0)
				else:
					ficheroDomains = sys.argv[6]
					if sys.argv[7] != "-ficheroContextOutput" and sys.argv[7] != "-fco":
						print "El cuarto parametro debe ser -ficheroContextOutput (o -fco) seguido del path en el que se guardaran los resultados."
						sys.exit(0)
					else:
						ficheroContextOutput = sys.argv[8]


else:
    print "Este programa necesita los parametros -ficheroContextInput -variant -domains -ficheroContextOutput, en ese orden. Se recomienda tener cuidado con los permisos de acceso a carpetas"
    sys.exit(0)




with open(ficheroContextInput) as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip('\n') for x in content] 
#print content[0] + '\n' + content[1]

with open(ficheroVariant) as f:
    variant = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
variant = [x.strip('\n') for x in variant] 
#print content[0] + '\n' + content[1]

variants = {}
for x in variant:
	variants[str(x.split('\t')[2].split('-')[2]+x.split('\t')[2].split('-')[3])] = (x.split('\t')[0])


with open(ficheroDomains) as f:
    domains = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
domains = [x.strip('\n') for x in domains]

dominios = {}
for x in domains:
	dominios[str(x.split('\t')[1].split('-')[2] +'-'+ x.split('\t')[2])] = x.split('\t')[0]


file = open(ficheroContextOutput,"w")
num = len(content)
n = 0
for y in content:
	#print "Progreso: "+str(n)+" de "+str(num)+", Faltan " + str(num - n)
	n +=1
	if "ctx" in y: 
		objetivo =  y.split('(')[0].split('_')[1]
		try:
			y = y +"#"+ dominios[str(objetivo)]
		except:
			y = y
	elif(not("ctx" in y) and ("#" in y)):
		y = y.replace(y.split('#')[0], variants[str(y.split('#')[0].split('-')[0]+y.split('#')[0].split('-')[1])])
	file.write(y+"\n")
file.close()