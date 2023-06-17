import csv, sys
import matplotlib.pyplot as plt
from collections import Counter

complexes = []
complex_sources = {}
exclusive_complexes = []
complex_method = {}
interaction_methods_list = []
method_counts = {}
method_counts_str = {}

if __name__ == "__main__":
	
	# Read in the file, filter on entrytype, expansionmodel, edgetype, organism and source
	# Store the filtered data in a new variable 'complexes'
	irefIndexFile = "All.mitab.08-22-2022_1Mlines.txt"
	with open(irefIndexFile, 'r',encoding="utf-8") as ppiFile:
		csvreader = csv.reader(ppiFile, delimiter='\t')
		header = next(csvreader)
		counter = 0
		
		for row in csvreader:
			counter += 1
			entryType = row[0]
			taxb = row[10]
			source = row[12]
			expansionModel = row[15]
			edgeType = row[52]
			if 'complex' in entryType and expansionModel == 'bipartite' and edgeType == 'C' and 'Homo sapiens' in taxb and 'intact' in source:
				complexes.append(row)

			if counter % 100000 == 0:
				print("Processed {} lines".format(counter))
		
	# Iterate over the complexes and make a dictionary with the complex ids for every source
	for complex_row in complexes:
		complex_id = complex_row[0]
		source = complex_row[12].split('(')[1].rstrip(')')

		if source not in complex_sources:
			complex_sources[source] = []
			complex_sources[source].append(complex_id)
		else:
			complex_sources[source].append(complex_id)
	
	# Make a list with all available sources
	source_list = list(complex_sources.keys())
	print(source_list)
	
	print('complex_ids')
	# Create a dictionary to store the numbers of complexes that are exclusively present in the sources seperately
	unique_counts_per_source = {}
	exclusive_ids_per_source = {}
	for source in source_list:
		complexes_source = set(complex_sources[source])
		for comparison_source in source_list:
			if comparison_source != source:
				complexes_source -= set(complex_sources[comparison_source])
		unique_counts_per_source[source] = len(complexes_source)
		exclusive_ids_per_source[source] = list(complexes_source)
	print('exclusive_ids')

	# Get the data for the exclusive complexes only
	row_dict = {row[0]:row for row in complexes}
	for id_list in exclusive_ids_per_source.values():
		for id in id_list:
			if id in row_dict:
				exclusive_complexes.append(row_dict[id])
	print('data for exclusive complexes')
	# For each complex_id, get the unique methods
	for row in exclusive_complexes:
		complex_id = row[0]
		interaction_method = row[6]
		if complex_id not in complex_method:
			complex_method[complex_id] = set()
			complex_method[complex_id].add(interaction_method)
		else:
			complex_method[complex_id].add(interaction_method)
	print('unique methods')

	# For each method, count the number of occurences
	for complex_id,method in complex_method.items():
		interaction_methods_list.append(method) 
	interaction_methods_list = [tuple(method) for method in interaction_methods_list] # Convert the sets of methods to tuples
	method_counts = dict(Counter(interaction_methods_list))
	print('occurences methods')

	# Convert the method tuple into a string to get rid of the extra parentheses
	for method_tuple,count in method_counts.items():
		method_str = method_tuple[0]
		method_counts_str[method_str] = count

	# Sort the counts of unique methods in descending order
	method_counts_sorted = sorted(method_counts_str.items(), key=lambda x: x[1], reverse=True)
	print('sort')

	# Store the method data in variables to plot them
	method = []
	frequencies = []
	for key,value in method_counts_sorted:
		method_term = key.split('(')[1].rstrip(')')
		method.append(method_term)
		frequencies.append(value)
	
	# Function to add the labels to the bars 
	def addlabels(x,y):
		for i in range(len(x)):
			plt.text(i,y[i]+5,y[i],ha='center')

	# Plot this method data
	fig,ax = plt.subplots()
	ax.bar(method[0:10], frequencies[0:10])
	ax.set(ylim=(0,800),xlabel="Interaction detection method",ylabel="Number of occurences",
	title="Number of occurences of each \ninteraction detection method - corum")
	addlabels(method[0:10],frequencies[0:10])
	plt.xticks(rotation=45, ha='right')
	plt.subplots_adjust(bottom=0.35)
	plt.show()