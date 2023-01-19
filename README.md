# Implementarea unui mecanism de control al congestiei. Aplicație demonstrativă

Congestia unei rețele este o stare care apare atunci când traficul este atât de încărcat încât încetinește timpul de răspuns al rețelei. Cu alte cuvinte, prin rețea circulă mai multe date decât ar trebui.
Efectele acesteia sunt: întârzierile, pierderea pachetelor sau blocarea noilor conexiuni.
Controlul congestiei este un mecanism prin care se evită apariția acesteia.

## Formatul pachetelor ce vor fi trimise

Pentru început, orice pachet va fi format din 8 biți în care se va stoca tipul controlului dorit.

| Tip control | Cod |
|-------------|-----|
| CONNECTION  | 0   |
| INSTRUCTION | 1   |
| RESPONSE    | 2   |

Pe următorii 8 biți, se va salva tipul comenzii ce se dorește a fi executată, în cadrul pachetului tip INSTRUCTION sau care a fost executată, în cadrul pachetului de tip RESPONSE.

| Nume comandă  | Cod |
|---------------|-----|
| LIST_FILES    | 0   |
| CREATE_FILE   | 1   |
| APPEND_FILE   | 2   |
| REMOVE_FILE   | 3   |
| MOVE_FILE     | 4   |
| DOWNLOAD_FILE | 5   |
| UPLOAD_FILE   | 6   |

Dacă pachetul este de tio CONNECTION, octetul va conține următoarele tipuri de notificări:

| Nume Notificare | Cod |
|-----------------|-----|
| SYN             | 0   |
| ACK             | 1   |
| LEAVE           | 2   |