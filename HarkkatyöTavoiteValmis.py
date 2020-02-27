######################################################################
# CT60A0202 Ohjelmoinnin ja data-analytiikan perusteet
# Tekijä: Ilmari Pekonen
# Päivämäärä: 19.11.2018
# Yhteistyö ja lähteet, nimi ja yhteistyön muoto: Stackoverflow, Youtube,
# w3schools
######################################################################
import HTLibTavoite
     
while True:
    print("Anna haluamasi toiminnon numero seuraavasta valikosta:")
    print("1) Lue sähköntuotantotiedot")
    print("2) Analysoi päivätuotanto")
    print("3) Tallenna päivätuotanto")
    print("4) Analysoi kuukausituotanto")
    print("5) Analysoi tuntituotanto")
    print("6) Tallenna kuukausituotanto")
    print("7) Tallenna tuntituotanto")
    print("0) Lopeta")
    valinta = int(input("Valintasi: "))
    if valinta == 1:
        nimi = input("Anna luettavan tiedoston nimi: ")
        vuosi = input("Anna analysoitava vuosi: ")
        tiedot = HTLibTavoite.lueTiedosto(nimi)
        print()
        
    if valinta == 2:
        paivatiedot = HTLibTavoite.analysoiPaiva(tiedot)
        print("Päivätuotanto analysoitu.\n")
        
    if valinta == 3:
        HTLibTavoite.tallennaPaiva(paivatiedot, vuosi)
        print("Päivätuotanto tallennettu tiedostoon 'tulosPaiva"+\
              str(vuosi)+".csv'.\n")

    if valinta == 4:
        kuukausitiedot = HTLibTavoite.analysoiKuukausi(tiedot)
        print("Kuukausituotanto analysoitu.\n")
        
    if valinta == 5:
        tuntitiedot, vuositunnit = HTLibTavoite.analysoiTunti(tiedot)
        print("Tuntituotanto analysoitu.\n")
##        for i in tuntitiedot:
##            print(i.kuukausi, i.tunti, i.sahkoT)
        
    if valinta == 6:
        HTLibTavoite.tallennaKuukausi(kuukausitiedot, vuosi)
        print("Kuukausituotanto tallennettu tiedostoon 'tulosKuukausi"+\
              str(vuosi)+".csv'.\n")
        
    if valinta == 7:
        HTLibTavoite.tallennatunti(tuntitiedot, vuositunnit, vuosi)
        print("Tuntituotanto tallennettu tiedostoon 'tulosTunti"+\
              str(vuosi)+".csv'.\n")

    if valinta == 0:
        print("Kiitos ohjelman käytöstä.")
        break
