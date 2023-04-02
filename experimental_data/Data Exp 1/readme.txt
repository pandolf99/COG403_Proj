The two files in this folder contain the main experimental data (sca1_data.txt) as well as a data file (sca1_subjs) with relevant subject data (e.g., age, sex, etc.). 

The different column headings in "sca1_data.txt" code the following factors: 

subjID:			a subject-ID
sex:			sex
age:			age
condition:		the four different scenarios shown in Fig. 8 in the manuscript (e.g., "Ons-diff_Delay-same" means the causes had different onset times but identical causal latencies/ delays)
taskOrder:		whether subjects first learned the causal delays or the onset differences (e.g., "DurFirst" means that subjects started with causal latency)
firstTower:		whether subjects began with tower North or tower South (e.g., "FT-North" means "first tower north")
earlyTower:		the tower that minimizes the sum of causal latency and onset time (e.g., "ET-North" means "early tower north")
targetCause:		the tower asked about in the singular causation test query (e.g., "Q-North" means the question referred to tower North)
scaleOrientation:	whether high values were on the left or the right side of the scale (e.g., "HC-L" means that high confidence was on the left side of the scale)
rating: 		the singualr causation rating subjects made (confidence that the tower mentioned in the test query caused the effect)
respTime:		the time (in ms) subjects took to answer the test query 
targetCauseRec:		indicating whether subjects were asked about the cause that minimized the sum of causal delay and onset time or not (e.g., "Early Tower" means that this was the case)
title:			a column used for the title of the panel showing subjects ratings in results graph 


Further column names listed solely in the "sca1_subj.txt" file: 

InstructionCheck_Attempts:	the number of times the subjects did the instruction check until they passed (or dropped out)
totalTime:			the total time subjects needed for completion of the study 
timeFinished:			the absolute time subjects finsihed the study