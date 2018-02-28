import numpy as np
def loadDataSet(fileName):   #读取文件，txt文档
    numFeat = len(open(fileName).readline().split('\t')) #自动检测特征的数目
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr =[]
        curLine = line.strip().split('\t')
        for i in range(numFeat):
            lineArr.append(curLine[i])
        dataMat.append(lineArr)
    return dataMat

def ExportData(data,fileName):#导出
    f=open(fileName,'w')
    for i in data:
        k='\t'.join([str(j) for j in i])
        f.write(k+"\n")
    f.close()


def countvol(data,volnum,start,end,cdt_volnum,cdt_eq):
    '''用于统计data第volnum列的值，落在start和end之间区间的个数,包括start，不包括end
    cdt_volnum为要满足某一条件的另一个列
    cdt_eq为条件应该等于啥'''
    c=0
    for i in range(np.shape(data)[0]):
        if int(data[i,volnum])>=start and int(data[i,volnum])<end and data[i,cdt_volnum]==cdt_eq:
            c+=1
    return c

Schedules=np.array(loadDataSet('/Users/XuLiu/MathC/Schedules.txt'))
#所有机型为9的飞机
Schedules_9=[]
for i in range(np.shape(Schedules)[0]):
    if Schedules[i,5]=='9':
        Schedules_9.append(list(Schedules[i]))
#受到影响的9的飞机
Schedules_impact=[]
for i in range(np.shape(Schedules)[0]):
    if int(Schedules[i,1])>=1461348000 and int(Schedules[i,1])<=1461358800 and Schedules[i,3]=='OVS' and Schedules[i,5]=='9':
        Schedules_impact.append(list(Schedules[i]))
    elif int(Schedules[i,2])<=1461358800 and int(Schedules[i,2])>=1461348000 and Schedules[i,4]=='OVS' and Schedules[i,5]=='9':
        Schedules_impact.append(list(Schedules[i]))
Schedules_impact=np.array(Schedules_impact)

plane_impact=list(set(list(Schedules_impact[:,-1])))#受到影响的飞机编号
##################################


Schedules_alt=np.zeros((np.shape(Schedules)[0],10))
Schedules_alt=Schedules_alt.astype(np.str)
for i in range(np.shape(Schedules)[0]):
    Schedules_alt[i,0:7]=Schedules[i,:]

for x in plane_impact:
    plane_test = []
    for i in range(np.shape(Schedules)[0]):
        if Schedules[i, -1] == x:
            plane_test.append(list(Schedules[i, :]))
    plane_test = np.array(plane_test)

    #plane_test[np.lexsort(plane_test[:, ::-1].T)]

    plane_alt = np.zeros(np.shape(plane_test))
    plane_alt = plane_alt.astype(np.str)

    for i in range(np.shape(plane_test)[0]):
        plane_alt[i, :] = plane_test[i, :]

    for i in range(np.shape(plane_test)[0]):
        if int(plane_alt[i, 1]) >= 1461348000 and int(plane_alt[i, 1]) <= 1461358800 and plane_test[i, 3] == 'OVS':
            if i == 0:
                plane_alt[i, 1] = 1461358800
                plane_alt[i, 2] = 1461358800 + int(plane_test[i, 2]) - int(plane_test[i, 1])
            else:
                plane_alt[i, 1] = int(plane_alt[i - 1, 2]) + 2700
                plane_alt[i, 2] = int(plane_alt[i, 1]) + int(plane_test[i, 2]) - int(plane_test[i, 1])
        if int(plane_alt[i, 2]) >= 1461348000 and int(plane_alt[i, 2]) <= 1461358800 and plane_test[i, 4] == 'OVS':
            plane_alt[i, 2] = 1461358800
            plane_alt[i, 1] = 1461358800 - (int(plane_test[i, 2]) - int(plane_test[i, 1]))
        if i > 0:
            if int(plane_alt[i, 1]) < (int(plane_alt[i - 1, 2]) + 2700):
                plane_alt[i, 1] = int(plane_alt[i - 1, 2]) + 2700
                plane_alt[i, 2] = int(plane_alt[i, 1]) + int(plane_test[i, 2]) - int(plane_test[i, 1])
        plane_alt[i, 2] = int(plane_alt[i, 1]) + int(plane_test[i, 2]) - int(plane_test[i, 1])

    for i in range(np.shape(plane_alt)[0]):
        for j in range(np.shape(Schedules_alt)[0]):
            if Schedules_alt[j,0]==plane_alt[i,0]:
                Schedules_alt[j,7]=plane_alt[i,1]
                Schedules_alt[j,8]=plane_alt[i,2]

