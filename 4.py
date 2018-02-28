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
        if float(data[i,volnum])>=start and float(data[i,volnum])<end and data[i,cdt_volnum]==cdt_eq:
            c+=1
    return c

pas_0=np.array(loadDataSet('/Users/XuLiu/MathC/4Pas_0.txt'))

#得到unique的飞机编号
plane_id=[]
for i in range(np.shape(pas_0)[0]):
    if pas_0[i,0] not in plane_id:
        plane_id.append(pas_0[i,0])

##计算每架航班上的人数
plane_count = np.zeros((np.shape(plane_id)[0], 2))
for i in range(np.shape(plane_id)[0]):
    plane_count[i, 0] = int(plane_id[i])

for i in range(np.shape(pas_0)[0]):
    for j in range(np.shape(plane_count)[0]):
        if float(pas_0[i, 0]) == plane_count[j, 0]:
            plane_count[j, 1] = float(plane_count[j, 1]) + float(pas_0[i, 11])

ExportData(plane_count, "/Users/XuLiu/MathC/4plane_count.txt")
#########################################
#首先，买联行的旅客到达时间距离其下一班飞机的离开时间要为2700，此处纯粹按人改，然后max改到飞机上，然后再改到人上
pas_00=np.zeros(np.shape(pas_0))
pas_00=pas_00.astype(np.str)
for i in range(np.shape(pas_00)[0]):
    pas_00[i,:]=pas_0[i,:]

for i in range(np.shape(pas_00)[0]-1):
    if pas_00[i,10]==pas_00[i+1,10] and pas_00[i,11]==pas_00[i+1,11] \
            and int(pas_00[i,8])+2700>int(pas_00[i+1,7]):
        pas_00[i+1,7]=max(int(pas_00[i,8])+2700,int(pas_00[i+1,1]))
        pas_00[i+1,8]=int(pas_00[i+1,7])+int(pas_00[i+1,2])-int(pas_00[i+1,1])
    if int(pas_00[i,8])-int(pas_00[i,2])==int(pas_00[i,7])-int(pas_00[i,1]):
        pas_00[i,9]=int(pas_00[i,7])-int(pas_00[i,1])

#飞机为单位的表，2Schedules_alt_00.txt作为初始
Schedules_0=np.array(loadDataSet('/Users/XuLiu/MathC/2Schedules_alt_00.txt'))

Schedules_01=np.zeros((np.shape(Schedules_0)[0],np.shape(Schedules_0)[1]-1))
Schedules_01=Schedules_01.astype(np.str)
for i in range(np.shape(Schedules_01)[0]):
    Schedules_01[i,:]=Schedules_0[i,0:10]

for i in range(np.shape(Schedules_01)[0]):
    for j in range(np.shape(pas_00)[0]):
        if pas_00[j,0]==Schedules_01[i,0] and int(pas_00[j,7])>int(Schedules_01[i,7]):
            Schedules_01[i,7]=pas_00[j,7]
            Schedules_01[i,8]=pas_00[j,8]
            if int(Schedules_01[i, 8]) - int(Schedules_01[i, 2]) == int(Schedules_01[i, 7]) - int(Schedules_01[i, 1]):
                Schedules_01[i, 9] = int(Schedules_01[i, 7]) - int(Schedules_01[i, 1])

##将以飞机为单位的时间Schedules_01再统一改到乘客那个表pas_00上
for i in range(np.shape(pas_00)[0]):
    for j in range(np.shape(Schedules_01)[0]):
        if pas_00[i,0]==Schedules_01[j,0] and pas_00[i,7]!=Schedules_01[j,7]:
            pas_00[i,7]=Schedules_01[j,7]
            pas_00[i,8]=Schedules_01[j,8]


#########计算总延迟，若联行，第一班的延迟但第二班的不延迟，则都算不延迟，
#若第二班延迟，无论第一班延迟还是不延迟都算延迟，总延迟为航班延迟*人数

