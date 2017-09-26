Atr=[]
n=int(input("Enter the total no of entities:"))
for x in range(n):
    L=[]
    print('Enter in the given format: Entity/type[attr1(cons1-cons2-...),attr2(cons1-cons2-...)')
    string=input()
    replacements=('/','[','(',')',',',']') #fix
    for r in replacements:
        string = string.replace(r,' ')
    L=string.split()
    L1=[]
    L2=[]
    L3=[]
    L4=[]
    L1.append(L[0])
    L2.append(L[1])
    for v in range(2,len(L),2):
        L3.append(L[v])
    print(L3)
    for i in range(3,len(L),2):
        L4.append(L[i])
    d={}
    L5=[]
    for y in range(len(L3)):
        d[L3[y]]=L4[y].split('-')
    L5.append(d)
    Atr.append(L5)

print('enter in the given format: Entity1[Relation1(Cardinality1),Relation2(Cardinality1)....];'
      'Entity2(Relation1(Cardinality1),Relation2(Cardinality1)....);')
string0=input()
replacements=(';') #fix
for r in replacements:
    string0 = string0.replace(r,' ')
string0 =string0.split()
EntRel = {}
EntCar = {}
RelRel = {}
for en in string0:
    replacement1 = ('(', ')', '[', ',', ']')
    for r in replacement1:
        en=en.replace(r,' ')
    en=en.split()
    key_temp = en[0]
    val_rel_temp = []
    val_car_temp = []
    for i in range(1,len(en),2):
        val_car_temp.append(en[i+1])
        val_rel_temp.append(en[i])
        check=0
        for kk in RelRel.keys():
            if kk ==en[i] and RelRel[kk] == 'identify':
                check=1
        if check ==1:
            continue
        if en[i+1] == 'W':
            RelRel[en[i]]= 'identify'
        else:
            RelRel[en[i]] = 'none'

    EntCar[key_temp]=val_car_temp
    EntRel[key_temp]=val_rel_temp
print(EntRel)
print(EntCar)
print(RelRel)
print(Atr)

'''
#Test Lists
listREL = {'Assigned':'none','Manages':'none','Teaches':'none'}
listEN = {'Employee':['Teacher','Clerk','HOD'],'Student':['Teaches','Assigned'],'Teacher':['Teaches','Manages'],'HOD':['Manages'],
          'Courses':['Teaches'],'Rooms':['Assigned'],'Clerk':[]}
listCAR = {'Employee':['N','N','N'],'Student':['1','1'],'HOD':['1'],'Courses':['N'],'Rooms':['1'],'Teacher':['1','1'],'Clerk':[]} #1:one , N:many ,W:weak->always many-one
listAT = [
            [{'EID': ['P', 'N'],'History': ['N', 'N'],'Name':['N','N'],'ContactNo':['N','M']}],
            [{'Name':['N','N'],'ID':['P','N']}],[{'ID':['P','N'],'Salary':['N','N'],'Major':['N','N']}],
            [{'HeadID':['P','N'],'Underling':['N','N'],'ContactNo':['P','N']}],[{'CID':['P','N'],'Name':['N','M']}],
            [{'RoomID':['P','N'],'Chairs':['N','M'],'Floor':['N','N']}]
         ]
'''
listEN = EntRel
listREL = RelRel
listCAR = EntCar
listAT = Atr


#function define and render
from graphviz import *
import os
os.environ["PATH"] += os.pathsep + 'C:/Graphviz2.38/bin/'

def relation(x,r):
    for key,value in r.items():
        if value=='identify':
            type='Mdiamond'
        else:
            type='diamond'
        x.node(key,shape=type)

def entity(x,l,c,rel):

    for key,value in l.items():
        count = 0  # number of classifications
        if 'W' in c[key]:
            sh='box3d'
        else:
            
            
            sh='rect'
        x.node(key, shape=sh)
        for i in range(0,len(value)):

            if c[key][i]=='N':      #cardinality is many
                point='none'
            else:
                point='diamond'
            if 'W' in c[key] and rel[value[i]]=='identify':       #if entity is weak , hence cardinality is always one-many
                point='none'
                x.edge(value[i],key, len='1.50', dir='both', arrowhead='none', arrowtail=point)
            if value[i] in list(l):

                if count==0:
                    new=key+'cls'
                    x.node(new,label='IS-A',shape='invtriangle')
                    x.attr('node',shape='rect')
                    x.edge(key,new,dir='none',penwidth='3')
                    x.edge(value[i],new,dir='none')
                    count=1
                else:
                    x.edge(value[i], new, dir='none')
            else:
                x.edge(key,value[i],dir='both',arrowhead='none',arrowtail=point)

def attribute(x,e,a):

    temp=list(e)

    for i in range(0,len(a)):
        for j in range(0,len(a[i])):
            if len(a[i][j])!=0:
                id=0
                for atr,ctr in a[i][j].items():
                    sty = 'solid' #style
                    shp = 'circle' #shape
                    #Keys
                    if ctr[0]=='P':
                        col='red'
                        wid = '2'
                    elif ctr[0]=='F':
                        col='blue'
                        wid = '2'
                    else:
                        col='black'
                        wid = '1'
                    #AttributeType
                    if ctr[1]=='D':
                        sty = 'dashed'
                    elif ctr[1]=='M':
                        shp = 'doublecircle'
                    foo=str(temp[i])+str(id) #temp id variable
                    # print(foo)
                    x.node(foo,label=str(atr),color=col,penwidth=wid,shape=shp,style=sty,fontsize='10')
                    x.edge(temp[i],foo,dir='none')
                    id+=1

check=0 #check Cardinality and Entity list: number of relation must match cardinalities given
for keyE in listEN.keys():

    if len(listEN[keyE]) != len(listCAR[keyE]):
        print("Relations-Cardinality Mismatch for - ",keyE)
        check=1
if check==0:
    page = Digraph(name='Model', engine='neato')
    relation(page, listREL)
    entity(page,listEN,listCAR,listREL)
    attribute(page, listEN, listAT)
    page.edge_attr.update(len='1.3')
    page.format = 'png'
    page.render('test-output/Final.gv', view=True)

