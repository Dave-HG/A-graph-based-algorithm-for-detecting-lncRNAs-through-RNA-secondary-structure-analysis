import xlwt
import pandas as pd
import numpy as np
import random

##########################################################################
##############               START FUNCTIONS                ##############

'''
compare(seq1, seq2, inf) compares the vectors seq1 and seq2; strings in SDBN,
and establishes the vector subst; substrings shared between them, of length >= inf.
'''

def compare(seq1,seq2,inf):
    a=seq1
    b=seq2
    m=len(b)     # "m" is the maximum length of the text to search.
    minor=inf
    subst=[]     # "subst" saves the found substrings but without repeats.
    start=[]     # "start" is a vector that indicates the start position of a substring.
    end=[]       # "end" is a vector that indicates the end position of a substring.
    ''' It searches substrings of length higher or equal to "minor". '''
    for u in range(0,m-minor+1):     # "u" is the start of the substring to search. Starts from lenght m and stops at lenght minor.
        for v in range(0,u+1):        
            d=b[v:v+(m-u)]           # In each iteration "u", the substrings have the length of m-u.
            m1=len(d)
            a2=a                      
            c=a2.find(d)             # "c" is the first position where is "d". If c=-1 then, d is not in a2.
            t=c                      # "t" will be used to save the start position; the end position will be "c+m1".
            if c>-1:
                if t+1 not in start and t+1+m1 not in end:
                   if d not in subst:
                      subst.append(d)
                   pass
                start.append(t+1)   # Add start position of "d".
                end.append(t+1+m1)  # Add end position of "d".
    return subst

'''
stnorep(subst) analyze the vector subst and select the strings that do not repeat
by establishing the vector comstnotrep; substrings shared without repeating.
'''

def stnotrep(subst):
    comstnorep =[]  # Where all shared substrings without repeats will be saved.
    s=len(subst)    # "s" is the length of substring set.
    for j in range(s):
        if subst[j] not in comstnorep:
            comstnorep.append(subst[j]) # Adds the substring without repeats.
    return comstnorep

'''
matrix(comstnorep, set) counts the times element comstnorep[j] is present in set[i];
'''

def matrix(comstnorep,Set):
    data=[]      # "data" will be the vector of length "a*s" with the number of times
                 # that the substring comstnorep[j] appears in the substring Set[i].
    a=len(Set)
    s=len(comstnorep)
    for i in range(a):
        for j in range(s):
            cont=Set[i].count(comstnorep[j]) # Count the times that the substring comstnorep[j] appear in the substring Set[i].
            data.append(cont)
    Data=np.array(data).reshape(a,s)         # Transform the vector "data" in an "axs" matrix.
    return Data

###############               END FUNCTIONS                ###############
##########################################################################


##########################################################################
#######         The sets A=AA0, B=BB0, C=CC0 in SDBN               #######

PV1=pd.read_excel('lncRNAs_H_SDBN.xls')
PV2=pd.read_excel('no-lncRANs_H_SDBN.xls')
#PV3=pd.read_excel('possible-lncARNs_H_SDBN.xls')

AA0=[]            
NOM1=[]
for I in PV1.index:
    AA0.append(PV1['NPPS'][I])
    NOM1.append((PV1['ARNS'][I]))
    
print('______________')
print('Conjunto A:')
print('______________\n')
#print(AA0)
print(NOM1)

BB0=[]            
NOM2=[]
for I in PV2.index:
    BB0.append(PV2['NPPS'][I])
    NOM2.append((PV2['ARNS'][I]))
    
print('______________')
print('Conjunto B:')
print('______________\n')
#print(BB0)
print(NOM2)

#CC0=[]            
#NOM3=[]
#for I in PV3.index:
#    CC0.append(PV3['NPPS'][I])
#    NOM3.append((PV3['ARNS'][I]))
    
print('______________')
print('Conjunto C:')
print('______________\n')
#print(CC0)
#print(NOM3)

#######      The sets A=AA0, B=BB0, C=CC0 in SDBN                  #######
##########################################################################


##########################################################################
##############               START ALGORITHM                ##############

##########################################################################
##############        Generating .XLS with results          ##############

# Create a workbook and sheet
libro = xlwt.Workbook()
hoja = libro.add_sheet('Sheet 1')

# Write data into cells
hoja.write(0, 0, 'Round j')
hoja.write(0, 1, 'Vector K')
hoja.write(0, 2, 'Vector V_R at round j')

##############        Generating .XLS with results          ##############
##########################################################################

print("\n========================================")
print('Please wait, analyzing the data sets:')
print("========================================\n")

