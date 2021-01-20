import requests
from bs4 import BeautifulSoup
import operator
import collections

def einlesen(schlagwort):
    url = 'https://www.ecosia.org/search?q=' + schlagwort
    word_list = []
    source_code = requests.get(url)
    soup = BeautifulSoup(source_code.text, "html.parser")
    for post_text in soup.find_all('p', {'class': 'result-snippet'}):
        word_list.append(post_text.text)    
    final_word_list = word_list
    #Jedes Element zu einzelnen Wörtern splitten
    split_list = []
    for word in final_word_list:
        split_word = word.split()
        for split_value in split_word:
            split_list.append(split_value)
    #Nicht gültige Elemente aus der Liste entfernen
    clean_word_list = []
    for word in split_list:
        if not word.istitle():
            word = ""
        symbols = "!:.,;‚+'<>&/()=?\"#[]" # "-" hier besser weggelassen
        forbiddenwords = ["Wörterbuch", "Kurzform", "Kurzwort", "Abkürzung", "Wörter", "Plural", "Singular", "Homo", "Name", "Jahr", "Bei", "Beim", "Jahrhundert", "Prozent", "Zeichen", "Symbol", "Wort", "Bezeichnung", "Sache", "Sprache", "Logik", "Gliederung", "Definition", "Bedeutung", "Dieser", "Duden", "Begriff", "Beispiel", "Leerzeichen", "Text", "Texte", "Diese", "Artikel", "Siehe", "Wiki", "Der", "Die", "Das", "Bearbeiten", "Seite", "Seiten", "Zufällige", "Letzte", "Änderungen", "Änderung", "Sie", "Er", "Es", "Ein", "Eine", "In", "Im"]
        for i in range(0, len(symbols)):
            word = word.replace(symbols[i], "")
        for i in forbiddenwords:
            if word == i:
                 word = ""
        for i in assoziationsliste:
            if word == i:
                word = word.replace(i, "")
        if schlagwort in word:
            word = ""
        if word in schlagwort:
            word = ""
        if len(word) > 1:
            clean_word_list.append(word)
    #Das meistbenutzteWort herausfinden und testen
    xyz = collections.Counter(clean_word_list).most_common(10)
    final_list = []
    for i in xyz:
        final_list.append(i[0])
    for i in final_list:
        source_code2 = requests.get("https://de.wikipedia.org/wiki/" + i)
        soup2 = BeautifulSoup(source_code2.text, "html.parser")
        if "momentan noch keinen Text und du bist auch nicht dazu berechtigt, diese Seite zu erstellen." in soup2.get_text() or "Diese Seite existiert nicht" in soup2.get_text() or "zur Unterscheidung mehrerer mit demselben Wort bezeichneter Begriffe" in soup2.get_text():
            continue
        else:
            maxT = i
            break
    #Vorgang abschließen
    assoziationsliste.append(maxT)
    return maxT
        

while True:
    try:
        anzahl = int(input("Geben Sie zuerst ein, wie viele Wörter Sie in einer Assoziationskette wollen."))
        break
    except:
        print("Sie müssen eine gültige Zahl eingeben")
while True:
    wert = input("Geben Sie ein Suchwort ein, zu dem eine Assoziationsliste " +
    " mithilfe von ECOSIA erstellt werden soll. Falls Sie die Zahl 1 eingeben, wird das Programm beendet.")
    if wert == "1":
        break
    assoziationsliste = []
    assoziationsliste.append(wert)
    for i in range(anzahl):
        wert = einlesen(wert)
        print(wert)
print("Programm beendet")
