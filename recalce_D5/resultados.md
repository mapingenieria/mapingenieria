# Recalce de D5: comparación preliminar de alternativas (A, A2, B, C)

**Estado: modelo de comparación, NO es diseño.** Cargas, secciones de vigas, ks del suelo y posición del foso son supuestos de trabajo. Sirve para ver tendencias entre alternativas y para saber qué datos reales cambian la decisión.

## Alternativas modeladas

| Clave | Descripción (supuestos geométricos) |
|---|---|
| Base | Z1 original 1,80 × 1,80 m en los 8 apoyos, cara exterior al ras del lindero (e = 0,75 m) |
| A | D5 sobre zapata nueva profunda de 1,80 × 1,80 m en la **grava** (ks = 25 000 kN/m³, sin datos del estudio) |
| A2 | D5 sobre cajón del foso integrado: losa-zapata de 2,10 × 2,90 m en arcilla, adosada al lindero y centrada en el eje 5 |
| B | D5 sobre zapata angosta y larga de 1,20 × 3,00 m a lo largo del lindero (e = 0,45 m) |
| C | D5 sin zapata propia, colgada de la viga de lindero (0,40 × 1,20 m) entre D3 y D6; D3 y D6 ampliadas a 2,20 × 2,20 m |
| T0 | Etapa de transición: D5 sin zapata y vigas actuales (¿cuánto puede tomar la parrilla existente?) |

## Modelo

- Parrilla de vigas (flexión + torsión) sobre resortes Winkler bajo cada zapata. Cada zapata se une rígidamente a la columna, con la excentricidad incluida.
- Zapatas sin tracciones: la zona de contacto se reduce de forma iterativa.
- Resorte rotacional de la columna 0,30 × 1,00 m sobre el nodo, como restricción mínima de la superestructura (eje débil, h = 3,0 m).
- Solo cargas gravitacionales de servicio. **No incluye sismo.**
- Vigas: VC.S‑55×40 interpretada como 0,40 × 0,55 m; la viga central VC.S‑6 (0,35 × 0,45 m) y las vigas de lindero (0,40 × 0,55 m) son supuestos. Concreto de 21 MPa, EI al 50 % por fisuración.
- Suelo de arcilla: ks = 60 000 kN/m³ (de E = 10 000 t/m², ν = 0,35, B = 1,8 m) y q_adm = 323,65 kPa (estudio de suelos).
- Pruebas: voladizo, torsión, zapata centrada y equilibrio de reacciones (`test_modelo.py`).

## Actualización: Z1 = 2,0 × 2,0 m y foso según la planta de segundo nivel

**Esta sección reemplaza a las posteriores donde haya diferencias.** Las corridas anteriores usaron Z1 de 1,8 × 1,8 m y el foso con su lado de 1,70 m hacia el interior; ambos supuestos estaban mal. Script: `correr_foso_real.py`; esquema: `esquema_supuestos.png`.

**Lectura de la planta de segundo nivel:** el hueco del ascensor (recuadro con X, 2,46–2,56 × 1,70 m, casi igual al pozo de 1,70 × 2,50 m del proveedor) queda pegado al lindero D, justo al sur de D5. Se extiende 2,50 m hacia el interior y 1,70 m a lo largo del lindero. Con muros de 0,20 m la huella exterior es 2,90 × 2,10 m. **Falta confirmar y0:** la distancia entre el eje de D5 y el borde norte del foso. Barrí 0,0 / 0,5 / 1,0 m.

Con Z1 de 2,0 m, la excentricidad respecto a la columna es 0,85 m. P_D5 = 85 t.

### Presión máxima bajo D5 / q_adm (restricción ×1 / ×3 / ×10), y0 = 0,5 m

| Alternativa | ×1 | ×3 | ×10 | Vecinas ×1 |
|---|---|---|---|---|
| V0, Z1 2 × 2 original | 1,85 | 1,47 | 1,07 | 1,85 |
| R, recorte y prolongación al norte (2,0 × 2,0) | 2,39 | 1,96 | 1,57 | 1,84 |
| Rc, solo recorte | 2,52 | 2,04 | 1,59 | 1,84 |
| S, corrida 0,9 m hacia el norte | 2,48 | 2,26 | 2,11 | 1,82 |
| A, zapata 2 × 2 profunda en grava | 431 kPa | 343 kPa | 265 kPa | 2,07 |
| A2, zapata recortada + cajón del foso | 1,91 | 1,54 | 1,17 | 1,91 |

La zapata en grava (A) no tiene q_adm de referencia. Sube las vecinas hasta 2,07 / 1,62 / 1,19 veces q_adm.