for i in range(np.shape(Schedules)[0]):
    if float(Schedules_alt[i,7])==0:
        Schedules_alt[i,7:9]=Schedules_alt[i,1:3]
    if int(Schedules_alt[i,7])-int(Schedules_alt[i,1])==int(Schedules_alt[i,8])-int(Schedules_alt[i,2]):
        Schedules_alt[i,-1]=int(Schedules_alt[i,7])-int(Schedules_alt[i,1])

Tot_delay=0
for i in range(np.shape(Schedules_alt)[0]):
    Tot_delay+=int(Schedules_alt[i,-1])
########################################################

ovs_time_min=1461298260
ovs_time_max=1461438300
ovs_time=[]#时间可能的取值
time=ovs_time_min
while time<=ovs_time_max:
    ovs_time.append(time)
    time+=150

#0时间区间，1起飞个数，2落地个数
time_count=np.zeros((np.shape(ovs_time)[0],3))
time_count=time_count.astype(np.str)
for i in range(np.shape(time_count)[0]-1):
    time_count[i,0]=ovs_time[i]
    time_count[i,1]=countvol(Schedules_alt,7,ovs_time[i],ovs_time[i+1],3,'OVS')
    time_count[i,2]=countvol(Schedules_alt,8,ovs_time[i],ovs_time[i+1],4,'OVS')

######################################
'''9型飞机延误的有9个从1461358800时间落地，但是一个时间段最多只能5个落地，
则分析这9个看哪个能往后延5*60个时间'''

change_landing=[]
for i in range(np.shape(Schedules_alt)[0]):
    if Schedules_alt[i,8]=='1461358800' and Schedules_alt[i,4]=='OVS':
        change_landing.append(Schedules_alt[i,6])

change_sche=[]
for x in change_landing:
    for i in range(np.shape(Schedules_alt)[0]):
        if Schedules_alt[i,6]==x:
            change_sche.append(list(Schedules_alt[i]))
change_sche=np.array(change_sche)

#####第一步，往后延迟落地的是第二波飞行不受此处延误影响的

for i in range (np.shape(change_sche)[0]-1):
    if int(change_sche[i,8])==1461358800 and int(change_sche[i+1,9])==0:
        change_sche[i,7]=int(change_sche[i,7])+300
        change_sche[i,8]=1461358800+300
    if int(change_sche[i,7])-int(change_sche[i,1])==int(change_sche[i,8])-int(change_sche[i,2]):
        change_sche[i,-1]=int(change_sche[i,8])-int(change_sche[i,2])

###第二个版本叫Schedules_alt_1，创建，把原来的靠过来
Schedules_alt_1=np.zeros(np.shape(Schedules_alt))
Schedules_alt_1=Schedules_alt_1.astype(np.str)
for i in range(np.shape(Schedules_alt_1)[0]):
    Schedules_alt_1[i,:]=Schedules_alt[i,:]

###将第一步改的时间，看看会不会影响第二版航程
for x in change_landing:
    change_alt = []
    for i in range(np.shape(change_sche)[0]):
        if change_sche[i, 6] == x:
            change_alt.append(list(change_sche[i, :]))
    change_alt = np.array(change_alt)


    for i in range(np.shape(change_alt)[0]):
        if i > 0:
            if int(change_alt[i, 7]) < (int(change_alt[i - 1, 8]) + 2700):
                change_alt[i, 7] = int(change_alt[i - 1, 8]) + 2700
                change_alt[i, 8] = int(change_alt[i, 7]) + int(change_test[i, 8]) - int(change_test[i, 7])
    ###将改好的这个飞机的航线时间改到Schedules_alt_1上
    for i in range(np.shape(change_alt)[0]):
        for j in range(np.shape(Schedules_alt_1)[0]):
            if Schedules_alt_1[j,0]==change_alt[i,0]:
                Schedules_alt_1[j,7]=change_alt[i,7]
                Schedules_alt_1[j,8]=change_alt[i,8]
                Schedules_alt_1[j,9]=change_alt[i,9]


Tot_delay_1=0
for i in range(np.shape(Schedules_alt_1)[0]):
    Tot_delay_1+=int(Schedules_alt_1[i,-1])

#0时间区间，1起飞个数，2落地个数
time_count_1=np.zeros((np.shape(ovs_time)[0],3))
time_count_1=time_count_1.astype(np.str)
for i in range(np.shape(time_count_1)[0]-1):
    time_count_1[i,0]=ovs_time[i]
    time_count_1[i,1]=countvol(Schedules_alt_1,7,ovs_time[i],ovs_time[i+1],3,'OVS')
    time_count_1[i,2]=countvol(Schedules_alt_1,8,ovs_time[i],ovs_time[i+1],4,'OVS')

ExportData(Schedules_alt_1,'/Users/XuLiu/MathC/1Schedules_alt_1.txt')



