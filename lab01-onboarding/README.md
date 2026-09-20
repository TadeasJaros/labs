# Cvičení 01 — Seznámení s HTTP a Gitem

**Délka:** 90 minut · **Výsledek:** propojení studentů do týmů, osvojení Gitu a práce s webovým
serverem.

V předmětu Webové aplikace (WEA) si v týmech osvojíme moderní technologie a postupy pro vývoj
webových aplikací. Na tomto úvodním cvičení spustíme první webový server, prozkoumáme jeho API,
budeme server volat z příkazové řádky a na závěr vytvoříme první pull request na GitHubu.

---

## Co vás čeká

Cílem cvičení je, aby se každý student zaregistroval do předmětu — ve formě JSON souboru
v adresáři `lab01-onboarding/roster/` (ukázka je v [_example.json](./roster/_example.json)).

Aby to nebylo tak jednoduché, musíte si nejdříve nastavit prostředí (kroky 0 a 1) a vyřešit
úkoly 2–5, které Vám prozradí, co do souboru vyplnit.

Stručný přehled úkolů (detaily jsou níže):

```
0. Prerekvizity
1. Fork tulwea26/labs → naklonovat k sobě
2. Spustit webový server (Docker nebo Python) a prozkoumat jeho API - v http://localhost:8000/docs
3. Zeptat se serveru na endpointu `/slot`, jaký stavový kód je Váš
4. Zjistit na endpointu `/status`, co ten kód znamená (a jak vypadá HTTP odpověď)
5. Zašifrovat svůj TUL alias
6. Přidat `roster/<github-login>.json`, commit, push
7. Otevřít pull request proti tulwea26/labs:main
8. Požádat souseda o zkontrolování a schválení pull requestu
9. Cvičící pull requesty zamerguje do main větve; vytvořený seznam studentů bude použit pro rozdělení do týmů
```

