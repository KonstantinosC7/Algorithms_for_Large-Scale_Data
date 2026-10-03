import random
import csv
from time import time
import os
import math

K = 0 				#gia na pernaei to programma

def MyReadDataRoutine(dataDocument, numDocuments):
	#diavazw to arxeio mexri ta prwta numDocuments eggrafa
	#kataskeuazw frozensets	
	next(f)			# gia na pame grammh 3 kai me thn epomenh read na diabasei apo th grammh 4 opou kai einai ta dedomena mas
	n = 1			# se poio dicID briskomaste na mpainoun ola sth swsth lista bash tou docID
	A = []			# h lista pou pairnei ta wordID gia to kathe ksexwristo docID
	wordSet = []	# h lista me ta frozensets (sumpaghs domh)
	while (n <= numDocuments):
		x = f.readline().rstrip()
		x = x.split()
		if (int(x[0]) >= n):		# gia na allazei lista an allaksei to docID
			n += 1
			B = tuple(A)
			fSet = frozenset(B)
			wordSet.append(fSet)
			A = []
			if (n > numDocuments):
				break
		A.append(int(x[1]))
	return wordSet

def MyJacSimWithSets(docID1,docID2):
	#docID1.intersection(docID2) for fun!
	counterIntersection = 0
	for wordID1 in docID1:
		for wordID2 in docID2:
			if (wordID1 == wordID2):
				counterIntersection += 1
	jacSim = counterIntersection / (len(docID1) + len(docID2) - counterIntersection)
	return jacSim


def MyJacSimWithOrderedLists(docID1, docID2):
	pos1 = 0
	pos2 = 0
	counterIntersection = 0
	len1 = len(docID1)
	len2 = len(docID2)
	while (pos1 < len1 and pos2 < len2):
		if (docID1[pos1] == docID2[pos2]):
			counterIntersection += 1
			pos1 += 1
			pos2 += 1
		else:
			if docID1[pos1] < docID2[pos2]:
				pos1 += 1
			else:
				pos2 += 1		
	jacSim = counterIntersection / (len(docID1) + len(docID2) - counterIntersection)
	return jacSim

def create_random_hash_function(p=2**33-355, m=2**32-1):
	a = random.randint(1,p-1)
	b = random.randint(0,p-1)
	return lambda x: 1 + (((a * x + b) %p) %m)

def str_list_to_int_list(str_list):
    int_list = [int(n) for n in str_list]
    return int_list	

def hashFunction(K,W):
	# mporousame na xrhsimopoihsoume json arxeia gia pio eukola dn to eidame nwris	
	permutations = []
	try:
		filename = 'hashFunctions.csv'
		with open(filename, 'x', newline="") as f:
			csvwriter = csv.writer(f) 			 # 2. create a csvwriter object
			csvwriter.writerow(['key', 'value']) # 4. write the header
			for i in range(K):
				h = create_random_hash_function()
				randomHash = {x:h(x) for x in range(int(W))}
				myHashKeysOrderedByValues = sorted(randomHash, key=randomHash.get)
				myHash = {myHashKeysOrderedByValues[x]:x for x in range(int(W)) }
				permutations.append(myHash) 	# pinakas
				myListHash = myHash.items()
				csvwriter.writerows(myListHash) # 5. write the rest of the data	
			f.close()
	# an uparxei hdh to arxeio den theloume na to ksanadhmiourghsei
	except FileExistsError:
		with open('hashFunctions.csv', mode='r') as infile:
			reader = csv.reader(infile)
			next(reader)
			wStart = int(W) + 1 				# epeidh xekiname apo thn 2h grammh tou arxeiou 
			temp1 = list(reader)				# diabazei olo to csv arxeio kai to metatrepei se lista 
			tempInt = []
			for x in temp1:
				x = str_list_to_int_list(x)
				tempInt.append(x)
			n = 0 								# counter gia na allazoume ta dioctionaries
			for k in range(K):
				temp = tempInt[n:int(W)+n] 		# kratame se lista posa stoixeia exei kathe to dioctionary 
				temp_dict = dict(temp) 			# metatrepoume thn lista se dictionary   
				permutations.append(temp_dict)	# bazoume to ekastote dictionary sto telos ths listas mas
				n += int(W) 					# gia na diabasei ta epomena W stoixeia pou antistoixoun sthn epomenh metathesh
	return permutations

