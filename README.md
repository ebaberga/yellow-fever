# Phylogenetic and evolutionary relationships among Yellow Fever virus isolates in Africa and South America

#### Eden Berga<sup>1,2</sup>, Sidney Bell<sup>1,3</sup>, Trevor Bedford<sup>1</sup>

<sup>1</sup>Vaccine and Infectious Disease Division, Fred Hutchinson Cancer Research Center, Seattle, WA, USA, <sup>2</sup>Mount Rainier High School, Des Moines, WA, USA, <sup>3</sup>Molecular and Cellular Biology Graduate Program, University of Washington, Seattle, WA, USA

## Introduction

	During my stay at the Bedford Lab, I have worked on building a phylogenetic tree for Yellow Fever viruses in Africa and South America. With this project, I intend to show the differences and similarities the viruses have in these regions and make a phylogeography to show the distribution.

For more information about Yellow Fever [click here](links/first.md).

## Project Questions

1.  How similar or Different are yellow fever outbreaks in Africa compared to South America?
2.  What can we tell about the distribution of Yellow Fever among this region, East Africa, West Africa, and South America?

### Targeted regions of my project:

1. East Africa 
2. West Africa
3. South America

_The reason I chose these regions is because they have redundant outbreaks of Yellow Fever since its discovery in 1927._

### Steps towards building my phylogenetic tree:

1.    Downloaded sequences of Yellow Fever virus from Africa and South America.
2.    Made a python script using Jupyter Notebook that extracts sequences with a host of monkey, human being or mosquito, and 	    sequences with countries in Africa and South America (Brazil & Venezuela).
3.    Imported my output file from the script to Geneious. Then used MAFT in Geneious to do my alignments. I used the command        	   line to do my alignment the second time.
4.    Imported my alignment.fasta file from Geneious to Beauti in order to add traits I wanted to express in my tree,country, 	    host, and region, and to convert the extension of the file from .fasta to .xml.
5.    Run Beast to infer evolutionary dynamics from sequence data.
6.    Created an MCC file using tree annotator, and displayed it with Figtree.
## Tree arranged by Country

![](figures/countrytree.png)

## Tree arranged by Region

![](figures/Regiontree.png)

	The tree arranged by country shows that the YF originates from Brazil, and on the other hand the tree arranged by region shows that the virus originates from West Africa. According to the country and region probability on the clades of the trees respectively, Brazil has 0.5324 chance to become an origin, while West Africa has 0.7938 chance. From these, I can conclude that YF is originated in West Africa because the region has more probability to be the ancestor of the tree.

## Tree arranged by Host

![](figures/Host.png)

	The host transmission tree shows that YF originates from a Mosquito. This makes sense because the virus can only be transmitted through Mosquitos. There is no way the virus will go from a monkey to another monkey, from a human to another human and from a human to a monkey or vise verse.

#### Things I understood from my Phylogenetic trees:
*   Most mosquito samples are taken from African countries, while most human samples are from South America(Brazil and 	Venezuela).
*  The virus tends to stay in one region for a long time.
*  The virus jumps from one species to another.
* Most of the time the virus goes from mosquitos to humans.
## Figures

* [Host Transition Rates](figures/yf_host_bf.png)
* [Host Transition Network](figures/yf_host_network.png)
* [Region Transition Rate](figures/yf_region_bf.png)
* [Region Transition Network](figures/yf_region_network.png)

### Phylogeography of Yellow Fever [VIDEO](https://www.youtube.com/watch?v=lEQfEna10jc)

<div class="embed-responsive embed-responsive-16by9">
	<iframe class="embed-responsive-item" src="http://www.youtube.com/embed/lEQfEna10jc"></iframe>
</div>

### [Hypothesis](links/result.md)

### Recent outbreak of Yellow Fever in Angola

	On January 20 2016, Yellow Fever  outbreak was reported in Angola. There is a very high probablity the virus will spread to Asian countries due to high number of Asian people moving in and out of Angola...[here](http://www.ncbi.nlm.nih.gov/pubmed/27156836)

### [What is next](links/next.md)
