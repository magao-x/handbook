# Cameras

Applications to control cameras have many common features. Most of them are implemented in the [standard camera interface](#Standard-Camera-Interface), but will only be enabled if a particular model of camera supports them.

**Driver details:** [ocam2KCtrl](#ocam2kctrl) | [baslerCtrl](#baslerCtrl) | ...

## Standard Camera Interface

All camera controllers implement the standard camera interface ([source code](https://github.com/magao-x/MagAOX/blob/master/libMagAOX/app/dev/stdCamera.hpp)) and expose the subset of those properties that their hardware and driver support.

### Modes

Modes are pre-defined hardware configurations, which include the size and binning of the readout.  They are defined in the configuration file with sections, where the section name is the name of the mode.  Example:
```
[mode_name]
configFile=/path/to/EDT-config #this is required
serialCommand=(string) #optional
centerX=(float) #optional
centerY=(float) #optional
sizeX=(int) #optional
sizeY=(int) #optional
binning=(int) #optional
maxFPS=(float) #optional
```
If `configFile` is not found, the section will not be treated as a mode.

Modes are controlled through INDI with the following properties:

| Property |  Element | Type  | Description|
| ---      | ---      | ---   | --- |
| `.mode`     | `.{names}`  | selection switch | A list of modes by name.  Selecting one will cause the camera to be configured for that mode |
| `.reconfigure` | `.request` | request switch | Pressing this switch will cause the current mode to be re-loaded. |


The following configuration options affect modes: 

| Short | Long                   | Config-File         | Type            | Description |
| ---   | ---                    | ---                   | ---             | --- |
|       | `--camera.startupMode`   | `camera.startupMode`    | string          | The mode to set upon power on or application startup. |


### Regions of Interest

If the camera supports reading out only a region of interest (ROI), you can use INDI properties to define it.  An ROI is specified by its (x,y) center coordinate and its width and height, and optionally binning in each direction.  All coordinates and dimensions are in pixels.  We use the convention that the center of the lower-left pixel of the full array is (0,0).  The center coordinate of the full array is then (0.5*(max_width-1), 0.5*(max_height-1)).  Widths and heights are integer values, and coordinates are floats which can have values of 0.5.

Not all values are valid, as some cameras restrict the increments (steps of 4, for example) of some of the values, or otherwise set limits.

To change ROI, you set the ``.target`` elements to define the ROI, and then use the `.roi_set.request` switch to configure the camera.  The following INDI properties pertain to ROIs:

| Property |  Element | Type  | Description|
| ---      | ---      | ---   | --- |
|`.roi_full_region `| .x | float | (READ ONLY) The x coordinate of the denter of the full region. |
|`.roi_full_region` | .y | float | (READ ONLY) The y coordinate of the center of the full region. |
|`.roi_full_region` | .w | int | (READ ONLY) The width of the full region. |
|`.roi_full_region` | .h | int | (READ ONLY) The height of the full region. |
|`.roi_region_bin_x` | `.current` | int | The current value of the ROI region binning in the x direction. |
|                  | `.target` | int | The target value of the ROI region binning in the x direction.  Not laoded until the roi_set.request switch is pressed. |
|`.roi_region_bin_y` | `.current` | int | The current value of the ROI region binning in the y direction. |
|                  | `.target` | int | The target value of the ROI region binning in the y direction.  Not laoded until the roi_set.request switch is pressed. |
|`.roi_region_h` | `.current` | int | The current value of the ROI region height. |
|              | `.target` | int | The target value of the ROI region height.  Not laoded until the roi_set.request switch is pressed. |
|`.roi_region_w` | `.current` | int | The current value of the ROI region width. |
|              | `.target` | int | The target value of the ROI region width.  Not laoded until the roi_set.request switch is pressed. |
|`.roi_region_x` | `.current` | float | The current value of the ROI region center x coordinate. |
|              | `.target` | float | The target value of the ROI region center x coordinate.  Not laoded until the roi_set.request switch is pressed. |
|`.roi_region_y` | `.current` | float | The current value of the ROI region center y coordinate. |
|              | `.target` | float | The target value of the ROI region center y coordinate.  Not laoded until the roi_set.request switch is pressed. |
|`.roi_set`      | `.request` | switch | Press this switch to configure with the target values of the .roi_region*`.target` elements above. |
|`.roi_set_full` | `.request` | switch | Press this switch to configure with the full ROI of the camera. |
|`.roi_set_last` | `.request` | switch | Press this switch to configure with the previously set ROI. |
|`.roi_set_startup` | `.request` | switch | Press this switch to configure with the startup ROI (see options below). |

The default ROI can be configured with the following options.  This ROI will be set each time the camera software is re-started or the camera is powered-on.

| Short | Long                   | Config-File          | Type            | Description |
| ---   | ---                    | ---                   | ---             | --- |
|       | --camera.startup_x     | camera.startup_x      | float           | The default ROI x position.|
|       | --camera.startup_y     | camera.startup_y      | float           | The default ROI y position.|
|       | --camera.startup_w     | camera.startup_w      | int             | The default ROI width.|
|       | --camera.startup_h     | camera.startup_h      | int             | The default ROI height.|
|       | --camera.startup_bin_x     | camera.startup_bin_x      | int             | The default ROI x binning.|
|       | --camera.startup_bin_y     | camera.startup_bin_y      | int             | The default ROI y binning.|


### Exposure Control

All MagAO-X cameras operate in free-run, meaning images are taken continuously with no user intervention needed.  The exposure time is either set directly, or by setting the frame rate, or both.  In cases where both options are given, see the camera specific documentation for details of how they are related.  The INDI properties for controlling exposure time and frame rate are:

| Property |  Element | Type  | Description|
| ---      | ---      | ---   | --- |
| .exptime | `.current` | float | the current exposure time, in seconds.|
|          | `.target`  | float | the target exposure time, in second. |
| .fps | `.current` | float | the current framerate, in frames per second.|
|          | `.target`  | float | the target frame rate, in frames per second. |

### Shutters

If the camera has an associated shutter, it is controlled with the following properties

| Property |  Element | Type  | Description|
| ---      | ---      | ---   | --- |
| `.shutter_status` | `.status` | string | Status of the shutter, e.g. POWEROFF, READY, etc.|
| `.shutter` | `.toggle` | toggle switch | Current state of the shutter: ON = SHUT (\|X\|), OFF = OPEN (\|O\|). Toggling the switch changes state.|

#### Uniblitz DSS Shutters

The cameras which use the Uniblitz DSS shutter control have the following additional configuration options 

| Short | Long                   | Config-File          | Type            | Description |
| ---   | ---                    | ---                   | ---             | --- |
|  | `--shutter.powerDevice`  | `shutter.powerDevice`  | string  | The device controlling this shutter's power |
|  | `--shutter.powerChannel`  | `shutter.powerChannel` | string  | The channel controlling this shutter's power  |
|  | `--shutter.dioDevice`  | `shutter.dioDevice` |string  |The device controlling this shutter's digital I/O.  |
|  | `--shutter.sensorChannel`  | `shutter.sensorChannel` |string  |The channel reading this shutter's sensor.  |
|  | `--shutter.wait`  | `shutter.wait` | int | The time to pause between checks of the sensor state during open/shut [msec]. Default is 100. |
|  | `--shutter.timeout`  | `shutter.timeout` | int  | Total time to wait for sensor to change state before timing out [msec]. Default is 2000. |

### Temperature 

All current cameras provide a measurement of the detector temperature.  Most provide a way to control the temperature based on a set point.

| Property |  Element | Type  | Description|
| ---      | ---      | ---   | --- |
| `.temp_ccd` | `.current` | float | the current detector temperature, in C. |
|           | `.target`  | float | only if temperature control is offered, the target temperature to set.|
| `.temp_controller` | `.toggle` | toggle switch | switch to turn on/off the temperature control system for this camera. |
| `.temp_control` | `.status` | string | the state of the temperature control, indicating whether it is on target, etc. |

The following configuration options also affect temperature:

| Short | Long                   | Config-File          | Type            | Description |
| ---   | ---                    | ---                   | ---             | --- |
|       | `--camera.startupTemp`     | `camera.startupTemp`    | float   | the temperature setpoint to set at startup |

## Framegrabber Interface

The standard MagAO-X framegrabber system is used by any application which collects images from hardware and writes them to a shared memory stream.  All cameras are framegrabbers.  The following INDI properties provide details about the framegrabber:

| Property |  Element | Type  | Description|
| ---      | ---      | ---   | --- |
| `.fg_shmimname` | `.name` | string | The name of the ImageStreamIO shared memory image. Will be seen as /milk/shm/<shmimName>.im.shm. |
| `.fg_framesize` | `.width` | int | The width of the frame in memory. |
|                 | `.height` | int | The height of the frame in memory. |

The following configuration options will be available in any application which is a framegrabber:

| Short | Long                   | Config-File          | Type            | Description |
| ---   | ---                    | ---                   | ---             | --- |
|      | --framegrabber.threadPrio | framegrabber.threadPrio | int | The real-time priority of the framegrabber thread.|
|      | --framegrabber.shmimName  | framegrabber.shmimName  | string | The name of the ImageStreamIO shared memory image. Will be used as /milk/shm/<shmimName>.im.shm. |
|      | --framegrabber.circBuffLength | framegrabber.circBuffLength | int | The length of the circular buffer. Sets m_circBuffLength, default is 1. |

### EDT Framegrabbers

A camera which uses an EDT framegrabber (PCIe card) will have the following additional configuration options:

| Short | Long                   | Config-File          | Type            | Description |
| ---   | ---                    | ---                   | ---             | --- |
| |--framegrabber.pdv_unit |framegrabber.pdv_unit | int | The EDT PDV framegrabber unit number.  Default is 0. |
| |--framegrabber.pdv_channel |framegrabber.pdv_channel | int | The EDT PDV framegrabber channel number.  Default is 0. |
| |--framegrabber.numBuffs | framegrabber.numBuffs | int | The EDT PDV framegrabber DMA buffer size [images].  Default is 4. |

## baslerCtrl

`baslerCtrl` controls a Basler camera.  It monitors and logs temperatures, configures the camera for the desired mode of operation, and manages the grabbing and processing of frames.  It is a MagAO-X [standard camera](#Standard-Camera-Interface) and a [standard framegrabber](#Framegrabber-Interface).

### Exposure Control 

The basler cameras use exposure time.  Acquisition FPS can be set as an upper limit.  As long as exposure time and ROI can support the set FPS, then it will be the framerate of the camera but actual exposure time will not change.  Setting `{name}.fps.target=0` causes the camera to run at its maximum possible FPS for its configuration.

### Regions of Interest

Basler cameras support [ROIs](#Regions-of-Interest).  Note that there are restrictions on possible settings, which depend on camera model.  For instance, the width or height may only be settable in multiples of 2 or 4.

### Temperature 

Temperature is passively monitored only.

### Options

Basler specific configuration options are:

| Short | Long                      | Config-File         | Type            | Description |
|-|-|-|-|-|
|       | `--camera.serialNumber`   | `camera.serialNumber`  | string  | The identifying serial number of the camera.  This is required to connect.|
|       | `--camera.bits`           | `camera.bits`  | int |The number of bits used by the camera.  Default is 10. |

## ocam2KCtrl

`ocam2KCtrl` controls the OCAM 2K EMCCD, which serves as the pyramid wavefront sensor detector in MagAO-X.  It monitors and logs temperatures, configures the camera for the desired mode of operation, and manages the grabbing and processing of frames.  It is a MagAO-X [standard camera](#Standard-Camera-Interface) and a [standard framegrabber](#Framegrabber-Interface) using the [EDT interface](#EDT-Framegrabbers).

### Options

OCAM specific configuration options are:

| Short | Long                      | Config-File         | Type            | Description |
| ---   |  ---                      | ---                 | ---             | ---         |
|       | `--camera.ocamDescrambleFile`   | `camera.ocamDescrambleFile`  | string  | The path of the OCAM descramble file, relative to MagAOX/config. |
|       | `--camera.maxEMGain`           | `camera.maxEMGain`  | unsigned int | The maximum EM gain which can be set by user. Default is 600.  Min is 1, max is 600. |