Kroky 1–8 jsou **povinné** (krok 9 udělá cvičící), bonusové úkoly pro rychlejší studenty jsou
[níže](#bonusy).

---

## 0. Prerekvizity

- Mít [GitHub účet](https://github.com/signup) — nejlépe s @tul.cz adresou. Po skončení cvičení
  aktivovat [GitHub Education](https://github.com/education/students) (studentské výhody —
  GitHub Copilot Pro a další).

Instalace software na Váš osobní počítač (v labu jsou pravděpodobně potřebné nástroje již
nainstalovány):

- [Git](https://git-scm.com/install/) — nástroj pro správu verzí softwarového kódu. Na Windows
  s ním nainstalujete i **Git Bash**, který budete v kroku 2 potřebovat.
- Jedno z následujících (viz krok 2):
  - [Docker Desktop](https://www.docker.com/products/docker-desktop/) — platforma pro
    kontejnerizaci aplikací (spouští aplikace v izolovaných prostředích), **nebo**
  - [Python](https://www.python.org/downloads/) 3.9 nebo novější — interpret programovacího
    jazyka Python.
- Libovolný textový editor, např. [Visual Studio Code](https://code.visualstudio.com/download).

## 1. Fork repozitáře se zadáním

Na <https://github.com/tulwea26/labs> klikněte na **Fork**.

**Poté** v adresáři, kde chcete mít kód:

```bash
git clone https://github.com/<Váš-github-login>/labs.git
cd labs/lab01-onboarding
git checkout -b feature/prihlaska
```

Toto vytvoří Vaši vlastní kopii repozitáře a vývojovou větev (práce přímo v hlavní větvi `main`
je nebezpečná, více se dozvíme později).

## 2. Spuštění pomocného serveru

Náš ukázkový server je malá aplikace napsaná v Pythonu, ve frameworku FastAPI. Má dva endpointy
a nemá žádný stav. Vyberte si jednu z cest, jak jej spustit — obě končí stejně, tj. na
<http://localhost:8000/docs>.

### Cesta A — Docker

Doporučeno, pokud máte [Docker](https://www.docker.com/) — nemusí být dostupný na počítačích
v laboratoři.

```bash
docker compose up
```

Tento příkaz stáhne všechny potřebné balíčky a spustí backend server jako Docker kontejner.
První spuštění chvíli trvá — staví se image, v terminálu poběží výpis instalace; server je
připravený, až uvidíte řádek `Uvicorn running on http://0.0.0.0:8000`. Pokud Docker nemáte,
vyzkoušejte cestu B — pomocí nainstalovaného Pythonu.

### Cesta B — Python (na školním počítači nebo bez Dockeru)

Potřebujete Python 3.9 nebo novější, zkontrolujte si ho: `python --version`. Pro vývoj v Pythonu
je doporučené vždy vytvořit virtuální prostředí, kam se nainstalují všechny potřebné balíčky
(`venv`):

**Windows** (PowerShell):

```powershell
cd server
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

> Pokud PowerShell odmítne spustit `Activate.ps1`, použijte
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` a zkuste to znovu, nebo místo toho
> spusťte `.\.venv\Scripts\activate.bat` v příkazové řádce (cmd).

**macOS / Linux**:

```bash
cd server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Spuštění webového serveru** (na všech systémech stejně, s aktivovaným `.venv`):

```bash
uvicorn main:app
```

### API dokumentace: Swagger

Ať jste zvolili kteroukoliv cestu, otevřete <http://localhost:8000/docs>. To je **Swagger UI** —
interaktivní dokumentace API vygenerovaná automaticky ze zdrojového kódu: každý endpoint,
parametr i tvar odpovědi. Prohlédněte si to; později v semestru budete své vlastní API
dokumentovat.

### Druhý terminál — v něm budete pracovat dál

Server si terminál drží pro sebe a píše do něj aplikační logy: dokud ho nezastavíte zkratkou
`Ctrl+C`, nic dalšího do něj nenapíšete. Nechte ho tedy běžet a **otevřete si druhý terminál** —
v něm uděláte všechny zbývající kroky. Server zastavte až na konci cvičení.

- **Windows:** ten druhý terminál musí být **Git Bash**. Nainstaloval se Vám spolu s Git for
  Windows; najdete ho v nabídce Start, nebo v Průzkumníku pravým tlačítkem → *Open Git Bash here*.
  Důvod je dvojí: PowerShell nemá `curl` (má jen stejnojmennou zkratku pro `Invoke-WebRequest`,
  která na krocích 3 a 4 spadne) a nemá ani `openssl`, který budete potřebovat v kroku 5. Git Bash
  má obojí a příkazy v něm vypadají úplně stejně jako na Linuxu.
- **Linux / macOS:** jakýkoliv další terminál.

V druhém terminálu se přepněte do adresáře cvičení, tedy tam, kde jste skončili v kroku 1:

```bash
cd <cesta-ke-klonu>/labs/lab01-onboarding
```

## 3. Zjistěte svůj kód

Server na endpointu `/slot` každému studentovi vrátí nějaký stavový kód protokolu HTTP (bude
potřeba v dalším bodu a také ve Vašem JSON souboru).

Pro interakci se serverem můžeme používat webový prohlížeč (viz Swagger API výše), my se ale
podíváme po alternativě — příkazu `curl`. Ten nám umožní se serverem interagovat přímo
z příkazové řádky. Všechny následující příkazy pište do **druhého terminálu** (Git Bash nebo
Bash), ne do toho, kde Vám běží server.

```bash
curl "http://localhost:8000/slot?github_handle=<Váš-github-login>"
```

## 4. Co ten kód znamená

Pomocí stavových kódů dává server najevo, jak se mu povedlo zpracovat klientský požadavek. Pokud
víte, co Váš stavový kód znamená, zapište si to do svého souboru v rosteru (viz krok 6). Pokud
ne, nevadí, o [stavových kódech](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) se
budeme učit později. Popis kódu zjistíte pomocí následujícího příkazu:

```bash
curl -i "http://localhost:8000/status?code=<Váš-kód>"
```

Parametr `-i` vypíše i hlavičky odpovědi, což je dobré pro zjištění detailů chybových stavů.
První řádek je **status line**, dále následují hlavičky (response headers) a potom tělo odpovědi
(response body).

> Volitelně můžete zkusit i parametr `-v` — zjistíte tak, co posílá klient.

V těle odpovědi máte oficiální název a jednořádkový popis kódu. Ideálně byste však do rosteru
napsali význam kódu **vlastními slovy** (za jakých okolností server takový kód pošle a co s ním
má klient udělat). Toto můžete zjistit např. v [RFC 9110](https://datatracker.ietf.org/doc/html/rfc9110),
na Googlu nebo se zeptejte oblíbeného chatbota.

> **Pokud Vám vyšlo `204 No Content`:** `curl -i` vypíše hlavičky a pak nic. To je správně.
> RFC 9110 §15.3.5 říká, že odpověď 204 nemá obsah, takže se tělo zahodí dřív, než se dostane
> na drát. Máte to nastavené dobře. Napište to do popisu pull requestu — právě jste
> odpověděli na otázku, kterou většina lidí nezná.

## 5. Zašifrování TUL aliasu

Repozitář předmětu je **veřejný**, pro zachování citlivých údajů svůj TUL alias
(`jmeno.prijmeni`) do něj nedávejte v čitelné podobě. Zašifrujte ho veřejným klíčem předmětu:

```bash
# musíte být v adresáři lab01-onboarding - po kroku 2, cestě B, jste v server/, tak se vraťte: cd ..
./tools/encrypt_me.sh jmeno.prijmeni
```

Na Windows to spusťte v **Git Bash** (viz druhý terminál v kroku 2) — jako jediný na Windows
má v sobě `openssl`. Kdo jede přes Docker, může to spustit i v kontejneru:

```bash
docker compose run --rm --entrypoint /work/tools/encrypt_me.sh onboarding jmeno.prijmeni
```

Celé to proběhne **u Vás na počítači**. Server žádný `/encrypt` endpoint nemá, a to schválně:
kdybyste svůj alias poslali serveru, aby Vám ho „ochránil", tak už ho ten server viděl (a cestou
možná ještě někdo jiný). Soukromý klíč k dešifrování má jen cvičící.

> Zkuste spustit šifrování se stejným parametrem dvakrát — dostanete dva různé výstupy. To je
> [RSA-OAEP](https://en.wikipedia.org/wiki/Optimal_asymmetric_encryption_padding) a jeho
> náhodný padding. Právě díky němu si nikdo nemůže zašifrovat tip `jan.novak` a porovnat ho
> s commitem.

Se šifrováním a `openssl` se potkáte později v semestru.

## 6. Záznam v rosteru

Vytvořte soubor `roster/<github-login>.json`. Název souboru musí být přesně Váš GitHub login,
malými písmeny.

Ukázkový `roster/jannovak99.json`:

```json
{
  "github_handle": "jannovak99",
  "http_code": 401,
  "description": "Server rozumí požadavku, ale odmítá ho obsloužit, dokud se klient neprokáže — typicky chybí nebo je neplatná hlavička Authorization. ...",
  "preferred_language": "typescript",
  "encrypted_alias": "O9j...ahQ=="
}
```

- **`github_handle`** — Váš GitHub login, malými písmeny (stejný jako název souboru).
- **`http_code`** — HTTP stavový kód, který server vrátil v kroku 3.
- **`description`** — popis významu stavového kódu, **vlastními slovy** (oficiální popis získáte
  v kroku 4). Kdy to server pošle? Co má klient udělat? Aspoň 40 znaků; samotný oficiální název neprojde kontrolou.
- **`preferred_language`** — jedno z `csharp`, `typescript`, `javascript`, `python`, `java`,
  `kotlin`, `go`, `rust`, `ruby`, `other`. Podle toho se (mimo jiné) skládají týmy, tak
  odpovězte upřímně. `php` zadání semestrálky vylučuje.
- **`encrypted_alias`** — Váš zašifrovaný TUL alias z kroku 5.

Vzor je v [`roster/_example.json`](./roster/_example.json).

**Před commitem si to zkontrolujte** — je to stejný skript, co běží v CI (opět z adresáře
`lab01-onboarding`):

```bash
python tools/validate_roster.py
```

## 7. Commit, push, pull request

Pokud na tomto počítači commitujete poprvé, git neví, kdo jste, a commit odmítne. Představte se
mu (stačí jednou, `--global` platí pro všechny repozitáře na tomto počítači):

```bash
git config --global user.name "Jan Novák"
git config --global user.email "jan.novak@tul.cz"
```

Toto jméno a e-mail se zapíše do každého Vašeho commitu a v historii veřejného repozitáře
zůstane natrvalo. Zapamatujte si to, vrátíme se k tomu v bonusu B.

```bash
git add roster/<github-login>.json
git commit -m "Claim HTTP <kód> for <login>"
git push -u origin feature/prihlaska
```

Pak na GitHubu otevřete pull request z Vašeho forku proti `tulwea26/labs` na větev `main`.
Vyplňte šablonu, je krátká.

**Váš pull request přidává přesně jeden soubor: ten Váš.** Všichni díky tomu mohou přidávat své
soubory paralelně (kdybychom měli jeden sdílený soubor, určitě nám nastanou konflikty).
Automatické testy odmítnou vše, co mění nebo maže něco jiného.

## 8. Review spolužáka

Se sousedem, nebo kýmkoli jiným, kdo již má také hotový pull request, si vyměňte úkoly. Kolegovi
napište code review (posudek jeho změn). Kontrolujete pět věcí:

- [ ] Popis pull requestu odpovídá tomu, co změna dělá.
- [ ] Vytvořený soubor je pojmenován `roster/<github-login>.json`.
- [ ] Kód odpovídá tomu, co pro jeho login vrátí `/slot`.
- [ ] `description` je věcně správně a je vlastními slovy, ne zkopírovaný.
- [ ] GitHub akce (testy) na pull requestu jsou zelené.

Review je od toho, abyste si četli kód a mluvili spolu. Cílem je buďto pull request schválit,
nebo kolegovi sdělit (buďto slovně, nebo přes komentáře v GitHubu), co by měl opravit. Merge
změny může provést jenom cvičící.

---

## Bonusy

Hotovo dřív, nebo děláte z domova?

**A. Prázdná odpověď.** Zkuste `curl -i "http://localhost:8000/status?code=204"` a do
komentáře v pull requestu vysvětlete, proč vidíte hlavičky a žádné tělo — a co by server
musel udělat jinak, aby tělo poslal. Pak zkuste `?code=101` a vysvětlete chybu, kterou
dostanete.

**B. Prolomte si vlastní šifru.** Váš alias je zašifrovaný 2048bitovým RSA klíčem. Bez
soukromého klíče se z toho nedostane. A přesto — spusťte tohle nad svým pull requestem:

```bash
git log --format='%an <%ae>' -1
```

Vaše jméno a e-mail jsou u každého commitu, který jste právě pushli. V čitelné podobě,
veřejně, napořád. Jestli máte v gitu nastavený školní e-mail, Váš TUL alias leží *hned
vedle* šifry, která ho měla chránit.

Toto nám ukazuje, že kryptografie není všespásná, citlivá data nám mohou utéct i jinými,
často na první pohled neviditelnými kanály.

**C. Ozdoba.** Přidejte do popisu pull requestu odkaz na `https://http.cat/<Váš-kód>` nebo
číslo sekce RFC, která Váš kód definuje.

---

## Když něco nejde

| Příznak | Příčina |
| --- | --- |
| `curl` se připojí, ale nic nevrátí, status 204 nebo 205 | Správné chování, viz krok 4. |
| `docker compose up` selže na portu 8000 | Něco na něm už běží. Změňte port v `docker-compose.yml`. |
| `uvicorn: command not found` | Nemáte aktivované `.venv`. Viz krok 2, cesta B. |
| `encrypt_me.sh: public key not found` | Ozvěte se cvičícímu — `server/public_key.pem` má být v repozitáři. |
| CI říká `http_code N is not the code /slot gives for ...` | Překlep v loginu nebo v kódu. Zavolejte `/slot` znovu. |
| CI říká, že pull request mění cizí soubory | Nejspíš jste commitli `.venv`, `__pycache__` nebo soubor editoru. Odeberte ho z commitu. |
| `curl` hlásí `Cannot process command ... Uri` nebo `Vzdálený server vrátil chybu` | Jste v PowerShellu, kde `curl` není curl, ale zkratka pro `Invoke-WebRequest`. Přejděte do Git Bash (krok 2). Když ho nemáte, pište všude `curl.exe` místo `curl`. |
| `Author identity unknown` / `Please tell me who you are` | Git neví, kdo jste. Nastavte `user.name` a `user.email`, viz krok 7. |
| `bash: ./tools/encrypt_me.sh: No such file or directory` | Jste v jiném adresáři. Přejděte do `lab01-onboarding` (z `server/` je to `cd ..`). |
| Místo Pythonu se otevře Microsoft Store | Python na tomto počítači není. Zkuste `py --version`; když ani ten nefunguje, nainstalujte Python z [python.org](https://www.python.org/downloads/) (zaškrtněte *Add python.exe to PATH*) a otevřete terminál znovu. |
| Server spadne na `TypeError: 'type' object is not subscriptable` | Máte Python starší než 3.9. Aktualizujte ho z [python.org](https://www.python.org/downloads/), nebo jděte cestou A (Docker). |
| `docker` hlásí `dockerDesktopLinuxEngine: The system cannot find the file specified` | Docker Desktop neběží. Spusťte ho, počkejte, až bude hlásit *Engine running*, a zkuste to znovu — nebo jděte cestou B. |

## Další cvičení

Kdo na cvičení nebyl, dodělejte prosím tento úkol z domova do 27. 9.

Jakmile se zaregistrují všichni (přes `roster/<github-alias>.json` soubory), rozdělíme Vás do
týmů. Poté každému týmu vytvoříme Git repozitář v rámci organizace tulwea26, v rámci něhož budete
během semestru pracovat na semestrální práci.
