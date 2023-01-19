# Implementarea unui mecanism de control al congestiei. Aplicație demonstrativă

Congestia unei rețele este o stare care apare atunci când traficul este atât de încărcat încât încetinește timpul de răspuns al rețelei. Cu alte cuvinte, prin rețea circulă mai multe date decât ar trebui.
Efectele acesteia sunt: întârzierile, pierderea pachetelor sau blocarea noilor conexiuni.
Controlul congestiei este un mecanism prin care se evită apariția acesteia.

## Stabilirea conexiunii către server

1. Conexiunea se realizează prin specificarea adresei IP, a portului sursă (client) și a portului destinație (server).
2. După stabilirea parametrilor de comunicare, se va realiza conectarea la baza de date și validarea utilizatorului ce dorește să folosească interfața.
3. Apoi, interfața devine activă iar utilizatorul poate trimite și recepționa pachete de la server.

## Configurarea server-ului

Configurarea unui server se realizează prin specificarea adresei IP și a portului sursă. Acestea trebuie să fie cunoscute și de clientul ce dorește să se conecteze.

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

Dacă pachetul este de tip CONNECTION, octetul va conține următoarele tipuri de notificări:

| Nume notificare | Cod |
|-----------------|-----|
| SYN             | 0   |
| ACK             | 1   |
| LEAVE           | 2   |