######################################################################
# CT60A0202 Ohjelmoinnin ja data-analytiikan perusteet
# Tekijä: Ilmari Pekonen
# Päivämäärä: 19.11.2018
# Yhteistyö ja lähteet, nimi ja yhteistyön muoto: Stackoverflow, Youtube,
# w3schools
######################################################################
import datetime
import sys


# Luodaan luokat eri analyysejä varten, joita sitten hyödynnetään
# aliohjelmissa kun analysoidaan dataa ja luodaan olioita.
class Analyysi:
    aika = None
    sahko = 0



class PaivaAnalyysi:
    paiva = None
    sahkoP = 0
    kumulatiivinen = 0



class KuukausiAnalyysi:
    kuukausi = None
    sahkoK = 0
    kokovuosi = 0
    prosentti = 0



class TuntiAnalyysi:
    kuukausi = None
    tunti = None
    sahkoT = 0
    kokovuosi = 0
    


def lueTiedosto(nimi):
    lista = []
    rivimaara = 0
    analyysi = 0

    try:
        tiedosto_luku = open(nimi, "r")
    except FileNotFoundError:
        print("Tiedoston '" + nimi + "' lukeminen epäonnistui, ei löydy," \
              " lopetetaan.")
        sys.exit(0)
    next(tiedosto_luku)
    
    while True:
        rivi = tiedosto_luku.readline()
        rivimaara = rivimaara + 1
        if rivi == "":
            print("Tiedosto '" + nimi + "' luettu,", rivimaara, "riviä,",\
                  analyysi, "otettu analysoitavaksi.")
            print("Analysoidaan", ekapaiva, "ja", paiva, "välistä dataa.")
            break
        data = rivi.split(";")  # Hajotetaan rivi listaksi, jotta voimme
                                # summata alkioita yhteen.

        # Muutetaan päivämäärät oikeaan muotoon jatkoa ajatellen.
        paiva = (datetime.datetime.strptime\
                 (data[0], "%Y-%m-%d %H:%M:%S"))\
                 .strftime("%d.%m.%Y %H:%M")

        # Lasketaan kaikki yhden rivin sähköntuotanto yhteen.
        summa = 0

        for i in range(1, 8):
            summa += float(data[i])
            
        if summa < 0:  
            summa = float(0)
        if summa >= 0:
            analyysi = analyysi + 1
        if analyysi == 1:  
            ekapaiva = paiva


        # Lisätään ajanhetki ja sänhkötuotanto aliohjelman alussa luotuun
        # tyhjään listaan.
        analysointi = Analyysi()
        analysointi.aika = paiva
        analysointi.sahko = summa
        lista.append(analysointi)  
    tiedosto_luku.close()

    return lista



def analysoiPaiva(x):
    paivadata = []  # Luodaan tyhjä lista johon lisätään päivittäinen data.
    
    for i in x:  
        loydetty = False 
        ahetki = i.aika.split() # Tehdään lista olion aika -jäsenmuuttujasta.
        paiva = ahetki[0]  # Otetaan käyttöön vain paivämäärä ilman kellonaikaa.
        # Tarkistetaan onko paivadata -listassa oliota kyseiselle päivälle
        # ja jos ei ole niin luodaan sinne sellainen.
        for r in paivadata:
            if r.paiva == paiva:
                r.sahkoP += i.sahko
                loydetty = True
        if not loydetty:
            analyysi = PaivaAnalyysi()
            analyysi.paiva = paiva
            analyysi.sahkoP = i.sahko
            paivadata.append(analyysi)
            
    # Lasketaan kumulatiivinen päivätuotanto käymällä jokainen olio yksitellen
    # läpi ja lisätään kump muuttujaan aina päivätuotanto kumulatiivisesti.
    kump = 0
    for j in paivadata:
        kump += j.sahkoP  
        j.kumulatiivinen = kump
                                
    return paivadata




# Luodaan aliohjelma päivädatan tallennusta varte. Tuodaan aliohjelmaan sisään
# aiemmin luotu lista, joka sisältää olioita.
def tallennaPaiva(tiedosto, a):
    kirjoitus = open("tulosPaiva" + str(a) + ".csv", "w")
    kirjoitus.write("Päivittäinen sähköntuotanto:\n;"+str(a)+"\n")
    
    for i in tiedosto:
        kirjoitus.write(str(i.paiva) + ";"+str(int(i.sahkoP)) + "\n")
    kirjoitus.write("\n\nKumulatiivinen päivittäinen sähköntuotanto:\n")
    kirjoitus.write(";" + str(a )+ "\n")
    
    for j in tiedosto:
        kirjoitus.write(str(j.paiva) + ";" + str(int(j.kumulatiivinen)) + "\n")
    kirjoitus.write("\n\n")  # Lisätään tiedoston loppuun kaksi rivinvaihtoa.
    
    kirjoitus.close()



