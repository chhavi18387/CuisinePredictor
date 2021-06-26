from tkinter import *
from tkinter.messagebox import *
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import metrics


def get_matrix(df,inputt):
	listt = df['ingredients']
	all_ingredients=[]
	for i in listt:
		j = ' '.join(i)
		all_ingredients.append(j)
	ingridentsss = ' '.join(inputt)
	all_ingredients.append(ingridentsss)
	tv = TfidfVectorizer(min_df=1)
	matrix = tv.fit_transform(all_ingredients)
	return matrix

def get_cuisine_type(df,matrix):
	
    
    labels = df['cuisine']
    matrix2 = matrix[:-1]
    
    vec= matrix[-1]
    clf = RandomForestClassifier()
    model=clf.fit(matrix2,labels)
    y_pred = clf.predict(vec)
    # print("Accuracy:",metrics.accuracy_score(matrix2,labels))
    return y_pred

def get_closely_related_cuisines(matrix,df,N):
    matrix2 = matrix[:-1]
    vec= matrix[-1]
    closely_related_cuisines_scores = cosine_similarity(vec,matrix2)
    sorted_closely_related_cuisines_scores = closely_related_cuisines_scores[0].argsort()[::-1][:N]
    closely_related_cuisines_scores_indices = [ (i,round(closely_related_cuisines_scores[0][i],4)) for i in sorted_closely_related_cuisines_scores ]
    ids = list(df['id'])
    cuisines = list(df['cuisine'])
    closest_cusines = []
    for i,j in closely_related_cuisines_scores_indices:
        closest_cusines.append((ids[i],j,cuisines[i]))
    return closest_cusines

df = pd.read_json('data.json')






























# GUI 

def show_answer():
    listt=ingredients.get().split(",")
    N_value=int(N.get())
    matrix = get_matrix(df,listt)
    ypred = get_cuisine_type(df,matrix)
    closest_cuisines=get_closely_related_cuisines(matrix,df,10)
    ans=ypred[0]
    cuisine_type.insert(0, ans)
    closest_cusines_output.insert(0,closest_cuisines)


main = Tk()
main.geometry("700x200")
main.title("CUISINE PREDICTOR")


Label(main, text = "Enter Ingredients:").grid(row=0,pady=10,padx=20)
Label(main, text = "Enter the Number of closely related cuisines to be shown in output:").grid(row=1,pady=10,padx=20)
Label(main, text = "Cuisine type:").grid(row=2,pady=10,padx=20)
Label(main, text = "Closest Cuisines:").grid(row=3,pady=10,padx=20)


ingredients = Entry(main)
N = Entry(main)
cuisine_type = Entry(main)
closest_cusines_output=Entry(main)


ingredients.grid(row=0, column=1,pady=10,padx=20)
N.grid(row=1, column=1,pady=10,padx=20)
cuisine_type.grid(row=2, column=1,pady=10,padx=20)
closest_cusines_output.grid(row=3, column=1,pady=10,padx=20)

Button(main, text='Quit', command=main.destroy).grid(row=4, column=0, sticky=W, pady=4)
Button(main, text='Show', command=show_answer).grid(row=4, column=1, sticky=W, pady=4,padx=20)

mainloop()