def MyMinHash(wordset,K): 
	SIG = []
	wordList = [[]]*int(W)				# edw 8a ftiaxoume to arxiko mhtrwo 
	wordLists = [[]]*int(numDocuments)	# edw ta frozensets tha ginoun sortarismenes listes 
	# initialize register of signatures(diplo for diafaneies)
	rows, cols = (K, len(wordset))		
	# arxikopoihsh SIG sto apeiro gia na mporoume na kanoume allages
	SIG = [[float('inf') for i in range(cols)] for j in range(rows)]
	# sortaroume tis listes eswterika gia na ftiaksoume pinaka arxikou mhtrwou
	docID = 0 
	for fSet in wordset:						# prospername ta frozenset
		wordLists[docID] = sorted(fSet)			# sortaroume tis listes
		for wordID in wordLists[docID]:			# bazoume ta wordID sto arxiko pinaka mhtrwou
			if (wordList[wordID-1] == []):
				wordList[wordID-1] = [docID+1]	# an den uparxei hdh me isothta vazoume
			else:
				wordList[wordID-1] += [docID+1]	# an uparxei hdh kanoume add
		docID += 1
	# ftiaxnoume mhtrwo ypografwn
	# sarwnoume to mhtrwou eggrafwn gia na ftiaxtei mhtrwo ypografwn
	j = 0		# gia na exoume to wordId (thesh) sto arxiko mhtrwo
	# shmeiwsh : to pinaka me to arxiko mhtrwo ton ksekinhsame apo to 0 ara kai to j ksekinaei apo 0
	for row in wordList:
		while(row != []):		# epeidh dn kseroume posa stoixeia mporei na exei h kathe lista
			for i in range(K):
				value = permutations[i][j]		# to proswrino value pairnei ws timh th thesh sth metathesh
				if(value < SIG[i][row[0]-1]):	# elegxos an h kainourgia thesh einai mikroterh apo prohgoumenh
					SIG[i][row[0]-1] = value 	# apothikeuoume th kainourgia thesh sto SIG
			row.remove(row[0])	# diagrafoume to prwto stoixeio[apo lista twn docIDs] kai to epomeno ths listas ginetai prwto
		j += 1	
	return SIG

def MySigSim(doc1, doc2, numPermutations):
	sigSim = 0
	for i in range(numPermutations):
		if(doc1[i] == doc2[i]):
			sigSim += 1
	sigSim = sigSim / numPermutations			
	return sigSim

def neighborsBF(numDocuments, NumNeighbors, choose, wordlist, d, numPermutations):
	myNeighborsDictBF = {} 
	distancesDict = {}
	distancesList = []
	# Sthn periptwsh pou o xrhsths epelexe thn Jaccard metrikh
	if(choose == 1):				
		for i in range(d,numDocuments):
			jacSimOrdered = MyJacSimWithOrderedLists(wordlist, wordListSorted[i])	# Jaccard Similarity 2 eggrafwn
			distanceJac = 1 - jacSimOrdered 										# Jaccard Distance
			distancesList.append(i+1)												# bazoume ton metrhth(docID) kai thn apostash dipla se mia lista
			distancesList.append(distanceJac)										# etsi wste na einai pio eykolh h metartoph se dictionary
	# Sthn periptwsh pou o xrhsths epelexe thn Signature metrikh
	else:
		for i in range(d,numDocuments):
			sigSim = MySigSim(wordlist, signatureList[i], numPermutations)						# default gia thn wra meta tha allaxei
			distanceSigSim = 1 - sigSim
			distancesList.append(i+1)
			distancesList.append(distanceSigSim)
	# metaroph ths listas se dioctionary opou kleidi einai to docID twn allwn eggrafwn se sxesh me to sugkekrimeno
	# docID pou to balame gia na broume tous geitones tou kai timh h apostash me to sygkrekrimeno docID
	distancesDict = {distancesList[i]: distancesList[i + 1] for i in range(0, len(distancesList), 2)}
	#sorted dictionary basei twn apostasewn
	dict1 = dict(sorted(distancesDict.items(), key=lambda item: item[1])) 
	c = 0
	# pairnoume tous kontinoterous geitones gia kathe kleidi(key)
	for key, value in dict1.items():
		if(c < NumNeighbors):
			# metatrepoume to distance se similarity
			myNeighborsDictBF[key] = 1 - value
			c += 1
		else:
			break	
	avgDocID = 0
	# prosthetoume ola ta similarities twn kontinoterwn geitonwn
	for value in myNeighborsDictBF.values():
		avgDocID += value
	avgDocID = avgDocID / len(myNeighborsDictBF)	
	if (choose == -1):	# xrhsimopoieitai gia na broume toys geitones enow sugkekrimenou docID
		return myNeighborsDictBF
	return 	avgDocID