pas_01=np.zeros((np.shape(pas_00)[0],np.shape(pas_00)[1]+1))#最后一列为次旅客的延误
pas_01=pas_01.astype(np.str)

for i in range(np.shape(pas_01)[0]):
    pas_01[i,0:12]=pas_00[i,:]

for i in range(np.shape(pas_01)[0]-1):
    if pas_01[i,10]==pas_01[i+1,10] and pas_01[i,11]==pas_01[i+1,11]:
        pas_01[i,12]=int(pas_01[i+1,9])*int(pas_01[i+1,11])
        pas_01[i+1,12]=pas_01[i,12]

#########计算每架航班的总延迟
plane_delay_0=np.zeros((np.shape(plane_id)[0],2))
for i in range(np.shape(plane_id)[0]):
    plane_delay_0[i,0]=int(plane_id[i])

for i in range(np.shape(pas_01)[0]):
    for j in range(np.shape(plane_delay_0)[0]):
        if float(pas_01[i,0])==plane_delay_0[j,0]:
            plane_delay_0[j,1]=float(plane_delay_0[j,1])+float(pas_01[i,12])


ExportData(plane_delay_0,"/Users/XuLiu/MathC/4plane_delay_0.txt")
ExportData(pas_01,"/Users/XuLiu/MathC/4pas_01.txt")
ExportData(Schedules_01,"/Users/XuLiu/MathC/4Schedules_01.txt")

ovs_time_min=1461298260
ovs_time_max=1461438300
ovs_time=[]#时间可能的取值
time=ovs_time_min
while time<=ovs_time_max:
    ovs_time.append(time)
    time+=300

#0时间区间，1起飞个数，2落地个数
time_count_0=np.zeros((np.shape(ovs_time)[0],3))
time_count_0=time_count_0.astype(np.str)
for i in range(np.shape(time_count_0)[0]-1):
    time_count_0[i,0]=ovs_time[i]
    time_count_0[i,1]=countvol(Schedules_01,7,ovs_time[i],ovs_time[i+1],3,'OVS')
    time_count_0[i,2]=countvol(Schedules_01,8,ovs_time[i],ovs_time[i+1],4,'OVS')
ExportData(time_count_0,"/Users/XuLiu/MathC/4time_count_0.txt")




###################################下面的已改好5升5降
Schedules_1=np.array(loadDataSet('/Users/XuLiu/MathC/4Schedules_1.txt'))
ovs_time_min=1461298260
ovs_time_max=1461438300
ovs_time=[]#时间可能的取值
time=ovs_time_min
while time<=ovs_time_max:
    ovs_time.append(time)
    time+=300

#0时间区间，1起飞个数，2落地个数
time_count_1=np.zeros((np.shape(ovs_time)[0],3))
time_count_1=time_count_1.astype(np.str)
for i in range(np.shape(time_count_1)[0]-1):
    time_count_1[i,0]=ovs_time[i]
    time_count_1[i,1]=countvol(Schedules_1,7,ovs_time[i],ovs_time[i+1],3,'OVS')
    time_count_1[i,2]=countvol(Schedules_1,8,ovs_time[i],ovs_time[i+1],4,'OVS')
ExportData(time_count_1,"/Users/XuLiu/MathC/4time_count_1.txt")




############################################################

alter_round=[]
for i in range(np.shape(Schedules_1)[0]-2):
    if int(Schedules_1[i,9])!=0 and Schedules_1[i,4]=='OVS'\
        and Schedules_1[i+1,3]=='OVS' and int(Schedules_1[i+1,9])!=0\
        and Schedules_1[i+2,4]=='OVS' and int(Schedules_1[i+2,9])!=0:
        alter_round.append(list(Schedules_1[i+1]))
        alter_round.append(list(Schedules_1[i+2]))
alter_round=np.array(alter_round)

alter_ID=[]
for i in range(np.shape(alter_round)[0]):
    if i%2==0:
        alter_ID.append(alter_round[i,0])

