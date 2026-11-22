from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DURACION = 480
REPLICAS = 30
TIPOS = ['Rapido', 'Normal', 'Lento', 'Muy lento']
PROB = {'Retiro': [0.23, 0.40, 0.17, 0.20],
        'Pago': [0.10, 0.20, 0.30, 0.40]}
SERVICIO = {'Retiro': [1, 2, 3, 4], 'Pago': [3, 3, 5, 7]}
LLEGADA = {'Retiro': [1, 2, 3, 3], 'Pago': [1, 2, 3, 4]}
ESCENARIOS = {'A_1R_2P': ['Retiro', 'Pago', 'Pago'],
              'B_2R_1P': ['Retiro', 'Retiro', 'Pago'],
              'C_2R_2P': ['Retiro', 'Retiro', 'Pago', 'Pago']}
SALIDA = Path(__file__).resolve().parent / 'resultados'
SALIDA.mkdir(exist_ok=True)

# Supuesto explicito: una corriente global de llegadas, con tiempo
# entre llegadas exponencial cuya media depende del usuario anterior.
# Esto NO es un proceso Poisson homogeneo ni un M/M/1 estricto.
def generar_clientes(semilla):
    rng = np.random.default_rng(semilla)
    clientes = []
    t = 0.0
    while True:
        accion = rng.choice(['Retiro', 'Pago'], p=[0.70, 0.30])
        tipo = int(rng.choice(4, p=PROB[accion]))
        t += rng.exponential(LLEGADA[accion][tipo])
        if t >= DURACION:
            break
        servicio = rng.exponential(SERVICIO[accion][tipo])
        clientes.append((t, accion, tipo, servicio))
    return clientes


def simular(clientes, cajas, escenario, replica):
    libres = np.zeros(len(cajas))
    registros = []
    for llegada, accion, tipo, servicio in clientes:
        elegibles = [i for i, especialidad in enumerate(cajas)
                     if especialidad == accion]
        cajero = min(elegibles, key=lambda i: libres[i])
        inicio = max(llegada, libres[cajero])
        fin = inicio + servicio
        libres[cajero] = fin
        registros.append({'Escenario': escenario, 'Replica': replica,
                          'Cajero': cajero + 1, 'Accion': accion,
                          'Tipo': TIPOS[tipo], 'Llegada': llegada,
                          'Servicio': servicio, 'Espera': inicio - llegada,
                          'Inicio': inicio, 'Salida': fin,
                          'Atendido_antes_cierre': fin <= DURACION})
    return registros


def main():
    datos = []
    for replica in range(1, REPLICAS + 1):
        clientes = generar_clientes(20261122 + replica)
        for escenario, cajas in ESCENARIOS.items():
            datos.extend(simular(clientes, cajas, escenario, replica))
    df = pd.DataFrame(datos)
    df.to_csv(SALIDA / 'detalle_clientes.csv', index=False, encoding='utf-8-sig')

    resumen = df.groupby(['Escenario', 'Replica']).agg(
        Llegadas=('Accion', 'size'),
        Atendidos_antes_cierre=('Atendido_antes_cierre', 'sum'),
        Espera_media=('Espera', 'mean'),
        Servicio_medio=('Servicio', 'mean'),
        Espera_maxima=('Espera', 'max')).reset_index()
    resumen['Pendientes_al_cierre'] = (resumen['Llegadas'] -
                                       resumen['Atendidos_antes_cierre'])
    cajeros = df.groupby(['Escenario', 'Cajero']).agg(
        Usuarios=('Cajero', 'size'),
        Servicio_medio=('Servicio', 'mean'),
        Espera_media=('Espera', 'mean')).reset_index()
    tipos = df.groupby(['Escenario', 'Replica', 'Accion', 'Tipo']).size().unstack(
        ['Accion', 'Tipo'], fill_value=0)
    tipos.columns = [f'{a}_{t}' for a, t in tipos.columns]
    tipos = tipos.reset_index()
    promedios_tipos = tipos.groupby('Escenario').mean(numeric_only=True)
    promedios_tipos = promedios_tipos.drop(columns='Replica', errors='ignore')
    comparacion = resumen.groupby('Escenario').agg(
        Llegadas_promedio=('Llegadas', 'mean'),
        Atendidos_promedio=('Atendidos_antes_cierre', 'mean'),
        Espera_promedio=('Espera_media', 'mean'),
        Espera_maxima_promedio=('Espera_maxima', 'mean'),
        Pendientes_promedio=('Pendientes_al_cierre', 'mean'))

    with pd.ExcelWriter(SALIDA / 'resultados_banco.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Detalle', index=False)
        resumen.to_excel(writer, sheet_name='Replicas', index=False)
        cajeros.to_excel(writer, sheet_name='Cajeros', index=False)
        tipos.to_excel(writer, sheet_name='Usuarios_por_tipo', index=False)
        promedios_tipos.to_excel(writer, sheet_name='Promedios_tipo')
        comparacion.to_excel(writer, sheet_name='Comparacion')

    ax = comparacion['Espera_promedio'].plot(kind='bar', figsize=(9, 5))
    ax.set_title('Tiempo medio de espera por escenario')
    ax.set_ylabel('Minutos')
    ax.set_xlabel('Configuracion de cajeros')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(SALIDA / 'comparacion_espera.png', dpi=160)
    plt.close()

    print('\nSIMULACION COMPLETADA - 30 REPLICAS POR ESCENARIO')
    print('\nCOMPARACION DE ESCENARIOS:')
    print(comparacion.round(2).to_string())
    print('\nPROMEDIOS POR CAJERO:')
    print(cajeros.round(2).to_string(index=False))
    print('\nArchivos guardados en:', SALIDA)
    print('\nNOTA: Los usuarios que llegan antes del cierre terminan su')
    print('servicio, aunque su salida ocurra despues del minuto 480.')


if __name__ == '__main__':
    main()
