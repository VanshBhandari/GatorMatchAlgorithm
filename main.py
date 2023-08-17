import pyrebase

config = {
    "apiKey": "AIzaSyASKSo3NJUrUEkR8ltOgI_I25unncEa6rU",
    "authDomain": "gatormatch-d708d.firebaseapp.com",
    "databaseURL": "https://gatormatch-d708d-default-rtdb.firebaseio.com/",
    "projectId": "gatormatch-d708d",
    "storageBucket": "gatormatch-d708d.appspot.com",
    "messagingSenderId": "976155734088",
    "appId": "1:976155734088:web:136a3e41d50a2a4dfc287d",
    "measurementId": "G-291GWBJ786"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()

def matchmaker_single(user_id):
    match_scores = {}
    all_responses = database.child("responses").get().val()
    my_responses = all_responses[user_id]
    my_name = my_responses.get("What is your name?")
    my_gender_preference = my_responses.get("Do you have a gender preference?")
    my_gender = my_responses.get("What gender do you identify with?")
    for i in range(len(all_responses)):
        match_score = 0
        if all_responses[i] == all_responses[user_id]:
            continue
        else:
            other_responses = all_responses[i]
            other_name = other_responses.get("What is your name?")
            other_instagram = other_responses.get("Drop your instagram @")
            other_gender = other_responses.get("What gender do you identify with?")
            other_gender_preference = other_responses.get("Do you have a gender preference?")
            if my_gender_preference == other_gender:
                if other_gender_preference == my_gender:
                    match_score += 10
                elif other_gender_preference == "None":
                    match_score += 10  
        for question in my_responses.keys():
            if (other_responses.get(question) == my_responses.get(question)):
                match_score += 1
        match_scores[other_name] = [match_score, other_instagram]
    sorted_matches = (sorted(match_scores.items(),
                      key=lambda x: x[1], reverse=True)) 
    number_matches = len(sorted_matches)
    if number_matches<5:
        number_displayed_matches = number_matches
    else:
        number_displayed_matches = 5
    return my_name, sorted_matches[:number_displayed_matches]

def matchmaker_all():
    all_matches = []
    all_responses = database.child("responses").get().val()
    for i in range(len(all_responses)):
        all_matches.append(matchmaker_single(i))  
    global all_matches_dict
    all_matches_dict = dict(all_matches)

matchmaker_all()

data = all_matches_dict
database.child("Matches").set(data)

