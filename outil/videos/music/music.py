"""Musiques originales (synthèse maison, libres de droits) pour les vidéos JBKT."""
import numpy as np, subprocess, sys
from scipy.signal import fftconvolve, butter, sosfilt

SR = 44100
rng = np.random.default_rng(7)

def midi(n): return 440 * 2 ** ((n - 69) / 12)

def env(n, a=0.005, d=0.3, s=0.0, r=0.05, length=None):
    t = np.arange(n) / SR
    e = np.where(t < a, t / a, s + (1 - s) * np.exp(-(t - a) / max(d, 1e-4)))
    if length:
        rel = t > length
        e = np.where(rel, e * np.exp(-(t - length) / r), e)
    return e

def lp(x, f, order=2):
    return sosfilt(butter(order, f, 'low', fs=SR, output='sos'), x)

def hp(x, f, order=2):
    return sosfilt(butter(order, f, 'high', fs=SR, output='sos'), x)

def epiano(f, dur):
    n = int((dur + 1.2) * SR); t = np.arange(n) / SR
    mod = np.sin(2 * np.pi * f * 14 * t) * 0.6 * np.exp(-t * 9)
    x = np.sin(2 * np.pi * f * t + mod) + 0.25 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 3)
    x += 0.08 * np.sin(2 * np.pi * f * 3 * t) * np.exp(-t * 6)
    trem = 1 + 0.12 * np.sin(2 * np.pi * 4.5 * t)
    return x * env(n, 0.003, 1.4, 0.0, 0.25, dur) * trem

def pad(f, dur):
    n = int((dur + 1.5) * SR); t = np.arange(n) / SR
    x = sum(2 * ((f * dt * t) % 1) - 1 for dt in (0.995, 1.0, 1.006))
    x = lp(x / 3, 1400)
    a = np.minimum(t / 0.6, 1); rel = np.where(t > dur, np.exp(-(t - dur) / 0.5), 1)
    return x * a * rel

def bass(f, dur):
    n = int((dur + 0.2) * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + 0.3 * np.tanh(3 * np.sin(2 * np.pi * f * t))
    return x * env(n, 0.01, 0.9, 0.55, 0.06, dur)

def kick():
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 48 + 90 * np.exp(-t * 35)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 7) + 0.15 * rng.standard_normal(n) * np.exp(-t * 200)

def hat(o=False):
    n = int((0.25 if o else 0.07) * SR); t = np.arange(n) / SR
    return hp(rng.standard_normal(n), 7000) * np.exp(-t * (14 if o else 60))

def clap():
    n = int(0.3 * SR); t = np.arange(n) / SR
    x = sosfilt(butter(2, [900, 2500], 'band', fs=SR, output='sos'), rng.standard_normal(n))
    e = np.exp(-t * 22) + sum(np.exp(-np.maximum(t - d, 0) * 120) * (t >= d) * 0.6 for d in (0.0, 0.012, 0.024))
    return x * e * 0.6

def reverb(x, sec=2.2, mix=0.25):
    n = int(sec * SR); t = np.arange(n) / SR
    ir = rng.standard_normal(n) * np.exp(-t * 3 / sec)
    ir = lp(ir, 5000); ir /= np.sqrt((ir ** 2).sum())
    w = fftconvolve(x, ir)[:len(x)]
    return x * (1 - mix) + w * mix * 1.2

TRACKS = {
    # nom: bpm, accords (notes midi), basses, ambiance
    'clair': dict(bpm=100, chords=[[65, 69, 72, 76], [57, 64, 67, 72], [62, 65, 69, 72], [58, 62, 65, 69]],
                  bass=[41, 45, 38, 46], drums='full', arp=True),
    'calme': dict(bpm=88, chords=[[60, 64, 67, 71], [57, 60, 64, 67], [53, 57, 60, 64], [55, 59, 62, 65]],
                  bass=[36, 33, 41, 43], drums='soft', arp=False),
    'elan':  dict(bpm=108, chords=[[62, 66, 69, 73], [59, 62, 66, 69], [55, 59, 62, 66], [57, 61, 64, 67]],
                  bass=[38, 35, 43, 45], drums='full', arp=True),
}

def place(buf, x, at, g=1.0):
    i = int(at * SR)
    if i >= len(buf): return
    m = min(len(x), len(buf) - i)
    buf[i:i + m] += x[:m] * g

def make(name, seconds=40):
    p = TRACKS[name]; beat = 60 / p['bpm']; bar = 4 * beat
    n = int((seconds + 3) * SR)
    keys, pads, bs, drums = (np.zeros(n) for _ in range(4))
    nbars = int(seconds / bar) + 1
    for b in range(nbars):
        t0 = b * bar; c = p['chords'][b % 4]; root = p['bass'][b % 4]
        for k, note in enumerate(c):  # léger strum
            place(pads, pad(midi(note - 12), bar), t0, 0.10)
            place(keys, epiano(midi(note), beat * 1.5), t0 + k * 0.012, 0.16)
            place(keys, epiano(midi(note), beat * 0.9), t0 + 2.5 * beat + k * 0.01, 0.10)
        if p['arp'] and b >= 2:
            seq = [c[0] + 12, c[2] + 12, c[1] + 12, c[3] + 12, c[2] + 12, c[0] + 12, c[3], c[1] + 12]
            for i, note in enumerate(seq):
                place(keys, epiano(midi(note), beat * 0.4), t0 + i * beat / 2, 0.07)
        pat = [(0, 1.5), (1.5, 0.4), (2, 1.5), (3.5, 0.4)]
        for at, d in pat:
            place(bs, bass(midi(root + (7 if at == 1.5 else 0)), d * beat), t0 + at * beat, 0.32)
        if b >= 1:
            ks = [0, 2.5] if p['drums'] == 'soft' else [0, 1.75, 2.5]
            for k in ks: place(drums, kick(), t0 + k * beat, 0.55)
            for k in (1, 3): place(drums, clap(), t0 + k * beat, 0.35 if p['drums'] == 'full' else 0.22)
            for i in range(8):
                place(drums, hat(i % 4 == 3), t0 + i * beat / 2 + (0.015 if i % 2 else 0), 0.06 if i % 2 else 0.09)
    # sidechain sur pad + basse
    t = np.arange(n) / SR
    ph = (t % beat) / beat
    duck = 1 - 0.45 * np.exp(-ph * 9) * (t > bar)
    mix = reverb(keys, 2.4, 0.35) + reverb(pads, 3.0, 0.4) * duck + bs * duck + reverb(drums, 1.0, 0.12)
    mix = hp(mix, 30)
    mix = mix / np.max(np.abs(mix)) * 1.6
    mix = np.tanh(mix) * 0.85
    mix = mix[:int(seconds * SR)]
    fade = int(2.0 * SR); mix[-fade:] *= np.linspace(1, 0, fade)
    st = np.stack([mix, np.roll(mix, int(0.011 * SR)) * 0.92 + mix * 0.08], 1)  # léger élargissement
    pcm = (st * 32767).astype('<i2').tobytes()
    out = f'music/{name}.m4a'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 's16le', '-ar', str(SR), '-ac', '2', '-i', '-',
                    '-af', 'loudnorm=I=-16:TP=-1.5', '-c:a', 'aac', '-b:a', '192k', out], input=pcm, check=True)
    print(out)

if __name__ == '__main__':
    import os; os.makedirs('music', exist_ok=True)
    for nm in (sys.argv[1:] or TRACKS): make(nm)
