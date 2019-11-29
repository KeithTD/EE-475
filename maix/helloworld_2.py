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


sensor.reset()                      # Reset and initialize the sensor. It will
                                    # run automatically, call sensor.run(0) to stop
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.
tim1 = time.ticks_ms()
tim2 = time.ticks_ms()

while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
    lcd.display(img)                # Display on LCD

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
        print(entry)                # Note: MaixPy's Cam runs about half as fast when connected
                                    # to the IDE. The FPS should increase once disconnected.
    if uart2.any():
        entry1 = uart2.read()
        entry1 = entry1.decode('utf-8')
        print(entry1)
        if entry1 == "13":
            uart1.write(bytes([13]))
            while uart2.any() < 4:
                1
            entry2 = uart2.read()
            entry2 = entry2.decode('utf-8')
            print(entry2)
            uart1.write(entry2)
        if entry1 == "18":
            uart1.write(bytes([18]))
