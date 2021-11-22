## Analisi dei risultati
### Accuratezza

#### Latino

Per quanto riguarda la prima lingua presa in considerazione, il latino, abbiamo dei risultati interessanti.
Le prestazioni in termini di accuratezza registrate dall'algoritmo *baseline* sono notevoli: parliamo di circa il ***95%*** delle parole taggate correttamente.
L'applicazione del modello di Markov, in particolare dell'algoritmo di Viterbi, ha portato a dei miglioramenti. Un occhio un pò meno attento, che vede l'incremento dell'accuratezza di un solo punto e mezzo percentuale, potrà pensare che l'algoritmo non è così tanto performante.

Considerando che la baseline ha già ottimi risultati e che l'introduzione di un PoS tagger probabilistico porta ad un incremento ulteriore in termini di accuratezza, possiamo, invece, promuovere l'adozione dell'algoritmo di Viterbi.

A seguire un line chart che mostra l'andamento dell'accuratezza al variare della tecnica di smoothing:



![](/home/francesco/Documents/TLN/Prima parte/line-graph.png)

Possiamo notare come ogni tecnica va a migliorare il già attimo risultato della *baseline*. Il peggior risultato si ottiene applicando la tecnica che associa alle parole sconosciute una probabilità di emissione pari a *1/(len(states))*, nel grafo è indicata con il nome *Smoothing3*. *Smoothing1* (parole sconosciute considerate nomi) e *Smoothing2* (parole sconosciute considerate nomi o verbi) si comportano in maniera simile con una leggera e prevedibile preferenza verso il secondo metodo.

La tecnica basata sulle parole che appaiono una sola volta all'interno del *dev corpus*, *Smoothing4*, produce un'accuratezza superiore a scapito di una complessità temporale e spaziale maggiore dovuta, appunto, al calcolo della distribuzione di probabilità.

Nel dettaglio:

| Tecnica di smoothing | Accuratezza | PoS corretti | PoS errati |
| :------------------: | :---------: | :----------: | :--------: |
|       Baseline       |   0.94974   |    22869     |    1210    |
|     Smoothing 1      |   0.95365   |    22963     |    1116    |
|     Smoothing 2      |   0.95464   |    22987     |    1092    |
|     Smoothing 3      |   0.95269   |    22940     |    1139    |
|     Smoothing 4      |   0.96237   |    23173     |    906     |



Facciamo un'ultima considerazione sulla tipologia degli errori effettuati dal PoS tagger. Notiamo come l'algoritmo *baseline* produce degli errori su ogni tag: esso associa erroneamente almeno una volta un tag a una parola, per ogni tag. Questo non vale per Viterbi.

*Smoothing1* a causa della varietà e del numero elevato delle parole non conosciute, associa fin troppe volte il tag *noun*. Fa un pò meglio *Smoothing2* sbagliando meno volte ad associare *noun* ma più volte il tag *verb*. La somma degli errori fa preferire la seconda tecnica.

Molto meglio *Smoothing3* e *Smoothin4* per quanto riguarda *verb* e *noun*. Il terzo metodo, però, associa erroneamente troppi *pron*: circa 300 in più rispetto a tutte le altre tecniche. Questo è il motivo della più bassa accuratezza di *Smoothing3*.

Se per *Smoothing1* il problema è che associa erroneamente troppi *nuon*, per *Smoothing2* troppi *verb* e per *Smoothing3* troppi *pron*, *Smoothing4* si dimostra il più meticoloso e in grado di non specializzarsi su un determinato tag.



Tabella riassuntiva dei tag associati in maniera scoretta:

|  PoS  | Baseline | Smoothing 1 | Smoothing 2 | Smoothing 3 | Smoothing 4 |
| :---: | :------: | :---------: | :---------: | :---------: | :---------: |
|  aux  |   135    |     103     |     103     |     103     |     103     |
| noun  |    56    |     666     |     271     |     74      |     74      |
| verb  |   173    |     45      |     416     |     259     |     346     |
| cconj |   102    |     25      |     25      |     25      |     25      |
| pron  |   280    |     195     |     195     |     585     |     195     |
|  adv  |    76    |     12      |     12      |     12      |     12      |
|  adp  |   169    |      4      |      4      |      4      |      4      |
|  adj  |    48    |     15      |     15      |     15      |     15      |
|   x   |    2     |      5      |      5      |      5      |      5      |
|  det  |    99    |      3      |      3      |      3      |      3      |
| punct |    44    |      0      |      0      |      0      |      0      |
| propn |    18    |     18      |     18      |     29      |     99      |
| sconj |    6     |      5      |      5      |      5      |      5      |
| part  |    1     |      0      |      0      |      0      |      0      |
|  num  |    1     |     20      |     20      |     20      |     20      |

#### 

#### Greco

