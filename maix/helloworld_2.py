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
tim1 = time.ticks_ms()
tim2 = time.ticks_ms()

while(True):
    clock.tick()
    img = sensor.snapshot()
    lcd.display(img)

    #if (time.ticks_diff(time.ticks_ms(), tim1)>5000):
    #    uart1.write("b")#(bytes([17]))
    #    tim1 = time.ticks_ms()
    #if (time.ticks_diff(time.ticks_ms(), tim2)>5000):
    #    uart2.write("a")#(bytes([17]))
    #    tim2 = time.ticks_ms()

    if uart1.any():
        entry = uart1.read()
        entry = entry.decode('utf-8')
        if entry == "3dd":
            uart2.write(entry)
        else:
            uart2.write(entry)
        print(entry)

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


