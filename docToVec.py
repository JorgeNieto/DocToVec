from gensim import utils
from gensim.models import doc2vec
from collections import namedtuple
from gensim.models import Doc2Vec

# numpy
import numpy, sys

factotum = True
min_count = 10
window = 5
size = 200
negative = 5
workers = 8
epoch = 5

if len(sys.argv) >= 5:
			if sys.argv[1] != "-ficheroProcesadoTrain" and sys.argv[1] != "-fpt":
				print "El primer parametro debe ser -ficheroProcesadoTrain (o -fpt) seguido del path al fichero de train procesado."
				sys.exit(0)
			else:
				ficheroProcesadoTrain = sys.argv[2]
				if sys.argv[len(sys.argv)-2] != "-modeloOutput" and sys.argv[len(sys.argv)-2] != "-mo":
					print "El ultimo parametro debe ser -modeloOutput (o -mo) seguido del path en el que se guardara el modelo."
					sys.exit(0)
				else:
					if sys.argv[len(sys.argv)-1][-3:]!='2dv':
						print 'Error la extension del fichero debe ser .2dv'
						sys.exit(0)
					else:
						modeloOutput = sys.argv[len(sys.argv)-1]
						if len(sys.argv) > 5:
							i = 3
							while i < len(sys.argv)-2:
								if sys.argv[i] == "-factotum" or sys.argv[i] == "-f":
									factotum = (sys.argv[i+1]=='True' or sys.argv[i+1]=='true')
								if sys.argv[i] == "-mincount" or sys.argv[i] == "-mc":
									min_count = int(sys.argv[i+1])
								if sys.argv[i] == "-window" or sys.argv[i] == "-w":
									window = int(sys.argv[i+1])
								if sys.argv[i] == "-size" or sys.argv[i] == "-s":
									size = int(sys.argv[i+1])
								if sys.argv[i] == "-negative" or sys.argv[i] == "-n":
									negative = int(sys.argv[i+1])
								if sys.argv[i] == "-workers" or sys.argv[i] == "-w":
									workers = int(sys.argv[i+1])
								if sys.argv[i] == "-epoch" or sys.argv[i] == "-e":
									epoch = int(sys.argv[i+1])
								i+=2

with open(ficheroProcesadoTrain) as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip('\n') for x in content]

temas=[]
helper = []
for x in content:
	if (len(x)>0):
		if "ctx" in x:
			tema = x.split('#')[1:]
		else:
			palabras = x.split(' ')
			for y in palabras:
				y = y.split('#')[0]
				helper.append(y)
			palabras = helper
			helper = []
	else:
		temas.append([palabras, tema])


model = doc2vec.Doc2Vec(min_count=min_count, window=window,size=size,negative=negative, workers=workers)

doc = []
helper = []
analyzedDocument = namedtuple('AnalyzedDocument', 'words tags')
for text in temas:
	for x in text[0]:
		helper.append(unicode(x))
	words = helper
	helper = []
	tags = []
	for x in text[1]:
		tags.append(unicode(x.upper()))
	if len(tags) < 1:
		tags.append(unicode('FACTOTUM'))
	if not(tags == 'FACTOTUM' and factotum == False):
		doc.append(analyzedDocument(words, tags))

model.sort_vocab()
model.build_vocab(doc)

for ep in range(epoch):

    model.train(doc)
    model.alpha -= 0.001  # decrease the learning rate
    model.min_alpha = model.alpha  # fix the learning rate, no decay
    model.update_weights()
    print ('Espera, realizados ' + str(ep) + ' epoch de ' + str(epoch))

model.save(modeloOutput)
print 'Finalizado.'
