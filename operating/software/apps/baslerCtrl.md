# baslerCtrl

## Name

baslerCtrl − Controls a Basler camera

## Synopsis

```
baslerCtrl -n name [options]
```

`baslerCtrl` is normally configured with a configuration file, set by the `-n name` option.

## Description

`baslerCtrl` controls a Basler camera.  It monitors and logs temperatures, configures the camera for the desired mode of operation, and manages the grabbing and processing of frames.  It is a MagAO-X `standard camera`, and a standard `framegrabber`.

### Exposure Control 

The basler cameras use exposure time.  Acquisition FPS can be set as an upper limit.  As long as exposure time and ROI can support the set FPS, then it will be the framerate of the camera but actual exposure time will not change.  Setting `.fps.target=0` causes the camera to run at its maximum possible FPS for its configuration.

### Regions of Interest

Basler cameras support ROIs.  Note that there are restrictions on possible settings, which depend on camera model.  For instance, the width or height may only be settable in multiples of 2 or 4.

### Temperature 

Temperature is passively monitored only.

## Options

To see the complete list of options, run 
```
[xsup@ ~]$ /opt/MagAOX/bin/baslerCtrl -h
```

baslerCtrl accepts the [standard options](index.html#standard-options)

baslerCtrl accepts the [standard camera](cameras.html#standard-camera-interface) options.  Baslers do not use modes, do use ROIs, provide no temperature control, and do not typically have shutters.

baslerCtrl accepts the [framegrabber](cameras.html#framegrabber-interface) options

Basler specific configuration options are:

| Short | Long                   | Config-File*         | Type            | Description |
| ---   |  ---                    | ---                 | ---             |             |
|       | --camera.serialNumber  | camera.serialNumber  | string  | The identifying serial number of the camera.  This is required to connect.|
|       | --camera.bits           | camera.bits  | int |The number of bits used by the camera.  Default is 10. |

\* format in the config file column is section.option which implies the format
```
[section]
option=value
```
in the config file.

## INDI Properties

baslerCtrl provides the INDI properties of [standard camera](cameras.html#standard-camera-interface) and [framegrabber](cameras.html#framegrabber-interface).





## Examples

To start the baslerCtrl as the Pyramid WFS tip camera:
```
/opt/MagAOX/bin/baslerCtrl -n camtip
```

## See also

[Source code.](../../../../MagAOX/group__baslerCtrl.html)
