# BPC-IoT Projekt #11 OTA aktualizace skrze CIoT technologie

Cílem tohoto projektu je provést aktualizaci firmwaru přes CIoT technologie NB-IoT a LTE cat-M. Podle kvality signálu rozhodne zařízení o použité technologii pro zaslání firmwaru, který bude následně zaslán ze serveru. Po jeho doručení proběhne ověření integrity pomocí hashovacího algoritmu SHA256 a nakonec i samotná aktualizace firmwaru.

## Zvolené parametry přenosu

Základní komunikace zařízení a serveru: NB-IoT

Transportní protokol: UDP

Aplikační protokol: žádný

Pro základní komunikaci je vhodnější technologie NB-IoT zejména kvůli lepšímu pokrytí. Pro zasílání firmwaru může být naopak vhodnější technologie LTE cat-M, a to hlavně při vhodných rádiových podmínkách a větší velikosti přenášeného firmwaru. Protokol UDP byl zvolen primárně z důvodu jeho jednoduchosti a malého overheadu. Aplikační protokol jsme nepoužili žádný, museli jsme tedy definovat princip zasílání a strukturu zpráv a také rozdělení zasílaného firmwaru na bloky, ale ušetřili jsme tím overhead a celkově zjednodušili přenos.
