"""
Preprocessing work :

1. Replace tabs with comma (,) in GvG Probabilities.
2. Convert that into csv by appending .csv to it.

Steps :

1. Read Batsman input from T1
2. Read Bowler input from T2

Loop :
	3. Determine their PvP Probabilities. 
	4. Determine their cluster numbers if PvP doesn't exist.
	5. Find GvG probability.
	6. RandomNumberGenerator of the array.
	7. Update Batsmen and Bowlers accordingly.
"""


import csv
import random

t1_bat_order = []
t1_bow_order = []
t2_bat_order = []
t2_bow_order = []
# tname = []

discrete_list = [0, 1, 2, 3, 4, 6, 7] # Here 7 refers to dismissal, Used for probability distribution.
									  # See method random_pick()



# Extraction of squads from the CSV and storing them in respective lists
with open('TestInputMatchNow.csv', 'r') as f:
	# print('input is proccessed\n')
	match_reader = csv.reader(f)
    #match_reader.next()
	for row in match_reader:
		t1_bat_order.append(row[0])
		t1_bow_order.append(row[1])
		t2_bat_order.append(row[2])
		t2_bow_order.append(row[3])
	t1_bat_order = [x for x in t1_bat_order if x != '']
	t1_bow_order = [x for x in t1_bow_order if x != '']
	t2_bat_order = [x for x in t2_bat_order if x != '']
	t2_bow_order = [x for x in t2_bow_order if x != '']
	t1_bow_order = t1_bow_order[:5] # Restricting to 5 bowlers
	t2_bow_order = t2_bow_order[:5]
print(t1_bat_order)
# print(t2_bat_order)
# print(t1_bow_order)
# print(t2_bow_order)

# To identify which cluster the batsman and bowler belong to.
def cluster_number(batsman, bowler) :
	# print('clusters are checked\n')
	# print(batsman,' ',bowler)
	# Determines respective batsman's cluster number
	with open('BatsmenCluster.csv', 'r') as f:
		# print('batcluster opened')
		bat_cluster_reader = csv.reader(f)
		for row in bat_cluster_reader:
			if batsman == row[0]:
				curr_bat_cluster_num = row[14]
				# print(type(curr_bat_cluster_num))
			else:
				curr_bat_cluster_num=str(random.randint(0,9))
				# print(type(curr_bat_cluster_num))
				# print(curr_bat_cluster_num)
				# print('bat found : ',curr_bat_cluster_num)


	# Determines respective bowler's cluster number
	with open('BowlerCluster.csv', 'r') as f:
		bow_cluster_reader = csv.reader(f)
		for row in bow_cluster_reader:
			if bowler == row[0]:
				curr_bow_cluster_num = row[13]
			else:
				curr_bow_cluster_num=str(random.randint(0,9))
				# print(curr_bow_cluster_num)
				# print('bowl found: ',curr_bow_cluster_num)

	return curr_bat_cluster_num, curr_bow_cluster_num


# Extract the corresponding row from PvP Probabilites file 
# Returns <Combo is existent or not>, <Probabilities list ('None' if it doesn't exist)>
def pvp_plist(batsman, bowler) :
	# print('pvp is called\n')
	pvp_check = False
	with open('PvP.csv', 'r') as f:
		pvp_reader = csv.reader(f)
		for row in pvp_reader:
			if batsman == row[0] and bowler == row[1]:
				pvp_check = True
				probs_list1 = row
			break
				
	if pvp_check :		
		probs_list = list(map(float, probs_list1))
		probs_list = probs_list[2:8]
		return pvp_check,probs_list
	else :
		return pvp_check,None
	
# Extract the corresponding row from GvG Probabilites file for non-existent combos
def gvg_plist(bat_cluster_number, bowler_cluster_number) :
	# print('gvg is called\n',bat_cluster_number,' ',bowler_cluster_number)
	with open('GvG.csv', 'r') as f:
		gvg_reader = csv.reader(f)
		for row in gvg_reader:
			if bat_cluster_number == row[0] and bowler_cluster_number == row[1]:
				probs_list1 = row[:-1]
				# print(row)
	probs_list = list(map(float, probs_list1))
	# print(probs_list)
	probs_list = probs_list[2:]
	return probs_list


