try:
     import pygame as pg
     from tkinter import *
     from tkinter import messagebox
     import mysql.connector as msc
     import random
     run=True
except:
     print("These Libraries must be installed!")
     print("pygame")
     print("tkinter")
     print("mysql.connector")
     print("random")
     run=False

# wtgw=width of game_window(gw) ;  htgw=height of gw ;  dimens=dimensions ;  t_lab=text for label ;  t_but=text for button ;   w_but=width of button ;
# lab_x=x coord. of label ;   and similarly for others  cmnd=command ;   plr=player ;   scr=score ;   con=connection of database n python ;   cur=cursor ;

cmnd1=lambda : name("320x150+300+300"," Enter Name "," OK ",3,4,70,61,checkplr,1,240)
cmnd2=lambda : name("380x200+300+300"," Enter Name of \nThe Person "," FIND ",5,15,113,104,checkscr,2,250)

def name(dimens,t_lab,t_but,w_but,lab_x,entr_y,but_y,cmnd,ht,but_x):
     global tplr,cont
     cont=Tk()
     cont.geometry(dimens)
     cont.config(bg="#bdffdb")
     lplr=Label(cont,width=13,height=ht,text=t_lab,bg="#bdffdb",fg="black",font="courier 23 bold")
     bplr=Button(cont,width=w_but,text=t_but,pady=-1,command=cmnd,bg='white',fg="black",font="courier 22 bold",bd=4)
     tplr=Entry(cont,width=12,bg='white',fg="black",font="courier 22 bold",bd=4)
     lplr.place(x=lab_x,y=14)
     tplr.place(x=20,y=entr_y)
     bplr.place(x=but_x,y=but_y)
     cont.mainloop()
     
def checkplr():
     global tplr,j,con,cur,players,cont,pname
     pname=tplr.get().strip()
     if len(pname)>0 and len(pname)<16:
          con=msc.connect(host="localhost",user="root",passwd=password,database="ping_pong")
          cur=con.cursor()
          q="select * from ping"
          cur.execute(q)
          players=cur.fetchall()
          cont.destroy()
          start()
     else:
          cont.destroy()
          messagebox.showinfo(""," Name Must Be of Length 1 to 15")
          cmnd1()

# vx=velocity of ball in x directn ;  vy=similar but in y directn ;   yball=ycoordinate of ball ;   rball=radius of ball ;   v=velocity of bar ;   wbar=width
#lbar=length ;   mx,my for continous movement in respective directions ;   pname =player name


def start():
     global i,vy,vx,yball,xball,rball,ybar,xbar,v,wbar,lbar,wtgw,htgw,mx,my,scr,j,con,cur,players,pname
     scrinc=0
     pg.init()
     gwin=pg.display.set_mode((wtgw,htgw))
     run=True
     font=pg.font.Font("freesansbold.ttf",30)
     xscr=yscr=10
     pg.mixer.music.load("3.mp3")
     pg.mixer.music.play()
     img=pg.image.load("8.jpg")
     while run:
          score=font.render("SCORE :"+str(scr),True,("white"))  #str(scr) bcz it accepts str type only
          gwin.blit(img,(0,0))
          gwin.blit(score,(xscr,yscr))
          i+=1
          pg.time.delay(-1)
          for ev in pg.event.get():
               if ev.type==pg.QUIT:
                    run=False
                    pg.mixer.music.stop()
          
          if i%1500==0:
               vx,vy=vy,vx
          elif i%5000==0:
               vx+=1
               vy+=1
               v+=2
               scrinc+=1
          keys=pg.key.get_pressed()
          if (keys[pg.K_d] or keys[pg.K_RIGHT]) and xbar+lbar+v<wtgw:
               xbar+=v
          elif (keys[pg.K_a] or keys[pg.K_LEFT]) and xbar>=v+3:
               xbar-=v
          
          if mx==0 or mx==1:
               xball-=vx
          elif mx==-1:
               xball+=vx
          
          if my==0 or my==1:
               yball+=vy
          elif my==-1:
               yball-=vy
          
          if xball+rball in range(wtgw-2*vx,wtgw-vx+1):
               mx=1
          elif xball-rball in range(0,vx):
               mx=-1
          
          if yball-rball in range(0,vy):
               my=1

          if (xball+rball-10 in range(xbar,xbar+lbar) or xball-rball-10 in range(xbar,xbar+lbar)) and (yball+rball) in range(htgw-wbar-2,htgw-wbar+2*vy):
               my=-1
               scr+=(2+scrinc)
          elif yball+rball>htgw-wbar+2*vy:
               run=False
               pg.mixer.music.stop()
               messagebox.showinfo(""," GAME OVER ")
               
          pg.draw.line(gwin,"white",(0,htgw-58),(wtgw,htgw-58),3)
          pg.draw.circle(gwin,"yellow",(xball,yball),rball)
          pg.draw.rect(gwin,"green",(xbar,ybar,lbar,wbar))
          pg.display.update()
     pg.quit()
     for name in players:
          if name[0]==str(pname):
               j=1
               if name[1]<scr:
                    q1="update ping set pscore={} where pname='{}'".format(scr,name[0])
                    cur.execute(q1)
               break
          else:
               j=0
     if j==0:
          q1="insert into ping values('{}',{})".format(pname,scr)
          cur.execute(q1)
     con.commit()
     lbar,wbar,v,xbar,ybar,rball,vx,vy,i,mx,my=200,50,5,300,740,50,2,3,0,0,0
     xball=random.randint(300,700)
     yball=random.randint(100,470)
     scr=0
     if messagebox.askretrycancel(""," RETRY ?"):
          start()
     con.close()

