import csv
import random

t1_bat=[]
t1_bow=[]
t2_bat=[]
t2_bow=[]
team=[]
com=[]

def do(hey,type1=None):
	l=[]
	h=-1
	if(type1=='venue'):
		h=venue_encoder.transform([hey])[0]
        #print(type(h))
	if(type1=='Team1'):
		try:
			h=Team1_encoder.transform([hey])[0]
		except ValueError:
			h=random.randint(0,465)
		else:
			h=Team1_encoder.transform([hey])[0]

	if(type1=='Team2'):
		try:
			h=Team2_encoder.transform([hey])[0]
		except ValueError:
			h=random.randint(0,465)
		else:
			h=Team2_encoder.transform([hey])[0]

	if(type1=='bat1'):
		try:
			h=ba1_encoder.transform([hey])[0]
		except ValueError:
			h=random.randint(0,465)
		else:
			h=ba1_encoder.transform([hey])[0]

	if(type1=='bat2'):
		try:
			h=ba2_encoder.transform([hey])[0]
		except ValueError:
			h=random.randint(0,465)
		else:
			h=ba2_encoder.transform([hey])[0]

	if(type1=='bow'):
		try:
			h=bo_encoder.transform([hey])[0]
		except ValueError:
			h=random.randint(0,465)
		else:
			h=bo_encoder.transform([hey])[0]

	if(h!=-1):
		l.append(h)
		return l
	else:
		if(type1=='ball'):
			l.append(float(hey))
			return l
		else:
			l.append(int(hey))
			return l

with open('simulate_team35.csv', 'r') as f:
	reader = csv.reader(f)
	for row in reader:
		if(row[0]=='venue'):
			venue=row[1]
			continue
		if(row[0]=='teams'):
			team.append(row[1])
			team.append(row[2])
			continue
		t1_bat.append(row[0])
		t1_bow.append(row[1])
		t2_bat.append(row[2])
		t2_bow.append(row[3])
	t1_bat = [x for x in t1_bat if x != '']
	t1_bow = [x for x in t1_bow if x != '']
	t2_bat = [x for x in t2_bat if x != '']
	t2_bow = [x for x in t2_bow if x != '']
	com.append(do(venue,'venue'))

def bat(batsman):
	# print(type(batsman))
	with open('BatsmenCluster.csv','r') as f:
		countba=0
		for r in f:
			e=r.split(',')
			# print(e[0])
			x=e[0].split(' ')
			# print(x)
			y=batsman.split(' ')
			# print(y)
			if(y[0][0]==x[0][0] and y[-1]==x[-1]):
				countba+=1
				return e[14][:-1],True
		if(countba==0):
			return str(random.randint(0,9)),False
def bow(bowler):
	with open('BowlerCluster.csv','r') as f:
		countbo=0
		for r in f:
			e=r.split(',')
			x=e[0].split(' ')
			y=bowler.split(' ')
			if(y[0][0]==x[0][0] and y[-1]==x[-1]):
				countbo+=1
				return e[13][:-1],True
		if(countbo==0):
			return str(random.randint(0,9)),False

def prediction(d):
	
	df = pd.DataFrame.from_dict(d)
    #print(df)
	return tree1.predict(df)[0]
    

def inn(bat_order, bow_order, inn) : 
	tot_wickets = 0
	m = 1  
	n = 0  
	bow_index_order = [1,0,0,1,2,3,4,2,3,4,2,3,4,2,3,4,1,0,1,0]  
	x = bow_index_order[0]
	total_runs = 0
	
	k = -1
	final=[]
	
	keyss=['venue','inns','ball','Team1','Team2','bat1','bat2','bow','batclus1','batclus2','bowclus']
	for i in range(0,120) :
		values=[]
		values.append(do(inn))
		over1=str(int((i/6))+1)
		over2=str(int(i%6)+1)
		over=over1+'.'+over2
		#print(over)
		values.append(do(over,'ball'))
		values.append(do(team[0],'Team1'))
		values.append(do(team[1],'Team2'))

		if((i)%6 == 0) and (i!=0) :
			k += 1
			x = bow_index_order[k]

			tmp_m = m
			m = n
			n = tmp_m

		curr_bat = bat_order[m]
		other_bat = bat_order[n] 
		curr_bow = bow_order[x] 
        
		batid1,yba1=bat(curr_bat)
		batid2,yba2=bat(other_bat)
		bowid,ybo=bow(curr_bow)
		if(yba1):
			values.append(do(curr_bat,'bat1'))
		else:
			values.append(do(random.randint(0,465)))
		if(yba2):
			values.append(do(other_bat,'bat2'))
		else:
			values.append(do(random.randint(0,465)))
		if(ybo):
			values.append(do(curr_bow,'bow'))
		else:
			values.append(do(random.randint(0,330)))
        
		values.append(do(batid1))
		values.append(do(batid2))
		values.append(do(bowid))
		final=com+values
		#print(final)
		dd={k:v for k,v in zip(keyss,final)}
		#print(dd)
		predict=prediction(dd)
		if predict==0.0 or predict==2.0 or predict==4.0 or predict==6.0: 
			total_runs+=predict 

		elif predict==1.0 or predict==3.0 or predict==7.0:
			total_runs+=predict
			tmp_m = m
			m = n
			n = tmp_m
			
		elif predict==-1.0:
			tot_wickets+=1
			m=max(m,n) + 1

			if m > 10 :
				break
		
		if inn == 2 and total_runs > first_score :
			break
			

	if inn == 1 :
		global first_innings_score1
		first_innings_score1 = total_runs
	return total_runs, str(total_runs)+"/"+str(tot_wickets)+" Overs : "+ str(float(over)-1)
		#print(curr_bat,',',other_bat,',',curr_bow)

first_score,ffs = inn(t1_bat, t2_bow, 1)
second_score,fsc = inn(t2_bat, t1_bow,2)
print(first_score,' ',ffs)
print(second_score,' ',fsc)

if(first_score>second_score):
	print(team[0],' Wins')
elif(first_score<second_score):
	print(team[1],' Wins')
else:
	print('Draw')
