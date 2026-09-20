# WEA 2026 — Webové aplikace

Repozitář předmětu **Webové aplikace (WEA)** na Fakultě mechatroniky, informatiky
a mezioborových studií Technické univerzity v Liberci.

Najdete tu zadání cvičení, startovací kód a ukázky. Projekt vašeho týmu bude žít ve vlastním
repozitáři.

## Cvičení

| | Cvičení | Témata |
| --- | --- | --- |
| 01 | **[Seznámení s HTTP a Gitem](./lab01-onboarding/README.md)** | fork/PR workflow, review, CI, anatomie HTTP, asymetrické šifrování |

## Semestrální projekt

Ve tříčlenných týmech postavíte **aplikaci s konfigurovatelnými dashboardy**: uživatel si
skládá dashboard z widgetů, které tahají data z cizích API — počasí, kurzy měn, informace
o zemích, zprávy přes MQTT — za přihlášením. Představte si hlavní stránku [Seznam.cz](https://seznam.cz).

Zákazník (cvičící) je k dispozici každý týden a zadání záměrně přichází po částech, Vaším úkolem je
se aktivně doptat na detaily.

> Příklad: „Implementujte komentáře" neříká, kdo je může přidávat, jestli jdou editovat ani jestli
> se dá odpovídat. Zadání, které je nejasné, od vás očekává, že se zeptáte.

Akceptační kritéria hotového produktu:

- Fungují všechny požadované funkce.
- Tři dny stability na produkčním serveru bez kritické chyby.
- Česká a anglická lokalizace.
- Struktura kódu podle MVC (Model-View-Controller) architektury.
- Kvalita kódu dohodnutá se zákazníkem, podložená nástrojem na statickou analýzu.
- Rovnoměrné rozložení práce, jak mezi členy týmu, tak v průběhu semestru.

## Co potřebujete

- Git a účet na [GitHubu](https://github.com/signup)
  - Ideálně i [GitHub Education](https://github.com/education/students) - odblokuje přístup k pokročilým funkcním GitHub a ke Copilotu
- Terminál s `curl`
- [Docker](https://www.docker.com/get-started/) s Docker Compose — na vlastním počítači; kde není, poslouží [Python 3.9+](https://www.python.org/downloads/)

## Pravidla

- Pracujte na větvi, otevřete pull request, nechte si ho zkontrolovat. Pokaždé.
- Nikdy necommitujte tajemství — API klíče, hesla, soukromé klíče, `.env` soubory. Několik
  cvičení vám dá do ruky skutečné přihlašovací údaje; patří do konfigurace, kterou git
  nesleduje.
- Kód, komentáře v kódu a commit messages píšeme ideálně **anglicky**. Zadání a instrukce jsou česky.
