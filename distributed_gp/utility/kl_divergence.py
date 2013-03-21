import math

error = 1e-8

def _check(pro):
	s = 0
	for pr in pro:
		if pr < error:
			return False
		s += pr
	return abs(1 - s) < error

def KLDivergence(pro1, pro2):
	if not _check(pro1):
		pro1 = normalizeWithSmoothing(pro1)
	if not _check(pro2):
		pro2 = normalizeWithSmoothing(pro2)
	s = 0
	for i in xrange(0, len(pro1)):
		s += pro1[i]*math.log(pro1[i]/pro2[i])/math.log(2)
	return s
	
def averageKLDivergence(pro1, pro2):
	return (KLDivergence(pro1, pro2) + KLDivergence(pro2, pro1))/2
	
def normalizeWithSmoothing(pro1):
	s = 0
	for i in xrange(0, len(pro1)):
		pro1[i] += error
		s += pro1[i]
	for i in xrange(0, len(pro1)):
		pro1[i] /= s
	return pro1 


if __name__ == '__main__':
	pro1 = [0.6, 0.3, 0.1]
	pro2 = [0.001, 0.001, 0.998]
	print averageKLDivergence(pro1, pro2)