Discorso diverso per quanto riguarda la lingua greca. L'accuratezza di tutte le strategie non è elevata, ma notiamo, comunque, un incremento significativo dell'accuratezza rispetto all'algoritmo base il quale si avvicina al ***65%***.
In questo caso l'utilizzo dell'algoritmo di Viterbi ha comportato delle migliorie importanti con un:

- +8% con la prima tecnica di smoothing,
- +10% con *Smoothing2*,

- +6% applicando la terza strategia di smoothing,

- **+11%** con la quarta tecnica di smoothing.

  

  Line chart:

  ![](/home/francesco/Documents/TLN/Prima parte/line-graph2.png)

Anche in questo caso *Smoothing4* si dimostra la migliore strategia dal punto di vista dell'accuratezza mentre *Smoothing3* la peggiore.

Da notare la riduzione del gap tra la prima e la quarta strategia.

Nel dettaglio:

|   Tecnica   | Accuratezza | PoS corretti | PoS errati |
| :---------: | :---------: | :----------: | :--------: |
|  Baseline   |   0.64607   |    13541     |    7418    |
| Smoothing 1 |   0.72651   |    15227     |    5732    |
| Smoothing 2 |   0.74746   |    15666     |    5293    |
| Smoothing 3 |   0.70566   |    14790     |    6169    |
| Smoothing 4 |   0.75199   |    15761     |    5198    |



Il risultato dell'analisi dei PoS scorretti della lingua greca è paragonabile a quanto detto per il latino. L'assottigliamento del gap tra *Smoothing2* e *Smoothing4* è dovuto dalla ottima gestione del tag *verb* da parte della seconda strategia. Gestione migliore rispetto a quanto fatto da *Smoothing4*.



Dettagliatamente:

|  PoS  | Baseline | Smoothing 1 | Smoothing 2 | Smoothing 3 | Smoothing 4 |
| :---: | :------: | :---------: | :---------: | :---------: | :---------: |
| noun  |   767    |    2815     |    1433     |     937     |     998     |
| part  |   1597   |    1132     |    1122     |    1385     |    1117     |
| cconj |   1070   |     184     |     184     |     169     |     184     |
|  adj  |   859    |     272     |     238     |     219     |     230     |
|  det  |   1246   |      2      |      2      |      1      |      2      |
| punct |   297    |      0      |      0      |      1      |      0      |
| verb  |   214    |      8      |     992     |     525     |    1345     |
| pron  |   455    |    1099     |    1103     |    2696     |    1103     |
|  adp  |   453    |      7      |      7      |      7      |      7      |
| sconj |   129    |     33      |     33      |     34      |     33      |
|  adv  |   250    |     136     |     135     |     151     |     135     |
|  num  |    67    |     44      |     44      |     44      |     44      |
| intj  |    14    |      0      |      0      |      0      |      0      |

#### 



### Tempi di esecuzione

#### Latino 

La complesità temporale delle varie strategie è allineata: sia la *baseline* che *Viterbi* impiegano poco meno di **30** secondi.
Nel caso di Viterbi va considerato anche il tempo trascorso per calcolare le probabilità di emissione e di transizione (circa 4 secondi).

| Tecnica di smoothing | Tempo di esecuzione (s) |
| :------------------: | :---------------------: |
|       Baseline       |          29.96          |
|     Smoothing 1      |          27.23          |
|     Smoothing 2      |          26.79          |
|     Smoothing 3      |          27.09          |
|     Smoothing 4      |          27.28          |

#### Greco

L'andamento si ripete per il greco: pressochè paragonabili i tempi di esecuzione di *baseline* e *Viterbi* i quali aumentano notevolmente se confrontati con il latino a causa dell'incremento dei corpus. Anche in questo caso ci sono da aggiungere circa 4 secondi per il calcolo delle probabilità di transizione ed emissione necessarie per *Viterbi*. Tale risultato potrebbe essere condizionato dal dispositivo di massa su cui sono salvati i corpus.

| Tecnica di smoothing | Tempo di esecuzione (s) |
| :------------------: | :---------------------: |
|       Baseline       |         131.73          |
|     Smoothing 1      |         138.93          |
|     Smoothing 2      |         137.43          |
|     Smoothing 3      |         136.38          |
|     Smoothing 4      |         138.39          |

### Conclusioni
I risultati empirici ottenuti dimostrano le ottime performance del modello di Markov per il PoS tagging, in particolare del metodo di Viterbi correlato ad opportune tecniche di smoothing per la gestione delle parole sconosciute al modello.

Il PoS tagger base per il latino, dopo una fase di pre-processing delle parole all'interno del corpus, raggiunte un livello di accuratezza già parecchio elevato. Migliorare questo già ottimo risultato non è scontato.

Per il greco, invece, partiamo da una *baseline* decisamente più bassa e che l'algoritmo di Viterbi riesce a migliorare di molto.
Questo risultato è influenzato dalla presenza di un numero superiore di frasi presenti nel *corpus* train e che consente un più accurato calcolo delle probabilità.