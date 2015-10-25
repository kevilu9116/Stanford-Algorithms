import argparse

def swap(inputArray, i, j):
	return inputArray[j], inputArray[i]

def quickSortPivotFirst(inputArray, left, right, numComparisons):

	"""
	Base case: Subarray to partition is of size 0 or 1, no sorting necessary, we simply return
	"""
	if right - left == 0 or right - left == 1:
		return inputArray, numComparisons

	#keep running total of number of comparisons done by QuickSort
	numComparisons += (right - left - 1) 
	pivot = inputArray[left]
	i = left + 1

	#loop to partition the array around the pivot
	for j in range(left + 1, right):
		if inputArray[j] < pivot:
			inputArray[i], inputArray[j] = swap(inputArray, i, j)
			i += 1

	inputArray[left], inputArray[i - 1] = swap(inputArray, left, i - 1)	#put pivot in proper place

	numComparisons = quickSortPivotFirst(inputArray, left, i - 1, numComparisons)[1]
	numComparisons = quickSortPivotFirst(inputArray, i, right, numComparisons)[1]

	return inputArray, numComparisons

def quickSortPivotLast(inputArray, left, right, numComparisons):

	"""
	Base case: Subarray to partition is of size 0 or 1, no sorting necessary, we simply return
	"""
	if right - left == 0 or right - left == 1:
		return inputArray, numComparisons

	numComparisons += (right - left - 1) #keep running total of number of comparisons done by QuickSort

	"""
	This version of quicksort uses the last entry in the array as the pivot, 
	so we swap the first and last entries and then proceed as if running 'QuickSortFirst'
	"""
	inputArray[left], inputArray[right - 1] = swap(inputArray, left, right - 1) 
	pivot = inputArray[left]
	i = left + 1

	#loop to partition the array around the pivot
	for j in range(left + 1, right):
		if inputArray[j] < pivot:
			inputArray[i], inputArray[j] = swap(inputArray, i, j)
			i += 1

	inputArray[left], inputArray[i - 1] = swap(inputArray, left, i - 1)	#put pivot in proper place

	numComparisons = quickSortPivotLast(inputArray, left, i - 1, numComparisons)[1]
	numComparisons = quickSortPivotLast(inputArray, i, right, numComparisons)[1]

	return inputArray, numComparisons

def quickSortPivotMid(inputArray, left, right, numComparisons):

	"""
	Base case: Subarray to partition is of size 0 or 1, no sorting necessary, we simply return
	"""
	if right - left == 0 or right - left == 1:
		return inputArray, numComparisons

	numComparisons += (right - left - 1) #keep running total of number of comparisons done by QuickSort

	"""
	This version of quicksort uses the 'median of three' pivot rule. That is, we look at the first, middle and last
	elements in the array and use the median of these three values as our pivot. This should give us considerable savings
	and help ensure that our runtime is optimized towards O(nlogn).
	"""
	first = inputArray[left]
	last = inputArray[right - 1]
	if (right - left) % 2 == 0:
		midIndex = left + (right - left) / 2 - 1
	else:
		midIndex = left + (right - left) / 2
	mid = inputArray[midIndex]

	if first < mid < last or last < mid < first:
		inputArray[left], inputArray[midIndex] = swap(inputArray, left, midIndex)
	elif mid < last < first or first < last < mid:
		inputArray[left], inputArray[right - 1] = swap(inputArray, left, right - 1)

	pivot = inputArray[left]
	i = left + 1

	#loop to partition the array around the pivot
	for j in range(left + 1, right):
		if inputArray[j] < pivot:
			inputArray[i], inputArray[j] = swap(inputArray, i, j)
			i += 1

	#put pivot in proper place
	inputArray[left], inputArray[i - 1] = swap(inputArray, left, i - 1)

	numComparisons = quickSortPivotMid(inputArray, left, i - 1, numComparisons)[1]
	numComparisons = quickSortPivotMid(inputArray, i, right, numComparisons)[1]

	return inputArray, numComparisons


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', help="Filepath to input file containing unsorted integers.")
	parser.add_argument('--mode', help="Indicator flag for quicksort performed. (1) first pivot,\
	 					(2) last pivot, (3, default) mid pivot.", type=int)
	args = parser.parse_args()

	inputFile = open(args.f, "r")
	inputArray = [int(x) for x in inputFile]

	if args.mode == 1:
		sortedArray, numComparisons = quickSortPivotFirst(inputArray, 0, len(inputArray), 0)
	elif args.mode == 2:
		sortedArray, numComparisons = quickSortPivotLast(inputArray, 0, len(inputArray), 0)
	else:
		sortedArray, numComparisons = quickSortPivotMid(inputArray, 0, len(inputArray), 0)

	print sortedArray
	print numComparisons

if __name__ == '__main__':
	main()


