import numpy as np
a=[[1,2,3],[2,3],[2,4,5]]
print([1,2]in a)
b=[]
b.append([1,2])
b.append([4,3])

b.append([2,1])
b.append([5,6])
x=np.array(b)
p=x[:,1]
print(p)
print(b.index([1,2]))
print([i for i,val in enumerate(b) if val==[1,2]])
f=p.tolist().index(1)
print(f)
tab=[1]
print(isinstance(tab,int))
for i in [tab]:
    print("yo",i)




    for indexo in range(0,len(emptyPos)):
        if len(allPossibleVals[indexo])==3 and allPossibleVals[indexo] not in seen3:
            seen3.append(allPossibleVals[indexo])
            seen3index.append([emptyPos[indexo]])
            count.append([0,0,0])
        elif len(allPossibleVals[indexo])==3:
            itsin=False
            g2=[i for i,val in enumerate(seen3) if val==allPossibleVals[indexo]]
            for g in g2:
                x1=seen3index[g][0][0]
                y1=seen3index[g][0][1]
                x2=emptyPos[indexo][0]
                y2=emptyPos[indexo][1]
                sq1=y1-y1%3+x1//3
                sq2=y2-y2%3+x2//3
                if x1==x2 or y1==y2 or sq1==sq2:
                    itsin=True
            if itsin==False:
                seen3.append(allPossibleVals[indexo])
                seen3index.append([emptyPos[indexo]])
                count.append([0,0,0])









        g2=[]
        inside=False
        if len(allPossibleVals[indexo]) == 2:
            for ui in range(0,len(seen3)):
                insidex=allPossibleVals[indexo][0] in seen3[ui]
                insidex=insidex and allPossibleVals[indexo][1] in seen3[ui]
                if insidex==True:
                    inside=True
                    g2.append(ui)
        else:
            inside=allPossibleVals[indexo] in seen3


        if inside:
            uniqueVal=False
            for g in g2:
                x1=seen3index[g][0]
                y1=seen3index[g][1]
                x2=emptyPos[indexo][0]
                y2=emptyPos[indexo][1]
                
                if x1 == x2:
                    count[g][0]=count[indexo][0]+1
                    seen3mode[g].append(0)
                    seen3index[g].append([x2,y2])

                if y1 == y2:
                    count[indexo][1]=count[indexo][1]+1
                    seen3mode[g].append(1)
                    seen3index[g].append([x2,y2])
                
                sq1=y1-y1%3+x1//3
                sq2=y2-y2%3+x2//3
                
                if sq1==sq2:
                    count[indexo][2]=count[indexo][2]+1
                    seen3mode[g].append(2)
                    seen3index[g].append([x2,y2])