# The Prediction
def random_pick(some_list, probabilities) :
	# print('random pick is called\n')
	x = random.uniform(0,sum(probabilities))
	cumulative_probability = 0.0
	for item, item_probability in zip(some_list, probabilities):
		cumulative_probability += item_probability
		if x < cumulative_probability: break
	return item


# def check(fir):



# Computation for every ball in an innings
# 'inn' refers to either first innings or second innings (1 or 2)
def innings(bat_order, bow_order, inn) : 
	# print('innings is called\n')
	tot_wickets = 0
	m = 1    # Index of current batsman (Will be swapped in loop)
	n = 0  # Index of standing batsman (Will be swapped in loop)

	# Assuming that only 5 players bowl
	# 20 elements. Each element represents which bowler has to bowl the respective over.

	bow_index_order = [0,1,0,1,2,3,4,2,3,4,2,3,4,2,3,4,0,1,0,1]  
	#bow_index_order=order
	x = bow_index_order[0]

	total_runs = 0
	k = -1

	for i in range(1,120) :

		# Swap batsmen and Change bowlers for every 6 balls
		if i%6 == 0 :
			k += 1
			x = bow_index_order[k]

			tmp_m = m
			m = n
			n = tmp_m

		curr_bat = bat_order[m] # Current Batsman
		other_bat = bat_order[n] # Standing Batsmangroovy song
		curr_bow = bow_order[x] # Current Bowler
		
		# Prediction
		existent, pvp_p_list = pvp_plist(curr_bat, curr_bow)  
		if existent :
			prediction = random_pick(discrete_list, pvp_p_list)
			# print('prediction of pvp: ',prediction)
		else :
			bat_c_num, bow_c_num = cluster_number(curr_bat, curr_bow)
			gvg_p_list = gvg_plist(bat_c_num, bow_c_num)
			prediction = random_pick(discrete_list, gvg_p_list)
			if(prediction==7):
				g='out'
			else:
				g=str(prediction)
			# print('prediction of gvg:',prediction)


			# print('ball ',i,' ',curr_bat,' v/s ',curr_bow,':',g,'::',' ',total_runs,'/',tot_wickets,'')
			# if(i%6==0 and i!=1):
			# 	print('\n')

		# If prediction is a dot ball or 2 runs or 4 runs or 6 runs
		if prediction==0 or prediction==2 or prediction==4 or prediction==6: 
			total_runs+=prediction 

		# If prediction is 1 run or 3 runs, Swap batsmen
		elif prediction==1 or prediction==3:
			total_runs+=prediction
			tmp_m = m
			m = n
			n = tmp_m
			
		# If prediction is a dismissal, Then arriving batsman replaces the current batsman
		else:
			tot_wickets+=1
			m=max(m,n) + 1

			# If they are all out
			if m > 10 :
				break
		
		# If it is second innings and if the team has chased the target
		if inn == 2 and total_runs > first_innings_score :
			break
			

	if inn == 1 :
		global first_innings_score1
		first_innings_score1 = total_runs
				
	num_of_overs_played = str(int((i+1)/6)) + "." + str((i+1)%6)  
	# print(total_runs,'  ',tot_wickets,'  ',num_of_overs_played)
	return total_runs, str(total_runs)+"/"+str(tot_wickets)+" Overs : "+ num_of_overs_played


# MAIN 

# print("Enter bowling order for first innings :\n")
# order=[]
# for x in range(1,21):
# 	y=int(input())
# 	z=y-1
# 	order.append(z)
total1=[]
total2=[]

for c in range(10):
	first_innings_score, formatted_score1 = innings(t1_bat_order, t2_bow_order, 1)
	total1.append(first_innings_score)

# print("Enter bowling order for second innings :\n")
# order=[]
# for x in range(1,21):
# 	y=int(input())
# 	z=y-1
# 	order.append(z)
	second_innings_score, formatted_score2 = innings(t2_bat_order, t1_bow_order, 2)
	total2.append(second_innings_score)
	print ("Team 1 Score : " + formatted_score1)
	print ("Team 2 Score : " + formatted_score2)
# print ("Team 1 Score : " + formatted_score1)
# print ("Team 2 Score : " + formatted_score2)
t1=sum(total1)/len(total1)
t2=sum(total2)/len(total2)
print(t1)
print(t2)

if t1 > t2 :
	print ("Team 1 wins!")
elif t2 > t1 :
	print ("Team 2 wins!")
else :
	print ("Match Tied.")