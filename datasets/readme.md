1. Creare una cartella con un qualsiasi nome.
2. Inserire `mapping_relations.tsv` (gli altri file simili non sono strettamente necessari).
3. Creare una sottocartella `user-item-prop`.
4. Nella sottocartella, mettere `amar_test.tsv`, `amar_train.tsv`, `kale_valid.tsv`, `kale_train.tsv` e anche `kale_test.tsv`, se esiste.

Tutti i valori definiti in questi file devono essere separati da una tabulazione (`\t`). 


* `mapping_relations.tsv` deve avere 2 colonne, una delle due deve contenere valori testuali, l'altra dovrà contenere valori numerici interi. Deve contenere una riga col valore "like" nella colonna testuale. 
* `amar_test.tsv` e `amar_train.tsv` devono contenere 3 colonne, tutte con valori numerici interi. La prima dovrà indicare gli ID degli user, la seconda gli ID degli item, la terza gli ID delle relazioni.
* `kale_valid.tsv`, `kale_train.tsv` e `kale_test.tsv` devono contenere 3 colonne, tutte con valori numerici interi. La prima dovrà indicare gli ID degli user, la seconda gli ID delle relazioni, la terza gli ID degli item.