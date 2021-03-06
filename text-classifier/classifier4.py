import nltk
from sklearn import svm

f=open("score1.txt","r")
txt=f.read()
lin=txt.split("\n")

aposlist={}
rposlist={}
vposlist={}
nposlist={}
aneglist={}
nneglist={}
vneglist={}
rneglist={}
dicy=[]

for l in lin:
    wds=l.split(' ')
    if(len(wds)>3):
        dicy.append(wds[1])
        aposlist["%s" % wds[1]]=0
        aneglist["%s" % wds[1]]=0
        nposlist["%s" % wds[1]]=0
        nneglist["%s" % wds[1]]=0
        rposlist["%s" % wds[1]]=0
        rneglist["%s" % wds[1]]=0
        vposlist["%s" % wds[1]]=0
        vneglist["%s" % wds[1]]=0
        
for l in lin:
    wds=l.split(' ')
    if(len(wds)>3):
        t=wds[0]
        if(t in 'a'):
            aposlist["%s" % wds[1]]=float(wds[2])
            aneglist["%s" % wds[1]]=float(wds[3])
        elif(t in 'r'):
            rposlist["%s" % wds[1]]=float(wds[2])
            rneglist["%s" % wds[1]]=float(wds[3])
        elif(t in 'n'):
            nposlist["%s" % wds[1]]=float(wds[2])
            nneglist["%s" % wds[1]]=float(wds[3])
        elif(t in 'v'):
            vposlist["%s" % wds[1]]=float(wds[2])
            vneglist["%s" % wds[1]]=float(wds[3])

f.close()

def valu(c,t):
    val=(0,0)
    if c in dicy:
            if ('JJ' in t):
                val=(aposlist["%s" % tt],aneglist["%s" % tt])
            elif ('NN' in t):
                val=(nposlist["%s" % tt],nneglist["%s" % tt])
            elif ('RB' in t):
                return 0
            elif ('VB' in t):
                val=(vposlist["%s" % tt],vneglist["%s" % tt])
    return val

def classy(a,b):
    if(a>b):
        return 1
    elif (b>a):
        return 0
    else:
        return (-1)

f=open("rt-polarity.neg","r")
negt=(f.read()).split(".")
f.close()
f=open("rt-polarity.pos","r")
posit=(f.read()).split(".")
f.close()

tot=0
accu=0

xx=[]
tgt=[]

for st in negt[0:1000]:
    wds=st.split()
    lst=[]
    for w in wds:
        if w.isalpha() and (len(w)>=1):
            lst.append(w)
    lng=len(lst)
    if(lng<3):
        continue
    if(tot%100==0):
        print tot,
    tot+=1
    post=nltk.pos_tag(lst)
    psum=0
    nsum=0
    cpsum=0
    cnsum=0
    a=0
    b=0
    fg=0
    for i in range(0,lng):
        t=post[i][1]
        tt=(post[i][0].lower())
        if tt in dicy and fg==1:
            tup=valu(tt,t)
            if(tup!=0):
                cpsum+=(2*(a-b)*tup[0])
                cnsum+=(2*(a-b)*tup[1])
                fg=0
            else:
                a+=rposlist["%s" % tt]
                b+=rneglist["%s" % tt]
        elif tt in dicy:
            tup=valu(tt,t)
            if(tup!=0):
                psum+=(tup[0])
                nsum+=(tup[1])
            else:
                a=rposlist["%s" % tt]
                b=rneglist["%s" % tt]
                fg=1

    totu=psum+nsum+(0.01)
    psum=(psum/totu)
    nsum=(nsum/totu)

    totu=cpsum+cnsum+(0.01)
    cpsum=(cpsum/totu)
    cnsum=(cnsum/totu)
    
    xx.append([psum,nsum,cpsum,cnsum])
    tgt.append(0)