def sortedLists(wordSet):					# sortaroume ola ta frozensets
	wordListSorted = []						
	for i in range(numDocuments):			# analoga me posa numdocuments zhtaei o xrhsths
		sortedList = sorted(wordSet[i])
		wordListSorted.append(sortedList)
	return	wordListSorted

def Signatures(SIG):						# gia na mporoume na paroume tis sthles apo to SIG
	for i in range(numDocuments):			# voleuei sth sigSim na xrhsimopoihthei
		signatureList.append([row[i] for row in SIG])
	return signatureList

def LSH(signatureList, rowsPerBands,choose):
	#kleidi -> apo 1 mexri numDoc (den 8a xrhsimopoihsw to SIG voleuei sthles)
	#value  -> timh pou antistoixei ton kado pou mpainei to kathe docID
	global myNeighborsDict
	dictLSH = {}
	candidatePairs = []
	numBands = math.floor(K/rowsPerBands)		# an prolavainoume na koitaksoume thn teleutaia mpanta (r-(2r-1) grammes)
	counter = 0
	findDocID = 1

	hashLSH = create_random_hash_function()
	for i in range(numBands):
		listLSH = []						# adeiazoume kathe fora th lista wste na apothikeutei to lexiko(xreiazetai logo tou extend)
		findDocID = 1						# na mpainei kathe fora to swsto docID gia key
		for col in signatureList:
			vector = col[0+counter:rowsPerBands+counter]	# pairnoume rowsPerBands grammes ths sthlhs
			vector_tuple = tuple(vector)					# tis metatrepoume pleiada
			hashValue = hash(vector_tuple)					# exoume thn timh
			tmp = hashLSH(hashValue)						# o kados
			dictLSH[findDocID] = tmp 						# pairnoume sto leksiko
			findDocID += 1									# auksanoume to docd id gia na pame sthn epomenh sthlh
		# sortaroume wste ta upopshfia zeugh na einai o enas meta ton allon
		newDict = {k: v for k, v in sorted(dictLSH.items(), key=lambda item: item[1])}	
		[listLSH.extend([k,v]) for k,v in newDict.items()]	# kanoume lista to sortarismeno dict
		counter += rowsPerBands								# na proxwraei kata rowsPerBands kathe fora (otan diabazoume thn prwth banta) 
		for i in range(1,len(listLSH)-2,2):					# gia kathe mpanta briskoume ta upospshfia zeugh
			# elegxoume an einai upopshfio zeugos kai tote apothikeuoume to docID tous
			# elegxoume an uparxei hdh to zeugos mesa sto candidate pairs
			if((listLSH[i] == listLSH[i+2]) and ([listLSH[i-1], listLSH[i+1]] not in candidatePairs)):
				candidatePairs.append([listLSH[i-1], listLSH[i+1]])
	candidatePairs = sorted(candidatePairs)
	# apo thn lista listwn pername se leksiko kleidi me times
	for i in range(0,len(candidatePairs)):
		# elegxoume an h prwth timh einai idia me prohgoumenh timh (dhladh uparxei hdh sto dict)
		if (candidatePairs[i-1][0] == candidatePairs[i][0]):
				myNeighborsDict[candidatePairs[i][0]].append(candidatePairs[i][1])
		else:
			# einai gia opoiodhpote zeugos den exei ksanampei mesa sto dict (apothikeuoume kleidi kai thn prwth tou timh)
			myNeighborsDict.setdefault(candidatePairs[i][0], [candidatePairs[i][1]])
	AvgSimDocID = 0
	for key,value in myNeighborsDict.items():
		avgDocID = neighborsLSH(NumNeighbors, choose, key, value, K)
		AvgSimDocID += avgDocID	
	AvgSimDocID = AvgSimDocID / numDocuments
	return AvgSimDocID 		

