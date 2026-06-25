# -*- coding: utf-8 -*-
"""萌宠视图 · 小红书内容运营 —— 用真实运营数据做的品牌风格成果页（无需原始截图）。"""
import os
from PIL import Image, ImageDraw, ImageFont

DST = r"D:\clawd\shiqi-portfolio\public\works\pets"
os.makedirs(DST, exist_ok=True)
CREAM=(255,248,240); BROWN=(90,50,35); PINK=(224,98,137); BLUE=(60,140,202)
RED=(223,67,49); YELLOW=(240,197,35); GREY=(150,130,120); WHITE=(255,255,255)
FONT=r"C:\Windows\Fonts\msyh.ttc"; FONTB=r"C:\Windows\Fonts\msyhbd.ttc"
def f(s,b=False): return ImageFont.truetype(FONTB if b else FONT,s)
def tw(d,t,fo): bb=d.textbbox((0,0),t,font=fo); return bb[2]-bb[0],bb[3]-bb[1]
def ctext(d,t,fo,y,W,fill): d.text(((W-tw(d,t,fo)[0])//2,y),t,fill=fill,font=fo)
W,H=1600,900

# ---------- 01 cover ----------
img=Image.new("RGB",(W,H),CREAM); d=ImageDraw.Draw(img)
d.rectangle([(0,250),(W,620)],fill=PINK)
for cx,col,r in [(150,YELLOW,46),(W-160,BLUE,52),(300,RED,24),(W-340,BROWN,30)]:
    d.ellipse([(cx-r,120-r),(cx+r,120+r)],fill=col)
ctext(d,"小红书 · 宠物内容运营",f(26),300,W,(255,248,240))
ctext(d,"萌宠视图",f(72,True),350,W,WHITE)
ctext(d,"会做内容，更能跑出数据",f(30),470,W,(255,248,240))
tags=[("选题策划",YELLOW),("脚本文案",BLUE),("拍摄剪辑",BROWN),("流量投放",RED)]
cf=f(23,True); ws=[tw(d,t,cf)[0]+48 for t,_ in tags]; total=sum(ws)+20*(len(tags)-1); x=(W-total)//2
for (t,col),wch in zip(tags,ws):
    d.rounded_rectangle([(x,545),(x+wch,592)],radius=24,fill=col); d.text((x+24,554),t,fill="white",font=cf); x+=wch+20
ctext(d,"单条笔记 3.5万赞 · 16万浏览 · 账号累计 5.3万获赞收藏",f(24,True),665,W,BROWN)
ctext(d,"邹诗琪 · 小红书 @猫咪收割机",f(20),810,W,GREY)
img.save(os.path.join(DST,"01.jpg"),quality=90); print("cover")

# ---------- 02 运营成果 ----------
img=Image.new("RGB",(W,H),CREAM); d=ImageDraw.Draw(img)
d.rectangle([(0,0),(W,110)],fill=BROWN); d.rectangle([(0,0),(14,110)],fill=PINK)
d.text((60,32),"运营成果",fill=CREAM,font=f(40,True))
d.text((W-60-tw(d,"小红书 @猫咪收割机 · IP浙江",f(20))[0],50),"小红书 @猫咪收割机 · IP浙江",fill=(255,248,240),font=f(20))
# 大数字条
stats=[("5.3万","账号累计获赞收藏",PINK),("10.6万","近7日笔记观看",BLUE),("2.4万","近7日互动",RED),("+137016%","互动周环比",YELLOW)]
bw=(W-120-3*24)//4; x=60
for val,lab,col in stats:
    d.rounded_rectangle([(x,140),(x+bw,300)],radius=20,fill=WHITE)
    d.rectangle([(x,140),(x+bw,150)],fill=col)
    ctext_x=x+bw//2
    vf=f(46,True); d.text((ctext_x-tw(d,val,vf)[0]//2,180),val,fill=col,font=vf)
    lf=f(20); d.text((ctext_x-tw(d,lab,lf)[0]//2,250),lab,fill=(90,70,60),font=lf)
    x+=bw+24
# 两个爆款卡
d.text((60,330),"两条爆款笔记",fill=BROWN,font=f(26,True))
hits=[
    ("「小猫咪拍奶嗝」· 视频","2026.06.23 发布 · 约1天",[("3.5万","点赞"),("15.3万","浏览"),("2033","收藏"),("282","评论")],PINK),
    ("「人，咪虽然没有伞」· 图文","2025.06.11 发布",[("1.2万","点赞"),("16.1万","浏览"),("335","收藏"),("488","评论")],BLUE),
]
cardw=(W-120-30)//2; x=60
for title,date,metrics,col in hits:
    d.rounded_rectangle([(x,375),(x+cardw,620)],radius=20,fill=WHITE)
    d.rectangle([(x,375),(x+12,620)],fill=col)
    d.text((x+36,400),title,fill=col,font=f(24,True))
    d.text((x+36,440),date,fill=GREY,font=f(18))
    mx=x+36; my=490
    for j,(v,l) in enumerate(metrics):
        col_i=j%2; row_i=j//2
        cxp=x+36+col_i*((cardw-72)//2); cyp=490+row_i*62
        d.text((cxp,cyp),v,fill=(40,40,40),font=f(30,True))
        d.text((cxp,cyp+38),l,fill=GREY,font=f(17))
    x+=cardw+30
# 洞察条
d.rounded_rectangle([(60,650),(W-60,720)],radius=18,fill=BROWN)
d.text((90,672),"2026.6.23 起日更宠物笔记，首条即爆 —— 用内容选题 + 标签流量撬动算法，账号进入高速增长期。",fill=CREAM,font=f(23,True))
# 能力脚注
d.text((60,760),"我负责的环节：",fill=BROWN,font=f(22,True))
skills=["选题策划","脚本文案","拍摄","剪辑","封面设计","标签/流量投放","评论区运营"]
x=300
for s in skills:
    wch=tw(d,s,f(19))[0]+36
    d.rounded_rectangle([(x,758),(x+wch,798)],radius=20,fill=(245,235,228))
    d.text((x+18,766),s,fill=(90,70,60),font=f(19)); x+=wch+14
img.save(os.path.join(DST,"02.jpg"),quality=90); print("results")
print("total",len(os.listdir(DST)))
