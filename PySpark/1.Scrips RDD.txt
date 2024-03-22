
#abrir pyspark
pyspark
#SparkContext - variavel sc
sc
#criar RDD
numeros = spark.parallelize([1,2,3,4,5,6,7,8,9,10])

#diversas ações 
numeros.take(5)
numeros.top(5)

#todos os elementos
numeros.collect()

#operacoes aritimeticas
numeros.count()
numeros.mean()
numeros.sum()
numeros.max()
numeros.min()
numeros.stdev()

#transformacoes
#filtro
filtro = numeros.filter(lambda filtro: filtro > 2)
filtro.collect()

#amostra com reposicao
amostra = numeros.sample(True,0.5,1)
amostra.collect()

#map, aplica uma funcao
mapa = numeros.map(lambda mapa: mapa * 2)
mapa.collect()

#criamos outro RDD
numeros2 = sc.parallelize([6,7,8,9,10])

#operador Union - gera rdd com os 2 conjuntos
uniao = numeros.union(numeros2)
uniao.collect()

#interacoes
interseccao = numeros.intersection(numeros2)
interseccao.collect()

#subtracao
subtrai =numeros.subtract(numeros2)
subtrai.collect()

#produto cartesiano
cartesiano = numeros.cartesian(numeros2)
cartesiano.collect()

#acao, contar por valor numero de vezes que cada valor aparece
cartesiano.countByValue()

#compras, codigo do cliente e valor
compras = sc.parallelize([(1,200),(2,300),(3,120),(4,250),(5,78)])
#separar chaves
chaves = compras.keys()
chaves.collect()
#separar valores
valores = compras.values()
valores.collect()
#conta elementos por chave
compras.countByKey()

#aplica funcao no valor, sem aterar chave
soma = compras.mapValues(lambda soma: soma + 1)
soma.collect()

#agrupa por chave
agrupa = compras.groupByKey().mapValues(list)
agrupa.collect()

#debitos, codigo cliente e valor
debitos = sc.parallelize([(1,20),(2,300)])

#inner join entre compras e debitos
resultado = compras.join(debitos)
resultado.collect()

#remove e mostra apenas quem tem debito
semdebito = compras.subtractByKey(debitos)
semdebito.collect()