def checkscr():
     global tplr,cont,pname
     pname=tplr.get().strip()
     if len(pname)>0 and len(pname)<16:
          cont.destroy()
          fetch("one")
     else:
          cont.destroy()
          messagebox.showinfo(""," Name Must Be of Length 1 to 15")
          cmnd2()

def fetch(x):
     global l,pname
     con=msc.connect(host="localhost",user="root",passwd=password,database="ping_pong")
     cur=con.cursor()
     if x=="one":
          q="select * from ping"
     else:
          q="select * from ping having max(pscore)"
     cur.execute(q)
     l=cur.fetchall()
     if x=="one":
          for i in l:
               if i[0]==pname:
                    dispscr(pname,i[1])
                    break
          else:
               messagebox.showinfo(""," Name Not Found")
     elif x=="top":
          dispscr(l[0][0],l[0][1])
     
          
def dispscr(plrname,plrscr):
     global tplr,l,cont,players,pname
     bgcol="#f0f0f0"
     fgcol="green"
     scrdisp=Tk()
     scrdisp.geometry("400x200+300+300")
     scrdisp.config(bg=bgcol)
     l10=Label(scrdisp,width=6,text="Name",bg=bgcol,fg=fgcol,font="courier 23 bold")
     l11=Label(scrdisp,width=5,text="Score",bg=bgcol,fg=fgcol,font="courier 23 bold")
     hsep=Label(scrdisp,width=30,pady=-2,text=" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -",bg=bgcol,fg='black',font="'' 20")
     l12=Label(scrdisp,width=10,text=plrname,bg=bgcol,fg=fgcol,font="courier 23 bold")
     l13=Label(scrdisp,width=3,text=plrscr,bg=bgcol,fg=fgcol,font="courier 23 bold")
     vsep=Label(scrdisp,width=0,text="",bg="black",font="'' 150 ")
     l10.place(x=40,y=30)
     l11.place(x=250,y=30)
     l12.place(x=0,y=130)
     l13.place(x=270,y=130)
     hsep.place(x=0,y=75)
     vsep.place(x=202,y=0)
     scrdisp.mainloop()
     
def __main__():
     global wtgw,htgw,lbar,wbar,v,xbar,ybar,rball,vx,vy,i,mx,my,j,xball,yball,scr
     wtgw,htgw=1440,795
     lbar,wbar,v,xbar,ybar,rball,vx,vy,i,mx,my,j=200,50,5,300,740,50,1,3,0,0,0,0
     xball=random.randint(300,700)
     yball=random.randint(100,470)
     scr=0

     root=Tk()
     #   wtmw x htmw     color=  #cdfcfc   or   #bdffdb
     root.geometry("1080x795+100+-3")
     root.configure(bg="#cdfcfc")
     root.title("   Ping   Pong")
     l1=Label(root,width=21,bg="#cdfcfc",fg="purple",text=" WELCOME  TO  PING  PONG ",font="algerian 60 underline")
     b1=Button(root,command=cmnd1,width=5,pady=0,bd=15,text=" PLAY ",bg="black",fg="white",font="courier 40 bold italic")
     b2=Button(root,command=cmnd2,width=11,pady=0,bd=15,text=" SEE SCORES ",bg="black",fg="white",font="courier 40 bold italic")
     b3=Button(root,command=lambda : fetch("top"),width=11,pady=0,bd=15,text=" BEST SCORE ",bg="black",fg="white",font="courier 40 bold italic")
     b4=Button(root,command=lambda : root.destroy(),width=5,pady=0,bd=10,text=" QUIT ",bg="black",fg="white",font=" forte 30 ")

     l1.place(x=25,y=100)
     b1.place(x=53,y=300)
     b2.place(x=249,y=431)
     b3.place(x=637,y=562)
     b4.place(x=450,y=700)
     root.mainloop()

def paswrd():
     def lenchk():
          global password
          if len(tp.get())>0:
               z.append(tp.get())
               password=tp.get()
               pcont.destroy()
          else:
               pcont.destroy()
               messagebox.showinfo("","Enter your MySQL Password")
               paswrd()
     z=[]
     pcont=Tk()
     pcont.geometry("450x200+300+300")
     pcont.config(bg="#bdffdb")
     lp=Label(pcont,text="Enter PASSWORD of your \nMySQL Server",bg="#bdffdb",fg="black",font="courier 23 bold")
     bp=Button(pcont,width=3,text="OK",pady=-1,command=lenchk,bg='white',fg="black",font="courier 22 bold",bd=4)
     tp=Entry(pcont,width=14,bg='white',fg="black",font="courier 22 bold",bd=4,show="*")
     lp.place(x=15,y=14)
     tp.place(x=40,y=117)
     bp.place(x=330,y=106)
     pcont.mainloop()
     if len(z)>0:
          try:
               con=msc.connect(user="root",host="localhost",passwd=password)
               cur=con.cursor()
               q="create database if not exists ping_pong"
               cur.execute(q)
               con.commit()
               q="use ping_pong"
               cur.execute(q)
               con.commit()
               q="create table if not exists ping(pname varchar(15) primary key,pscore int)"
               cur.execute(q)
               con.commit()
               con.close()
               __main__()
          except:
               messagebox.showerror(""," Wrong Password ")
               paswrd()


if __name__=="__main__" and run:
     paswrd()
