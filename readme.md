## Installazione

1. Installare Java e GCC.

    ```
    sudo apt install default-jre
    sudo apt install gcc
    ```

2. Una volta scaricato il contenuto della presente repository, spostarlo nel percorso che si preferisce (d'ora in poi, `CHOSEN_PATH`).

3. Spostarsi nel percorso scelto.

    ```
    cd CHOSEN_PATH
    ```

4. Installare l'ambiente virtuale. Ci sono due opzioni:

    * Con ANACONDA

        ```
        conda env create -f environment.yml
        conda activate pipeline_env
        ```

    * Con VENV

        *Scegliere un percorso dove creare l'ambiente virtuale (d'ora in poi, `ENV_PATH`)*

        ```
        cd ENV_PATH
        python3 -m venv pipeline_env --python="/usr/bin/python3.8"
        . pipeline_env/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
        ```

5. Dopo aver [scaricato](https://github.com/dig-team/amie/releases/tag/3.0) AMIE [^1], rinominare il file in `amie-init.jar` e spostarlo in `CHOSEN_PATH/scripts/utils/jars`.

6. Installare Elliot [^2].
    
    *Scegliere un percorso dove installare Elliot (d'ora in poi, `ELLIOT_PATH`)*

    ```
    pip install --upgrade pip
    cd ELLIOT_PATH
    git clone https://github.com//sisinflab/elliot.git
    cd elliot
    pip install -e . --verbose
    ```

## Uso

1. Importare un dataset nella cartella `CHOSEN_PATH/datasets`, seguendo [queste](/datasets/readme.md) indicazioni.

2. Attivare l'ambiente virtuale che si è precedentemente installato:

    * Con ANACONDA

        ```
        conda activate pipeline
        ```

    * Con VENV

        ```
        cd ENV_PATH
        . pipeline_env/bin/activate
        ```

3. Spostarsi nella cartella degli script (per semplice comodità, non perché sia strettamente necessario).

    ```
    cd CHOSEN_PATH/scripts
    ```

4. Eseguire gli script desiderati.

## Gli script

La presente suite è composta da una serie script, ciascuno dei quali corrisponde a diverse fasi della pipeline che è stato oggetto del tirocinio. I principali script sono i seguenti.

* Da eseguire una sola volta per dataset:

    ```
    python .\initDataset.py DATASET_NAME
    ```

* Da eseguire per ogni diversa configurazione di AMIE:

    ```
    python .\mineAndGroundRules.py DATASET_NAME [AMIE_SETTINGS]
    ```

* Da eseguire per ogni diverso sottoinsieme di regole sul quale si vuole sperimentare:

    ```
    python .\initRulesSubset.py DATASET_NAME [AMIE_SETTINGS] [RULES_FILTER]
    ```

* Da eseguire per ogni diversa configurazione di KALE:

    ```
    python .\runKaleAmarElliot.py DATASET_NAME [AMIE_SETTINGS] [RULES_FILTER] [KALE_SETTINGS] [AMAR_SETTINGS]
    ```

Questi script in particolare realizzano delle macro-fasi, cioè eseguono in sequenza alcune fasi della pipeline che sono strettamente correlate tra loro. Per esempio, oltre a `runKaleAmarElliot.py`, ci sono anche `runKale.py`, `runAmar.py` e `runElliot.py`. Tali script minori possono comunque tornare utili, magari quando gli script più complessi non riescono a completare tutte le fasi a cui corrispondono. Se `runKaleAmarElliot.py` completasse la fase legata a KALE, per poi interrompersi per problemi tecnici (tipicamente, assenza di sufficiente memoria allocabile), invece di rieseguire lo stesso script, sarebbe molto più conveniente riprendere il processo da dove si è interrotto lanciando piuttosto `runAmarElliot.py`.

### Parametri

I valori di default sono definiti nei file che si trovano nella cartella `CHOSEN_PATH/scripts/utils/defaultValues`. Tali valori sono liberamente modificabili, o addirittura eliminabili, ma i file in questione devono obbligatoriamente esistere e devono risultare essere dei JSON validi. Notare pure che si è scelto di rendere impossibile definire valori di default per i parametri di tipo `bool`, per timore che ciò potesse risultare confusionario per gli utenti. I parametri per i quali non sono definiti valori di default, o per i quali il valore di default indicato è `null`, devono obbligatoriamente essere impostati da linea di comando, nel momento in cui si esegue uno script che li coinvolge.
Segue un elenco dei vari parametri.

`AMIE_SETTINGS`

| Parametro               | Tipo        | Descrizione                          |
| -----------------------:|:-----------:|:------------------------------------:|  
| `--maxad`               | `int`       | Massimo numero di [atomi](https://it.wikipedia.org/wiki/Formula_atomica) delle regole da considerare |

I valori di default sono definiti in `amieSettings.json`:

```
{
    "maxad": 4
}
```

`RULES_FILTER`

| Parametro               | Tipo        | Descrizione                                         	  				 |
| -----------------------:|:-----------:|:----------------------------------------------------------------------:|  
| `--minStdConfidence`    | `float`     | Minimo valore di "Standard Confidence" delle regole da considerare |
| `--minPcaConfidence`    | `float`     | Minimo valore di "PCA Confidence" delle regole da considerare |
| `--minHeadCoverage`     | `float`     | Minimo valore di "Head Coverage" delle regole da considerare |
| `--minBodySize`         | `int`       | Minimo valore di "Body Size" delle regole da considerare |
| `--minPcaBodySize`      | `int`       | Minimo valore di "PCA Body Size" delle regole da considerare |
| `--minPositiveExamples` | `int`       | Minimo valore di "Positive Examples" delle regole da considerare |
| `--likeInHead`          | `bool`      | Considerare solo regole con relazione `like` nella testa |

I valori di default sono definiti in `rulesFilter.json`:

```
{
    "minStdConfidence": 0,
    "minHeadCoverage": 0,
    "minPositiveExamples": 0,
    "minPcaConfidence": 0,
    "minBodySize": 0,
    "minPcaBodySize": 0
}
```

`KALE_SETTINGS`

| Parametro               | Tipo        | Descrizione                          												|
| -----------------------:|:-----------:|:---------------------------------------------------------------------------------:|  
| `--m_d` | `float` | / |
| `--m_gE` | `float` | / |
| `--m_gR` | `float` | / |
| `--weight` | `float` | / |
| `--miniBatch` | `int` | / |
| `--iterations` | `int` | Numero di iterazioni totali della configurazione da considerare |
| `--skip` | `int` | Numero di iterazioni di output della configurazione da considerare |
| `--dims` | `list[int]` | Elenco delle dimensioni degli embeddings da considerare |
| `--itemProperties` | `bool` | Considerare anche le triple del grafo con relazioni "item-prop" |

I valori di default sono definiti in `kaleSettings.json`:

```
{
    "miniBatch": 100,
    "m_d": 0.1,
    "m_gE": 0.05,
    "m_gR": 0.05,
    "iterations": 500,
    "skip": 50,
    "weight": 0.01
}
```

`AMAR_SETTINGS`

| Parametro               | Tipo        | Descrizione                                |
| -----------------------:|:-----------:|:------------------------------------------:|
| `--top`                 | `list[int]` | Elenco del numero di previsioni da considerare |

I valori di default sono definiti in `amarSettings.json`:

```
{
    "top": [5, 10]
}
```

## Esempi d'uso

Una volta che ci si è spostati nella cartella `CHOSEN_PATH/scripts`, data l'esistenza di una cartella `CHOSEN_PATH/datasets/dbbook` che rispetti i requisiti precedentemente indicati, ecco come questi script potrebbero essere utilizzati.

```
conda activate pipeline_env

python initDataset.py dbbook

python runKaleAmarElliot.py dbbook --iterations 1 --skip 1 --dims 256 512 768 --top 10 20

python mineAndGroundRules.py dbbook --maxad 3
python runKaleAmarElliot.py dbbook --maxad 3 --iterations 1 --skip 1 --dims 256 512 --itemProperties --top 5

python initRulesSubset.py dbbook --maxad 3 --minStdConfidence 0.2
python runKaleAmarElliot.py dbbook --maxad 3 --minStdConfidence 0.2 --iterations 1 --skip 1 --dims 768 --itemProperties
```

## Note

* Gli script danno per scontato che le uniche due relazioni "user-item" possano essere `like` e `dislike`. Tutte le altre sono automaticamente considerate relazioni "item-prop".
* La relazione `dislike` può in realtà essere assente da `mapping_relations.tsv`, ma la presenza della relazione `like` nel medesimo file è assolutamente mandatoria. Inoltre, ha ovviamente poco senso utilizzare questi script su dataset che non presentano almeno quella specifica relazione "user-item" nelle triple.
* Eseguire la funzione `runElliot()` (definita in `runElliot.py` e chiamata pure in `runKaleAmarElliot.py` e in `runAmarElliot.py`) più di una volta non elimina i file di output precedentemente prodotti.
* Se si intende eseguire la funzione `runElliot()`, assicurarsi di star utilizzando Python 3.8 (dovrebbe essere automaticamente impostato se si installa `environment.yml` con Anaconda), poiché s'è osservato che il framework in questione semplicemente non funziona con versioni successive di Python.
* I contenuti della cartella `CHOSEN_PATH/src/kale` sono irrilevanti all'esecuzione degli script. Tale cartella contiene solo il codice (non prodotto, bensì solo leggermente modificato, dal sottoscritto) dal quale sono stati esportati la maggior parte dei file `.jar` che vengono adoperati durante la pipeline.
* Per quanto riguarda specificatamente gli script `runKale.py`, `runAmar.py`, `runElliot.py`, `runAmarElliot.py`, `runKaleAmarElliot.py`, i parametri appartenenti ad `AMIE_SETTINGS` non vengono inizializzati ai valori di default, perché sono opzionali (in questo modo, se `--maxad` non viene impostato, viene inizializzata la pipeline senza regole). Di conseguenza, sempre per quegli script, se `--maxad` non viene impostato, vengono CORRETTAMENTE ignorati i seguenti parametri (nonostante possano comunque risultare impostati):
    * tutti i parametri appartenenti a `RULES_FILTER`;
    * il parametro `weight` appartenente a `KALE_SETTINGS`.

## Problemi

* Eseguire `runKale.py` o `runKaleAmarElliot.py` con `--maxad` impostato e con `--itemProperties` non impostato, causa un malfunzionamento. Ciò è probabilmente dovuto al fatto che si dà in input al processo un file `relationid.txt` che fa riferimento solo alle relazioni "user-item", quando i file `groundings.txt` fanno riferimento anche alle relazioni "item-prop". Non si è ancora risolto il problema semplicemente perché per il momento non è stato necessario eseguire la pipeline con impostazioni simili. 
* Se il file `groundings.txt` è troppo piccolo (?), l'esecuzione di `/scripts/utils/jars/KALEJointProgram.jar` fallisce. Ciò succede, per esempio, sul sottoinsieme delle regole estratte da "dbbook", inizializzato con `--maxad 3 --minStdConfidence 0.7`. Non si è investigato ulteriormente sulla causa, poiché il problema era irrilevante rispetto ai compiti a me assegnati e si è presentato solo durante un test fine a sé stesso.
    ```
    java.lang.NullPointerException
        at kale.joint.StochasticUpdate.stochasticIteration(StochasticUpdate.java:87)
        at kale.joint.KALEJointModel2.TransE_Learn(KALEJointModel2.java:211)
        at kale.joint.KALEProgram2.main(KALEProgram2.java:94)
    ```
* Se il processo Python lanciato richiede troppa memoria, un `SIGKILL` (che, per definizione, è impossibile da catturare e gestire) lo fa immediatamente interrompere. In quei casi, il programma non arriva dunque a mostrare la schermata riepilogativa del processo, dove appunto segnalarebbe che si è verificato qualche errore. Ciò può tipicamente avvenire durante l'esecuzione della funzione `runAmar()` (definita in `runAmar.py` e chiamata pure in `runKaleAmarElliot.py` e in `runAmarElliot.py`).
* Durante l'esecuzione di `KALEJointProgram.jar`, inizializzata dalla funzione `runKale()` (definita in `runKale.py` e chiamata pure in `runKaleAmarElliot.py`) può capitare che un `SIGSEGV` interrompa il processo. Quando ciò succede, la causa è quasi certamente (se non proprio sicuramente) la mancanza di sufficiente memoria allocabile.
* Le funzioni `runAmar()` e `runElliot()` hanno una gestione degli errori assai grossolana: se una qualsiasi `Exception` (classe built-in di Python) viene intercettata all'interno di quelle funzioni, viene emessa una generica `AmarException` o `ElliotException`, che può risultare poco indicativa del problema riscontrato.

## Possibili miglioramenti

* Aggiungere altri parametri ad `AMIE_SETTINGS` (quali?).
* Aggiungere altri parametri ad `AMAR_SETTINGS` (ce ne sono?).
* Aggiungere parametri di Elliot (quali?).
* Aggiungere un parametro a `RULES_FILTER` per la colonna "Functional Variable" dell'output di AMIE (non si è riuscito a capire come sarebbe opportuno filtrarlo).
* Aggiungere parametri a `RULES_FILTER` per specificare anche valori massimi dei vari attributi (sarebbe utile?).
* Permettere di dare in input il simbolo col quale un dataset rappresenta la relazione "user-item" che esprime apprezzamento (al momento si assume che sia `like`, che potrebbe invece diventare il valore di default di questo eventuale parametro).
* Permettere di dare in input un elenco delle relazioni "user-item" che non siano `like`, oppure rendere obbligatoria la presenza nel dataset importato anche dei file `mapping_items.tsv` e `mapping_props.tsv`, così che queste informazioni possano essere inferite dalle triple (contenute nel file `kale_train.tsv`). 
* Permettere di dare in input agli script il percorso di un file che descriva i valori da assegnare ai vari parametri (per rendere gli esperimenti più facilmente riproducibili).
* In generale, implementare una più rigorosa gestione degli errori, così da evitare completamente messaggi criptici.
* Trovare un modo più sofisticato per gestire la memoria (quale?), così da gestire l'impossibilità di allocazione in modo più aggraziato (anche solo mostrando un messaggio di errore più comprensibile), evitando quindi `SIGKILL` improvvisi.
* Rendere effettivamente possibile eseguire `runKale.py` o `runKaleAmarElliot.py` con `--maxad` impostato e con `--itemProperties` non impostato.
* Eliminare l'output precedente ogni volta che si esegue `runElliot()` (per evitare confusione nella cartella corrispondente).
* Il flusso di esecuzione di alcuni degli script può finire per valutare inutilmente più di una volta il metodo di istanza `AmieSettings::areValid()`. Si potrebbe fare in modo che l'espressione in questione venga valutata una sola volta (all'inizio del programma) e "impacchettarne" i risultati corrispondenti in un'istanza di una specializzazione della classe `KaleSettings` (per esempio, un eventuale `KaleJointSettings` potrebbe contenere un override di un eventuale metodo virtuale `getJarFile()`, che fornirebbe il nome del corretto programma da eseguire, o qualcosa del genere).
* Utilizzare un vero e proprio database (forse persino uno di tipo relazionale potrebbe essere opportuno), invece di una serie di file e cartelle (e se proprio necessario, creare delle infrastrutture che permettano di esportare certe moli di dati nei vari schemi TSV attualmente impiegati).
* Forse sarebbe meno confusionario definire distintamente un `runKaleJoint.py` e un `runKaleTrip.py`, e similari, così che solo il primo abbia tra i suoi parametri `AMIE_SETTINGS` e `RULES_FILTER`.
* Definire una variabile d'ambiente che specifichi la posizione della cartella `/datasets`, invece di assumere che si trovi in `/scripts/../`.
* Parallelizzare le diverse fasi di `runAmarElliot.py` e `runKaleAmarElliot.py`. Per esempio, una volta che KALE è concluso su una dimensione, potrebbe essere possibile sganciare un nuovo processo che esegua AMAR ed Elliot in sequenza su quella dimensione, mentre KALE sulla dimensione successiva potrebbe essere contemporaneamente eseguito sul processo principale.
    * Ciò potrebbe essere poco utile, a causa degli elevati requisiti di memoria che hanno sia KALE che AMAR, che potrebbero quindi finire per contendersi lo spazio allocabile, causando errori sulle macchine meno performanti. Però magari questa potrebbe comunque essere un'opzione attivabile tramite flag?

[^1]: https://github.com/dig-team/amie
[^2]: https://github.com/sisinflab/elliot/