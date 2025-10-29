import pandas as pd
import xlwt 

##########################################################################
##############               START FUNCTIONS                ##############

#########################################################################
####   Given the DBN a number vector codifying the DBN is obtained   ####
def dbn2vector(P):
    p = len(P)
    PairsP = []
    for i in range(p):
        if P[i] == '.':
            PairsP.append([i, i])
        elif P[i] == '(':
            PairsP.append([i, 1])
        elif P[i] == ')':
            PairsP.append([i, -1])

    for r in range(p):
        if PairsP[r][1] == -1:  
           for s in range(r):
                if PairsP[r-s][1] == 1:  
                    PairsP[r][1] = PairsP[r-s][0]
                    PairsP[r-s][1] = PairsP[r][0]
                    break
    return (PairsP)

###################################################
##  Given the number vector the DBN is obtained  ##
def vector2dbn(E):
    e = len(E)
    G = ''
    for j in range(e):
        if E[j][0] == E[j][1]:
            G = G+'.'
        elif E[j][0] < E[j][1]:
            G = G+'('
        elif E[j][0] > E[j][1]:
            G = G+')'
    return G

###################################################
###  Looks for one step stems and removes them  ###
def remstep(E):
    e = len(E)
    conte = 0
    for g in range(e-2):
        if E[g][0] == E[g][1] and E[g+1][0] != E[g+1][1] and E[g+2][0] == E[g+2][1]:
            p = E[g+1][1]
            conte = conte+1
    for h in range(conte):
        g = 0
        while g < e-2:
            if E[g][0] == E[g][1] and E[g+1][0] != E[g+1][1] and E[g+2][0] == E[g+2][1]:
                p = E[g+1][1]
                if E[p-1][0] == E[p-1][1] and E[p][0] != E[p][1] and E[p+1][0] == E[p+1][1]:
                    E[g+1][1] = E[g+1][0]
                    E[p][1] = E[p][0]
                    break
            g = g+1
    return E

####################################################
# Removes bulges without two consecutive basepairs #
def rembulge(D):
    E = D
    n = len(E)
    cont = 0
    for g in range(n-2):  # Este es un punto E[g+1][0]==E[g+1][1].
        if E[g+1][0] == E[g+1][1] and D[g][0] != D[g][1] and D[g+2][0] != D[g+2][1]:
            if abs(D[g][1]-D[g+2][1]) < 3:
                cont = cont+1
    for h in range(cont):
        n = len(D)
        i = 0
        while i < n:
            if D[i][0] != D[i][1] and D[i+1][0] == D[i+1][1] and D[i+2][0] != D[i+2][1]:
                if abs(D[i][1]-D[i+2][1]) == 1:
                    for k in range(n):
                        if D[k][0] > D[i+1][0]:
                            D[k][0] = D[k][0]-1
                    for k in range(n):
                        if D[k][1] > D[i+1][1]:
                            D[k][1] = D[k][1]-1
                    D.remove(D[i+1])
                    break
                if abs(D[i][1]-D[i+2][1]) == 2:
                    g=D[i+2][1]+1
                    D[g][1] = D[i+1][0]
                    D[i+1][1]=D[g][0]
            i = i+1
    return D

####################################################
#####  Adds a point to junctions where nedded  ##### 
def addpoint(E): 
  n=len(E)
  cont3=0
  for g in range(n-2):
    if E[g][0]!=E[g][1] and E[g+1][0]!=E[g+1][1]:
        if abs(E[g][1]-E[g+1][1])>1:
          cont3=cont3+1
  for h in range(cont3):
    g=0
    while g<n:
      if E[g][0]!=E[g][1] and E[g+1][0]!=E[g+1][1]:
          if abs(E[g][1]-E[g+1][1])>1:
            for k in range(n):
              if E[k][0]>E[g][0]:
                E[k][0]=E[k][0]+1
            for k in range(n):
              if E[k][1]>E[g][0]:
                E[k][1]=E[k][1]+1
            E.insert(E[g][0]+1, [E[g][0]+1,E[g][0]+1])
            break
      g=g+1
  return E
###############               END FUNCTIONS                ###############
##########################################################################


##########################################################################
##############               START ALGORITHM                ##############

###################################################################################
######### In this part the three sets A=AA0, B=BB0, C=CC0 in DBN are added ########
###################################################################################

##############################
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Hoja 1")
sheet1.write(0,1,'RNAS')
sheet1.write(0,2,'SDBN')
sheet1.write(0,3,'|L|')

PVD=pd.read_excel('lncRNAs_H_DBN.xls')
#PVD=pd.read_excel('no-lncRANs_H_DBN.xls')
#PVD=pd.read_excel('possible-lncARNs_H_DBN.xls')

#############################################################################
######### In this part add the three sets A=AA0, B=BB0, C=CC0 in DBN ########
#############################################################################

AA1=[]
NOMLNC=[]
for I1 in PVD.index:
    AA1.append('...' + PVD['DBN'][I1] + '...')
    NOMLNC.append(PVD['RNAS'][I1])

Reduc=[]

print("\n========================================")
print('Please wait, from DBN to SDBN:')
print("========================================\n")

for j in PVD.index:
      # Apply the Gan rules to each DBN.
      P = AA1[j]
      D = dbn2vector(P)
      H1 = remstep(D)
      H2 = rembulge(H1)
      H3=addpoint(H2)
      H4=remstep(H3)
      K4=vector2dbn(H4)
      
      # Consecutive sequences of the same character reduced to one character.   
      aaa=len(K4)
      B='.'
      for k in range(aaa-1):
          if K4[k]!=K4[k+1]: 
              B=B+K4[k+1]
      print(j,B)
      print()
      Reduc.append(B)
      
      sheet1.write(j+1,0,j)
      sheet1.write(j+1,1,NOMLNC[j])
      sheet1.write(j+1,2,f'{B}')
      sheet1.write(j+1,3,len(B))
      book.save('lncRNAs_H_SDBN.xls')
      #book.save('no-lncRANs_H_SDBN.xls')
      #book.save('possible-lncARNs_H_SDBN.xls')
pass

##############                END ALGORITHM                 ##############

##########################################################################