def neighborsLSH(NumNeighbors, choose, keyDict, valuesDict, numPermutations):
	distancesDict = {}
	distancesList = []
	myNeighborsDict1 = {}
	if (choose == 1):
		for i in valuesDict:
			jacSimOrdered = MyJacSimWithOrderedLists(wordListSorted[keyDict-1], wordListSorted[i-1])
			distanceJac = 1 - jacSimOrdered
			distancesList.append(i+1)				#epeidh oi listes xekinane apo to 0 kai emeis 8eloume ta docIDs na xekinane apo to 1
			distancesList.append(distanceJac)
	else:
		for i in valuesDict:
			sigSim = MySigSim(signatureList[keyDict-1], signatureList[i-1], numPermutations)						# default gia thn wra meta tha allaxei
			distanceSigSim = 1 - sigSim
			distancesList.append(i+1)				#epeidh oi listes xekinane apo to 0 kai emeis 8eloume ta docIDs na xekinane apo to 1
			distancesList.append(distanceSigSim)
	distancesDict = {distancesList[i]: distancesList[i + 1] for i in range(0, len(distancesList), 2)}	
	dict1 = dict(sorted(distancesDict.items(), key=lambda item: item[1]))
	c = 0
	for key, value in dict1.items():
		if(c < NumNeighbors):
			myNeighborsDict1[key] = 1 - value
			c += 1
		else:
			break	
	avgDocID = 0
	for value in myNeighborsDict1.values():
		avgDocID += value
	avgDocID = avgDocID / len(myNeighborsDict1)
	return avgDocID

#---------------------------------------------------------------------------
#---------------------------EXPERIMENTAL EVALUATION-------------------------
#------------------------------------ MAIN ---------------------------------

#Ta arxeia pros epexergasia briskontai ston idio katalogo me ton kwdika
print() 
print("#################################################################")
print("		EXPERIMENTAL EVALUATION")
print("#################################################################")
print()
print("=================================================================")
print("Choose a file (1 or 2) to find K nearest neighbors :")
print("	1. DATA_1-docword.enron.txt.")
print("	2. DATA_2-docword.nips.txt.")
print("=================================================================")

choose = int(input("Type 1 or 2 depending on the file you want : "))
while(choose != 1 and choose != 2):
	print("Try again!")
	choose = int(input("Type 1 or 2 depending on the file you want : "))

if(choose == 1):
	dataDocument = "DATA_1-docword.enron.txt"
else:
	dataDocument = "DATA_2-docword.nips.txt"
print("-----------------------------------------------------------------")
print("You selected : " + dataDocument + " !")
print("-----------------------------------------------------------------")

#open the selected file to read the statistics in order to do correct evaluations
f = open(dataDocument)
D = f.readline().rstrip() # num of Documents (diavazei thn prwth grammh)

print("The selected file has <" + str(D) + "> different documents.")
numDocuments = int(input("Select the number of Documents you want to process from the file : "))

#check for numDocuments
while(numDocuments > int(D)  or numDocuments < 1):
	print("Try again!")
	print("The number of Documents you selected are more or less than the actual number that the selected file has!")
	numDocuments = int(input("Select again the number of Documents you want to process : "))
		

print("-----------------------------------------------------------------")
print("You selected : " + str(numDocuments) + " Documents!")
print("-----------------------------------------------------------------")
#Different word IDs that the selected file has
W = f.readline().rstrip()	# diavazei thn deuterh grammh

wordSet = MyReadDataRoutine(dataDocument, numDocuments)		#list from frozenSets
NumNeighbors = int(input("Select the number of neighbors (for instance 2,3,4 or 5 ,max number 10) you want to find for every document : "))
while(NumNeighbors > 10):
	print("Try again!")
	NumNeighbors = int(input("Select the number of neighbors (for instance 2,3,4 or 5 ,max number 10) you want to find for every document : "))

print("-----------------------------------------------------------------")
print("You selected : " + str(NumNeighbors) + " neighbors!")
print("-----------------------------------------------------------------")

permutations = []
print("Suggestion : Permutations should be a power of 2!")
K = int(input("Determined the number of permutations : "))
print("-----------------------------------------------------------------")
print("You selected : " + str(K) + " permutations!")
print("-----------------------------------------------------------------")

