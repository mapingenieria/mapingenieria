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
python3 modelo_parrilla.py        # escribe resultados.json
python3 generar_informe.py        # escribe comparacion.png
```
