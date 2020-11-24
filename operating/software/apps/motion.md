# Stages and filter wheels

Stages and filter wheels are controlled by apps derived from the [stdMotionStage](https://github.com/magao-x/MagAOX/blob/master/libMagAOX/app/dev/stdMotionStage.hpp) implementation, meaning they share some common properties and options.

## filterWheelCtrl

`filterWheelCtrl` controls an MCBL 3006S based filter wheel for MagAO-X.  As of Dec, 2018, there are 6 such wheels in MagAO-X.  This program communicates with the MCBL 3006S controller via USB.  It monitors the position and motion status of the wheel, and via INDI accepts commands to home and change wheel position.

### Options

| Short | Long                   | Config-File        | Type              | Description |
|-------|------------------------|----------------------|-------------------|---|
|       | `--power.device`       | power.device         | string            | Device controlling power for this app's device (INDI name). |
|       | `--power.outlet`       | power.outlet         | string            | Outlet (or channel) on device for this app's device (INDI name). |
|       | `--power.element`      | power.element        | string            | INDI element name.  Default is "state", only need to specify if different. |
|       | `--usb.idVendor`       | usb.idVendor         | string            | USB vendor id, 4 digits |
|       | `--usb.idProduct`      | usb.idProduct        | string            | USB product id, 4 digits |
|       | `--usb.serial`         | usb.serial           | string            | USB serial number |
|       | `--usb.baud`           | usb.baud             | real              | USB tty baud rate (i.e. 9600) |
|       | `--timeouts.write`     | timeouts.write       | int               | The timeout for writing to the device [msec]. Default = 1000 |
|       | `--timeouts.read`      | timeouts.read        | int               | The timeout for reading the device [msec]. Default = 1000 |
|       | `--motor.acceleration` | motor.acceleration   | real              | The motor acceleration parameter. Default=1000. |
|       | `--motor.speed`        | motor.speeed         | real              | The motor speed parameter.  Default=1000. |
|       | `--motor.circleSteps`  | motor.circleSteps    | long              | The number of steps in 1 revolution. |
|       | `--motor.homeOffset`   | motor.homeOffset     | long              | The homing offset in motor counts. |
|       | `--motor.powerOnHome`  | motor.powerOnHome    | bool              | If true, home at startup/power-on. Default=false. |
|       | `--filters.names`      | filters.names        | vector of strings | The names of the filters. |
|       | `--filters.positions`  | filters.positions    | vector of doubles | The positions of the filters.  If omitted or 0 then order is used. |
