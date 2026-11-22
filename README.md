# Simulación bancaria — Actividad 2-M3

## Descripción

Simulación de un banco que opera durante 8 horas (480 minutos), con atención exclusiva para **retiros** y **pagos o consignaciones**. El objetivo es comparar la distribución de cajeros y evaluar el efecto de incorporar una cuarta caja.

El modelo considera que el **70 %** de los usuarios realiza retiros y el **30 %** realiza pagos o consignaciones. Para cada operación se distinguen cuatro tipos de usuarios: rápido, normal, lento y muy lento, con probabilidades y tiempos medios de llegada y servicio establecidos en el enunciado de la actividad.

## Escenarios evaluados

| Escenario | Cajeros de retiros | Cajeros de pagos | Total de cajeros |
|---|---:|---:|---:|
| `A_1R_2P` | 1 | 2 | 3 |
| `B_2R_1P` | 2 | 1 | 3 |
| `C_2R_2P` | 2 | 2 | 4 |

Se realizan **30 réplicas por escenario**, con semillas reproducibles. Los tres escenarios reciben el mismo conjunto de llegadas en cada réplica para facilitar la comparación.

## Requisitos

- Python 3.10 o posterior.
- Bibliotecas indicadas en `requirements.txt`.

Instalar dependencias desde una terminal situada en la carpeta del proyecto:

```bash
py -m pip install -r requirements.txt
```

En sistemas donde `py` no esté disponible, utilizar `python -m pip install -r requirements.txt`.

## Ejecución

```bash
py simulacion_bancaria.py
```

Alternativamente:

```bash
python simulacion_bancaria.py
```

El programa crea automáticamente la carpeta `resultados/` y genera los siguientes archivos:

| Archivo | Contenido |
|---|---|
| `resultados/resultados_banco.xlsx` | Libro con hojas `Detalle`, `Replicas`, `Cajeros`, `Usuarios_por_tipo`, `Promedios_tipo` y `Comparacion`. |
| `resultados/detalle_clientes.csv` | Datos de cada usuario simulado, su cajero, tiempos y condición al cierre. |
| `resultados/comparacion_espera.png` | Gráfica del tiempo medio de espera de los escenarios. |

## Resultados de referencia

Con las semillas definidas en el programa y las 30 réplicas, los tiempos medios de espera aproximados son:

| Escenario | Espera media (minutos) |
|---|---:|
| A: 1 retiro + 2 pagos | 5,81 |
| B: 2 retiros + 1 pago | 2,56 |
| C: 2 retiros + 2 pagos | 0,57 |

Entre las alternativas con **tres cajeros**, el escenario **B (2 retiros y 1 pago)** presenta el menor tiempo medio de espera. La cuarta caja reduce adicionalmente la espera, pero su conveniencia económica requeriría información de costos y metas de servicio.

## Supuestos y alcance del modelo

- El banco recibe llegadas durante 480 minutos. Los clientes que ingresan antes del cierre pueden terminar su atención después del minuto 480.
- Cada cajero atiende una sola persona a la vez y se dedica exclusivamente a una operación.
- Cuando existen varios cajeros elegibles, se asigna el que queda disponible más temprano.
- Los tiempos de servicio son exponenciales con medias que dependen de la operación y del tipo de usuario.
- **Precisión metodológica:** el código genera una corriente global de llegadas con intervalos exponenciales cuya media depende del tipo de usuario sorteado. Por ello, aunque modela cajeros individuales y colas, **no constituye un proceso de Poisson homogéneo ni un modelo M/M/1 estricto**. Esta limitación debe considerarse al interpretar los resultados.

## Organización sugerida del repositorio

```text
Simulacion-Bancaria-M3/
├── simulacion_bancaria.py
├── README.md
├── requirements.txt
└── resultados/
    ├── resultados_banco.xlsx
    ├── detalle_clientes.csv
    └── comparacion_espera.png
```

## Contexto académico

Actividad  2-M3 — Solución de un problema bancario. Simulación de escenarios de atención bancaria y análisis estadístico de réplicas.
