# DocToVec

Este ejercicio intenta catalogar deficiniciones de palabras en diferentes categorías.

## Instrucciones

### Procesamiento

Para empezar deberemos procesar dos ficheros situados en la carpeta *Contextos* : *Context(Train)* y *Context(Test)*. Lo ideal sería dividir el fichero *Context(Todos)* en dos trozos, para que no se repita información. Una vez lo tenemos dividido procederemos a procesarlo, para eso utilizaremos el fichero Python *procesador.py*

El fichero *procesador.py* requiere de una serie de parametros para su correcto funcionamiento. A continuación se explican cuales son esos parametros. Todas las rutas se escriben a partir del path *./DocToVec*

|Nombre Parametro|Abreviatura|Necesario|Descripción|
| :---: | :---: | :---: | :---: |
|-ficheroContextInput|-fci|<img src="http://www.autoroyal.it/wp-content/uploads/2015/07/plainicon.com-54418-128px-51c.png" width="20"> | Ruta al fichero de contexto|
|-variant|-v|  <img src="http://www.autoroyal.it/wp-content/uploads/2015/07/plainicon.com-54418-128px-51c.png" width="20">|Ruta al fichero variants|
|-domains|-d|<img src="http://www.autoroyal.it/wp-content/uploads/2015/07/plainicon.com-54418-128px-51c.png" width="20">|Ruta al fichero de dominios|
|-ficheroContextOutput|-fco|<img src="http://www.autoroyal.it/wp-content/uploads/2015/07/plainicon.com-54418-128px-51c.png" width="20">|Ruta donde queremos que se guarden los resultados.

Un ejemplo de los comandos necesarios para procesar los dos contextos serian:

```bash
python procesarHash.py -fci ./Contextos/Context\(Train\).txt 
-v FicherosNecesarios/wei_eng-30_variant.tsv -d FicherosNecesarios/wei_ili_to_domains.tsv 
-fco FicherosProcesados/Train.txt
```

```bash
python procesarHash.py -fci ./Contextos/Context\(Test\).txt 
-v FicherosNecesarios/wei_eng-30_variant.tsv -d FicherosNecesarios/wei_ili_to_domains.tsv 
-fco FicherosProcesados/Test.txt
```

### Creando el modelo

Una vez tenemos los datos listos procederemos a crear el modelo. Para crearlo utilizaremos el fichero *docToVec.py*. Después de entrenar el modelo lo podremos utilizar para clasificar textos, frases... Para crear el modelo, el fichero *docToVec.py* admite diferentes parametros:

|Nombre Parametro|Abreviatura|Necesario|Descripción|
| :---: | :---: | :---: | :---: |
|-ficheroProcesadoTrain|-fpt|<img src="http://www.autoroyal.it/wp-content/uploads/2015/07/plainicon.com-54418-128px-51c.png" width="20"> |Ruta al fichero de entrenamiento|
|-modeloOutput|-mo| <img src="http://www.autoroyal.it/wp-content/uploads/2015/07/plainicon.com-54418-128px-51c.png" width="20">|Ruta donde queremos que se guarde el modelo.(.2dv)|
|-factotum|-f|<img src="http://www.clker.com/cliparts/Z/Z/S/Y/S/w/red-circle-cross-transparent-background-md.png" width="20">|Incluye el label factotum|
|-mincount|-mc|<img src="http://www.clker.com/cliparts/Z/Z/S/Y/S/w/red-circle-cross-transparent-background-md.png" width="20">|Ignorar todas las palabras con una frecuencia total menor que ésta.|
|-window|-w|<img src="http://www.clker.com/cliparts/Z/Z/S/Y/S/w/red-circle-cross-transparent-background-md.png" width="20">|La distancia máxima entre la palabra actual y la predicha.|
|-size|-s|<img src="http://www.clker.com/cliparts/Z/Z/S/Y/S/w/red-circle-cross-transparent-background-md.png" width="20">|Dimensionalidad de los vectores de características en la salida. 100 es un buen número. Si eres extremista, puedes subir hasta los 400.|
|-negative|-n|<img src="http://www.clker.com/cliparts/Z/Z/S/Y/S/w/red-circle-cross-transparent-background-md.png" width="20">|si > 0, se utilizará muestreo negativo, el int para negativo especifica cuántas "palabras de ruido" se deben dibujar.|
|-workers|-w|<img src="http://www.clker.com/cliparts/Z/Z/S/Y/S/w/red-circle-cross-transparent-background-md.png" width="20">|hilos de trabajo para entrenar el modelo.|
|-epoch|-e|<img src="http://www.clker.com/cliparts/Z/Z/S/Y/S/w/red-circle-cross-transparent-background-md.png" width="20">|Cantidad de epoch en el eltrenamiento.|

