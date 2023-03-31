from django.http import HttpResponse , HttpResponseRedirect
from django.template import loader
from .models import Members
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from sklearn.datasets import make_classification
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import classification_report
import os
import matplotlib.pyplot as plt
import json
from django.contrib import messages
ans = dict()

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({},request))

def signup(request):
    template = loader.get_template('signup.html')
    return HttpResponse(template.render({},request))

def adddetail(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        cnfpassword = request.POST['cnfpassword']
        fullname = request.POST['fullname']
        dob = request.POST['dob']
        num = request.POST['num']
        gender = request.POST['gender']

        if password != cnfpassword:
            return HttpResponseRedirect('../?error=passwordcheck')
        else:
            memberEmail = Members.objects.filter(email = email) 
            if memberEmail.exists():
                return HttpResponseRedirect('../?emailalreadyexists')   
            else:
                memberAdd = Members(email=email,password=password,cnfpassword=cnfpassword,fullname=fullname,dob=dob,num=num,gender=gender)
                memberAdd.save()
                return HttpResponseRedirect('../?usercreated')

                
def logininc(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            member = Members.objects.get(email = email)
            if member.password != password:
                return HttpResponseRedirect('../?passwordwrong')
            else:
                global ans
                ans={
                    'userdetail':member,
                }
                return redirect('dashboard/')
        except ObjectDoesNotExist:
                return HttpResponseRedirect('../?userdoesnotexist')
        
def dashboard(request):
    template = loader.get_template('dashboard.html')
    return HttpResponse(template.render({},request))

def bmipage(request):
    template = loader.get_template('bmipage.html')
    return HttpResponse(template.render({},request))

def home(request):
    return render(request,"home.html")

def result(request):
    global ans
    symptoms = []

    symptoms.append(request.POST['s1'])
    symptoms.append(request.POST['s2'])
    symptoms.append(request.POST['s3'])
    symptoms.append(request.POST['s4'])
    symptoms.append(request.POST['s5'])

    ans['symptom1']=request.POST['s1']
    ans['symptom2']=request.POST['s2']
    ans['symptom3']=request.POST['s3']
    ans['symptom4']=request.POST['s4']
    ans['symptom5']=request.POST['s5']

    import numpy as np
    import pandas as pd
    import warnings

    warnings.filterwarnings("ignore")

    #medical_data = {}

    #medicines = [[],[],[]]

    #below code import json array file for symptom
    fO = open("\home\prashant\Downloads\majorProject-20221209T161659Z-001\majorProject\majorProjectApp\symptom.json")
    l1=json.load(fO)
    #convert into python list 


    #below code import json array file for disease
    fO1 = open("\home\prashant\Downloads\majorProject-20221209T161659Z-001\majorProject\majorProjectApp\symptom.json")
    disease=json.load(fO1)
    #convert into python list
            
    # for i in range(len(disease)):
    #     medical_data[disease[i]] = medicines[i]
    

    medicine ={
                'Fungal infection':['clotrimazole','econazole'],
                'Allergy':['Cetrizine','Loratradine'],
                'GERD':['esomeprazole','Iansprozole'],
                'Chronic cholestasis':['Actigall','Urso'],
                'Drug Reaction':['Antihistamines','Corticosteroids'],
                'Peptic ulcer diseae':['omeprazole','patoprazole'],
                'AIDS':['abacavir','emtricitabine'],
                'Diabetes':['fortamet','glumetza'],
                'Gastroenteritis':[ 'Pedialyte','BRAT diet'],
                'Bronchial Asthma':['Theophylline','budesonide'],
                'Hypertension':['Pronivil','Zestril'],
                'Migraine':['sumatriptan','Dihydroergotamine'],
                'Cervical spondylosis':['ibuprofen','naproxen sodium'],
                'Paralysis (brain hemorrhage)':['anti-anxiety drugs','anti-epileptic drugs'],
                'Jaundice':['Ceftriaxone','cholestyramine'],
                'Malaria':['Qualaquin','vibramycin'],
                'Chicken pox':['Sitavig','Zovirax'],
                'Dengue':['acetaminophen','tramadol'],
                'Typhoid':['ciprofloxacin','ampicillin'],
                'Hepatitis A':['Manage nausea.','Avoid alcohol and use medications with care.'],
                'Hepatitis B':['Entecavir (Baraclude)','Interferon injections'],
                'Hepatitis C':['Entecavir (Baraclude)','tenofovir (Viread)'],
                'Hepatitis D':['Entecavir (Baraclude)','lamivudine (Epivir)'],
                'Hepatitis E':['Entecavir (Baraclude)','adefovir (Hepsera) '],
                'Alcoholic Hepatitis':['quitting drinking','consulting therapies to ease the signs and symptoms of liver damage'],
                'Tuberculosis':['rifampicin','isoniazid'],
                'Common Cold':['Antihistamines','codeine'],
                'Pneumonia':['ibuprofen','acetaminophen'],
                'Dimorphic hemmorhoids(piles)':['acetaminophen','aspirin'],
                'Heartattack':['Nitroglycerin','Morphine'],
                'Varicoseveins':['Self-care — such as exercise, raising the legs when sitting or lying down, or wearing compression stockings','Wearing compression stockings all day'],
                'Hypothyroidism':['methimazole','propylithiouracil'],
                'Hyperthyroidism':['methimazole','propylithiouracil'],
                'Hypoglycemia':['Eat or drink 15 to 20 grams of fast-acting carbohydrates. ','Recheck blood sugar levels 15 minutes after treatment.'],
                'Osteoarthristis':['acetaminophen','duloxetine hydrochloride'],
                'Arthritis':['ibuprofen','naproxen sodium'],   
                '(vertigo) Paroymsal  Positional Vertigo':['Canalith repositioning','Surgical alternative'],
                'Acne':['tretinoin','adapalene'],
                'Urinary tract infection':['Trimethoprim/sulfamethoxazole','Fosfomycin'],
                'Psoriasis':['Corticosteroids','calcipotriene'],
                'Impetigo':['amoxicillin/clavulanate (Augmentin)','clindamycin (Cleocin)']
    } 

    #below code import json object file for disease link
    fileOpen = open(r"C:\Users\Public\Documents\eightsem\majorProject\majorProjectApp\diseaseLink.json")
    link=json.load(fileOpen)
    #convert into python dict 

    l2 = []

    for i in range(0,len(l1)):
        l2.append(0)

    df=pd.read_csv("majorProjectApp\Prototype.csv")

    df.replace({'prognosis':{'Fungal infection':0,'Allergy':1,'GERD':2,'Chronic cholestasis':3,'Drug Reaction':4,
    'Peptic ulcer diseae':5,'AIDS':6,'Diabetes ':7,'Gastroenteritis':8,'Bronchial Asthma':9,'Hypertension ':10,
    'Migraine':11,'Cervical spondylosis':12,
    'Paralysis (brain hemorrhage)':13,'Jaundice':14,'Malaria':15,'Chicken pox':16,'Dengue':17,'Typhoid':18,'hepatitis A':19,
    'Hepatitis B':20,'Hepatitis C':21,'Hepatitis D':22,'Hepatitis E':23,'Alcoholic hepatitis':24,'Tuberculosis':25,
    'Common Cold':26,'Pneumonia':27,'Dimorphic hemmorhoids(piles)':28,'Heart attack':29,'Varicose veins':30,'Hypothyroidism':31,
    'Hyperthyroidism':32,'Hypoglycemia':33,'Osteoarthristis':34,'Arthritis':35,
    '(vertigo) Paroymsal  Positional Vertigo':36,'Acne':37,'Urinary tract infection':38,'Psoriasis':39,
    'Impetigo':40}},inplace=True)

    X= df[l1]

    y = df[["prognosis"]]
    
    tr=pd.read_csv("majorProjectApp\Prototype_1.csv")

    tr.replace({'prognosis':{'Fungal infection':0,'Allergy':1,'GERD':2,'Chronic cholestasis':3,'Drug Reaction':4,
    'Peptic ulcer diseae':5,'AIDS':6,'Diabetes ':7,'Gastroenteritis':8,'Bronchial Asthma':9,'Hypertension ':10,
    'Migraine':11,'Cervical spondylosis':12,
    'Paralysis (brain hemorrhage)':13,'Jaundice':14,'Malaria':15,'Chicken pox':16,'Dengue':17,'Typhoid':18,'hepatitis A':19,
    'Hepatitis B':20,'Hepatitis C':21,'Hepatitis D':22,'Hepatitis E':23,'Alcoholic hepatitis':24,'Tuberculosis':25,
    'Common Cold':26,'Pneumonia':27,'Dimorphic hemmorhoids(piles)':28,'Heart attack':29,'Varicose veins':30,'Hypothyroidism':31,
    'Hyperthyroidism':32,'Hypoglycemia':33,'Osteoarthristis':34,'Arthritis':35,
    '(vertigo) Paroymsal  Positional Vertigo':36,'Acne':37,'Urinary tract infection':38,'Psoriasis':39,
    'Impetigo':40}},inplace=True)

    X_test= tr[l1]
    y_test = tr[["prognosis"]]
    # ------------------------------------------------------------------------------------------------------

    def DecisionTree():
        from sklearn import tree
        c = 0
        clf3 = tree.DecisionTreeClassifier() 
        clf3 = clf3.fit(X,np.ravel(y))
        decision_count = 0
        from sklearn.metrics import accuracy_score
        y_pred_des=clf3.predict(X_test)
        plot_confusion_matrix(clf3, X_test, y_test)
        my_path = os.path.abspath(__file__)
        my_path = my_path[:-8] + "static\img"
        #print(my_path)
        plt.savefig(my_path + "\Plot.png")
        psymptoms = symptoms

        for k in range(0,len(l1)):
            for z in psymptoms:
                if(z==l1[k]):
                    l2[k]=1

        inputtest = [l2]
        predict = clf3.predict(inputtest)
        # print(classification_report(y_test, y_pred_des, target_names=disease))
        predicted=predict[0]
        temp = X_test.iloc[predicted]

        for i in temp:
            if l2[c] == i:
                decision_count += 1
            c += 1
        print(round(((decision_count/95)*100),2))
        h='no'
        for a in range(0,len(disease)):
            if(predicted == a):
                h='yes'
                break

        if (h=='yes'):
            ans['Decision_Tree'] = disease[a]
            ans['Decision_Percentage'] =round(((decision_count/95)*100),2)
        else:
            ans['Decision_Tree'] = "Not Found"
        return decision_count


    def randomforest():
        from sklearn.ensemble import RandomForestClassifier
        clf4 = RandomForestClassifier()
        clf4 = clf4.fit(X,np.ravel(y))
        random_count = 0
        c = 0
        y_pred_res=clf4.predict(X_test)
        
        psymptoms = symptoms

        for k in range(0,len(l1)):
            for z in psymptoms:
                if(z==l1[k]):
                    l2[k]=1

        inputtest = [l2]

        predict = clf4.predict(inputtest)
        predicted=predict[0]
        #print(classification_report(y_test, y_pred_res, target_names=disease))
        plot_confusion_matrix(clf4, X_test, y_test)
        my_path = os.path.abspath(__file__)
        my_path = my_path[:-8] + "static\img"
        #print(my_path)
        plt.savefig(my_path + "\Plot1.png")  
        psymptoms = symptoms
        temp = X_test.iloc[predicted]

        for i in temp:
            if l2[c] == i:
                random_count += 1
            c += 1
        print(round(((random_count/95)*100),2))

        h='no'
        for a in range(0,len(disease)):
            if(predicted == a):
                h='yes'
                break

        if (h=='yes'):
            ans['Random_Forest'] = disease[a]
            ans['Random_Percentage'] =round(((random_count/95)*100),2)
        else:
            ans['Random_Forest'] = "Not Found"
        return random_count

    def NaiveBayes():
        from sklearn.naive_bayes import GaussianNB
        gnb = GaussianNB()
        gnb=gnb.fit(X,np.ravel(y))

        from sklearn.metrics import accuracy_score
        y_pred=gnb.predict(X_test)

        psymptoms = symptoms
        for k in range(0,len(l1)):
            for z in psymptoms:
                if(z==l1[k]):
                    l2[k]=1

        inputtest = [l2]
        predict = gnb.predict(inputtest)
        predicted=predict[0]
        temp = X_test.iloc[predicted]
        naive_count = 0
        c = 0
        for i in temp:
            if l2[c] == i:
                naive_count += 1
            c += 1
        print(round(((naive_count/95)*100),2))
        # print(classification_report(y_test, y_pred, target_names=disease))
        plot_confusion_matrix(gnb, X_test, y_test) 
        my_path = os.path.abspath(__file__)
        my_path = my_path[:-8] + "static\img"
        #print(my_path)
        plt.savefig(my_path + "\Plot2.png") 
        psymptoms = symptoms
        
        h='no'
        for a in range(0,len(disease)):
            if(predicted == a):
                h='yes'
                break

        if (h=='yes'):
            ans['Naive_Bayes'] = disease[a]
            ans['Naive_Percentage'] =round(((naive_count/95)*100),2)
        else:
            ans['Naive_Bayes'] = "Not Found"
        return naive_count
    decision_result=DecisionTree()
    random_result=randomforest()
    naive_result=NaiveBayes()
    #print(decision_result)
    #print(random_result)
    #print(naive_result)
    maxi=0
    #print(prediction_ans)
    if(decision_result>maxi):
        maxi=decision_result
    if(random_result>maxi):
        maxi=random_result
    if(naive_result>maxi):
        maxi=naive_result
    if(decision_result == random_result):
        ans['main']=ans['Decision_Tree']
    elif(decision_result == naive_result):
        ans['main']=ans['Decision_Tree']
    elif(random_result == naive_result):
        ans['main']=ans['Random_Forest']
    else:
        if(maxi==decision_result):
            ans['main']=ans['Decision_Tree']
        elif(maxi==random_result):
            ans['main']=ans['Random_Forest']
        else:
            ans['main']=ans['Naive_Bayes']


    key=ans['main']
    if key in medicine.keys():
        ans['medicine1']=medicine[key][0]
        ans['medicine2']=medicine[key][1]
    
    if key in link.keys():
        ans['indirect']=link[key]
    
    #print(ans['indirect'])
    #print(ans['userdetail'].email)
    
        
    return render(request,"result.html",ans)


        
        


