# Hello World Example
#
# Welcome to the MaixPy IDE!
# 1. Conenct board to computer
# 2. Select board at the top of MaixPy IDE: `tools->Select Board`
# 3. Click the connect buttion below to connect board
# 4. Click on the green run arrow button below to run the script!

import sensor, image, time, lcd
from fpioa_manager import fm
from machine import UART
from board import board_info
import KPU as kpu

lcd.init(freq=15000000)
lcd.rotation(2)

fm.register(board_info.PIN9, fm.fpioa.UART1_TX, force=True)
fm.register(board_info.PIN10, fm.fpioa.UART1_RX, force=True)
fm.register(board_info.PIN15, fm.fpioa.UART2_TX, force=True)
fm.register(board_info.PIN17, fm.fpioa.UART2_RX, force=True)
uart1 = UART(UART.UART1, 115200,8,0,0, timeout=1000, read_buf_len=4096)
uart2 = UART(UART.UART2, 115200,8,0,0, timeout=1000, read_buf_len=4096)


sensor.reset()

sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()
faceDetect = 0
checkForDay = 0
user = 'k'
tim1 = tim1 = time.ticks_ms()

while(True):
    clock.tick()
    img = sensor.snapshot()
    lcd.display(img)
    if faceDetect:
        uart1.write("b")
        faceDetect = 0
    if uart1.any():
        entry = uart1.read()
        entry = entry.decode('utf-8')
        if entry == 'x0':
            entry = '1m' + user
        if entry == 'x1':
            entry = '1t' + user
        if entry == 'x2':
            entry = '1w' + user
        if entry == 'x3':
            entry = '1r' + user
        if entry == 'x4':
            entry = '1f' + user
        if entry == 'x5':
            entry = '1s' + user
        if entry == 'x6':
            entry = '1n' + user
        print("entry:")
        print(entry)
        uart2.write(entry)

    if uart2.any():
        entry1 = uart2.read()
        entry1 = entry1.decode('utf-8')
        print("entry1:")
        print(entry1)
        if entry1 == "10":
            uart1.write(bytes([10]))
        if entry1 == "11":
            uart1.write(bytes([11]))
            while uart2.any() < 12:
                1
            entry2 = uart2.read()
            entry2 = entry2.decode('utf-8')
            print("entry2(11):")
            print(entry2)
            uart1.write(entry2)
        if entry1 == "12":
            uart1.write(bytes([12]))
            while uart2.any() < 12:
                1
            entry2 = uart2.read()
            entry2 = entry2.decode('utf-8')
            print("entry2(12):")
            print(entry2)
            uart1.write(entry2)
        if entry1 == "13":
            uart1.write(bytes([13]))
            while uart2.any() < 4:
                1
            entry2 = uart2.read()
            entry2 = entry2.decode('utf-8')
            print("entry2(13):")
            print(entry2)
            uart1.write(entry2)
        if entry1 == "14":
            uart1.write(bytes([14]))
            while uart2.any() == 0:
                1
            entry2 = uart2.read(1)
            entry2 = entry2.decode('utf-8')
            print("entry2(20):")
            print(entry2)
            uart1.write(entry2)
            while uart2.any() < int(entry2)*4:
                1
            entry3 = uart2.read()
            entry3 = entry3.decode('utf-8')
            print("entry3(20):")
            print(entry3)
            uart1.write(entry3)
        if entry1 == "16":
            uart1.write(bytes([16]))
        if entry1 == "17":
            uart1.write(bytes([17]))
        if entry1 == "18":
            uart1.write(bytes([18]))
        if entry1 == "20":
            uart1.write(bytes([20]))
            while uart2.any() == 0:
                1
            entry2 = uart2.read(1)
            entry2 = entry2.decode('utf-8')
            print("entry2(20):")
            print(entry2)
            uart1.write(entry2)
            if int(entry2) > 0:
                while uart2.any() < int(entry2)*12:
                    1
                entry3 = uart2.read()
                entry3 = entry3.decode('utf-8')
                print("entry3(20):")
                print(entry3)
                uart1.write(entry3)