Sensibilidad a y0:
- **y0 = 0,0:** R sube a 2,84 / 2,36 / 1,96, Rc a 3,30 / 2,68 / 2,15, S a 2,96 / 2,70 / 2,53. A2 se mantiene en 1,89 / 1,53 / 1,16.
- **y0 = 1,0:** no hay interferencia en planta. R y Rc dan lo mismo que V0 (1,85 / 1,48 / 1,11), S queda en 2,02 / 1,83 / 1,70 y A2 en 1,91 / 1,54 / 1,17.

### Lectura
1. **Con Z1 de 2 × 2 m el problema es menor,** pero V0 sigue por encima de q_adm: 1,85 con restricción ×1, 1,47 con ×3 y 1,07 con ×10. La restricción al giro sigue siendo la incógnita dominante.
2. **La interferencia en planta es parcial:** solo entre 0 y 1,0 m del borde sur de la zapata (según y0).
3. **Recortar y desplazar la zapata hacia el norte empeora.** Saca el centroide del eje de la columna: la columna queda en el borde sur y aumenta la excentricidad en y, con torsión en la viga de lindero. La corrida angosta hacia el norte falla por lo mismo. **La zapata debe quedar centrada bajo la columna.**
4. **A2 (zapata recortada + cajón del foso integrado)** rinde como la original, sin importar y0 (1,89–1,91 con ×1). Compensa el recorte y evita bajar a la grava, siempre que la base del cajón quede en arcilla; eso depende de la cota del sótano.
5. **A (profunda en grava)** carga más a las vecinas (+12 %) y depende de datos de la grava que no existen.
6. **Pendiente:** y0, la cota del sótano, el cuadro de elementos de las vigas y la restricción al giro real.

## Actualización con P_D5 = 85 t (carga medida)

Se toma 85 t ≈ 834 kN como carga **de servicio**. Si es mayorada, hay que reescalar. Las vecinas se cargan con el mismo reparto tributario (supuesto), así que también están cerca de 80 t. Script: `correr_85t.py`; figura: `comparacion_85t.png`.

**La incógnita que domina el resultado es cuánto giro restringen las vigas y la superestructura en el nodo de D5.** Se barre con multiplicadores ×1, ×3 y ×10 sobre un resorte base de 4EI/h de la columna 0,30 m.

### Resultado principal

La zapata original no pasa en este modelo. Con 85 t, la presión máxima bajo D5 es:

| Restricción rotacional | ×1 | ×3 | ×10 |
|---|---|---|---|
| Z1 original, p_máx / q_adm | 2,00 | 1,58 | 1,18 |

Para llegar a q_adm hace falta una restricción de ×28. Incluso con presión uniforme (sin excentricidad) serían 257 kPa = 0,80 q_adm.

**Ampliar la zapata hacia el interior no ayuda.** El ancho de contacto lo fija el equilibrio del momento (la columna está al ras del lindero), no el tamaño de la zapata. Lo que sí ayuda es **estrecharla y alargarla a lo largo del lindero**, porque baja la excentricidad y el momento que hay que equilibrar.

### Alternativas con 85 t (p_máx bajo D5 / q_adm; M_exc = R·e en kN·m)

| Alternativa | ×1 | ×3 | ×10 | M_exc (kN·m) |
|---|---|---|---|---|
| Base (Z1 1,8 × 1,8) | 2,00 | 1,58 | 1,18 | 550–660 |
| A, zapata profunda en grava | 1,43 | 1,15 | 0,93 | ≈ 610 |
| A2, cajón 2,1 × 2,9 | 1,46 | 1,15 | 0,84 | 480–810 |
| B, 1,2 × 3,0 | 1,43 | 1,15 | 0,93 | ≈ 400 |
| Corrida 0,9 × 5,0 | 1,00 | 0,83 | 0,70 | ≈ 270 |
| Corrida 0,6 × 5,0 | 1,12 | 1,02 | 0,96 | ≈ 133 |
| C, colgada de la viga de lindero | vecinas 3,40 | 2,83 | 2,23 | n/a |
| T0, D5 sin zapata | vecinas 4,44 | 3,69 | 3,08 | n/a |

- **A** además sube las vecinas hasta 2,24 / 1,76 / 1,33 y deja asentamientos diferenciales de 7 mm.
- **C y T0** siguen sin ser viables: sobrecargan las vecinas y la viga de lindero.
- **A2 depende de la restricción.** Su excentricidad es la mayor (0,90 m) y su momento crece con la restricción. Si el cajón no entrega rigidez real, rinde apenas como B.
- **La corrida de 0,9 × 5,0 m** es la mejor en presión y en momento, pero ocupa unos 5 m de lindero (D3 y D6 quedan a unos 1 m de su borde) y no sé si libra el foso.

