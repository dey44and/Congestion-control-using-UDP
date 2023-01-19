# Implementarea unui mecanism de control al congestiei. Aplicație demonstrativă

Congestia unei rețele este o stare care apare atunci când traficul este atât de încărcat încât încetinește timpul de răspuns al rețelei. Cu alte cuvinte, prin rețea circulă mai multe date decât ar trebui.
Efectele acesteia sunt: întârzierile, pierderea pachetelor sau blocarea noilor conexiuni.
Controlul congestiei este un mecanism prin care se evită apariția acesteia.

## Protocolul UDP

UDP (User Datagram Protocol) este un protocol ce trimite pachete independente de date, numite datagrame, de la un calculator către altul, fără a garanta în vreun fel ajungerea acestora la destinație. <br/><br/>
Este un serviciu neorientat conexiune: nu se stabilește o conexiune între client și server. Așadar, server-ul nu așteaptă apeluri de conexiune, ci primește direct datagrame de la clienți. <br/><br/>
Este întâlnit în sistemele client-server în care se transmit puține mesaje și în general prea rar pentru a menține o conexiune activă între cele două entități. <br/><br/>
Nu se garantează ordinea primirii mesajelor și nici prevenirea pierderilor pachetelor. UDP-ul se utilizează mai ales în rețelele în care există o pierdere foarte mică de pachete și în cadrul aplicațiilor pentru care pierderea unui pachet nu este foarte gravă (ex. Aplicațiile de streaming video). <br/>

## Gestionarea congestiei

Protocolul UDP este orientat pe trimiterea pachetelor și nu este orientat pe conexiune, așa cum se întâmplă în cazul protocolului TCP.<br/></br>
În cadrul protocolului TCP, există o serie de algoritmi care tratează apariția congestiei. Printre aceștia, amintim: Tahoe, Reno, New Reno și Vegas.<br></br>
Aplicația va implementa funcționalitatea algoritmului _Tahoe_ pentru transmisia pachetelor folosind UDP într-o arhitectură de tip **client-server**.

## Configurarea server-ului

Configurarea unui server se realizează prin specificarea adresei IP și a portului sursă. Acestea trebuie să fie cunoscute și de clientul ce dorește să se conecteze.

## Stabilirea conexiunii către server

1. Conexiunea se realizează prin specificarea adresei IP, a portului sursă (client) și a portului destinație (server).
2. După stabilirea parametrilor de comunicare, se va realiza conectarea la baza de date și validarea utilizatorului ce dorește să folosească interfața.
3. Apoi, interfața devine activă iar utilizatorul poate trimite și recepționa pachete de la server.

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

## Structura pachetelor prin care se va realiza comunicarea

Pentru pachetul ce va cere __afișarea fișierelor__ sau __deconectarea de la server__, structura este:

| COD_INSTRUCȚIUNE | COD_COMANDĂ |
|------------------|-------------|
| 8 BIȚI           | 8 BIȚI      |

Pentru pachetul ce va cere __adăugarea unui fișier__ sau __ștergerea unui fișier__, structura este:

| COD_INSTRUCȚIUNE | COD_COMANDĂ | NUME_FIȘIER |
|------------------|-------------|-------------|
| 8 BIȚI           | 8 BIȚI      | x BIȚI      |

Pentru pachetul ce va realiza __adăugarea de conținut__, __descărcarea unui fișier__ sau __încărcarea unui fișier__, structura este:

| COD_INSTRUCȚIUNE  | COD_COMANDĂ | NUMĂR_PACHET  | LUNGIME_FIȘIER | NUME_FIȘIER | CONȚINUT_PACHET |
|-------------------|-------------|---------------|----------------|-------------|-----------------|
| 8 BIȚI            | 8 BIȚI      | 8 BIȚI        | 8 BIȚI         | x BIȚI      | 1 - 512 BIȚI    |