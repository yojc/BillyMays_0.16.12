# Billy Mays & KatajNapsika

Pakiet dwóch botów pod Discorda, napisanych w Pythonie na bazie [BasicBot](https://github.com/Habchy/BasicBot)a.

Billy Mays (*billy.py*) jest kontynuacją Mariusza_Stefana, stworzonego na potrzeby #nfaircc7 na bazie IRCowego bota Phenny (obecnie Sopel). 

KatajNapsika (*kathai.py*) to tak naprawdę nie jest bot, tylko bardzo zaawansowana sztuczna inteligencja.

Boty są od siebie niezależne, aczkolwiek współdzielony jest plik *config.py*.

## Wymagania

Ten projekt do uruchomienia wymaga Pythona 3 wraz z jakimiś doinstalowanymi pakietami. Jeśli o niczym nie zapomniałem, to poniżej jest lista czego potencjalnie możesz nie mieć:

```
bs4
discord
cleverwrap
colorama
emoji
requests
unidecode
wolframalpha
```

**Ten bot nie zadziała z Pythonem w wersji 3.7**. Przynajmniej mi się nie udało. Zawsze możesz spróbować zrobić osobną instalację 3.6: https://tecadmin.net/install-python-3-6-ubuntu-linuxmint/

## Klucze do aplikacji

Utwórz plik *config.py* o następującej zawartości:

```
billy_key = ""
kathai_key = ""
cleverbot_key = ""
wolfram_key = ""
twitch_key = ""
```

Wypełnij puste pola odpowiednimi wartościami. Może sobie poradzisz, może nie.

## Tryb debug

W pliku *billy_shared.py* przestaw wartość zmiennej *testing* na *True*, jeśli chcesz włączyć proste debugowe informacje zrzucane do konsoli. Może ci się przyda, może nie.

## Automatyczny restart

Z jakichś powodów boty czasem potrafią się wyłączyć, nie podając przy tym żadnego błędu. Zawsze można obejść problem uruchamiając je za pomocą shellowego skryptu, przykładowo:

```
while true
do
	python3 /sciezka/do/pliku.py
	now="$(date)"
	echo -e "\e[91m$now Script ended! Restarting in 10 secs...\e[39m"
	sleep 10
done
```

(przeklejając z Windowsa należy pamiętać o podmianie \r\n na \n...)

## Inne

Projekt jest w fazie rozwoju, tylko mi się nie chce.
