import pandas as pd
import csv
import numpy as np
import tensorflow as tf
from tensorflow import keras
from utils.arguments import AmieSettings, Arguments, KaleSettings, RulesFilter, AmarSettings
from utils.forEachEmbeddingDimension import forEachEmbeddingDimension
from utils.exceptions import AmarException
from utils.paths import getEntityIDFilePath, getMatrixEFilePath, getUserItemAmarTestFilePath, getUserItemAmarTrainFilePath, getPredictions1FilePath, getResultsFolderPath, getTopPredictionsFolderPath, getModelFilePath, getPredictions1FilePath

def top_scores(predictions,n):
  top_n_scores = pd.DataFrame()
  for u in list(set(predictions['users'])):
    p = predictions.loc[predictions['users'] == u ]
    top_n_scores = top_n_scores.append(p.head(n))
    #pd.concat([top_n_scores, p.head(n)])
  return top_n_scores

def read_ratings(filename):
  user=[]
  item=[]
  rating=[]
  #reading item ids
  with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    #next(csv_reader)
    for row in csv_reader:
        user.append(int(row[0]))
        item.append(int(row[1]))
        rating.append(int(row[2]))
  return user, item, rating
    
def read_kale_ratings(filename, folder):
    
  # load map dataset-matrix
  f_map = open(folder+"_map-dataset-matrix.txt", "r", encoding="utf-8")
  dataset_matrix = {}

  for line in f_map:
      
      dataset_value = line.split("\t")[0].strip()
      matrix_value = line.split("\t")[1].strip()
      
      dataset_matrix[dataset_value] = matrix_value

  f_map.close()


  user=[]
  item=[]
  rating=[]

  #reading item ids
  with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    #next(csv_reader)
    for row in csv_reader:
        if row[0] in dataset_matrix and row[1] in dataset_matrix:
            user.append(int(row[0]))
            item.append(int(row[1]))
            rating.append(int(row[2]))
  return user, item, rating

def read_kale_embeddings(datasetFolderName, kaleSettings: KaleSettings, amieSettings: AmieSettings, rulesFilter: RulesFilter, dimension: int):
  matrixEFilePath = getMatrixEFilePath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, dimension)
  entityIdPath = getEntityIDFilePath(datasetFolderName, kaleSettings)

  # load map dataset-matrix
  f_map = open(entityIdPath, "r", encoding="utf-8")
  #f_map = open(folder+"map.txt", "r", encoding="utf-8")
  dataset_matrix = {}

  for line in f_map:
      
      dataset_value = line.split("\t")[1].strip()
      matrix_value = line.split("\t")[0].strip()
      
      dataset_matrix[dataset_value] = matrix_value

  f_map.close()

  # open file
  f_in = open(matrixEFilePath, mode="r", encoding="utf-8")

  # read header
  header = f_in.readline().split(";")
  rows = int(header[0].split(":")[1].strip())
  columns = int(header[1].split(":")[1].strip())

  # matrix inizialization
  embeddings = np.zeros((rows, columns))
  row = 0
  col = 0

  # file reading and embeddings population
  for vector in f_in:
      emb = vector.split("\t")
      col = 0
      for value in emb:
          embeddings[row][col] = float(value)
          col += 1
      row += 1
      
  f_in.close()

  return embeddings, dataset_matrix
  


def matching_kale_emb_id(user, item, rating, embeddings, dataset_matrix):
  y = np.array(rating)
  dim_embeddings = len(embeddings[0])
  dim_X_cols = 2
  dim_X_rows = len(user)
  X = np.empty(shape=(dim_X_rows,dim_X_cols,dim_embeddings))

      
  #matching between ids and embeddings
  i=0
  c=0
  while i < dim_X_rows:

      # get user and item id
      user_id = user[i]
      item_id = item[i]
          
      if str(user_id) in dataset_matrix and str(item_id) in dataset_matrix:
          
          # get indeces of the matrix related to user and item from the map
          ind_user = int(dataset_matrix[str(user_id)])
          ind_item = int(dataset_matrix[str(item_id)])
              
          # get embeddings of user and item
          X[c][0] = embeddings[ind_user]
          X[c][1] = embeddings[ind_item]
          
          c += 1
          
      i=i+1
      
      
  return X, y, dim_embeddings

def isolate_kale_user_item_emb(users, items, graph_embeddings, dataset_matrix):

  embs = []
  i=0
  user_map = {}
  item_map = {}

  for usr in users:
    ind_u = int(dataset_matrix[str(usr)])
    embs.append(graph_embeddings[ind_u])
    user_map[usr] = i
    i+=1

  for itm in items:
    ind_i = int(dataset_matrix[str(itm)])
    embs.append(graph_embeddings[ind_i])
    item_map[itm] = i
    i+=1


  return embs, user_map, item_map


import tensorflow as tf
from tensorflow import keras

#from models.DataGenerator import DataGenerator as dg

