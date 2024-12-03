import random
from datetime import datetime

import haravasto

MIINAT = 10
KORKEUS = 10
LEVEYS = 10

DOUCEMNT = "tilastot.txt"

kentta = []
miinoitettu_kentta = []
vapaa_kentta = []
peli_tila = True
aloitus_aika = None

tilastot = {
    "paivamaara" : "",
    "lopputulos" : "",
    "kesto" : 0,
    "vuoroja": 0,
    "miinat_kpl": 0,
    "kentan_koko": 0,
}

imgSource = "/Users/danielforsell/Ohjelmiston Alkeet 2024/Projekti/spritet"

def luo_kentta(leveys, korkeus):
    for y in range(korkeus):
        rivi = []
        for x in range(leveys):
            rivi.append(" ")
        kentta.append(rivi)

    for y in range(korkeus):
        rivi = []
        for x in range(leveys):
            rivi.append(" ")
        miinoitettu_kentta.append(rivi)

def miinoita(kentta, miinojen_lkm):
    for y in range(KORKEUS):
        for x in range(LEVEYS):
            vapaa_kentta.append((y, x))

    while miinojen_lkm > 0:
        x, y = random.choice(vapaa_kentta)
        kentta[y][x] = "x"
        vapaa_kentta.remove((x, y))
        miinojen_lkm -= 1

def laske_miinat(y, x, kentta):
    korkeus = len(kentta)
    leveys = len(kentta[0])
    miinat = 0
    for i in range(y - 1, y + 2):
        for j in range(x - 1, x + 2):
            if 0 <= i < korkeus and 0 <= j < leveys and (i != y or j != x):
                if kentta[i][j] == "x":
                    miinat += 1
    return miinat

def tulvataytto(x, y):
    korkeus = len(kentta)
    leveys = len(kentta[0])
    if kentta[y][x] == "x":
        miinoitettu_kentta[y][x] = "x"
        return False
    
    alkio = [(x, y)]
    kaydyt = set()

    while alkio:
        alkio_x, alkio_y = alkio.pop()
        if (alkio_x, alkio_y) in kaydyt:
            continue
        kaydyt.add((alkio_x, alkio_y))

        miinat = laske_miinat(alkio_y, alkio_x, kentta)
        miinoitettu_kentta[alkio_y][alkio_x] = str(miinat) if miinat > 0 else "0"

        if miinat == 0:
            for i in range(alkio_y - 1, alkio_y + 2):
                for j in range(alkio_x - 1, alkio_x + 2):
                    if 0 <= i < korkeus and 0 <= j < leveys and (i != alkio_y or j != alkio_x):
                        if kentta[i][j] != "x" and (j, i) not in kaydyt:
                            alkio.append((j, i))
    return True
    
def piirra_kentta():
    for y, rivi in enumerate(miinoitettu_kentta):
        for x, ruutu in enumerate(rivi):
            haravasto.lisaa_piirrettava_ruutu(ruutu, x * 40, (len(miinoitettu_kentta) - y - 1) * 40)
    haravasto.piirra_ruudut()

def kasittele_hiiri(x, y, nappi, muokkausnappaimet):
    global peli_tila
    x = int(x / 40)
    y = int(len(kentta) - y / 40)
    if peli_tila: 
        if nappi == haravasto.HIIRI_VASEN:
            tilastot["vuoroja"] += 1
            peli_tila = tulvataytto(x, y)
            if tarkista_voitto():
                lopetus_aika = datetime.now()
                tilastot["kesto"] = f"{float((lopetus_aika - aloitus_aika).total_seconds()):.1f}"
                tilastot["lopputulos"] = "Voitto"
                kirjaa_tilastot()
                haravasto.aseta_piirto_kasittelija(lopeta_peli_voitto)
    if not peli_tila:
        lopetus_aika = datetime.now()
        tilastot["kesto"] = f"{float((lopetus_aika - aloitus_aika).total_seconds()):.1f}"
        tilastot["lopputulos"] = "Häviö"
        kirjaa_tilastot()
        haravasto.aseta_piirto_kasittelija(lopeta_peli)
          
def lopeta_peli(): 
    haravasto.piirra_tekstia("Hävisit pelin :(", (LEVEYS * 20) / 2, 
                            (KORKEUS * 40) / 2, vari=(255, 0, 0, 255), 
                            fontti="Arial", koko=25)
    piirra_kentta()
    
def lopeta_peli_voitto():
    haravasto.piirra_tekstia("Voitit pelin! :)", 
                             LEVEYS * 10, KORKEUS * 20, 
                             vari=(0, 255, 0, 255), 
                             fontti="Arial", koko=25)
    piirra_kentta()

def tarkista_voitto():
    for rivi in miinoitettu_kentta:
        for ruutu in rivi:
            if ruutu == " ":
                return False
    return True

def hae_tilastot(doc):
    with open (doc,"r") as tiedosto:
        for rivi in tiedosto.readlines():
            paivamaara, lopputulos, kesto, vuoroja, miinat_kpl, kentan_koko = rivi.split(",")
            print(f""" 
                {paivamaara}\n
                {lopputulos}\n
                {kesto}\n
                {vuoroja}\n
                {miinat_kpl}\n
                {kentan_koko}\n""")
    valinta()

def kirjaa_tilastot():
    try:
        with open(DOUCEMNT, "a") as tiedosto:
            rivi = f"Päivämäärä: {tilastot['paivamaara']}, Lopputulos: {tilastot['lopputulos']}, Kesto: {tilastot['kesto']}, Vuoroja: {tilastot['vuoroja']}, Miinojen_kpl: {tilastot['miinat_kpl']}, Kentän koko:{tilastot['kentan_koko']}\n"

            tiedosto.write(rivi)
    except IOError: 
        print("Virhe tiedoston kirjoittamisessa.")
    
def main():
    luo_kentta(LEVEYS, KORKEUS)
    miinoita(kentta, MIINAT)
    haravasto.lataa_kuvat(imgSource)
    haravasto.luo_ikkuna(LEVEYS * 40, KORKEUS * 40)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    haravasto.aloita()

def valinta():
    global aloitus_aika
    print("Hei! käynnistit miinantallaaja pelin!")
    print("(A)loita peli > ")
    print("(K)atso tilastot > ")
    print("(S)ulje ohjelma > ")
    valinta = input("Valiste: ").lower()
    if valinta == "a":
        tilastot["miinat_kpl"] = MIINAT
        tilastot["kentan_koko"] = f" x: {LEVEYS} y:{KORKEUS}"
        aloitus_aika = datetime.now()
        tilastot["paivamaara"] = aloitus_aika.strftime("%Y-%m-%d %H:%M:%S")
        main()
    elif valinta == "k":
        hae_tilastot(DOUCEMNT)
    elif valinta == "s":
        exit()
    else:
        print("Väärä kirjian/merkki, yritä uudelleen")



if __name__ == "__main__":
    valinta()
