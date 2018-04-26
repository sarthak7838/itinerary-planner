city=["Jaipur, Rajasthan", "Jaisalmer, Rajasthan", "Jodhpur, Rajasthan","Ajmer, Rajasthan","Udaipur, Rajasthan"]
city1=["Jaipur, Rajasthan, India","Jaisalmer, Rajasthan 345001, India", "Jodhpur, Rajasthan, India","Ajmer, Rajasthan, India","Udaipur, Rajasthan, India"]
name=[
		['Machine Learning Coursera','Machne Learning, Udacity','Machine Learning Udemy','Machine Learning Class-Central','Machine Learning edX','Master Machine Learning on Python & R','Machine Learning Coding Blocks'],
		['Introduction to Cyber Security Specialization, Coursera','Cybersecurity and Mobility','Cybersecurity Nanodegree Udacity','The Complete Cyber Security Course : Network Security!','Cyber Security Economics'],
		['Bioinformatics Specialization,Coursera','Statistical Analysis in Bioinformatics','Tales from the Genome Udacity','DNA Research using Biopython','Learn Bioinformatics in 6 Days,Udemy'],
		['Cryptography I','Applied Cryptography Udacity','Mathematical Cryptography - Crack The Code','Blockchain & Cryptography Courses edX'],
		['Data Structures and Algorithms Specialization,Coursera','Algorithms, Part I','Algorithms, Part II','Intro to Algorithms','Learning Data Structures and Algorithms,Udemy ']
		
		]
dist =[[0, 560, 350, 135,400],
		[560, 0, 290, 480, 530],
		[350, 290, 0, 200, 260],
		[135, 480, 200, 0, 265],
		[400, 530, 260, 265, 0]
		]

time=[[0, 9.5, 6, 2.5,6.5],
		[9.5, 0,  4.5, 8, 8.5],
		[6, 4.5, 0, 4, 5],
		[2.5, 8, 4, 0, 4.5],
		[6.5, 8.5, 5, 4.5, 0]
		]
cnt=[7,5,5,4,5]
vis_time=[10,8,4,3,5]

def suggest(prob_mat):
	sugg_places=[]
	sugg_cities=[]
	pref=[0,0,0,0,0]
	prob_arr=[0,0,0,0,0]
	for i in range(0,5):
		for j in range(0,cnt[i]):
			if prob_mat[i,j]>0.5:
				sugg_places.append(name[i][j])
			if prob_mat[i,j]!=0:
				prob_arr[i]+=2*prob_mat[i,j]-1
		if prob_arr[i]>0:
			sugg_cities.append(i)
	print(prob_arr)
	pp=[]
	for i in range(5):
		x=-10
		xi=0
		for j in range(len(prob_arr)):
			if j not in pp:
				if x<prob_arr[j]:
					x=prob_arr[j]
					xi=j
		pref[xi]=5-i
		pp.append(xi)

	return {'sugg_places':sugg_places,'sugg_cities':sugg_cities, 'pref':pref}
	# max_prob=prob_arr[0]
	# max_ind=0
	# for i in (1,5):
	# 	if prob_arr[i]>max_prob:
	# 		max_prob=prob_arr[i]
	# 		max_ind=i
# def middle(a,b):
# 	c=[b[0] for b in rows]
# 	d=[0,0,0,0,0]
# 	for x in c:
# 		d[c]=d[c]+1





def grph(b,days,pref):
	global vis_time,time,city,dist,cnt
	st=0
	en=0
	su=0
	while days<2*len(b)-1:
		mini=pref[0]
		minin=0
		for i in range(len(pref)):
			if mini<pref[i]:
				mini=pref[i]
				minin=i
		del b[minin]
		pref.remove(mini)
	while 3*len(b)<days:
		for i in range(5):
			if i not in b:
				b.append(i)
				break
	# for i in b:
	# 	su+=vis_time[i]
	# ma=sum
	# for i in b:
	# 	if vis_time[i]<ma:
	# 		ma=vis_time[i]
	for i in range(0,5):
		if i in b:
			st=i;
			mi=0
			pos=i
			for j in range(i+1,5):
				if j in b:
					if mi<time[i][j]:
						pos=j
						mi=time[i][j]
			en=pos;
			break;
	start=city[st]
	end=city[en]
	fixed=[start,end]
	waypts=[]
	daycnt={}
	for i in b:
		if i!=st and i!=en:
			waypts.append(city[i])
	sd=0
	totdays=0
	for i in  b:
		totdays=totdays+vis_time[i]

	for i in range(len(b)-1):
		v=int(round(((vis_time[b[i]])*days)/totdays))
		daycnt[city1[b[i]]]=v
		sd=sd+v
	daycnt[city1[b[len(b)-1]]]=days-sd

	return {'fixedpts':fixed , 'waypts':waypts, 'daycnt':daycnt}