# define the keras model
def run_model(X, y, dim_embeddings, epochs, batch_size):
  model = keras.Sequential()

  input_users = keras.layers.Input(shape=(dim_embeddings,))

  x1 = keras.layers.Dense(512, activation=tf.nn.relu)(input_users)
  x1_2 = keras.layers.Dense(256, activation=tf.nn.relu)(x1)
  x1_3 = keras.layers.Dense(128, activation=tf.nn.relu)(x1_2)

  input_items = keras.layers.Input(shape=(dim_embeddings,))

  x2 = keras.layers.Dense(512, activation=tf.nn.relu)(input_items)
  x2_2 = keras.layers.Dense(256, activation=tf.nn.relu)(x2)
  x2_3 = keras.layers.Dense(128, activation=tf.nn.relu)(x2_2)

  concatenated = keras.layers.Concatenate()([x1_3, x2_3])

  d1 = keras.layers.Dense(64, activation=tf.nn.relu)(concatenated)
  d2 = keras.layers.Dense(64, activation=tf.nn.relu)(d1)
  out = keras.layers.Dense(1, activation=tf.nn.sigmoid)(d2)

  model = keras.models.Model(inputs=[input_users,input_items],outputs=out)
  model.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9), metrics=['accuracy'])
  model.fit([X[:,0],X[:,1]], y, epochs=epochs, batch_size=batch_size)

  return model


import os
import pandas as pd
import numpy as np
import tensorflow as tf

def runAmar(datasetFolderName: str, rulesFilter: RulesFilter, kaleSettings: KaleSettings, amarSettings: AmarSettings, dimension: int, amieSettings: AmieSettings):
  try:
    # set input files and output files
    dest = getResultsFolderPath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, dimension)
    
    modelFilePath = getModelFilePath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, dimension)

    # create folders if needed
    if not os.path.exists(dest):
        os.makedirs(dest)
        print(f"New path: {dest}")
    
    # load kale embeddings for training and the map dataset -> matrix
    ent_embeddings, dataset_matrix = read_kale_embeddings(datasetFolderName, kaleSettings, amieSettings, rulesFilter, dimension)
    
    # read user-item/user-item-prop train set

    # user-item-prop train
    #user, item, rating = read_ratings('datasets/movielens/train2id.tsv')
    
    # user-item train
    user, item, rating = read_ratings(getUserItemAmarTrainFilePath(datasetFolderName))
    
    # match KALE ids with dataset ids
    X, y, dim_embeddings = matching_kale_emb_id(user, item, rating, ent_embeddings, dataset_matrix)
    
    print("\tEmbedding dimension: ", dim_embeddings)
    
    # run model
    batch = 512
    epo = 25
    model = run_model(X, y, dim_embeddings, epochs=epo, batch_size=batch)
        
    # creates a HDF5 file 'model.h5'
    model.save(modelFilePath)
    print(f"New file: {modelFilePath}")
    # load ratings to produce predictions

    # user-item-prop test
    #user, item, rating = read_ratings('datasets/movielens/test2id.tsv')
    
    # user-item test
    user, item, rating = read_ratings(getUserItemAmarTestFilePath(datasetFolderName))
    
    # select kale embeddings for predictions
    X, y, dim_embeddings = matching_kale_emb_id(user, item, rating, ent_embeddings, dataset_matrix)
    
    # predict   
    print("\tPredicting...")
    score = model.predict([X[:,0],X[:,1]])
    
    # write predictions
    print("\tComputing predictions...")
    score = score.reshape(1, -1)[0,:]
    predictions = pd.DataFrame()
    predictions['users'] = np.array(user)
    predictions['items'] = np.array(item)
    predictions['scores'] = score
    
    predictions = predictions.sort_values(by=['users', 'scores'],ascending=[True, False])

    for k in amarSettings.topK:
      topFolderPath = getTopPredictionsFolderPath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, dimension, k)

      if not os.path.exists(topFolderPath):
          os.makedirs(topFolderPath)
          print(f"New path: {topFolderPath}")

      topPredictionsFilePath = getPredictions1FilePath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, dimension, k)

      topScores = top_scores(predictions, k)
      topScores.to_csv(topPredictionsFilePath, sep='\t',header=False,index=False)
      print(f"New file: {topPredictionsFilePath}")
  except Exception as e:
      raise AmarException("a generic error occured", e)

if __name__ == "__main__":
  parser = Arguments()
  
  parser.addAmieSettingsOptionalArguments()
  parser.addRulesFilterArguments()
  parser.addKaleSettingsArguments()
  parser.addAmarSettingsArguments()

  (datasetFolderName, args) = parser.parse()

  amieSettings = AmieSettings(args)
  rulesFilter = RulesFilter(args)
  kaleSettings = KaleSettings(args)
  amarSettings = AmarSettings(args)

  forEachEmbeddingDimension(kaleSettings, lambda kaleSettings, dim: runAmar(datasetFolderName, rulesFilter, kaleSettings, amarSettings, dim, amieSettings))