DDS1=AA0   # "DDS1" is the vector of A with the sequences in SDBN.
DDS2=BB0   # "DDS2" is the vector of B with the sequences in SDBN.


############################
# Restriction:
############################
l0=18      # "l0" is the minimum length of repeated substrings that will be searched.

##########################################################################
###########   Compare the substrings in SDBN within each set   ########### 

lng = len(AA0) # Note that len(AA0)=len(BB0).
shseq21=[]     # Save all shared sequences of A with repeats.
shseq22=[]     # Save all shared sequences of B with repeats.

for im in range(lng):
    for jm in range(lng-im-1):
        f1=compare(DDS1[im],DDS1[im+jm+1],l0)
        shseq21.extend(f1)    # Add the shared substrings of A of length >= l1.
        f2=compare(DDS2[im],DDS2[im+jm+1],l0)
        shseq22.extend(f2)    # Add the shared substrings of B of length >= l1.

# Remove the repeated substrings in the set of shared substrings.

SNR21=stnotrep(shseq21)  #repeated sequences from A.
SNR22=stnotrep(shseq22)  #repeated sequences from B.
r1=len(SNR21)
r2=len(SNR22)

###########   Compare the substrings in SDBN within each set   ########### 
##########################################################################


######################################################################################
###  Taking into account strings with lenght between l1 and l2 with l0 < l1 < l2   ###  

############################
# Restriction:
############################
l1=22       #22
l2=34       #34
############################   

SSRRA=[]                   # SSRRA are strings with lenght between l1 and l2 from SNR21.
for ll in range(r1):
  long=len(SNR21[ll])
  if l1 <= long <= l2:
    SSRRA.append(SNR21[ll])

SSRRB=[]                   # SSRRB are strings with lenght between l1 and l2 from SNR22.
for ll in range(r2):
  long=len(SNR22[ll])
  if l1 <= long <= l2:
    SSRRB.append(SNR22[ll])

###  Taking into account strings with lenght between l1 and l2 with l0 < l1 < l2   ### 
######################################################################################

##########################################################################
##########################################################################
### We randomly took quantity=30 subsets of numelements=12 elements of A, Ai, and 30 subsets of to_C=3 elements of A, CAi. The sets Ai and CAi are disjoint. 
### Similarly are obtained the subsets Bj and CBj for j = 1, 2, . . . , 30. 


############################
# Generate random sets
############################
quantity=30                 #30   30     
numelements=35              #12   35
to_C=10                     #6    10       
############################  

print('Using',
quantity,'subsets with',numelements,'elements from A,',
quantity,'subsets with',numelements, 'elements from B and', 
quantity,'subsets with',2*to_C, 'elements', to_C, 'from A and', to_C, 'from B.')
print()

hits=0      # hits keeps track of the number of correctly detected lncRNAs.
p0=0        # pj keeps track of the number of times teh element j from CC0 is detected as lncRNA.
p1=0
p2=0
p3=0
p4=0
p5=0
p6=0
p7=0
p8=0
p9=0
p10=0
p11=0
p12=0
p13=0
p14=0
p15=0
p16=0
p17=0
p18=0
p19=0


n = len(AA0) 
tod = list(range(n))

##########################################################################
##########################################################################

prom=0
trials=500                # Performing trials=500 times the algorithm   $\mathcal{A}(A_i,B_j,CA_3+CB_5)$.

