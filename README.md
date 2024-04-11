# Photobooth

This is currently a small script I wrote a few years ago for a friends' wedding.
I currently just set up this repo to save this old script.

The box took photos, assembled them and printed them using cups.

There are multiple LEDs and a single button for user interaction.

The python script was started on boot using the `/etc/rc.local` file.

## Requirements

- python3
- python3-pip
- python3-gpiozero
- git
- gphoto2
- cups

## Configuring cups

Install cups, add user to lpadmin group and enable remote cups webinterface.
Last step may take a minute.

```shell
sudo apt install cups
sudo usermod -a -G lpadmin <user>
cupsctl --remote-admin
```

Install Gutenprint drivers to add support for Canon Selphy CP-820.

```shell
sudo apt install printer-driver-gutenprint
```

Open [CUPS webinterface](https://10.10.10.152:631/) and add printer using Gutenprint drivers.
