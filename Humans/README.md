# A-graph-based-algorithm-for-detecting-long-non-coding-RNAs-through-RNA-secondary-structure-analysis
______________________________________________________________________________

We present a graph-based algorithm to represent and  compare RNA secondary structures. Rooted tree graphs were used to compare two groups of Humans RNA sequences: lncRNAs and not lncRNAs, by searching for structural similarities between each group. When applied to a novel candidate sequence dataset, the algorithm evaluated whether characteristic structures identified in known lncRNAs recurred. If so, the sequences were classified as likely lncRNAs.

# These are some basic instructions to use the algorithms necessary to obtain possible lncRNAs. It is divided into four steps:

1. Use a folding program, such as NupackWeb, to give the RNA raw sequences from sets A, B and C, obtain the DBN sets ^A (lncRNAS_H_DBN.xls), ^B (no-lncRNAs_H_DBN.xls) and ^C (possible-lncRNAS_H_DBN.xls).

2. Run the file ¨From_DBN_to_SDBN.py¨ from DBN sets to obtain the sets A, B and C in SDBN.

3. Run the file ¨Bootstrapping Algorithm A.py¨ from SDBN sets to obtain the vector V_R with the results.

You can change the values of the parameters l1-l5:

l1          in line 195.
 
l2          in line 196.

l3          in line 353.

l4          in line 402.

l5          in line 403.

trials     in line 249 (Number of times the algorithm will be executed, default trials=500).
