#input: beast .log file with country.actualRates and country.indicator parameters; xml with list of country classes (in order)
#output: rates and bf: csv with formatted matrices, heatmaps. network diagram.
#expects: script.py logfile xml burnin(integer; n states)
#burnin must be a sampled state; removal is inclusive

print 'loading modules'
import argparse
import elementtree.ElementTree as ET
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

#################### Parse and reformat input #####################
print 'parsing input'

parrot = argparse.ArgumentParser(description="Analyze log files; make figures.")
parrot.add_argument('-burnin', default=5000000, type=int, help="Number of states to remove as burnin.")
parrot.add_argument('-cutoff', default=5.0, type=float, help="BF Cutoff for Network Diagram.")
parrot.add_argument('-logfile', type=str, help=".log file to be analyzed.")
parrot.add_argument('-xml', type=str, help=".xml to pull country (& host) states and priors from.")
args = vars(parrot.parse_args())
burnin, logfile, xmlfile, cutoff = args['burnin'], open(args['logfile'], 'r'), open(args['xml'], 'r'), args['cutoff']

log_data = pd.read_csv(logfile, skiprows=2, sep="\t", index_col='state')	#parse the log file as a df
logfile.close()


xml = ET.parse(xmlfile)	
root = xml.getroot()												#get the list of countries (and/or hosts), in order, from the xml
traits = root.findall('generalDataType')
host_list = None
for trait in traits:
	if trait.get('id').startswith('host'):
		host_list = [ state.get('code') for state in trait ]
		n_hosts = len(host_list)
	elif trait.get('id').startswith('country'):
		country_list = [ state.get('code') for state in trait ] 
		n_countries = len(country_list)

xmlfile.close()
print 'found these %d countries:'%len(country_list)
print country_list
if host_list:
	print 'found these %d hosts:'%len(host_list)
	print host_list

################# Deal with burnin, make data structures ###############################

												
assert burnin in log_data.index, ('ERROR: burnin must be a sampled state. Valid options are:', log_data.index)

burnin_indices = [range(0, log_data.index.get_loc(burnin)+1)] #drop (inclusively) all states before the specified burnin state.
log_data.drop(log_data.index[burnin_indices], inplace=True)

log_data = log_data.append(pd.DataFrame(log_data.mean(), columns=['avg']).T)	#get the average posterior values for each column

def find_bf(indicator_avg, prior_expectation, n_demes, len_chain=50000000): # Demes == 'categories' (e.g., countries, or host species)
	priorProbabilityNumerator = prior_expectation					# Number of transitions we 'guessed' would have happened before seeing the data
	priorProbabilityDenominator = (n_demes**2) - n_demes			# Total number of transitions that *could* have happened
	priorProbability = float(priorProbabilityNumerator)/float(priorProbabilityDenominator)	# Probability = number of 'successes' / total possible ways to 'win'
	priorOdds = float(priorProbability) / float(1-priorProbability) # Odds = probability / (1 - probability)
	posteriorOdds=(((indicator_avg-(1/float(len_chain)))/float((1-(indicator_avg-(1/float(len_chain)))))))	# Indicator average value is the actual observed probability; posterior odds then = p / (1-p) as above.
	bf = float(posteriorOdds) / float(priorOdds) # Bayes factor = posterior odds / prior odds. I.e., how much more certain are we of this transition *after* seeing the data than we were *before* we saw the data? 
	return bf


def fill_matrix(df, series):

	#did we give it an appropriately sized df?
	assert len(df.columns) == len(df.index)		
	n_demes = len(df.columns)
	n_params = len(series)
	#do we have a valid number of parameters?
	assert n_params == (n_demes**2) - n_demes, 'ERROR: invalid number of parameters'

	skip_to = 1									#the [0,0] index of the df is on the diagonal; skip it, and fill to the end fo the row.
	for index, row in df.iterrows():
		if skip_to == len(row):					#unless we've run off the end of the matrix....
			break
		else:
			fill_length = len(row) - skip_to	#we need to fill from the skip_to starting point to the end of the row.
			row[skip_to:len(row)] = series[0:fill_length]	#fill those in from the series
			series = series[fill_length:]		#trim the already-used values off the series.
			skip_to += 1						#bump over one more when we start the next row.
				
									
	skip_to = 1									#do the same thing to fill the bottom triangle, but iterate over columns, rather than rows.
	for index, column in df.iteritems():
		if skip_to == len(column):					
			break
		else:
			fill_length = len(column) - skip_to	
			column[skip_to:len(column)] = series[0:fill_length]	
			series = series[fill_length:]		
			skip_to += 1						
			
	assert len(series) == 0						#there's something wrong if we still have values left.
	return df

def make_heatmap(matrix, title, outfilename):		#make simple heatmaps; save to file.
	plt.figure(figsize=(13,9))
	heatmap = sns.heatmap(matrix, cmap = plt.cm.GnBu, square = True, linecolor = 'black', robust=True, linewidths = 0.5, annot=True)
	heatmap.axes.set_title(title)
	plt.yticks(rotation=0)
	plt.xticks(rotation=90) 
	plt.tight_layout(pad=1)
	plt.savefig(outfilename)
	plt.clf()

#############  Fill data structures ###################
file_stem = args['logfile'].split('/')[-1].split('.')[0].split('_')[0]

print 'filling data structures'
country_actualRates = pd.DataFrame(dtype = 'float', index=country_list, columns=country_list)	#make empty DFs to hold the actual rates and the bf
country_bf = pd.DataFrame(dtype = 'float', index=country_list, columns=country_list)

