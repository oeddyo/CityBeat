lines = open('number.csv')

lats = []
lngs = []
for line in lines:
    t = line.split(',')
    lats.append(float(t[0]))
    lngs.append(float(t[1]))

sorted_lats = sorted(lats)
sorted_lngs = sorted(lngs)

print sorted_lats[0],sorted_lats[1]

print sorted_lngs[0], sorted_lngs[1]

print min(lats), max(lats)
print min(lngs), max(lngs)

print sorted_lats
print sorted_lngs
