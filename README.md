# BPC-IoT Projekt #11 OTA aktualizace skrze CIoT technologie

Cílem tohoto projektu je provést aktualizaci firmwaru přes CIoT technologie NB-IoT a LTE cat-M. Podle kvality signálu rozhodne zařízení o použité technologii pro zaslání firmwaru, který bude následně zaslán ze serveru. Po jeho doručení proběhne ověření integrity pomocí hashovacího algoritmu SHA256 a nakonec i samotná aktualizace firmwaru.


## Technické parametry přenosu

Základní komunikace zařízení a serveru: NB-IoT

Transportní protokol: UDP

Aplikační protokol: žádný

Pro základní komunikaci je vhodnější technologie NB-IoT zejména kvůli lepšímu pokrytí. Pro zasílání firmwaru může být naopak vhodnější technologie LTE cat-M, a to hlavně při vhodných rádiových podmínkách a větší velikosti přenášeného firmwaru. Protokol UDP byl zvolen primárně z důvodu jeho jednoduchosti a malého overheadu. Aplikační protokol jsme nepoužili žádný, museli jsme tedy definovat princip zasílání a strukturu zpráv a také rozdělení zasílaného firmwaru na bloky, ale ušetřili jsme tím overhead a celkově zjednodušili přenos.

## Princip funkce jednotlivých částí kódu
### Logika komunikace zařízení a serveru

Zařízení i server budou posílat několik typů zpráv, při přijetí zprávy bude z hlavičky vyčten její typ, délka a id. 

#### Zprávy odesílané serverem

- UPDATE_START
- NO_UPDATE
- DATA_BLOCK

#### Zprávy odesílané zařízením

- POLL
- ACK
- NACK

### Funkce zařízení

- Zařízení bude měřit teplotu a periodicky ji odesílat na server. Součást zprávy bude i aktuální verze firmwaru.
- Pokud zařízení přijme zprávu o nové dostupné verzi firmwaru, pošle serveru žádost o jeho zaslání.
- Po přijetí firmwaru provede kontrolní součet SHA256 a porovná ho se součtem vytvořeným serverem
- Provede aktualizaci. Úspěšná aktualizace bude signalizována změnou barvy blikající LED na zařízení

### Funkce serveru

- Bude přijímat zprávy o teplotě
- Porovná aktuální verzi firmwaru zařízení s nejnovější dostupnou verzí firmwaru
- Pokud se verze liší, pošle zařízení zprávu o nové dostupné verzi firmwaru
- Po přjietí žádosti zařízení o zaslání firmwaru odešle firmware a následně hodnotu jeho kontrolního součtu SHA256


