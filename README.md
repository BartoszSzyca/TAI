# TAI
TAI - test artificial intelligence

## Wersja
Aktualna wersja: v0.1.0

## Autor
Bitrax

## Opis
Prosty bot do rozpoznawania mowy, który może prowadzić rozmowy w języku polskim i angielskim. Bot ma zdolność nauki na podstawie wcześniejszych rozmów.


## Funkcje
- Bot nasłuchuje i odpowiada na wypowiedzi w języku polskim i angielskim.
- Ma zdolność nauki na podstawie wcześniejszych rozmów, zapisując je do pliku CSV.

## Korzystanie
1. Uruchom program.
2. Powiedz "thai", aby włączyć tryb słuchania.
3. Wprowadź pytania i rozmawiaj z botem.
4. Powiedz "zakończ", aby zakończyć program.

## Wymagania
- Python 3.x
- Biblioteki: speech_recognition, nltk, pandas, pyttsx3

## Instalacja
1. Sklonuj repozytorium: `git clone https://github.com/twoje_repozytorium.git`
2. Przejdź do katalogu projektu: `cd twoje_repozytorium`
~~3. Zainstaluj wymagane biblioteki: `pip install -r requirements.txt`~~

## Konfiguracja
1. Otwórz plik `conversations.csv` i dodaj własne dane do treningu klasyfikatora.

## Użycie
```bash
python bot_TAI.py
```
## Rozwój
Aktualnie program obsługuje podstawowe funkcje. Bot nasłuchuje i odpowiada na wypowiedzi w języku polskim.
- Ma zdolność nauki na podstawie wcześniejszych rozmów, zapisując je do pliku CSV. Planowane funkcje do dodania:

- [x] Uczenie modelu w trakcie rozmowy
- [x] Używanie spotyfi
- [x] Zapisywanie spotkań/wydarzeń w kalendarzu google

## Licencja
Ten projekt jest objęty licencją [MIT](LICENSE).

