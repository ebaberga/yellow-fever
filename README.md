#Phylogenetic and evolutionary relationships among Yellow Fever virus isolates in Africa and South America

####Eden Berga<sup>1,2</sup>, Sidney Bell<sup>1,3</sup>, Trevor Bedford<sup>1</sup>

<sup>1</sup>Vaccine and Infectious Disease Division, Fred Hutchinson Cancer Research Center, Seattle, WA, USA, <sup>2</sup>Mount Rainier High School, Des Moines, WA, USA, <sup>3</sup>Molecular and Cellular Biology Graduate Program, University of Washington, Seattle, WA, USA

![](http://www.historyofvaccines.org/sites/default/files/uploaded-timeline-overview-images/000425_265.jpg)


##Introduction
During my stay at the Bedford Lab I have worked on building a Phylogenetic tree for Yellow Fever viruses in Africa and South America. With this project I intend to show the differences and similarities the viruses have in these regions, and make a phylogeography to show the distribution.

For more information about Yellow Fever [click here] (links/first.md)

##Project Questions
1. How similar or Different are yellow fever outbreaks in Africa compared to South America?
2. What can we say about the distribution of Yellow Fever among this regions, East Africa, West Africa, and South America?


###Targeted regions of my project:
1. East Africa 
2. West Africa
3. South America

_The reason I chose these regions is because they have redundant outbreaks of Yellow Fever since its discovery in 1927._
###Steps towards building my phylogenetic tree:
1. Downloaded sequences of Yellow Fever virus from Africa and South America. 
2.  Made a python script using Jupyter Notebook that extracts sequences with a host of monkey, human being or mosquito, and sequences with a countries in  Africa and South America (Brazil & Venezuela).
3.  Imported my out put file from the script to Geneious. Then used MAFT in Geneious to do my alignments. I used command line to do my aligment the second time. 
4.  Imported my alignment.fasta file from Geneious to Beauti inorder to add traits I wanted to express in my tree,country, host and region, and to convert the extension of the file from .fasta to .xml.
5.  Run Beast to infer evolutionary dynamics from sequence data.
6.  Created an mcc file using tree annotator, and displayed it with Figtree.

##Tree arranged by Country

![](figures/countrytree.png)

##Tree arrange by Region

![](figures/Regiontree.png)

##Tree arrange by Host

![](figures/Host.png)

####Things I understood from my Phylogenetic trees:
* Most mosquito samples are taken from African counties, while most human samples are from South America(Brazil and Venezuela).
* The virus tends to stay in a one region for a long time.
* The virus jump from one species to another.
* Most of the time the virus goes from mosquitos to humans.

##Figures

* [Host Transition Rates](figures/yf_host_bf.png)
* [Host Transition Network](figures/yf_host_network.png)
* [Region Transition Rate](figures/yf_region_bf.png)
* [Region Transition Network](figures/yf_region_network.png)

###Phylogeography of Yellow Fever [VIDEO] (https://www.youtube.com/watch?v=lEQfEna10jc)

<div class="embed-responsive embed-responsive-16by9">
	<iframe class="embed-responsive-item" src="http://www.youtube.com/embed/lEQfEna10jc"></iframe>
</div>

###[Hypothesis](links/result.md)

###[What is next](links/next.md)
