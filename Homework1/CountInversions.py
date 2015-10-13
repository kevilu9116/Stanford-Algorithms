import sys

def mergeAndCount(inputList, numInversions):
	numElements = len(inputList)
	sortedListAndNumInversions = []

	"""
	base case (if statement): if we have an array of length 1
	we return the single element in the array and 0
	for no inversions found

	recursive case (else statement): we call 'mergeAndCount'
	for the left half and the right half of the array. This gives us
	sorted halves and the number of inversions found for each half. Then
	we merge the two sorted halves and in addition, count the number of
	cross inversions and return the sorted array and the total number of inversions
	(leftInversions + rightInversions + crossInversions)
	"""
	if numElements == 1:
		sortedListAndNumInversions.append(inputList)
		sortedListAndNumInversions.append(0)
	else:
		leftResults = mergeAndCount(inputList[:(numElements / 2)], numInversions)
		rightResults = mergeAndCount(inputList[(numElements / 2):], numInversions)

		leftList = leftResults[0]
		rightList = rightResults[0]
		mergedList = []

		numCrossInversions = 0
		i = 0
		j = 0

		for k in range(len(leftList) + len(rightList)):
			if leftList[i] <= rightList[j]:
				mergedList.append(leftList[i])
				i += 1

				if i == len(leftList):
					mergedList += rightList[j:]
					break
			else:
				mergedList.append(rightList[j])
				numCrossInversions += len(leftList) - i
				j += 1

				if j == len(rightList):
					mergedList += leftList[i:]
					break

		sortedListAndNumInversions.append(mergedList)
		sortedListAndNumInversions.append(leftResults[1] + rightResults[1] + numCrossInversions)

	return sortedListAndNumInversions


def main():
	inputFile = open(sys.argv[1], "r")
	inputList = [int(line) for line in inputFile]
	results = mergeAndCount(inputList, 0)
	print results[1]

if __name__ == '__main__':
	main()
