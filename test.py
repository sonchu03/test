import pandas as pd
from scipy import spatial
import operator

movies = pd.read_csv('E:/python/KNN/KNNP2/TheMovieDB8000.csv')

# Preprocessing genres
movies['Genres'] = movies['Genres'].str.strip('[]').str.replace(' ','').str.replace("'",'')
movies['Genres'] = movies['Genres'].str.split(',')

# Preprocessing cast
movies['Cast'] = movies['Cast'].str.strip('[]').str.replace(' ','').str.replace("'",'').str.replace('"','')
movies['Cast'] = movies['Cast'].str.split(',')

# Preprocessing director
movies['Director'] = movies['Director'].fillna('')
movies['Director'] = movies['Director'].astype(str)

# Preprocessing keywords
movies['Keywords'] = movies['Keywords'].str.strip('[]').str.replace(' ','').str.replace("'",'').str.replace('"','')
movies['Keywords'] = movies['Keywords'].str.split(',')
def binary(genre_list):
    binaryList = []
    
    for genre in genreList:
        if genre in genre_list:
            binaryList.append(1)
        else:
            binaryList.append(0)
    
    return binaryList
# genres
for i, j in zip(movies['Genres'], movies.index):
    list2 = []
    if isinstance(i, list):
        list2 = i
        list2.sort()
    movies.loc[j, 'Genres'] = str(list2)
movies['Genres'] = movies['Genres'].str.strip('[]').str.replace(' ','').str.replace("'",'')
movies['Genres'] = movies['Genres'].str.split(',')
genreList = []
for index, row in movies.iterrows():
    genres = row["Genres"]
    
    for genre in genres:
        if genre != '' and genre not in genreList:
            genreList.append(genre)
movies['genres_bin'] = movies['Genres'].apply(lambda x: binary(x))

# cast
for i, j in zip(movies['Cast'], movies.index):
    list2 = []
    if not isinstance(i, float):
        list2 = i[:4]
    movies.loc[j, 'Cast'] = str(list2)
movies['Cast']=movies['Cast'].str.strip('[]').str.replace(' ','').str.replace("'",'')
castList = []
for index, row in movies.iterrows():
    cast = row["Cast"]
    
    for i in cast:
        if i not in castList:
            castList.append(i)
movies['cast_bin'] = movies['Cast'].apply(lambda x: binary(x))
# director
def xstr(s):
    if s is None:
        return ''
    return str(s)
movies['Director'] = movies['Director'].apply(xstr)
for i,j in zip(movies['Keywords'],movies.index):
    list2 = []
    list2 = i
    movies.loc[j,'Keywords'] = str(list2)
directorList=[]
for i in movies['Director']:
    if i not in directorList:
        directorList.append(i)
movies['director_bin'] = movies['Director'].apply(lambda x: binary(x))
# keywords
movies['Keywords'] = movies['Keywords'].str.strip('[]').str.replace(' ','').str.replace("'",'').str.replace('"','')
movies['Keywords'] = movies['Keywords'].str.split(',')
for i,j in zip(movies['Keywords'],movies.index):
    list2 = []
    list2 = i
    movies.loc[j,'Keywords'] = str(list2)
movies['Keywords'] = movies['Keywords'].str.strip('[]').str.replace(' ','').str.replace("'",'')
movies['Keywords'] = movies['Keywords'].str.split(',')
for i,j in zip(movies['Keywords'],movies.index):
    list2 = []
    list2 = i
    list2.sort()
    movies.loc[j,'Keywords'] = str(list2)
movies['Keywords'] = movies['Keywords'].str.strip('[]').str.replace(' ','').str.replace("'",'')
movies['Keywords'] = movies['Keywords'].str.split(',')
words_list = []
for index, row in movies.iterrows():
    genres = row["Keywords"]
    
    for genre in genres:
        if genre not in words_list:
            words_list.append(genre)
movies['words_bin'] = movies['Keywords'].apply(lambda x: binary(x))
# Function to calculate similarity between movies
def similarity(movie_id1, movie_id2):
    a = movies.iloc[movie_id1]
    b = movies.iloc[movie_id2]
    
    genreDistance = spatial.distance.cosine(a['genres_bin'], b['genres_bin'])
    scoreDistance = spatial.distance.cosine(a['cast_bin'], b['cast_bin'])
    directDistance = spatial.distance.cosine(a['director_bin'], b['director_bin'])
    wordsDistance = spatial.distance.cosine(a['words_bin'], b['words_bin'])
    
    return genreDistance + directDistance + scoreDistance + wordsDistance
    
new_id = list(range(0,movies.shape[0]))
movies['new_id']=new_id
movies=movies[['Title','Genres','Vote Average','genres_bin','cast_bin','new_id','Director','director_bin','words_bin']]
# Function to predict score for a given movie
def getNeighbors(baseMovie, K):
    distances = []

    for index, movie in movies.iterrows():
        if movie['new_id'] != baseMovie['new_id'].values[0]:
            dist = similarity(baseMovie['new_id'].values[0], movie['new_id'])
            distances.append((movie['new_id'], dist))

    distances.sort(key=operator.itemgetter(1))
    neighbors = []

    for x in range(K):
        neighbors.append(distances[x])
    return neighbors
def predict_score(name):
    new_movie = movies[movies['Title'].str.contains(name)].iloc[0].to_frame().T
    result = 'Selected Movie: ' + str(new_movie.Title.values[0]) + '\n'
    K = 10
    avgRating = 0
    neighbors = getNeighbors(new_movie, K)
        
    result += '\nRecommended Movies: \n'
    for neighbor in neighbors:
           avgRating = avgRating + movies.iloc[neighbor[0]][2]  
           result += movies.iloc[neighbor[0]][0] + " | Genres: " + str(movies.iloc[neighbor[0]][1]).strip('[]').replace(' ','') + " | Rating: " + str(movies.iloc[neighbor[0]][2]) + '\n'
        
    result += '\n'
    avgRating = avgRating / K
    result += 'The predicted rating for %s is: %f\n' % (new_movie['Title'].values[0], avgRating)
    result += 'The actual rating for %s is %f' % (new_movie['Title'].values[0], new_movie['Vote Average'])
    
    return result

# Example usage
#result = predict_score('The Baker')
#print(result)