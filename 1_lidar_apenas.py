from rplidar import RPLidar
import matplotlib.pyplot as plt
import keyboard as kb
import numpy as np

if __name__ == '__main__':

    comLidar1 = 'COM4'

    limMinDistancia = 0  # mm
    limMaxDistancia = 400

    limMinAngulo = 90  # graus
    limMaxAngulo = 270

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, dpi=200)
    ax.set_ylim(0, limMaxDistancia)

    # Inicializa as linhas do gráfico para dois LIDARs
    line, = ax.plot([], [], 'r.', markersize=0.5, label='LIDAR 1')

    # Inicialização do RPLidar
    lidar1 = RPLidar(comLidar1)

    info1 = lidar1.get_info()
    print('LIDAR 1 Info:', info1)

    health1 = lidar1.get_health()
    print('LIDAR 1 Health:', health1)

    lidar1.clean_input()  # limpa buffer do lidar

    # Coleta e plota os dados
    for scan in lidar1.iter_scans():
        angles, distances = [], []

        for c in range(len(scan)):
            distancia = scan[c][2]
            angulo = scan[c][1]

            if limMinDistancia <= distancia <= limMaxDistancia:
                if limMinAngulo <= angulo <= limMaxAngulo:
                    angles.append(np.deg2rad(angulo))
                    distances.append(distancia)

        line.set_data(angles, distances)
        ax.relim()
        ax.autoscale_view()

        plt.draw()
        plt.pause(0.01)  # Pausa para permitir a atualização visual

        if not plt.fignum_exists(''):
            break

    lidar1.stop()
    lidar1.stop_motor()
    lidar1.disconnect()