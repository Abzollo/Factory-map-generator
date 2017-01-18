# USER-DEFINED FUNCTIONS #
def readLines(s):
	if '\r\n' in s:
		return s.split('\r\n')
	else:
		return s.split('\n')

def seqToStr(s): return '-'.join([str(n) for n in s])

def pairwiseExchange(s):
	allSeq = [s]
	new_s = list(s)  # Copy new one, don't point to s
	for i in range(0, len(s)):
		for j in range(i+1, len(s)):
			(new_s[i], new_s[j]) = (s[j], s[i])
			allSeq.append(new_s)
			new_s = list(s)
	return allSeq

def mov(pos, d):
    (x,y) = pos
    if d == 'u':
        return (x,y+1)
    elif d == 'd':
        return (x,y-1)
    elif d == 'r':
        return (x+1,y)
    else:
        return (x-1,y)

def mapSFC(start,SFC):
    pos = start
    curve = [pos]
    for d in SFC:
        pos = mov(pos,d)
        curve.append(pos)
    return curve

def ingrid(pos): return pos[0] in range(1,11) and pos[1] in range(1,11)

def fillCurve(depSeq, curveMap):
	# We assign coordinates for each machine based on the SFC map
	new_map = [(0,0) for i in range(0,100)]
	for i in range(0,100):
		new_map[depSeq[i]-1] = curveMap[i]
	# Also add coordinates of raw parts and end products storages (just in case)
	new_map += [(5,-1),(5,11)]
	return new_map


# Read speed factors data file and convert to array of ints
f = open("sfactor.txt", "r")
dataString = readLines(f.read())
f.close()
sfactor = list(map(int, dataString[:-1]))

# Get departments based on speed factors
dep = {}
for i in range(0,100):
    if sfactor[i] not in dep:
        dep[sfactor[i]] = []
    dep[sfactor[i]].append(i+1)

# Follow a predefined SFC curve (define start point and directions for curve)
# Each letter denote direction of line from the defined start point (should be 99 letters in total)
start = (1,1)
SFC_string = "uuuuuuuuurdddddddddruuuuuuuuurdddddddddruuuuuuuuurdddddddddruuuuuuuuurdddddddddruuuuuuuuurddddddddd"
SFC_string0 = ""

# Make a sequence of departments
init_seq = [1,4,3,5,2]
allSeq = pairwiseExchange(init_seq)

# Make map files for all sequences from pairwise exchanges
for i, seq in enumerate(allSeq):
	# Get sequence of machine IDs
	seqSFC = []
	for d in seq:
		seqSFC += dep[d]
	# Get coordinates for SFC
	SFC_map = mapSFC(start, SFC_string)
	# Check if map is feasible (in grid) and complete (no missing or extra coordinates)
	assert all([ingrid(t) for t in SFC_map])
	assert len(set(SFC_map)) == 100
	# Fill the SFC with machine IDs based on the sequence we have
	filledMap = fillCurve(seqSFC, SFC_map)
	# Write out the map the way Arena wants it (one column of data: x1,y1,x2,y2,etc)
	mapForArena = ''.join([str(x)+'\r\n'+str(y)+'\r\n' for (x,y) in filledMap])
	# The new map file for this sequence
	mapFile = "map_"+str(i+1)+".txt"
	# Explain what's going on
	print("Writing the map of the sequence: %s\nto the file: %s\n" % (seqToStr(seq),mapFile))
	open(mapFile, 'w').write(mapForArena)
	

