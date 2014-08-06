import re
pattern = re.compile(r"\s+")

f = open("test.txt", "r")

ciphertext = ""
plaintext = ""

for line in f:
	ciphertext += line

ciphertext = re.sub(pattern, "", ciphertext)

print "\nCiphertext:\n%s\n" % ciphertext

alpha = {0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F", 6:"G", 7:"H", 8:"I", 9:"J", 10:"K", 11:"L", 12:"M", 13:"N", 14:"O", 15:"P", 16:"Q", 17:"R", 18:"S", 19:"T", 20:"U", 21:"V", 22:"W", 23:"X", 24:"Y", 25:"Z"}

numerical = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7, "I":8, "J":9, "K":10, "L":11, "M":12, "N":13, "O":14, "P":15, "Q":16, "R":17, "S":18, "T":19, "U":20, "V":21, "W":22, "X":23, "Y":24, "Z":25} 

letter_prob = {0:0.082, 1:0.015, 2:0.028, 3:0.043, 4:0.127, 5:0.022, 6:0.020, 7:0.061, 8:0.070, 9:0.002, 10:0.008, 11:0.040, 12:0.024, 13:0.067, 14:0.075, 15:0.019, 16:0.001, 17:0.060, 18:0.063, 19:0.091, 20:0.028, 21:0.010, 22:0.023, 23:0.001, 24:0.020, 25:0.001}
 
lower_margin = 0.01
upper_margin = 0.022
IC_lowerbound = 0.065 - lower_margin
IC_upperbound = 0.065 + upper_margin

found_m = False
m = 0

while found_m == False:	
	m = m + 1
	found_m = True
	subtext = ""
	len_subtexts = []
	list_frequency = []
	for i in range(0, m):
		j = i
		while j < len(ciphertext):
			subtext += ciphertext[j:j+1]
			j = j + m
		len_subtexts.insert(i, len(subtext)) 
		print "Subtext for m=%d: %s " % (m, subtext)

		#find frequency of all letters in subtext		
		frequency = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0, 21:0, 22:0, 23:0, 24:0, 25:0}
		for s in subtext:
			s = numerical[s.upper()]
			frequency[s] = frequency.get(s) + 1
		list_frequency.insert(i, frequency)

		numerator = 0
		for key, value in frequency.iteritems():
			numerator += value*(value-1)
		n = len(subtext)

		#calculate IC
		IC = (float(numerator)) / (n*(n-1))
		print "IC = %.3f\n" % IC	

		#check if we found m
		if ((IC > IC_upperbound) or (IC < IC_lowerbound)): 		
			found_m = False
		subtext = ""

print "m is %d\n" % m

keys = []
for i in range(0, len(list_frequency)):			
	print "i=%d" % (i+1)
	for g in range(0, 26):
		Mg = 0
		for key, value in list_frequency[i].iteritems():
			Mg += (letter_prob[key]*((float(list_frequency[i][(key+g) % 26]))/len_subtexts[i]))		
		print "Mg=%.3f (shift %s)" % (Mg, alpha[g])
		if ((Mg > IC_lowerbound) and (Mg < IC_upperbound)):
			keys.append(alpha[g])
	print "key_%d = %s" % (i, keys[i])
	print "\n"

print "Keyword:"
for k in keys:
	print k, 

i = 0
for y in ciphertext:
	d_k = (numerical[y.upper()] - numerical[keys[i]]) % 26
	plaintext += alpha[d_k].lower()
	i = (i + 1) % len(keys)

print "\n\nPlaintext:\n%s" % plaintext