def delay_time_file(ID,Schedules_alt_0,maybe_change_time,n):
    '''ID 为待置换的航班的唯一编号
    n 为第n对
    生成文件delay_time_file,格式为：
    A的计划离开OVS   A的计划到达某地  A的置换后实际离开OVS A的置换后实际到达某地    A的此趟的总延误
    A的计划离开某地   A的计划到达OVS  A的置换后实际离开某地  A的置换后实际到达OVS   A的此趟的总延误
    B的计划离开OVS   B的计划到达某地  B的置换后实际离开OVS B的置换后实际到达某地    B的此趟的总延误
    B的计划离开某地   B的计划到达OVS  B的置换后实际离开某地  B的置换后实际到达OVS   B的此趟的总延误
'''
##计算置换后的延误总和
    for i in range(np.shape(Schedules_alt_0)[0]):
        if Schedules_alt_0[i, 0] == ID:
            last_leave_time = float(Schedules_alt_0[i, 7])  # 要比A航班能离开的最早时间last_leave_time要早才有换的意义
            plan_leave_time = float(Schedules_alt_0[i, 1])  # 要比A航班原计划的离开时间plan_leave_time晚
            plan_arr_time = float(Schedules_alt_0[i + 1, 2])  # 要比A航班原计划到达OVS的时间晚
            Ai1 = float(Schedules_alt_0[i, 2])
            Ai10 = float(Schedules_alt_0[i + 1, 1])
    if np.shape(maybe_change_time)[0]>0:
        delay_time=np.zeros((4,5))
        delay_time[0,0]=plan_leave_time
        delay_time[0,1]=Ai1
        delay_time[0,2]=max(float(maybe_change_time[n,7]),plan_leave_time)
        delay_time[0,3]=delay_time[0,2]+(Ai1-plan_leave_time)


        delay_time[1,0]=Ai10
        delay_time[1,1]=plan_arr_time
        delay_time[1,2]=max(Ai10,delay_time[0,3]+2700)
        delay_time[1,3]=delay_time[1,2]+(plan_arr_time-Ai10)



        delay_time[2,0:2]=maybe_change_time[n,1:3]
        delay_time[2,2]=max(last_leave_time,float(maybe_change_time[n,1]))
        delay_time[2,3]=delay_time[2,2]+(float(maybe_change_time[n,2])-float(maybe_change_time[n,1]))

        delay_time[3,0:2]=maybe_change_time[n+1,1:3]
        delay_time[3,2]=max(float(maybe_change_time[n+1,1]),delay_time[2,3]+2700)
        delay_time[3,3]=delay_time[3,2]+(float(maybe_change_time[n+1,2])-float(maybe_change_time[n+1,1]))

        if delay_time[0,2]-delay_time[0,0]==delay_time[0,3]-delay_time[0,1]:
            delay_time[0,4]=delay_time[0,3]-delay_time[0,1]
        if delay_time[1,2]-delay_time[1,0]==delay_time[1,3]-delay_time[1,1]:
            delay_time[1,4]=delay_time[1,3]-delay_time[1,1]

        if delay_time[2, 2] - delay_time[2, 0] == delay_time[2, 3] - delay_time[2, 1]:
            delay_time[2, 4] = delay_time[2, 3] - delay_time[2, 1]
        if delay_time[3, 2] - delay_time[3, 0] == delay_time[3, 3] - delay_time[3, 1]:
            delay_time[3, 4] = delay_time[3, 3] - delay_time[3, 1]
        return delay_time
    else:
        return []



##找到待置换航线，来回的，需要的时间

#将置换好的飞机写到Schedules_alt_1上
Schedules_alt_1=np.zeros((np.shape(Schedules_1)[0],14))
Schedules_alt_1=Schedules_alt_1.astype(np.str)
for i in range(np.shape(Schedules_1)[0]):
    Schedules_alt_1[i,0:9]=Schedules_1[i,0:9]
    Schedules_alt_1[i,9:13]=Schedules_1[i,3:7]
    Schedules_alt_1[i,-1]=Schedules_1[i,-1]