# tha dhmiourghthoun oi hashFunctions mono mia fora 
# an theloume alles hashFunctions sbhnoume to arxeio pou exei dhmiourghthei
print("=================================================================")
print("You can choose if you want to use new hash functions for the algorithm 'Min Hash' or you load the permutations from an existing file.")
print("Note: If you give different permutations number from the previous time you have to type 'new' or 'update' !")
print("	1. Create a new csv (only if you dont have a previous csv file !!!)")
print("	2. Update an existing file (generate new csv file)")
print("	3. Keep your previous csv (remember you have to give the same permutations)")
print("=================================================================")

fileChoose = int(input("Type 1 or 2 or 3 depending on what you prefer to do : "))
while(fileChoose < 1 or fileChoose > 3):
	print("Try again!")
	fileChoose = int(input("Type 1 or 2 or 3 depending on what you prefer to do : "))
print("Calculating be patient...")
if (fileChoose == 1):
	print("We create a new file!")
	permutations = hashFunction(K,W)		# Save the permutations	
elif (fileChoose == 2):
	os.remove("hashFunctions.csv")
	print("We delete the existing file and we create a new one!")
	permutations = hashFunction(K,W)		# Save the permutations	
else:
	print("We will use the existing file")
	permutations = hashFunction(K,W)	# Save the permutations
SIG = MyMinHash(wordSet,K) 				# We create the signature with the algorithm Min Hash

wordListSorted = []
signatureList = []
wordListSorted = sortedLists(wordSet)
signatureList = Signatures(SIG)

print("=================================================================")
print("Determine if you want to give a further check to the metric system.")
print("	1. Jaccard Similarity")
print("	2. Signature Similarity")
print("	3. Continue")
print("=================================================================")

choose = int(input("Type 1 or 2 depending on the similarity metric you want or 3 to continue: "))
while(choose < 1 or choose > 3):
	print("Try again!")
	choose = int(input("Type 1 or 2 depending on the similarity metric you want or 3 to continue: "))
if (choose == 1 or choose == 2):
	docID1 = int(input("Give the first docID: "))
	docID2 = int(input("Give the second docID: "))
	if (choose == 1):
		startTime = time()
		jacsim = MyJacSimWithSets(wordSet[docID1-1], wordSet[docID2-1])
		endTime = time()
		print("Execution time for Jaccard Similarity With Sets: %f" %(endTime - startTime))
		print("jacsim = %f" %jacsim)
		startTime = time()
		jacsim = MyJacSimWithOrderedLists(sorted(wordSet[docID1-1]), sorted(wordSet[docID2-1]))
		endTime = time()
		print("Execution time for Jaccard Similarity With Ordered Lists: %f" %(endTime - startTime))
		print("jacsim = %f" %jacsim)
	else:
		temp = int(input("If you want to specify the number of permutations in Signature Similarity press 1 otherwise press 2 : "))
		if(temp == 1):
			numPermutations = int(input("Specify how many lines you want to check from SIG max(" +str(K)+") : "))
			while(numPermutations > K):
				print("Try Again!")
				numPermutations = int(input("Specify how many lines you want to check from SIG max(" +str(K)+") : "))
		else:
			print("You didn't choose number of permutation so the deafault number is ", K)
			numPermutations = K
		startTime = time()
		sigsim = MySigSim(signatureList[docID1-1], signatureList[docID2-1], numPermutations)
		endTime = time()
		print("Execution time for Signature Similarity : %f" %(endTime - startTime))
		print("sigsim = ", sigsim)

print("=================================================================")
print("Determine the desired similarity metric to use.")
print("	1. Jaccard Similarity")
print("	2. Signature Similarity")
print("=================================================================")

choose = int(input("Type 1 or 2 depending on the similarity metric you want : "))
while(choose != 1 and choose != 2):
	print("Try again!")
	choose = int(input("Type 1 or 2 depending on the similarity metric you want : "))

print("=================================================================")
print("Determine if you want to use the brutal Force method, or the LSH method.")
print("	1. Brute Force Method")
print("	2. LSH method")
print("=================================================================")

method = int(input("Type 1 or 2 depending on the method you want : "))
while(method != 1 and method != 2):
	print("Try again!")
	method = int(input("Type 1 or 2 depending on the method you want : "))

