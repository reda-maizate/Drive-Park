from firebase import firebase
import datetime 



    
def envoi () :
    fbcon = firebase.FirebaseApplication('https://drivepark-61df6.firebaseio.com/')

    now = datetime.datetime.now()

    data_upload =  {
        'date'  : now.strftime("%Y-%m-%d à %H:%M"),
    }

    result = fbcon.get('/recipes/0/ingredients',None)

    lastIndex = len(result)

    result = fbcon.put('/recipes/0/ingredients/',lastIndex, now.strftime(" Vous vous êtes garé le %Y-%m-%d à %H:%M"))

    return 1

# envoi()