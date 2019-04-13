import csv,json
import collections

class Probabilities:
	def __init__(self,p_0, p_1, p_2, p_3, p_4, p_6, p_out):
		self.counter = 1
		self.p_0 = p_0
		self.p_1 = p_1
		self.p_2 = p_2
		self.p_3 = p_3
		self.p_4 = p_4
		self.p_6 = p_6
		self.p_out = p_out		
	
	def add_p_0(self,p):
		self.p_0 += p

	def add_p_1(self,p):
		self.p_1 += p

	def add_p_2(self,p):
		self.p_2 += p

	def add_p_3(self,p):
		self.p_3 += p

	def add_p_4(self,p):
		self.p_4 += p

	def add_p_6(self,p):
		self.p_6 += p

	def add_p_out(self,p):
		self.p_out += p

	def increment_count(self):
		self.counter += 1

	def get_count(self):
		return str(self.counter)

	def get_p_0(self):
		return self.p_0

	def get_p_1(self):
		return self.p_1
	
	def get_p_2(self):
		return self.p_2
	
	def get_p_3(self):
		return self.p_3
	
	def get_p_4(self):
		return self.p_4
	
	def get_p_6(self):
		return self.p_6
	
	def get_p_out(self):
		return self.p_out

	def get_st(self):
		return str(self.p_0/self.counter) + ','+ str(self.p_1/self.counter) + ','+ str(self.p_2/self.counter) + ','+ str(self.p_3/self.counter) + ','+ str(self.p_4/self.counter) + ',' + str(self.p_6/self.counter) + ',' + str(self.p_out/self.counter)

#End of class Probabilities
#Player,Pos,Mat,Inns,NO,Runs,HS,Avg,BF,SR,Hundreds,Fifties,Fours,Sixes,CLUSTER - Batsman Cluster Format
class Player:
	def __init__(self, type, name, cluster_id):
		self.name = name
		self.cluster_id = cluster_id
		self.type = type

	def __str__(self):
		return str(self.cluster_id)[0:-1] + ',' + str(self.type) + ',' + str(self.name)

def get_cluster_set(line, category):
	cluster_set = set()
	extracts = line.split(',')
	cluster_set.add(Player(category, extracts[0],int(extracts[-1])))
	return cluster_set

batting_cluster_list = list()
bowling_cluster_list = list()

with open('BatsmenCluster.csv', 'r', newline='\n') as batting_file:
	for row in batting_file:
		extracts = row.split(',')
		if len(batting_cluster_list) > int(extracts[-1]):
			batting_cluster_list[int(extracts[-1])].add(Player('Batsman', extracts[0], extracts[-1]))
			#print('Added batsman {} to existing set'.format(extracts[0]))
		else:
			batting_cluster_list.append(get_cluster_set(row, 'Batsman'))
			#print('++Added batsman {} to new set'.format(extracts[0]))

with open('BowlerCluster.csv', 'r', newline='\n') as bowling_file:
	for row in bowling_file:
		extracts = row.split(',')
		if len(bowling_cluster_list) > int(extracts[-1]):
			bowling_cluster_list[int(extracts[-1])].add(Player('Bowler', extracts[0], extracts[-1]))
			#print('Added bowler {} to existing set'.format(extracts[0]))
		else:
			bowling_cluster_list.append(get_cluster_set(row, 'Bowler'))
			#print('==Added bowler {} to new set'.format(extracts[0]))
# with open('test.csv','w',newline='\n') as test:

#Main cluster dict
cluster_dict = {}
batsman = 'plhba'
bowler = 'plhbo'
with open('PvP.csv', 'r', newline='\n') as pvp_probabilities:
	# count=0
	c=0
	for row in pvp_probabilities:
		
		line = row.split(',')
		
		if(line[0]==''):
			continue
		# print((line[2]))
		# print(line)
		c+=1
		for batting_cluster in batting_cluster_list:
			for player in batting_cluster:
				#print('Batsman', line[0], player.name)
				if line[0] == player.name:
					#print('Batsman loop:', player)
					batsman = player.cluster_id
				# else:
				# 	print('nope')
				# 	break
					# print('Batsman {} found on line {}'.format(line[0], line))
		for bowling_cluster in bowling_cluster_list:
				for player in bowling_cluster:
					#print('Bowler', line[0], player.name)
					if line[1] == player.name:
						#print('Bowler loop:', player)
						bowler = player.cluster_id
						# print('Bowler {} found on line {}'.format(line[1], line))
		# if(int(batsman)<0 or int(batsman)>9):
		# 	print(heyeyeyeyye)
		# 	break
		# if(int(bowler)<0 or int(bowler)>9):
		# 	print(heyeyeyeyye)
		# 	break
		index_string = str(batsman)[0:-1] + ',' + str(bowler)[0:-1]
		# if (int(bowler)):
		# 	print(batsman)
		if not(len(str(index_string)))==3:
			# print(index_string)
			continue
		# print(f'Index string {index_string}',len(str(index_string)))
		#Order: Batsman, Bowler, p(0), p(1), p(2), p(3), p(4), p(6), p(out), balls_faced
		if cluster_dict.__contains__(index_string):
			cluster_dict[index_string].add_p_0(float(line[2]))
			cluster_dict[index_string].add_p_1(float(line[3]))
			cluster_dict[index_string].add_p_2(float(line[4]))
			cluster_dict[index_string].add_p_3(float(line[5]))
			cluster_dict[index_string].add_p_4(float(line[6]))
			cluster_dict[index_string].add_p_6(float(line[7]))
			cluster_dict[index_string].add_p_out(float(line[8]))
			cluster_dict[index_string].increment_count()
			# print('Added to existing index {}'.format(index_string))
		else:
			cluster_dict[index_string] = Probabilities(
			                                           float(line[2]),
			                                           float(line[3]),
			                                           float(line[4]),
			                                           float(line[5]),
			                                           float(line[6]),
			                                           float(line[7]),
			                                           float(line[8]))
	# print(c)

cluster_dict2={}
for di,va in cluster_dict.items():
	cluster_dict2[di]=cluster_dict[di]
	# print(cluster_dict[di].get_st())
	# print(cluster_dict[index_string].get_st())
for div,va in cluster_dict.items():
	cluster_dict2[div]=cluster_dict[div].get_st()
	



with open('GvG.csv', 'w', newline='\n') as csvfile:
	# cluster_dict1=cluster_dict
	x=[]
	# print(cluster_dict['1,1'].get_p_0())
	# cluster_dict1=cluster_dict
	print(type(cluster_dict2))
	cluster_dict1 = dict(sorted(cluster_dict2.items()))
	for key,v in cluster_dict1.items():
 		l=[]
 		# print(key)
 		v1=v.split(',')
 		# print(v1[0])

 		# print(len(key))
 		l.append(key[0])
 		if(len(key)==3):
 				l.append(key[2])
 		else:
 			continue
 		l1=l+v1
 		# print(xk0,xk1)
 		x.append(l1)
	for i in x:
 		for c in i:
 			csvfile.write(str(c) +',')
 		csvfile.write('\n')