country_actualRates_series = pd.Series([ series['avg'] for column, series in log_data.iteritems() if 'country.actualRates' in column ]) #pull the average posterior values from appropriate columns in order
#convert indicators to bayes factors while we're at it
country_bf_series = pd.Series([ find_bf(series['avg'], n_countries-1, n_countries) for column, series in log_data.iteritems() if 'country.indicator' in column ]) #we will then use this to fill our matrices.

country_actualRates = fill_matrix(country_actualRates, country_actualRates_series)				#fill our matrices
country_bf = fill_matrix(country_bf, country_bf_series)

country_actualRates.to_csv(file_stem+'_country_actualRates.csv')								#and write them to file
country_bf.to_csv(file_stem+'_country_bf.csv')

country_bf_name = "%s_country_bf.png"%file_stem
country_actualrates_name = "%s_host_AR.png"%file_stem
country_map_name = "%s_country_network.png"%file_stem


make_heatmap(country_actualRates, 'Geographic Transition Rates', country_actualrates_name)		# Make pretty heat map figures.
make_heatmap(country_bf, 'Bayes Factors for Geographic Transitions', country_bf_name)


## If we have a host trait, too, then do the same for this data.

if host_list:
	print 'filling data structures'
	host_actualRates = pd.DataFrame(dtype = 'float', index=host_list, columns=host_list)	#make empty DFs to hold the actual rates and the bf
	host_bf = pd.DataFrame(dtype = 'float', index=host_list, columns=host_list)

	host_actualRates_series = pd.Series([ series['avg'] for column, series in log_data.iteritems() if 'host.actualRates' in column ]) #pull the average posterior values from appropriate columns in order
	#convert indicators to bayes factors while we're at it
	host_bf_series = pd.Series([ find_bf(series['avg'], n_hosts-1, n_hosts) for column, series in log_data.iteritems() if 'host.indicator' in column ]) #we will then use this to fill our matrices.

	host_actualRates = fill_matrix(host_actualRates, host_actualRates_series)				#fill our matrices
	host_bf = fill_matrix(host_bf, pd.Series(host_bf_series))

	host_actualRates.to_csv(file_stem+'_host_actualRates.csv')								#and write them to file
	host_bf.to_csv(file_stem+'_host_bf.csv')

	host_bf_name = "%s_host_bf.png"%file_stem													# Make pretty heat map figures.
	host_actualrates_name = "%s_host_AR.png"%file_stem
	host_map_name = "%s_host_network.png"%file_stem

	make_heatmap(host_actualRates, 'Host Transition Rates', host_actualrates_name)
	make_heatmap(host_bf, 'Bayes Factors for Host Transitions', host_bf_name)


######################### Make a pretty network diagram ########################################

print 'making network map'

nparams = len(country_actualRates_series)

G = nx.DiGraph()						#initialize a networkx graph
directed = True

G.add_nodes_from(country_list)			#each deme is a node

for from_country in country_list:
	for to_country in country_list:
		bayesfactor = country_bf.at[from_country, to_country]
		rate = country_actualRates.at[from_country, to_country]
		if bayesfactor >= 5and rate > 0:
			G.add_edge(from_country, to_country,{'rate': '%.3f'%rate, 'support': bayesfactor})
		else:
			continue


#networkx apparently can't access its native node names when graphing.
node_labels = {}						
for node,d in G.nodes(data=True):
	node_labels[node] = node

#nor can it access edge attributes as weights. so, pull them manually.
bf = [float(G[u][v]['support']) for u,v in G.edges()]	
rates = [float(G[u][v]['rate'])*1.5 for u,v in G.edges()]

#make network; show, rather than saving to file.
plt.figure(figsize=(15,10))
pos = nx.spring_layout(G, iterations=20, k=2)	#set layout
nx.draw(G, pos, edges=G.edges(), width=rates, edge_color='dimgray', node_color=range(len(country_list)), cmap=plt.cm.viridis, alpha=0.6, node_size = 2000)
nx.draw_networkx_labels(G, pos, node_labels=node_labels, fontsize=28, font_weight='bold')
plt.bbox_inches="tight"
plt.savefig(country_map_name)

if host_list:
	print 'making network map'

	nparams = len(host_actualRates_series)

	G = nx.DiGraph()						#initialize a networkx graph
	directed = True

	G.add_nodes_from(host_list)			#each deme is a node

	for from_host in host_list:
		for to_host in host_list:
			bayesfactor = host_bf.at[from_host, to_host]
			rate = host_actualRates.at[from_host, to_host]
			if bayesfactor >= 5 and rate > 0:
				G.add_edge(from_host, to_host,{'rate': '%.3f'%rate, 'support': bayesfactor})
			else:
				continue


	#networkx apparently can't access its native node names when graphing.
	node_labels = {}						
	for node,d in G.nodes(data=True):
		node_labels[node] = node

	#nor can it access edge attributes as weights. so, pull them manually.
	bf = [float(G[u][v]['support']) for u,v in G.edges()]	
	rates = [float(G[u][v]['rate'])*1.5 for u,v in G.edges()]

	#make network; show, rather than saving to file.
	plt.figure(figsize=(15,10))
	pos = nx.spring_layout(G, iterations=20, k=2)	#set layout
	nx.draw(G, pos, edges=G.edges(), width=rates, edge_color='dimgray', node_color=range(len(host_list)), cmap=plt.cm.viridis, alpha=0.6, node_size = 2000)
	nx.draw_networkx_labels(G, pos, node_labels=node_labels, fontsize=28, font_weight='bold')
	plt.bbox_inches="tight"
	plt.savefig(host_map_name)
