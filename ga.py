import random
import statistics as sta
import xlwt

class generation:
    def __init__(self):
        ## INITIALISATION VARIABLES
        self.fit=100
        self.totstu=1000 ## TOTAL NUMBER OF STUDENTS
        self.stuperroom=5 ## STUDENTS PER ROOM
        self.stulist=[] ## MAIN ARRAY THAT STORES THE STUDENTS CHOICES
        self.li=[] ## USED FOR RANDOMLY GENERATING CHROMOSOMES
        self.chromelist=[]  ## CHROMOSOME CONTAINER FOR THE GENERATION
        self.optrang=[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4] ## RANGE OF CHOICES AVAILABLE TO EACH ATTRIBUTE LENGTH OF THIS LIST DECIDES THE NUMBER OF ATTRIBUTES PER STUDENT
        self.mainlist=[]

    ## THE CHROMOSOME CLASS
    class chromo:
        def __init__(self,a):
            self.p=a ## LIST THAT CONTAINS THE STUDENTS GROUPED TOGETHER
            self.fitness=0
            
        def prnt(self): ## PRINT FUNCTION
            print("persons: ",self.p,"   fitness : ",self.fitness)
            
        def calc_fitness(self,stulist): ## FITNESS FUNCTION
            ## THE MEAN OF THE VARIANCE IN THE CHOICES OF EACH ATTRIBUTE
            ## OF EACH OF THE STUDENT IN THAT PARTICULAR GROUP
            data=[]
            for i in range(len(stulist[0])):
                data1=[]
                for j in range(len(self.p)):
                    data1.append(stulist[self.p[j]][i]) 
                data.append(sta.variance(data1))
            self.fitness=sta.mean(data)

    ## FUNCTION FOR RANDOMLY GENERATING THE DATA
    def generate_data(self):
        for i in range(self.totstu):
            self.stulist.append([])
            self.li.append(i)
            for j in range(len(self.optrang)):
                self.stulist[i].append(random.randrange(self.optrang[j]))
    def calcu_fitness(self):
        sum=0
        for val in self.chromelist:
            val.calc_fitness(self.stulist)
            sum=sum+val.fitness
        self.fit=sum/len(self.chromelist)
        ##print(self.fit)
        
    ## FUNCTION FOR GENERATING THE INITIAL CHROMOSOMES
    def setinitstate(self):
        for i in range(int(self.totstu/self.stuperroom)):
            a=[]
            for j in range(self.stuperroom):
                k=self.li[random.randrange(len(self.li))]
                self.li.remove(k)
                a.append(k)
            self.chromelist.append(self.chromo(a))
            self.chromelist[i].calc_fitness(self.stulist)## CALCULATE FITNESS WHILE CREATING THE CHROMOSOME

    ## FUNCTION FOR PRINTING THE CURRENT GENERATION
    def print_gen(self):
        for i in range(len(self.chromelist)):
            print("chromosome ",i," :")
            self.chromelist[i].prnt()
    
    ## FUNCTION FOR PERFORMING THE CROSSOVER
    def crossover(self):
        chlist1=list(self.chromelist)
        chlist=[]
        count=0
        chlist1.sort(key=lambda x: x.fitness, reverse=False)
        for ch in chlist1:
            if ch.fitness < 1:
                count+=1
                self.mainlist.append(ch)
                chlist1.remove(ch)
        prev=0
        print(len(self.mainlist))
        for ch in chlist1:
            ch.fitness=((ch.fitness-chlist1[0].fitness)/(chlist1[len(chlist1)-1].fitness-chlist1[0].fitness))
        while len(chlist1)>0:
            select=[]
            if(len(chlist1)>1):
                for i in range(2):
                    num=random.randrange(len(chlist1))
                    select.append(chlist1[num])
                    chlist1.pop(num)  
                pocross=self.cross(select)
                for i in range(len(pocross)):
                    chlist.append(self.chromo(pocross[i]))
            else:
                 chlist.append(chlist1[0])
                 chlist1.pop()
        return chlist
        
            
    def cross(self,a):
       
        leng=len(a)
        p=[]
        pocross=[]
        for i in range(leng):
            pocross.append([])
            for val in a[i].p:
                p.append(val)
                
        while len(p)>0:
            for i in range(leng):
                a=p[random.randrange(len(p))]
                p.remove(a)
                pocross[i].append(a)
        return pocross
            
            
## WRITE THE DRIVER CODE AFTER THIS COMMENT
g1=generation()
g1.generate_data()
g1.setinitstate()
wb = xlwt.Workbook()
wb.add_sheet("init")
c_sh=wb.get_sheet(0)
for m in range(len(g1.mainlist)):
    for n in range(g1.stuperroom):
        c_sh.write(m, n, g1.mainlist[m].p[n])
    c_sh.write(m, g1.stuperroom + 1, str(g1.mainlist[m].fitness))
for m in range(len(g1.chromelist)):
    for n in range(g1.stuperroom):
        c_sh.write(len(g1.mainlist)+m, n, g1.chromelist[m].p[n])
    c_sh.write(len(g1.mainlist)+m, g1.stuperroom + 1, str(g1.chromelist[m].fitness))
c_sh.write(len(g1.chromelist)+1,0,str(g1.fit))
sheetno=1
for j in range(10):
    for i in range(10):
        g2 = generation()
        a = g1.crossover()
        g2.stulist = list(g1.stulist)
        g2.chromelist = a
        g2.mainlist=g1.mainlist
        g2.calcu_fitness()
        g1 = g2
        wb.add_sheet("Generation "+str(j)+","+str(i))
        c_sh = wb.get_sheet(sheetno)
        sheetno=sheetno+1
        for m in range(len(g2.mainlist)):
            for n in range(g2.stuperroom):
                c_sh.write(m,n,g2.mainlist[m].p[n])
            c_sh.write(m,g1.stuperroom+1,str(g2.mainlist[m].fitness))
        for m in range(len(g2.chromelist)):
            for n in range(g2.stuperroom):
                c_sh.write(len(g2.mainlist)+m, n, g2.chromelist[m].p[n])
            c_sh.write(len(g2.mainlist)+m, g1.stuperroom + 1, str(g2.chromelist[m].fitness))
        ##print(g2.fit)
        c_sh.write(len(g2.mainlist)+len(g2.chromelist)+1,0,str(g2.fit))
wb.save("ga.xls")