myNeighborsDict = {} 						# apo8hkeuw tous kontinoterous geitones
avgSimDocIDs = 0
if(method == 1 and choose == 1):			#Brute Force Method selected with Jaccard Similarity
	print("-----------------------------------------------------------------")
	print("Brute Force method selected with Jaccard Similarity!")
	print("-----------------------------------------------------------------")
	startTime = time()
	for i in range(numDocuments-1):			#numDocuments-1 den theloume to teleutaio egrrafo na to sygkrinoume me kapoio allo
		avgDocID = neighborsBF(numDocuments, NumNeighbors, choose, wordListSorted[i], i+1, K) 		# i+1 : gt den theloume metaxy tous na sygkrinei idia eggrafa
		avgSimDocIDs += avgDocID
	avgSimDocIDs = avgSimDocIDs / numDocuments
	endTime = time()
	print("Execution time : %f\n" %(endTime - startTime))
	print("Average Similarity = ", avgSimDocIDs)
elif(method == 1 and choose == 2):			#Brute Force Method selected with Signature Similarity
	print("-----------------------------------------------------------------")
	print("Brute Force method selected with Signature Similarity!")
	print("-----------------------------------------------------------------")
	startTime = time()
	for i in range(numDocuments-1):		#numDocuments-1 den theloume to teleutaio egrrafo na to sygkrinoume me kapoio allo
		avgDocID = neighborsBF(numDocuments, NumNeighbors, choose, signatureList[i], i+1, K) 		# i+1 : gt den theloume metaxy tous na sygkrinei idia eggrafa
		avgSimDocIDs += avgDocID
	avgSimDocIDs = avgSimDocIDs / numDocuments
	endTime = time()
	print("Execution time : %f\n" %(endTime - startTime))
	print("Average Similarity = ", avgSimDocIDs)

elif(method == 2 and choose == 1):			#LSH Method selected with Jaccard Similarity
	print("-----------------------------------------------------------------")
	print("LSH method selected with Jaccard Similarity!")
	print("-----------------------------------------------------------------")

	#Selection about the rows per band
	print("You have the option to choose the number of rows per Band or you can leave it to the program.")
	selection = input("Τype (yes/no) depending on if you want to put a number of rows in bands yourself : ")
	while(selection != "yes" and selection != "no"):
		print("Try again!")
		selection = int(input("Τype (yes/no) depending on if you want to put a number of rows per bands yourself : "))

	if(selection == "yes"):
		rowsPerBand = int(input("Enter the number of rows you want per Band : "))
	else:
		rowsPerBand = 2 		# default timh
	startTime = time()
	avgApotelesma = LSH(signatureList, rowsPerBand, choose)		# pairname to signatureList anti gia to SIG gia pio eukolh ulopoihsh
	endTime = time()
	print("Execution time : %f" %(endTime - startTime))
	print("Average Similarity = ", avgApotelesma)



elif(method == 2 and choose == 2):			#LSH Method selected with Signature Similarity
	print("-----------------------------------------------------------------")
	print("LSH method selected with Signature Similarity!")
	print("-----------------------------------------------------------------")
	#Selection about the rows per band
	print("You have the option to choose the number of rows per Band or you can leave it to the program.")
	selection = input("Τype (yes/no) depending on if you want to put a number of rows in bands yourself : ")
	while(selection != "yes" and selection != "no"):
		print("Try again!")
		selection = input("Τype (yes/no) depending on if you want to put a number of rows per bands yourself : ")

	if(selection == "yes"):
		rowsPerBand = int(input("Enter the number of rows you want per Band : "))
	else:
		rowsPerBand = 2			#default timh
	startTime = time()
	avgApotelesma = LSH(signatureList, rowsPerBand, choose)		# pairname to signatureList anti gia to SIG gia pio eukolh ulopoihsh
	endTime = time()
	print("Execution time : %f" %(endTime - startTime))
	print("Average Similarity = ", avgApotelesma)

dict1 = {}
selection = input("Do you want to request the nearest neighbors for specific documents?(type yes/no) : ")
if(selection == "yes"):
	docID = int(input("Give docID (max docID "+str(numDocuments) +") : "))
	if(method == 2):
		if (docID in myNeighborsDict.keys()):	
			print("Nearest Neighbors for "+ str(docID) + " are : ", myNeighborsDict[docID])
		else:
			print("The docID you asked have 0 neighbors")
	else:
		dict1 = neighborsBF(numDocuments, NumNeighbors, -1, signatureList[docID-1], docID, K)
		neighborsBF = []
		for key in dict1:
			neighborsBF.append(key)
		print("Nearest Neighbors for "+ str(docID) + " are : ", neighborsBF)	