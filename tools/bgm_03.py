import numpy as np
from scipy.io import wavfile
sr=44100; bpm=96; beat=60/bpm; dur=19.0
N=int(sr*dur); out=np.zeros(N)
def add(sig,t):
    i=int(t*sr); j=min(N,i+len(sig))
    if i<N: out[i:j]+=sig[:j-i]
def pluck(f,l=0.5,v=0.2):
    t=np.arange(int(sr*l))/sr
    s=np.sin(2*np.pi*f*t)+0.4*np.sin(4*np.pi*f*t)+0.15*np.sin(6*np.pi*f*t)
    return v*s*np.exp(-t*6)*np.minimum(1,t*400)
def pad(f,l,v=0.05):
    t=np.arange(int(sr*l))/sr
    s=np.sin(2*np.pi*f*t)+0.5*np.sin(2*np.pi*f*1.003*t)
    env=np.minimum(1,t*4)*np.minimum(1,(l-t)*4)
    return v*s*env
def kick(v=0.5):
    t=np.arange(int(sr*0.25))/sr
    return v*np.sin(2*np.pi*(50+90*np.exp(-t*30))*t)*np.exp(-t*14)
def hat(v=0.06):
    t=np.arange(int(sr*0.05))/sr
    return v*np.random.default_rng(1).standard_normal(len(t))*np.exp(-t*90)
def clap(v=0.12):
    t=np.arange(int(sr*0.12))/sr
    return v*np.random.default_rng(2).standard_normal(len(t))*np.exp(-t*35)
n=lambda m:440*2**((m-69)/12)
chords=[[65,69,72],[60,64,67],[62,65,69],[58,62,65]]  # F C Dm Bb
arp=[0,2,1,2,0,1,2,1]
bar=0
while bar*4*beat<dur:
    c=chords[bar%4]; t0=bar*4*beat
    for m in c: add(pad(n(m),4*beat),t0)
    add(pluck(n(c[0]-24),0.9,0.28),t0); add(pluck(n(c[0]-24),0.6,0.2),t0+2.5*beat)
    for k in range(8):
        add(pluck(n(c[arp[k]]+12),0.45,0.16),t0+k*beat/2)
        if bar>=1: add(hat(),t0+k*beat/2)
    if bar>=1:
        for b in range(4): add(kick(),t0+b*beat)
        add(clap(),t0+beat); add(clap(),t0+3*beat)
    bar+=1
t=np.arange(N)/sr
out*=np.minimum(1,t*3)*np.minimum(1,(dur-t)/1.5)
out=out/np.max(np.abs(out))*0.7
wavfile.write('bgm.wav',sr,(np.stack([out,out],1)*32767).astype(np.int16))