for w in range(trials):  # Vary RC=X[w] each iteration.

    ##########################################################################
    ### Randomly generating lists of numbers from which, in the next 
    ### step, will be used to obtain $A_i,CA_i, B_j,CB_j$ 
    
    ranA=[]
    ranB=[]
    raaC=[]
    rabC=[]
    for k in range(quantity):
      raA=[]
      raB=[]
      raC=[]
      rbC=[]
      
      while len(raA)<numelements+to_C:
        af=random.choice(tod)     
        if af not in raA:
          raA.append(af)
      ranA.append(raA[0:numelements])
      raaC.append(raA[numelements:numelements+to_C])            
     
      while len(raB)<numelements+to_C:
        ag=random.choice(tod)     
        if ag not in raB:
          raB.append(ag)
      ranB.append(raB[0:numelements])
      rabC.append(raB[numelements:numelements+to_C])               
    
    RA=ranA   # "quantity" subsets with "numelements" elements from A.
    RB=ranB   # "quantity" subsets with "numelements" elements from B.
    RaC=raaC  # "quantity" subsets with "to_C" elements from A.
    RbC=rabC  # "quantity" subsets with "to_C" elements from B.

    ### Randomly generating lists of numbers from which, in the next 
    ### step, will be used to obtain $A_i,CA_i, B_j,CB_j$. 
    ##########################################################################

    n70=0  # n_j counts the number of times the j-th RNA in the set $C$ is detected as an lncRNA 
    n71=0  
    n72=0
    n73=0
    n74=0
    n75=0
    n76=0  
    n77=0
    n78=0
    n79=0
    n80=0
    n81=0  
    n82=0
    n83=0
    n84=0
    n85=0
    n86=0  
    n87=0
    n88=0
    n89=0

    ##########################################################################
    ##########################################################################
    ########   The algorithm   $\mathcal{A}(A_i,B_j,CA_3+CB_5)$       ########

    for x in range(quantity):
      for y in range(quantity):

        #############################################################################
        ## Obtaining the sets $A_x,CA_x, B_y,CB_y$ and $D=A_x + B_y+,CA_x, + CB_y$ ##
       
        RAA0=[]
        RBB0=[]
        RCC0=[]
        for j in range(numelements):
          RAA0.append(AA0[RA[x][j]])
          RBB0.append(BB0[RB[y][j]])
    
        RC=RaC[3]+RbC[5]    # We fix the third set to $CA_3+CB_5$
        
        for j in range(to_C):
          RCC0.append(AA0[RC[j]])
        for k in range(to_C):
          RCC0.append(BB0[RC[2+k]])
       
        
        ''' HERE YOU CHOOSE WHICH CC0 IS GOING TO USE '''
        DD0=RAA0+RBB0+RCC0 # Use this set DD0 for bootstrapping.  
        #DD0=RAA0+RBB0+CC0   # Use this set DD0 when CC0 is the set of NOMPOSSIBLES lncRNAs.   
        ''' HERE YOU CHOOSE WHICH CC0 IS GOING TO USE '''         
        
        ## Obtaining the sets $A_x,CA_x, B_y,CB_y$ and $D=A_x + B_y+,CA_x, + CB_y$ ##
        #############################################################################
       
        # Computing matrices $M_{AA}$, $M_{AB}$, $M_{BB}$ and  $M_{BA}$, respectively.
        SSRRAenA=matrix(SSRRA,RAA0) 
        SSRRAenB=matrix(SSRRA,RBB0) 
        SSRRBenB=matrix(SSRRB,RBB0)           
        SSRRBenA=matrix(SSRRB,RAA0)   
            
        # Computing vectors $C_{AA}$, $C_{AB}$, $C_{BB}$ and  $C_{BA}$, respectively.
        SumColAnA=np.sum(SSRRAenA, axis=0)  
        SumColAnB=np.sum(SSRRAenB, axis=0)  
        SumColBnB=np.sum(SSRRBenB, axis=0)  
        SumColBnA=np.sum(SSRRBenA, axis=0)  
        
        # Determining $C_{AA}-C_{AB} \geq l_3=2$ and $C_{BB}-C_{BA}\geq l_3=2$.
        difSSRRA=SumColAnA-SumColAnB     
        difSSRRB=SumColBnB-SumColBnA     
        
        # Determining $S^{'}_{A}$ and $S^{'}_{B}$.  
        L=len(SumColAnA)
        NEWSSRRA=[]                      # is the new vector $S^{'}_{A}$.
        
        ############################
        # Restriction:
        ############################
        l3=2                 #o 3
        ############################
        
        for j in range(L):
          if  difSSRRA[j]>=l3:         
              NEWSSRRA.append(SSRRA[j])
    
        LL=len(SumColBnB)
        NEWSSRRB=[]                      # is the new vector $S^{'}_{B}$.
        for j in range(LL):
          if  difSSRRB[j]>=l3:          
              NEWSSRRB.append(SSRRB[j])
    
        #computing matrices $M^{'}_{AA}$, $M^{'}_{BB}$, $M^{'}_{AD}$, and $M^{'}_{BD}$, respectively. 
        NEWSSRRAenA=matrix(NEWSSRRA,RAA0) 
        NEWSSRRBenB=matrix(NEWSSRRB,RBB0) 
        NEWSSRRAenC=matrix(NEWSSRRA,DD0) 
        NEWSSRRBenC=matrix(NEWSSRRB,DD0) 
             
        #Computing vectors $R_{AA}$, $R_{BB}$, $R_{AD}$ and $R_{BD}$, respectively.
        sumrowNEWSSRRAenA=np.sum(NEWSSRRAenA, axis=1)
        sumrowNEWSSRRBenB=np.sum(NEWSSRRBenB, axis=1)
        sumrowNEWSSRRAenC=np.sum(NEWSSRRAenC, axis=1)          
        sumrowNEWSSRRBenC=np.sum(NEWSSRRBenC, axis=1)  
    
        # Computing quartiles $Q1_A$ and $Q1_B$, respectively.
        q1a=np.quantile(sumrowNEWSSRRAenA, .25)   
        q1b=np.quantile(sumrowNEWSSRRBenB, .25)     

        # Determine if the $i$-th entries $R_{ADi}$ and $R_{BDi}$ satisfy: $R_{ADi}>0.5*Q1_A$ $R_{BDi}<1.5*Q1_B$.
        cc=len(DD0)   
        vector=[]     # It will store the RNAs from C  that pass the restrictions.
        vectorA=[]    # It will store the RNAs from Ax that pass the restrictions.
        vectorB=[]    # It will store the RNAs from By that pass the restrictions.
        
        for kk in range(cc):  
          if ((q1a *.5)<= sumrowNEWSSRRAenC[kk]) and (sumrowNEWSSRRBenC[kk] <= (q1b*1.5)):
            vector.append(kk)
            if (kk<= len(AA0)):
              vectorA.append(kk)
            if ( len(AA0)+1<=kk<=  len(AA0)+ len(AA0)):
              vectorB.append(kk)
              
        # Determine if the numbers $N_A=len(vectorA)$ and $N_B=len(vectorB)$ of elements of $A$ and $B$,
        # satisfy  $N_A\geq l_4=7$ and $N_B\leq l_5=3$.
        
        ############################
        # Restriction:
        ############################
        l4=19
        l5=8
        ############################
        
        if (l4<= len(vectorA)) and (len(vectorB) <= l5):
          if 70 in vector:      # n_j counts the number of times the j-th RNA in the set $C$ is detected as an lncRNA. 
              n70=n70+1
          if 71 in vector:
              n71=n71+1              
          if 72 in vector: 
              n72=n72+1
          if 73 in vector:
              n73=n73+1                
          if 74 in vector:
              n74=n74+1
          if 75 in vector:
              n75=n75+1    
          if 76 in vector:
              n76=n76+1
          if 77 in vector:
              n77=n77+1              
          if 78 in vector: 
              n78=n78+1
          if 79 in vector:
              n79=n79+1                
          if 80 in vector:
              n80=n80+1
          if 81 in vector:
              n81=n81+1 
          if 82 in vector:
              n82=n82+1
          if 83 in vector:
              n83=n83+1              
          if 84 in vector: 
              n84=n84+1
          if 85 in vector:
              n85=n85+1                
          if 86 in vector:
              n86=n86+1
          if 87 in vector:
              n87=n87+1 
          if 88 in vector:
              n88=n88+1
          if 89 in vector:
              n89=n89+1              
           
     
    list=[n70,n71,n72,n73,n74,n75,n76,n77,n78,n79,n80,n81,n82,n83,n84,n85,n86,n87,n88,n89]             # The set $K$.
    aaa=np.amax([n70,n71,n72,n73,n74,n75,n76,n77,n78,n79,n80,n81,n82,n83,n84,n85,n86,n87,n88,n89]) 
    bbb=np.amax([n70,n71,n72,n73,n74,n75,n76,n77,n78,n79])
    if aaa==bbb:
        hits=hits+1
    
    position=list.index(aaa)
    if 0==position:
        p0=p0+1
    if 1==position:
        p1=p1+1
    if 2==position:
        p2=p2+1 
    if 3==position:
        p3=p3+1
    if 4==position:
        p4=p4+1
    if 5==position:
        p5=p5+1     
    if 6==position:
        p6=p6+1
    if 7==position:
        p7=p7+1
    if 8==position:
        p8=p8+1 
    if 9==position:
        p9=p9+1
    if 10==position:
        p10=p10+1
    if 11==position:
        p11=p11+1  
    if 12==position:
        p12=p12+1
    if 13==position:
        p13=p13+1
    if 14==position:
        p14=p14+1 
    if 15==position:
        p15=p15+1
    if 16==position:
        p16=p16+1
    if 17==position:
        p17=p17+1  
    if 18==position:
        p18=p18+1
    if 19==position:
        p19=p19+1
      
    
    V_R=[p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19]                    # The set $V_R$.
    print('Results of round',w+1,':',list, '. Here, is detected as lncRNA the string number:', position+1)
    print('Accumulated results',V_R)
    print()
   
    # Save results to the workbook
    hoja.write(w+1, 0, w+1)
    hoja.write(w+1, 1, str([n70,n71,n72,n73,n74,n75,n76,n77,n78,n79,n80,n81,n82,n83,n84,n85,n86,n87,n88,n89]))
    hoja.write(w+1, 2, str([p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19]))

libro.save('Results.xls')
print('Vector V_R=', V_R)

##############                END ALGORITHM                 ##############
##########################################################################