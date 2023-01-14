import serial
import matplotlib.pyplot as plt

def open_com(portname = '/dev/ttyACM0'): # функция открытия com порта, имя аргумента задано по умолчанию
    try:
        # com-порт, с которого считываются данные
        delay = 0.06 # с
        ser = serial.Serial(port = portname,baudrate = 9600,parity = serial.PARITY_NONE,
                            stopbits = serial.STOPBITS_ONE,bytesize = serial.EIGHTBITS,timeout = delay)
    except:
        ser = 'none'
    return ser

def serial_read(ser):# Чтение данных из com-порта в режиме ожидания данных
    if ser == 'none':
        print('COM-порт не подключен')
    else:
        ser.flushInput()
        ser.flushOutput()

        no_msg = 1

        while (no_msg != 0):
            while (ser.inWaiting() > 0):
                x = ser.readline()
                y = x.decode('utf-8')
                z = y.split(' ')

                if x and (len(z) == 10):
                    year  = int(z[0])
                    month = int(z[1])
                    day   = int(z[2])
                    hour  = int(z[3])
                    minut = int(z[4])
                    sec   = float(z[5])
                    temp1 = float(z[6])
                    temp2 = float(z[7])
                    temp3 = float(z[8])
                    hum   = float(z[9])

                    no_msg = 0
                    ser.flushInput()
                    ser.flushOutput()

                else:
                    continue

        # Возврат данных
        if (no_msg == 0):
            return year, month, day, hour, minut, sec, temp1, temp2, temp3, hum

def main(num = 1):
    count = 0
    if num == 1:
        ser = open_com('/dev/ttyACM0') # через кабель
    elif num == 2:
        ser = open_com('/dev/rfcomm0') # через bluetooth
    else:
        print('Выберите способ подключения метеостанции (1 - кабель, 2 - bluetooth)')

    if ((num == 1) or (num == 2)) and (ser != 'none'):
        tims  = []
        hums  = []
        temps = []
        plt.ion()
        while count <= 790:
            count += 1
            [year, month, day, hour, minut, sec, temp1, temp2, temp3, hum] = serial_read(ser)
            temperature_mean = round((temp1 + temp2 + temp3)/3,2)

            ## Вывод гарфика в режиме реального времени
            time_hour = hour + minut/60 + sec/(60*60)
            tims.append(time_hour)
            temps.append(temperature_mean)
            hums.append(hum)

            plt.clf()

            plt.subplot(2, 1, 1)
            plt.plot(tims, temps)
            plt.ylabel('град. Цельсия')
            plt.title('Температура')
            plt.subplot(2, 1, 2)
            plt.plot(tims, hums)
            plt.xlabel('Время,часы')
            plt.ylabel('%')
            plt.title('Влажность')

            plt.draw()
            plt.gcf().canvas.flush_events()

        plt.ioff()
        plt.show()
        ser.close()