### Qué significa
1. **Cómo se equilibró el momento en el diseño original** pasa a ser la pregunta clave. M = R·e ≈ 550–660 kN·m por apoyo. La viga VC.S‑55×40 interpretada como 0,40 × 0,55 m tiene un φMn indicativo de ≈ 320 kN·m.
2. **Un límite de presión mayor sí es una opción.** Con Fs = 5,27, q_ult ≈ 1 700 kPa. Una presión de borde de 2 × q_adm mantiene un factor local cercano a 2,6 (sin descontar el ancho efectivo). Eso lo debe dictaminar el geotecnista.
3. **Hay que pedir** el cuadro de elementos (Z1, vigas) y las cargas reales de D3, D6 y A5.

## Corrida angosta con el foso adosado al lindero (P_D5 = 85 t)

Script: `correr_corrida_foso.py`; figura: `comparacion_corrida_foso.png`.

**Geometría supuesta (a confirmar):**
- Foso adosado al lindero D, caja libre de 1,70 × 2,50 m más muros de 0,20 m: huella de 2,10 (x) × 2,90 m (a lo largo del lindero), centrada en el eje 5.
- Donde la corrida pasa bajo la huella del foso debe ir **más profunda que la placa del foso** (base entre −2,4 y −2,55 m bajo el piso del sótano, en la grava, ks = 25 000 kN/m³ supuesto).
- Fuera de la huella queda al nivel original, en arcilla.
- Por eso se modela **escalonada**: un tramo profundo de 2,90 m con ks de grava y tramos someros de arcilla a los lados.

### Resultado (p_máx en los tramos de arcilla / q_adm)

| Caso | ×1 | ×3 | ×10 | M_exc (kN·m) |
|---|---|---|---|---|
| Corrida 0,9 × 5,0 escalonada, foso centrado | 1,34 | 1,14 | 1,00 | ≈ 265 |
| Corrida 0,9 × 4,0 escalonada | 1,76 | 1,53 | 1,38 | ≈ 260 |
| Corrida 0,6 × 5,0 escalonada | 1,58 | 1,46 | 1,38 | ≈ 130 |
| Corrida 0,9 × 5,0, foso desplazado +1,0 m | 1,82 | 1,63 | 1,50 | ≈ 265 |
| Corrida 0,9 × 5,0, foso desplazado −1,0 m | 1,94 | 1,72 | 1,58 | ≈ 265 |
| Referencia: toda en arcilla (sin foso) | 1,00 | 0,83 | 0,70 | ≈ 270 |
| Para comparar: Base / B / A2 | 2,00 / 1,43 / 1,46 | 1,58 / 1,15 / 1,15 | 1,18 / 0,93 / 0,84 | 550–660 / 400 / 480–810 |

La presión en el tramo de grava queda entre 130 y 260 kPa. **No hay q_adm de la grava**, así que no puedo decir si pasa.

### Sensibilidad
- **Rigidez de la grava (corrida 0,9 × 5,0, foso centrado).** Con ks = 15 000 la grava toma solo el 26 % de la carga y los tramos de arcilla suben a 1,51 / 1,29 / 1,15. Con ks = 25 000 toma el 37 %. Con grava tan rígida como la arcilla (ks = 60 000) se recupera la referencia sin foso: 1,00 / 0,83 / 0,70.
- **Largo total (restricción ×1 / ×3 / ×10, ancho 0,9 m).**

| Largo | ×1 | ×3 | ×10 |
|---|---|---|---|
| 5,0 m | 1,34 | 1,14 | 1,00 |
| 6,0 m | 1,10 | 0,92 | 0,79 |
| 7,0 m | 0,94 | 0,78 | 0,66 |

Con 7,0 m la corrida llega al borde de las zapatas de D3 y D6, o sea que queda como una corrida de lindero continua. Con ancho de 1,2 m la mejora es pequeña (0,84 contra 1,00 con restricción ×10, a 5,0 m de largo).

### Lectura
1. **Con el foso adosado, la ventaja de la corrida angosta se reduce mucho.** Sigue siendo mejor que la zapata original (2,00 / 1,58 / 1,18), pero queda en el mismo orden que B y A2 en presión.
2. **Lo que mantiene su ventaja es el momento de excentricidad.** M_exc ≈ 265 kN·m contra 400–810 en B y A2, así que depende bastante menos de la restricción al giro, que es la incógnita dominante.
3. **La grava blanda descarga el tramo profundo.** Aunque la columna está sobre él, toma solo 26 a 37 % de la carga, y el resto lo toman los tramos someros de arcilla. Por eso importa mucho la rigidez de la grava y la ubicación del foso respecto a la columna.
4. **Para cumplir q_adm con restricción ×1** la corrida tendría que alargarse a unos 7 m, hasta unirse con D3 y D6.
5. **La excavación en grava suelta junto al lindero sigue siendo el riesgo constructivo.**

Limitaciones: la posición y las dimensiones del foso son supuestas. No se modelan la unión del escalón, la interacción de los muros y la placa del foso con la corrida, ni el apoyo lateral. Las vecinas siguen en su presión original porque dependen de cargas que no tengo.