for st in posit[0:1000]:
    wds=st.split()
    lst=[]
    for w in wds:
        if w.isalpha() and (len(w)>=1):
            lst.append(w)
    lng=len(lst)
    if(lng<3):
        continue
    if(tot%100==0):
        print tot,
    tot+=1
    post=nltk.pos_tag(lst)
    psum=0
    nsum=0
    cpsum=0
    cnsum=0
    a=0
    b=0
    fg=0
    for i in range(0,lng):
        t=post[i][1]
        tt=(post[i][0].lower())
        if tt in dicy and fg==1:
            tup=valu(tt,t)
            if(tup!=0):
                cpsum+=(2*(a-b)*tup[0])
                cnsum+=(2*(a-b)*tup[1])
                fg=0
            else:
                a+=rposlist["%s" % tt]
                b+=rneglist["%s" % tt]
        elif tt in dicy:
            tup=valu(tt,t)
            if(tup!=0):
                psum+=(tup[0])
                nsum+=(tup[1])
            else:
                a=rposlist["%s" % tt]
                b=rneglist["%s" % tt]
                fg=1

    totu=psum+nsum+(0.01)
    psum=(psum/totu)
    nsum=(nsum/totu)

    totu=cpsum+cnsum+(0.01)
    cpsum=(cpsum/totu)
    cnsum=(cnsum/totu)
    
    xx.append([psum,nsum,cpsum,cnsum])
    tgt.append(1)

clf=svm.SVC()
clf.fit(xx,tgt)

accu=0
tot=0

for st in negt[1000:1500]:
    wds=st.split()
    lst=[]
    for w in wds:
        if w.isalpha() and (len(w)>=1):
            lst.append(w)
    lng=len(lst)
    if(lng<3):
        continue
    if(tot%100==0):
        print tot,
    post=nltk.pos_tag(lst)
    psum=0
    nsum=0
    cpsum=0
    cnsum=0
    a=0
    b=0
    fg=0
    for i in range(0,lng):
        t=post[i][1]
        tt=(post[i][0].lower())
        if tt in dicy and fg==1:
            tup=valu(tt,t)
            if(tup!=0):
                cpsum+=(2*(a-b)*tup[0])
                cnsum+=(2*(a-b)*tup[1])
                fg=0
            else:
                a+=rposlist["%s" % tt]
                b+=rneglist["%s" % tt]
        elif tt in dicy:
            tup=valu(tt,t)
            if(tup!=0):
                psum+=(tup[0])
                nsum+=(tup[1])
            else:
                a=rposlist["%s" % tt]
                b=rneglist["%s" % tt]
                fg=1

    totu=psum+nsum+(0.01)
    psum=(psum/totu)
    nsum=(nsum/totu)

    totu=cpsum+cnsum+(0.01)
    cpsum=(cpsum/totu)
    cnsum=(cnsum/totu)
    
    tmp=clf.predict([[psum,nsum,cpsum,cnsum]])
    t=classy(tmp[0],(0.5))

    if(tot%10==0):
        print tot,tmp,t,[psum,nsum,cpsum,cnsum],"0"

    if ((t==0) or (t==(-1))):
        accu+=1
    tot+=1
    
print (accu*(1.0)/tot)

for st in posit[1000:1500]:
    wds=st.split()
    lst=[]
    for w in wds:
        if w.isalpha() and (len(w)>=1):
            lst.append(w)
    lng=len(lst)
    if(lng<3):
        continue
    if(tot%100==0):
        print tot,
    post=nltk.pos_tag(lst)
    psum=0
    nsum=0
    a=0
    b=0
    fg=0
    for i in range(0,lng):
        t=post[i][1]
        tt=(post[i][0].lower())
        if tt in dicy and fg==1:
            tup=valu(tt,t)
            if(tup!=0):
                psum+=(2*(a-b)*tup[0])
                nsum+=(2*(a-b)*tup[1])
                fg=0
            else:
                a+=rposlist["%s" % tt]
                b+=rneglist["%s" % tt]
        elif tt in dicy:
            tup=valu(tt,t)
            if(tup!=0):
                psum+=(tup[0])
                nsum+=(tup[1])
            else:
                a=rposlist["%s" % tt]
                b=rneglist["%s" % tt]
                fg=1

    totu=psum+nsum+(0.01)
    psum=(psum/totu)
    nsum=(nsum/totu)

    totu=cpsum+cnsum+(0.01)
    cpsum=(cpsum/totu)
    cnsum=(cnsum/totu)

    tmp=clf.predict([[psum,nsum,cpsum,cnsum]])
    t=classy(tmp[0],(0.5))

    if ((t==1) or (t==(-1))):
        accu+=1
    tot+=1
    
print (accu*(1.0)/tot)
