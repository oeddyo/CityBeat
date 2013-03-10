

def computeKappa(v11, v10, v01, v00):
	n = v11 + v10 + v01 + v00
	pa = 1.0 * (v00 + v11) / n
	yes_1 = 1.0 * (v11 + v10) / n
	yes_2 = 1.0 * (v01 + v11) / n
	no_1 = 1 - yes_1
	no_2 = 1 - yes_2
	yes_both = yes_1 * yes_2
	no_both = no_1 * no_2
	pe = yes_both + no_both
	print pa, pe
	return (pa - pe)/ (1- pe)

def computeAgreementMatrix(dict1, dict2):
	v11 = 0
	v10 = 0
	v01 = 0
	v00 = 0
	for key, v1 in dict1.items():
		assert key in dict2.keys()
		
		v2 = dict2[key]
		if v1 == v2:
			if v1 == 1:
				v11 += 1
			else:
				v00 += 1
		else:
			print key
			if v1 == 1:
				v10 += 1
			else:
				v01 += 1
				
	print computeKappa(v11, v10, v01, v00)

def main():
	dict1 = {}
	dict2 = {}
	fid1 = open('labeled_data_cf/kappa_xia.txt', 'r')
	for line in fid1:
		line = line.split(',')
		dict1[line[0]]=int(line[1])
	fid1.close()
	
	fid2 = open('labeled_data_cf/true_label2.txt', 'r')
	for line in fid2:
		line = line.split(',')
		dict2[line[0]]=int(line[1])
	fid2.close()
	computeAgreementMatrix(dict1, dict2)
	
if __name__ == '__main__':
	main()