# Luodaan aliohjelma kuukausianalyysia varten. Niin kuin alussakin aloitamme
# tarkastamalla rivi kerrallaan löytyykö listasta kyseista kuukautta ja jos ei
# löydy niin luodaan listaan sellainen kuukausi, lopuksi vielä lasketaan koko
# vuoden data, sekä prosenttiosuudet joka kuukaudelle.
def analysoiKuukausi(x):
    kuukausidata = []
    
    for i in x:
        loydetty = False
        ahetki = i.aika
        ahetki = ahetki.split()
        ahetki = ahetki[0].split(".")
        kuukausi = ahetki[1]
        
        for r in kuukausidata:
            if r.kuukausi == kuukausi:
                r.sahkoK += i.sahko
                loydetty = True
        if not loydetty:
            analyysi = KuukausiAnalyysi()
            analyysi.kuukausi = kuukausi
            analyysi.sahkoK = i.sahko
            kuukausidata.append(analyysi)

    kokovuosi = 0
    
    for j in kuukausidata:
        kokovuosi += j.sahkoK
    j.kokovuosi = kokovuosi

    prs = 0
    
    for k in kuukausidata:
        prs = int((k.sahkoK / kokovuosi) * 100)
        k.prosentti = prs
        
    return kuukausidata


# Tallennetaan kuukausidata omaan tiedostoon.
def tallennaKuukausi(tiedosto, a):
    kirjoitus = open("tulosKuukausi" + str(a) + ".csv", "w")
    kirjoitus.write("Kuukausittainen sähköntuotanto:\n;" + str(a) \
                    + ";%-osuus\n")
    
    for i in tiedosto:
        kirjoitus.write(" " + str(i.kuukausi) + "/" + str(a) + ";" \
                        + str(int(i.sahkoK)) + ";"+str(i.prosentti) + "%\n")
    kirjoitus.write("Yhteensä;" + str(int(i.kokovuosi)))
    kirjoitus.write("\n\n\n")
    kirjoitus.close()


# Luodaan aluksi tuntidata listaan aluksi jokaisen kuukauden jokaiselle tunnille
# oma kohta, jonka tuotannon oletusarvona on nolla, sillä jos testidatassa ei
# ole joka tunnilta dataa niin se ei mene oikealle paikalleen palautettavassa
# listassa. Listan luomisen jälkeen lisätään vain data oikealle paikalleen
# testidatasta ja lasketaan vielä vuotuinen sähköntuotantomäärä.
def analysoiTunti(x):
    tuntidata = []

    for kuukausi in range(1, 13):
        for tunti in range(0, 24):
            analyysi = TuntiAnalyysi()
            analyysi.kuukausi = str(kuukausi)
            analyysi.tunti = str(tunti)
            analyysi.sahkoT = float(0)
            tuntidata.append(analyysi)
                   
    for i in x:
        ahetki = i.aika
        ahetki = ahetki.split()
        tunti = ahetki[1].split(":")
        tunti = tunti[0]
        if tunti == str('00'):
            tunti = str(0)
        else:
            tunti = tunti.lstrip("0")
        kuukausi = ahetki[0].split(".")
        kuukausi = kuukausi[1].lstrip("0")
        for r in tuntidata:
            if r.kuukausi == kuukausi and r.tunti == tunti:
                r.sahkoT += i.sahko

    # Luodaan uusi lista yksittäisille tunneille vuosituotannossa.
    tunnit = []
    
    for j in range(0, 24):
        tunnit.append(float(0))
        
    for k in tuntidata:
        tunti = k.tunti
        tunnit[int(tunti)] += k.sahkoT
        
    kokovuosi = 0
    
    for p in tuntidata:
        kokovuosi += p.sahkoT
    p.kokovuosi = kokovuosi
    
    return tuntidata, tunnit

     
# Tallennetaan data omaan tiedostoonsa ja lasketaan vielä lopuksi
# prosenttiosuudet joka tunnille.
def tallennatunti(tiedosto, tunnittainen, a):

    kirjoitus = open("tulosTunti" + str(a) + ".csv", "w")
    kirjoitus.write("Tuntipohjainen sähköntuotanto:\n")
    
    for i in range(0, 24):
        kirjoitus.write(";" + str(i))
    kk = 0
    
    for j in tiedosto:
        if j.kuukausi != str(kk):
            kk += 1
            kirjoitus.write("\n")
            if len(str(kk)) == 1:
                kirjoitus.write(" 0" + str(j.kuukausi) + "/" + str(a))
            else:
                kirjoitus.write(" " + str(j.kuukausi) + "/" + str(a))
        kirjoitus.write(";" + str(int(j.sahkoT)))
    kirjoitus.write("\nYhteensä")
    
    for p in tunnittainen:
        kirjoitus.write(";" + str(int(p)))
    kirjoitus.write("\n\n\n")

    kirjoitus.write("Yksittäisen tunnin osuus vuosittaisesta "\
                    "sähköntuotannosta:\n")
    for k in range(0, 24):
        kirjoitus.write(";" + str(k))
    kirjoitus.write("\n%-osuus")
    kokovuosi = j.kokovuosi
    
    for h in tunnittainen:
        prs = int((h / kokovuosi) * 100)
        kirjoitus.write(";" + str(prs) + "%")
    kirjoitus.write("\n\n\n")        
        
    kirjoitus.close()
