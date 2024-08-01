from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np

# Criação de uma nova figura e configuração da resolução
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, dpi=200)
ax.set_ylim(0, 600)

def on_key(event):
    if event.key.lower() == 'c':  # 'c' ou 'C' para fechar
        plt.close(fig)  # Fecha a janela do gráfico
        lidar1.stop()
        lidar1.stop_motor()
        lidar1.disconnect()
        lidar2.stop()
        lidar2.stop_motor()
        lidar2.disconnect()

fig.canvas.mpl_connect('key_press_event', on_key)

# Inicialização dos RPLidars
lidar1 = RPLidar('COM9')
lidar2 = RPLidar('COM10')  # Assumindo que o segundo LIDAR está na COM10

info1 = lidar1.get_info()
info2 = lidar2.get_info()
print('LIDAR 1 Info:', info1)
print('LIDAR 2 Info:', info2)

health1 = lidar1.get_health()
health2 = lidar2.get_health()
print('LIDAR 1 Health:', health1)
print('LIDAR 2 Health:', health2)

# Inicializa as linhas do gráfico para dois LIDARs
line1, = ax.plot([], [], 'r.', markersize=0.5, label='LIDAR 1')
line2, = ax.plot([], [], 'b.', markersize=0.5, label='LIDAR 2')

def update_plot(scan1, scan2):
    angles1 = [np.deg2rad(measure[1]) for measure in scan1 if (measure[2] < 400 and (measure[1] < 90 or measure[1] > 270))]
    distances1 = [measure[2] for measure in scan1 if (measure[2] < 400 and (measure[1] < 90 or measure[1] > 270))]
    angles2 = [np.deg2rad(measure[1]) for measure in scan2 if (measure[2] < 400 and (measure[1] < 90 or measure[1] > 270))]
    distances2 = [measure[2] for measure in scan2 if (measure[2] < 400 and (measure[1] < 90 or measure[1] > 270))]

    line1.set_data(angles1, distances1)
    line2.set_data(angles2, distances2)
    ax.relim()
    ax.autoscale_view()

# Coleta e plota os dados
for i, (scan1, scan2) in enumerate(zip(lidar1.iter_scans(scan_type='express', max_buf_meas=30000, min_len=3),
                                        lidar2.iter_scans(scan_type='express', max_buf_meas=30000, min_len=3))):
    update_plot(scan1, scan2)
    plt.draw()
    plt.pause(0.01)  # Pausa para permitir a atualização visual

    # for c in range(len(scan1)):
    #     if scan1[c][2] < 300:
    #         print(f'LIDAR 1 - {c}: {scan1[c]}')
    # for c in range(len(scan2)):
    #     if scan2[c][2] < 300:
    #         print(f'LIDAR 2 - {c}: {scan2[c]}')
    # print()

    # Saia do loop após um número de iterações
    # if i > 50:
    #     break

# Exibe o gráfico
plt.legend()
plt.show()

# Para os LIDARs após fechar o gráfico
lidar1.stop()
lidar1.stop_motor()
lidar1.disconnect()
lidar2.stop()
lidar2.stop_motor()
lidar2.disconnect()