####################################################置换核心！！！！！！
for ID in alter_ID:
    for i in range(np.shape(Schedules_alt_1)[0]):
        if Schedules_alt_1[i,0]==ID:
            last_leave_time=float(Schedules_alt_1[i,7])#要比A航班能离开的最早时间last_leave_time要早才有换的意义
            plan_leave_time=float(Schedules_alt_1[i,1])#要比A航班原计划的离开时间plan_leave_time晚
            last_arr_time =float(Schedules_alt_1[i+1,8])#要比A航班能到达VOS的最早时间早
            plan_arr_time=float(Schedules_alt_1[i+1,2])#要比A航班原计划到达OVS的时间晚
            plane_type=Schedules_alt_1[i,5]
            min_duration=last_arr_time-last_leave_time
            raw_delay=float(Schedules_alt_1[i,-1])+float(Schedules_alt_1[i+1,-1])
            Ai1=float(Schedules_alt_1[i,2])
            Ai3=float(Schedules_alt_1[i,8])
            Ai10=float(Schedules_alt_1[i+1,1])
            Ai12=float(Schedules_alt_1[i+1,7])
            plane_weihao=Schedules_alt_1[i,6]
            plane_go=Schedules_alt_1[i,4]


    maybe_change=[]
    for i in range(np.shape(Schedules_alt_1)[0]-2):
        if Schedules_alt_1[i,3]=='OVS' \
                and Schedules_alt_1[i+1,4]=='OVS' and float(Schedules_alt_1[i,7])<last_leave_time\
            and float(Schedules_alt_1[i+2,1])>float(Schedules_alt_1[i,7])+min_duration+2700 \
                and float(Schedules_alt_1[i+1,8])>=plan_arr_time:
                #B航班返回OVS的时间+2700要早于B航班下一次出发的时间
            maybe_change.append(list(Schedules_alt_1[i]))
            maybe_change.append(list(Schedules_alt_1[i+1]))
    maybe_change=np.array(maybe_change)


    ###计算每种方案的延误时间，每一个来回为一个相同的
    '''9列为B航班的延误情况，10列是加上A航班的延误的总延误，11列为置换过的延误总延误，12列为时间差'''

    if np.shape(maybe_change)[0]!=0:
        maybe_change_time=np.zeros((np.shape(maybe_change)[0],np.shape(maybe_change)[1]+3))
        maybe_change_time=maybe_change_time.astype(np.str)
        for i in range(np.shape(maybe_change)[0]):
            maybe_change_time[i, 0:9] = maybe_change[i, 0:9]
            maybe_change_time[i,-1]=maybe_change[i,-1]

        for i in range(np.shape(maybe_change)[0]):
            if i%2==0:
                maybe_change_time[i,10]=raw_delay+float(maybe_change_time[i,-1])+float(maybe_change_time[i+1,-1])
                delay_time=delay_time_file(ID, Schedules_alt_1, maybe_change_time,i)
                if maybe_change_time[i,5]==plane_type:
                    maybe_change_time[i,11]=sum(delay_time[:,-1])
                else:
                    maybe_change_time[i, 11] = sum(delay_time[:, -1])+1800
                maybe_change_time[i, 12] = float(maybe_change_time[i, 10]) - float(maybe_change_time[i, 11])
            elif i%2==1:
                maybe_change_time[i,10]=maybe_change_time[i-1,10]
                maybe_change_time[i, 11] = maybe_change_time[i - 1, 11]
                maybe_change_time[i, 12] = maybe_change_time[i - 1, 12]


        best_change=[]
        max_reduce = 0

        for i in range(np.shape(maybe_change_time)[0]):
            if float(maybe_change_time[i,12])>max_reduce:
                max_reduce=float(maybe_change_time[i,12])

        for i in range(np.shape(maybe_change_time)[0]):
            if float(maybe_change_time[i,12])==max_reduce:
                best_change.append(list(maybe_change_time[i]))
        best_change=np.array(best_change)
        if np.shape(best_change)[0]>0:
            best_change_plane=best_change[0,0]

        best_delay=delay_time_file(ID,Schedules_alt_1,best_change,0)
        ###best_delay为ID这个来回的航线和best_change_plane航线置换的方案，
        # best_change_plane航线的信息在best_change中
        if np.shape(best_delay)[0]>0 and np.shape(best_change)[0]>0:
            #先把ID航线的信息改为best_change_plane的
            for i in range(np.shape(Schedules_alt_1)[0]-1):
                if Schedules_alt_1[i,0]==ID and float(Schedules_alt_1[i,1])==float(best_delay[0,0])\
                        and Schedules_alt_1[i,3]==best_change[0,3]=='OVS'\
                        and Schedules_alt_1[i+1,4]==best_change[1,4]=='OVS':
                    Schedules_alt_1[i,7]=best_delay[0,2]
                    Schedules_alt_1[i,8]=best_delay[0,3]
                    Schedules_alt_1[i,-1]=best_delay[0,-1]
                    Schedules_alt_1[i,11:13]=best_change[0,5:7]
                    Schedules_alt_1[i+1,7]=best_delay[1,2]
                    Schedules_alt_1[i+1,8]=best_delay[1,3]
                    Schedules_alt_1[i+1,-1]=best_delay[1,-1]
                    Schedules_alt_1[i+1,11:13]=best_change[1,5:7]
            #再把best_change_plane的换成ID的
            for j in range(np.shape(Schedules_alt_1)[0]-1):
                if float(Schedules_alt_1[j,0])==float(best_change_plane) and float(Schedules_alt_1[j,1])==float(best_delay[2,0])\
                    and Schedules_alt_1[j,3]==Schedules_alt_1[j+1,4]=='OVS':
                    Schedules_alt_1[j,7]=best_delay[2,2]
                    Schedules_alt_1[j,8]=best_delay[2,3]
                    Schedules_alt_1[j,-1]=best_delay[2,-1]
                    Schedules_alt_1[j,10]=plane_go
                    Schedules_alt_1[j,11]=plane_type
                    Schedules_alt_1[j,12]=plane_weihao
                    Schedules_alt_1[j+1,7]=best_delay[3,2]
                    Schedules_alt_1[j+1,8]=best_delay[3,3]
                    Schedules_alt_1[j+1,-1]=best_delay[3,-1]
                    Schedules_alt_1[j+1,9]=plane_go
                    Schedules_alt_1[j+1,11]=plane_type
                    Schedules_alt_1[j+1,12]=plane_weihao

            rote = "/Users/XuLiu/MathC/4best_delay_%s_%s.txt" % (ID,best_change_plane)
            ExportData(best_delay,rote)

########################################################
ExportData(Schedules_alt_1,"/Users/XuLiu/MathC/4Schedules_alt_1.txt")

ovs_time_min=1461298260
ovs_time_max=1461438300
ovs_time=[]#时间可能的取值
time=ovs_time_min
while time<=ovs_time_max:
    ovs_time.append(time)
    time+=300

#0时间区间，1起飞个数，2落地个数
time_count_0=np.zeros((np.shape(ovs_time)[0],3))
time_count_0=time_count_0.astype(np.str)
for i in range(np.shape(time_count_0)[0]-1):
    time_count_0[i,0]=ovs_time[i]
    time_count_0[i,1]=countvol(Schedules_0,7,ovs_time[i],ovs_time[i+1],3,'OVS')
    time_count_0[i,2]=countvol(Schedules_0,8,ovs_time[i],ovs_time[i+1],4,'OVS')

ExportData(time_count_0,"/Users/XuLiu/MathC/4time_count_0.txt")