## Hallazgo previo: calibración del caso base

Con mi carga supuesta (6 000 kN, P_D5 ≈ 876 kN) el caso base no pasa: la presión máxima llega a 2,1 × q_adm. En este modelo, las zapatas excéntricas de lindero alcanzan q_adm con **P_D5 ≈ 406 kN (≈ 41 t)**. Con restricción rotacional total serían ≈ 107 t (33 t/m² × 3,24 m²).

Es decir, la capacidad real del sistema depende del giro que restrinjan las vigas y la superestructura. **Hace falta la carga real de D5 de sus modelos parciales.** Todo lo que sigue se evalúa con la carga que lleva Z1 original justo a q_adm, así que compara contra el original y no da valores absolutos.

## Resultados a carga calibrada (W = 2 782 kN)

| Caso | D5 p_máx (kPa) | Contacto D5 | Vecinas p_máx (kPa) | Δ asent. (mm) | M viga lindero (kN·m) |
|---|---|---|---|---|---|
| Base | 324 | 89 % | 324 | 1,1 | 18 |
| A (grava) | 234 | 100 % | 363 (D3) | 3,6 | 46 |
| A2 | 234 | 68 % | 324 | 1,1 | 23 |
| B | 229 | 100 % | 324 | 1,1 | 24 |
| C | n/a | n/a | 573 (D3), 482 (D6) | 2,1 | 761 (≈ 44 % de φMn indicativo de 0,40 × 1,20) |
| T0 | n/a | n/a | 729 (D3), 681 (D6) | 2,5 | 460 (indicativo 0,40 × 0,55: ≈ 320) |

q_adm de arcilla = 323,65 kPa. Para A no hay q_adm de la grava.

## Sensibilidad (27 combinaciones de ks arcilla × ks grava × fisuración)

- **A2 y B** reducen la presión máxima bajo D5 entre un **22 y 31 %** respecto al original (A2: 0,70–0,75; B: 0,69–0,78) y no cargan a las vecinas. Es un resultado robusto.
- **A** depende totalmente de la grava: la presión bajo D5 va de 0,43 a 1,30 veces la del original, y las vecinas suben hasta un 40 %, con asentamientos diferenciales de hasta 7 mm. Está sujeta a la incógnita geotécnica.
- **C** sobrecarga a D3 y D6 (1,5 a 2,0 veces) aun con zapatas ampliadas. No es viable como está planteada.
- **T0:** al quitar la zapata de D5, las vecinas llegan a 2 a 2,5 veces su presión y la viga de lindero actual se pasa del momento indicativo. **La parrilla existente no sustituye a D5**, así que se necesita apuntalamiento propio y transferencia de carga.

## Lectura

1. A2 y B son las que mejor se comportan con la menor incertidumbre. Dependen de datos que no tengo: la cota del sótano y la posición real del foso.
2. A queda en suspenso hasta que el geotecnista dé parámetros de la grava.
3. C no funciona sin ampliar mucho D3 y D6, y T0 muestra que la parrilla no basta durante la transferencia.
4. B tiene contacto completo (e = 0,45 m). A2 pierde contacto (68 %) por su e = 0,90 m, así que está más expuesta a la rigidez real del cajón. La rigidez de los muros, que este modelo no captura, sería la que decide.

## Limitaciones

- Sin sismo y sin rigidez real de la superestructura (muros confinados, diafragmas).
- Cargas calibradas, no reales. Secciones, ks de grava y posición del foso supuestos.
- Zapatas rígidas. No se verifican punzonamiento, pedestal, refuerzo ni la geometría exacta del foso.
- Contacto sin tracciones en una sola dirección (x).
- La interacción muro-placa del cajón de A2 no se modela.

## Datos que más cambian la respuesta

1. P real de D5 y vecinas (de los modelos de diagnóstico) y sismo.
2. Cuadro de elementos: dimensiones reales de Z1 y vigas, y refuerzo.
3. Cota del sótano respecto al terreno y posición del foso.
4. Parámetros de la grava (c, φ, E) del geotecnista.

## Reproducir

```
cd recalce_D5
PYTHONPATH=. python3 test_modelo.py
PYTHONPATH=. python3 modelo_parrilla.py     # carga calibrada -> resultados.json
PYTHONPATH=. python3 generar_informe.py     # comparacion.png
PYTHONPATH=. python3 correr_85t.py          # P_D5 = 85 t -> resultados_85t.json, comparacion_85t.png
PYTHONPATH=. python3 correr_corrida_foso.py # corrida angosta con foso adosado (supuestos antiguos) -> resultados_corrida_foso.json
PYTHONPATH=. python3 correr_foso_real.py    # Z1 2x2 y foso segun planta de 2.o nivel -> resultados_foso_real.json
```
