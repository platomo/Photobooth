import os
import subprocess
import time

from gpiozero import Button, LEDBoard


def reboot_shutdown():
    button_leds.blink(
        on_time=0.1,
        off_time=0.1,
        fade_in_time=0,
        fade_out_time=0,
        n=10,
        background=False,
    )
    if go_button.is_pressed:
        subprocess.call("sudo nohup poweroff", shell=True)
    else:
        subprocess.call("sudo nohup reboot", shell=True)


print("initializing leds")
cam_leds = LEDBoard(25, 5, 6, 13, 19, 26, pwm=True)
# snap_leds = cam_leds[:4]
snap_leds = LEDBoard(12, 16, 20, 21, pwm=True)
# button_leds = cam_leds[:2]
button_leds = LEDBoard(23, 24, pwm=True)
# printer_leds = cam_leds[2:]
printer_leds = LEDBoard(14, 15, 17, 18, pwm=True)

print("initializing buttons")
go_button = Button(4, hold_time=5, pull_up=True)
go_button.when_held = reboot_shutdown

print("turn leds on")
cam_leds.on()
snap_leds.on()
button_leds.on()
printer_leds.on()

print("wait for button press")
go_button.wait_for_press()

print("turn leds off")
cam_leds.off()
snap_leds.off()
button_leds.off()
printer_leds.off()

while True:
    for led in button_leds:
        led.blink(1.2, 0, 1.2, 1.2)
        time.sleep(1.8)

    go_button.wait_for_press()
    print("Let's go!")

    # for led in button_leds:
    # led.off()
    button_leds.off()

    subprocess.call("rm /home/frunika/photobooth/*.jpg", shell=True)

    snap = 0

    cam_leds.blink(0, 0, 6, 0, 1, background=False)

    while snap < 4:
        snap_leds[snap].pulse(0.25, 0.25, 5, background=False)
        snap_leds[snap].pulse(0.5, 0.5)
        cam_leds.on()
        # cam_leds.pulse(0.5, 0.5, 2, background=False)
        # cam_leds.blink(0.5,0,0.5,0,1,background=False)
        for led in reversed(cam_leds):
            led.pulse(0, 0.5, 1, background=False)

        print("SNAP " + str(snap))
        filenm = "/home/frunika/photobooth/photobooth_" + str(snap) + ".jpg"
        gpout = subprocess.check_output(
            "gphoto2 --capture-image-and-download --keep --filename " + filenm,
            stderr=subprocess.STDOUT,
            shell=True,
        )
        # time.sleep(3)

        for led in cam_leds:
            led.blink(0.6, 0.6, 0.1 / 2, 0.1 / 2)
            time.sleep(0.1 / 2)

        # print(gpout)
        if os.path.isfile(filenm):
            snap += 1
            time.sleep(2)
        # snap += 1
        cam_leds.off()
        for led in snap_leds[:snap]:
            led.on()

    # print("photos stitchen")

    subprocess.call("/home/frunika/assemble_and_print", shell=True)

    cam_leds.off()
    snap_leds.off()
    # for led in snap_leds:
    # led.value = 0.2

    # printer_leds.on()

    for led in reversed(printer_leds):
        led.blink(0, 1.2, 0.6, 0.6)
        time.sleep(0.6)

    gpout = subprocess.check_output("lpstat -p", stderr=subprocess.STDOUT, shell=True)

    # while "Leerlauf" not in gpout:
    #     gpout = subprocess.check_output(
    #         "lpstat -p", stderr=subprocess.STDOUT, shell=True
    #     )    # while "Leerlauf" not in gpout:
    #     gpout = subprocess.check_output(
    #         "lpstat -p", stderr=subprocess.STDOUT, shell=True
    #     )
    #  print("warte noch auf Drucker")

    time.sleep(60)

    cam_leds.off()
    button_leds.off()
    snap_leds.off()
    printer_leds.off()
