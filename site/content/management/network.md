---
title: Network
draft: false
author: Mackenzie McFate
date: 2021-05-22T06:40:53-05:00
socialshare: false
weight: 80
---
<!--
menu:
  main:
    identifier: prices
    pre: dollar-sign
    weight: 200
-->

<hr/>

## Networks and Other Connections

The Wieting's systems are identified as follows:

{{<table "table table-striped table-bordered">}}
| System Name | Description | Addressing | Physical Locations |
| --- | --- | ---- | --- |
| THEATRE | This is the SSID of the Wieting's internet connection and house network. | 10.0.0.0 / 24 | Provides service to OPERATIONS and WEITING-WIFI/GUEST only. |
| OPERATIONS | Cinema system network for systems control. | 10.11.128.0 / 24 | Ethernet only in the Projection Booth |
| WEITING-WIFI | Wireless only via our EERO devices. | 192.168.4.x / 24 | Wireless in the auditorium and south addition. |
| WEITING-GUEST | Guest wireless only via our EERO devices. | 192.168.4.x / 24 | Wireless in the auditorium and south addition. |
| Others | All other names indicate connection types of limited length like `USB`, `OPTICAL-AUDIO`, `HDMI`, `SERIAL`, etc. | Not applicable | Wherever the connected devices are. |
| \*MEDIA | Cinema system gigabit network for transfer of media/content. | 10.0.0.0 / 23 | Ethernet only in the Projection Booth |
{{< /table >}}            

<!-- Notes from Andrew Peevler...

10.0.0.x = MEDIA Network
10.11.128.x = OPERATIONS network... everything cinema-related except MEDIA

Problem:  When the iMac's ethernet connection is active, the iMac cannot access the internet!

-->

## Diagram

{{< imgfig "/img/_Wieting-Networks-Topology-2021.png" >}}


## Wieting Network Topology "Secret Decoder Ring"

{{<table "table table-striped table-bordered">}}
| Device Code | Description | Physical Location |
| --- | --- | --- |
| A | Wieting-Booth iMac | Projection Booth - Projection Desk |
| B | Samsung Blu-Ray Player | Projection Booth - Projection Desk |
| C | GDC SX-2000AR Cinema Server | Projection Booth - Projector Pedastal |
| D | QSC DPM 100 Audio Processor | Projection Booth - Audio Rack |
| E | Eero Wireless Mesh Gateway | Light Board Desk w/ 2 Satelite Units in the Annex |
| F | Simplex Grinnell Fire Alarm | Stage North |
| G | Netgear 16-Port Gigabit Switch | Projection Booth - Top of Audio Rack |
| H | 4-Port HDMI Switch w/ Optical Audio Input | Projection Booth - Projection Desk |
| J | JNIOR A-310 Programmable Logic Controller | Projection Booth - Rear of Cinema Pedestal |
| K | 2-Port Ethernet Punch Box | **To Be Removed** |
| L | Ubuntu-Trailers Linux Desktop | **To Be Removed** |
| M | Thompson DCM476 Cable Modem from Mediacom | Projection Booth - Top of Audio Rack |
| O | Wieting-BoxOffice Windows Desktop Computer | Box Office - North Desk |
| P | Christie CP2210 Cinema Projector | Projection Booth - Cinema Pedestal |
| R | NetGear 4-Port + Wireless Router | Projection Booth - Top of Audio Rack |
| S | NetGear ProSafe 8-Port Gigabit Switch | Projection Booth - Rear of Cinema Pedestal |
| W | Three Individual Ethernet Terminations | Stage - North (2) and South (1) Wings |
| X | Booth-Windows - Windows 10 Desktop | Projection Booth - Projection Desk |
{{< /table >}}            

### Cable Label Convention

Each end of a cable should be labeled following this convention:

  `DeviceCode.Port - Network or Cable Type - DeviceCode.Port`

Labels should be applied such that the `DeviceCode.Port` corresponding to a particular device is nearest that device.  This will require placing one of the labels "upside down". \*See the first example below for clarification.  

#### Examples

  - A `THEATRE` network cable running from device `R`, port 1, to an unidentified port on device `F` will have a pair of labels marked `R.1 - THEATRE - F.x`.  \*For example, at device `R` the `R.1` end of the label should be nearest device `R`, while at device `F` the `F.x` end of that label should be nearest device `F`.
  - A `USB` cable running from an unidentified port on device `L` to an `In` port on device `X` will carry a pair of lables marked `L.x - USB - X.In`.
  - An `HDMI-to-DVI` cable running from the `Out` port on device `H` to a `DVI` port on device `P` will be labeled `H.Out - HDMI-to-DVI - P.DVI`.
