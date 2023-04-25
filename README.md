Connect Waveshare SIM7600X-4G-HAT(B) to Raspberry Pi Zero W/2 W

# A. Set up driver

## 1. Find IP address of Raspberry Pi

After boot Raspberry Pi OS (with local wifi), find IP address of Pi:

on Ubuntu:

```
sudo apt-get install arp-scan

ifconfig ## Get device network

sudo arp-scan --interface=[device network] --localnet
```

ssh to Pi using user and password that was set in setup process

## 2. Get HAT package

`wget https://www.waveshare.com/w/upload/4/4e/SIM7600X-4G-HAT%28B%29-Demo.7z`

## 3. Install driver

```
sudo apt-get install p7zip-full

7z x 'SIM7600X-4G-HAT(B)-Demo.7z' -r -o/home/pi

mv /home/pi/'SIM7600X-4G-HAT(B)-Demo' /home/pi/SIM7600X-4G-HAT-B-Demo

sudo chmod 777 -R /home/pi/SIM7600X-4G-HAT-B-Demo

sudo nano /etc/rc.local
```

Add the following line to rc.local to start Waveshare 4G HAT drivers on the boot-up of the Raspberry Pi.

`sh /home/pi/SIM7600X-4G-HAT-B-Demo/Raspberry/c/sim7600_4G_hat_init`

Install driver

```
cd /home/pi/SIM7600X-4G-HAT-Demo/Raspberry/c/bcm2835

chmod +x configure && ./configure && sudo make && sudo make install
```

# B. Setup RNDIS for SIM7600G HAT to work like a network card

## 1. Check if HAT is recognized

`ls /dev/ttyUSB*`

## 2. Run AT command

`python3 example/AT-test.py`

Send the follwing command to switch to RNDIS

`AT+CUSBPIDSWITCH=9011,1,1`

Check if the setup was successfully

`ifconfig`

# Appendix

## GPS fields' info:

GPS format:

```
+CGPSINFO: [<lat>],[<N/S>],[<log>],[<E/W>],[<date>],[<UTC time>],[<alt>],[<speed>],[<course>]

<lat>: Latitude of current position. Output format is ddmm.mmmmmm
<N/S>: N/S Indicator, N=north or S=south
<log>: Longitude of current position. Output format is dddmm.mmmmmm
<E/W>: E/W Indicator, E=east or W=west
<date>: Date. Output format is ddmmyy
<UTC time>: UTC Time. Output format is hhmmss.s
<alt>: MSL Altitude. Unit is meters.
<speed>: Speed Over Ground. Unit is knots.
<course>: Course. Degrees.
<time>: The range is 0-255, unit is second, after set <time> will report the GPS information every the seconds
```

GNSS format:

```
+CGNSSINFO: [<mode>],[<GPS-SVs>],[<GLONASS-SVs>],[BEIDOU-SVs],[<lat>],[<N/S>],[<log>],[<E/W>],[<date>],[<UTC-time>],[<alt>],[<speed>],[<course>],[<PDOP>],[HDOP],[VDOP]

<mode>: Fix mode 2=2D fix 3=3D fix
<GPS-SVs>: GPS satellite valid numbers, scope: 00-12
< GLONASS-SVs >: GLONASS satellite valid numbers scope: 00-12
<BEIDU-SVs>: BEIDOU satellite valid numbers scope: 00-12
<lat>: Latitude of current position. Output format is ddmm.mmmmmm
<N/S>: N/S Indicator, N=north or S=south
<log>: Longitude of current position. Output format is dddmm.mmmmmm
<E/W>: E/W Indicator, E=east or W=west
<date>: Date. Output format is ddmmyy
<UTC time>: UTC Time. Output format is hhmmss.s
<alt>: MSL Altitude. Unit is meters.
<speed>: Speed Over Ground. Unit is knots.
<course>: Course. Degrees.
<time>: The range is 0-255, unit is second, after set <time> will report the GPS information every the seconds.
<PDOP>: Position Dilution Of Precision.
<HDOP>: Horizontal Dilution Of Precision.
<VDOP>: Vertical Dilution Of Precision
```