Un ejemplo para crear un modelo sería:

```bash
python docToVec.py -fpt ./FicherosProcesados/Train.txt
-f True -mc 10 -w 5 -s 300 -n 10 -w 16 -e 10 
-mo Modelos/GrandeConFactotum.2dv
```
###### *Aviso*: Dependiendo de los valores elegidos el tiempo de entrenamiento puede alargarse mucho.

### Probando el modelo.

Una vez tenemos el modelo creado, pasamos a testearlo. En este caso para probar lo bueno que es nuestro modelo, utilizaremos el fichero *tester.py*. La ejecución de este fichero, nos devolverá información sobre nuestro modelo.

El fichero *tester.py* requiere de una serie de parametros para su correcto funcionamiento. A continuación se explican cuales son esos parametros.

|Nombre Parametro|Abreviatura|Necesario|Descripción|
| :---: | :---: | :---: | :---: |
|-ficheroProcesadoTest|-fpt|<img src="http://www.autoroyal.it/wp-content/uploads/2015/07/plainicon.com-54418-128px-51c.png" width="20"> |Ruta al fichero procesado Test|
|-dominio|-d| <img src="http://www.autoroyal.it/wp-content/uploads/2015/07/plainicon.com-54418-128px-51c.png" width="20">|Ruta a otro fichero de dominios.|
|-modelo|-m|<img src="http://www.autoroyal.it/wp-content/uploads/2015/07/plainicon.com-54418-128px-51c.png" width="20">|Ruta al modelo que queremos probar.|
|-check|-c|<img src="http://www.clker.com/cliparts/Z/Z/S/Y/S/w/red-circle-cross-transparent-background-md.png" width="20">|Al comprobar tiene en cuenta los primeros 10 labels.(Sino solo el 1º)|
|-verbose|-v|<img src="http://www.clker.com/cliparts/Z/Z/S/Y/S/w/red-circle-cross-transparent-background-md.png" width="20">|Imprime el resultado esperado, seguido de los obtenidos.|
|-factotum|-f|<img src="http://www.clker.com/cliparts/Z/Z/S/Y/S/w/red-circle-cross-transparent-background-md.png" width="20">|Prueba tambien los resultados del label factotum|

Un ejemplo para ejecutar un test sería:

```bash
python tester.py -fpt FicherosProcesados/Test.txt 
-d FicherosNecesarios/wei_domains.tsv 
-m Modelos/GrandeConFactotum.2dv -c -v -f
```

Para guardar el resultado:

```bash
python tester.py -fpt FicherosProcesados/Test.txt 
-d FicherosNecesarios/wei_domains.tsv 
-m Modelos/GrandeConFactotum.2dv -c -v -f > ./Ruta para guardar
```

Deberíamos obtener unos resultados como estos:
```
...
* FACTOTUM * <-- Esperado
FACTOTUM , 0.243247911334 <-- Acertado
TAX , 0.222206294537
ARCHITECTURE , 0.212506860495
FURNITURE , 0.210013270378
CYCLING , 0.192896276712
ACOUSTICS , 0.189596027136
DANCE , 0.189572304487
THEATRE , 0.18843844533
ARCHERY , 0.186074733734
PSYCHOLOGICAL_FEATURES , 0.179820671678
---------------------------
* POLITICS * <-- Esperado
FACTOTUM , 0.243247911334
TAX , 0.222206294537
ARCHITECTURE , 0.212506860495
FURNITURE , 0.210013270378
CYCLING , 0.192896276712
ACOUSTICS , 0.189596027136
DANCE , 0.189572304487
THEATRE , 0.18843844533
ARCHERY , 0.186074733734
PSYCHOLOGICAL_FEATURES , 0.179820671678
--------------------------- No Acertado
Resultados del programa de clasificacion
--------------------------------
Acertados: 302
Fallados: 631
Total: 933
--------------------------------
Porcentaje acertados: 32.3687031083%
Porcentaje fallados: 67.6312968917%
```



## Referencias

Para crear este repositorio he utilizado [Gensim], puedes conseguirlo descargandolo [aquí] o en el siguiente [repositorio].

Puedes conseguir información adicional en este [enlace].

[Gensim]: https://radimrehurek.com/gensim/
[aquí]: https://radimrehurek.com/gensim/install.html
[repositorio]: https://github.com/RaRe-Technologies/gensim
[enlace]: http://linanqiu.github.io/2015/10/07/word2vec-sentiment/




