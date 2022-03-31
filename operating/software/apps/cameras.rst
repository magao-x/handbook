Cameras
=======

Applications to control cameras have many common features. Most of them
are implemented in the `standard camera
interface <#Standard-Camera-Interface>`__, but will only be enabled if a
particular model of camera supports them.

**Driver details:** `ocam2KCtrl <#ocam2kctrl>`__ \|
`baslerCtrl <#baslerCtrl>`__ \| …

Standard Camera Interface
-------------------------

All camera controllers implement the standard camera interface (`source
code <https://github.com/magao-x/MagAOX/blob/master/libMagAOX/app/dev/stdCamera.hpp>`__)
and expose the subset of those properties that their hardware and driver
support.

Modes
~~~~~

Modes are pre-defined hardware configurations, which include the size
and binning of the readout. They are defined in the configuration file
with sections, where the section name is the name of the mode. Example:

::

   [mode_name]
   configFile=/path/to/EDT-config #this is required
   serialCommand=(string) #optional
   centerX=(float) #optional
   centerY=(float) #optional
   sizeX=(int) #optional
   sizeY=(int) #optional
   binning=(int) #optional
   maxFPS=(float) #optional

If ``configFile`` is not found, the section will not be treated as a
mode.

Modes are controlled through INDI with the following properties:

+-----------------+-----------------+-----------------+-----------------+
| Property        | Element         | Type            | Description     |
+=================+=================+=================+=================+
| ``.mode``       | ``.{names}``    | selection       | A list of modes |
|                 |                 | switch          | by name.        |
|                 |                 |                 | Selecting one   |
|                 |                 |                 | will cause the  |
|                 |                 |                 | camera to be    |
|                 |                 |                 | configured for  |
|                 |                 |                 | that mode       |
+-----------------+-----------------+-----------------+-----------------+
| `               | ``.request``    | request switch  | Pressing this   |
| `.reconfigure`` |                 |                 | switch will     |
|                 |                 |                 | cause the       |
|                 |                 |                 | current mode to |
|                 |                 |                 | be re-loaded.   |
+-----------------+-----------------+-----------------+-----------------+

The following configuration options affect modes:

+-------------+-------------+-------------+-------------+-------------+
| Short       | Long        | Config-File | Type        | Description |
+=============+=============+=============+=============+=============+
|             | ``          | ``camera.st | string      | The mode to |
|             | --camera.st | artupMode`` |             | set upon    |
|             | artupMode`` |             |             | power on or |
|             |             |             |             | application |
|             |             |             |             | startup.    |
+-------------+-------------+-------------+-------------+-------------+

Regions of Interest
~~~~~~~~~~~~~~~~~~~

If the camera supports reading out only a region of interest (ROI), you
can use INDI properties to define it. An ROI is specified by its (x,y)
center coordinate and its width and height, and optionally binning in
each direction. All coordinates and dimensions are in pixels. We use the
convention that the center of the lower-left pixel of the full array is
(0,0). The center coordinate of the full array is then
(0.5\ *(max_width-1), 0.5*\ (max_height-1)). Widths and heights are
integer values, and coordinates are floats which can have values of 0.5.

Not all values are valid, as some cameras restrict the increments (steps
of 4, for example) of some of the values, or otherwise set limits.

To change ROI, you set the ``.target`` elements to define the ROI, and
then use the ``.roi_set.request`` switch to configure the camera. The
following INDI properties pertain to ROIs:

+-----------------+-----------------+-----------------+-----------------+
| Property        | Element         | Type            | Description     |
+=================+=================+=================+=================+
| ``.ro           | .x              | float           | (READ ONLY) The |
| i_full_region`` |                 |                 | x coordinate of |
|                 |                 |                 | the denter of   |
|                 |                 |                 | the full        |
|                 |                 |                 | region.         |
+-----------------+-----------------+-----------------+-----------------+
| ``.ro           | .y              | float           | (READ ONLY) The |
| i_full_region`` |                 |                 | y coordinate of |
|                 |                 |                 | the center of   |
|                 |                 |                 | the full        |
|                 |                 |                 | region.         |
+-----------------+-----------------+-----------------+-----------------+
| ``.ro           | .w              | int             | (READ ONLY) The |
| i_full_region`` |                 |                 | width of the    |
|                 |                 |                 | full region.    |
+-----------------+-----------------+-----------------+-----------------+
| ``.ro           | .h              | int             | (READ ONLY) The |
| i_full_region`` |                 |                 | height of the   |
|                 |                 |                 | full region.    |
+-----------------+-----------------+-----------------+-----------------+
| ``.roi          | ``.current``    | int             | The current     |
| _region_bin_x`` |                 |                 | value of the    |
|                 |                 |                 | ROI region      |
|                 |                 |                 | binning in the  |
|                 |                 |                 | x direction.    |
+-----------------+-----------------+-----------------+-----------------+
|                 | ``.target``     | int             | The target      |
|                 |                 |                 | value of the    |
|                 |                 |                 | ROI region      |
|                 |                 |                 | binning in the  |
|                 |                 |                 | x direction.    |
|                 |                 |                 | Not laoded      |
|                 |                 |                 | until the       |
|                 |                 |                 | roi_set.request |
|                 |                 |                 | switch is       |
|                 |                 |                 | pressed.        |
+-----------------+-----------------+-----------------+-----------------+
| ``.roi          | ``.current``    | int             | The current     |
| _region_bin_y`` |                 |                 | value of the    |
|                 |                 |                 | ROI region      |
|                 |                 |                 | binning in the  |
|                 |                 |                 | y direction.    |
+-----------------+-----------------+-----------------+-----------------+
|                 | ``.target``     | int             | The target      |
|                 |                 |                 | value of the    |
|                 |                 |                 | ROI region      |
|                 |                 |                 | binning in the  |
|                 |                 |                 | y direction.    |
|                 |                 |                 | Not laoded      |
|                 |                 |                 | until the       |
|                 |                 |                 | roi_set.request |
|                 |                 |                 | switch is       |
|                 |                 |                 | pressed.        |
+-----------------+-----------------+-----------------+-----------------+
| ``              | ``.current``    | int             | The current     |
| .roi_region_h`` |                 |                 | value of the    |
|                 |                 |                 | ROI region      |
|                 |                 |                 | height.         |
+-----------------+-----------------+-----------------+-----------------+
|                 | ``.target``     | int             | The target      |
|                 |                 |                 | value of the    |
|                 |                 |                 | ROI region      |
|                 |                 |                 | height. Not     |
|                 |                 |                 | laoded until    |
|                 |                 |                 | the             |
|                 |                 |                 | roi_set.request |
|                 |                 |                 | switch is       |
|                 |                 |                 | pressed.        |
+-----------------+-----------------+-----------------+-----------------+
| ``              | ``.current``    | int             | The current     |
| .roi_region_w`` |                 |                 | value of the    |
|                 |                 |                 | ROI region      |
|                 |                 |                 | width.          |
+-----------------+-----------------+-----------------+-----------------+
|                 | ``.target``     | int             | The target      |
|                 |                 |                 | value of the    |
|                 |                 |                 | ROI region      |
|                 |                 |                 | width. Not      |
|                 |                 |                 | laoded until    |
|                 |                 |                 | the             |
|                 |                 |                 | roi_set.request |
|                 |                 |                 | switch is       |
|                 |                 |                 | pressed.        |
+-----------------+-----------------+-----------------+-----------------+
| ``              | ``.current``    | float           | The current     |
| .roi_region_x`` |                 |                 | value of the    |
|                 |                 |                 | ROI region      |
|                 |                 |                 | center x        |
|                 |                 |                 | coordinate.     |
+-----------------+-----------------+-----------------+-----------------+
|                 | ``.target``     | float           | The target      |
|                 |                 |                 | value of the    |
|                 |                 |                 | ROI region      |
|                 |                 |                 | center x        |
|                 |                 |                 | coordinate. Not |
|                 |                 |                 | laoded until    |
|                 |                 |                 | the             |
|                 |                 |                 | roi_set.request |
|                 |                 |                 | switch is       |
|                 |                 |                 | pressed.        |
+-----------------+-----------------+-----------------+-----------------+
| ``              | ``.current``    | float           | The current     |
| .roi_region_y`` |                 |                 | value of the    |
|                 |                 |                 | ROI region      |
|                 |                 |                 | center y        |
|                 |                 |                 | coordinate.     |
+-----------------+-----------------+-----------------+-----------------+
|                 | ``.target``     | float           | The target      |
|                 |                 |                 | value of the    |
|                 |                 |                 | ROI region      |
|                 |                 |                 | center y        |
|                 |                 |                 | coordinate. Not |
|                 |                 |                 | laoded until    |
|                 |                 |                 | the             |
|                 |                 |                 | roi_set.request |
|                 |                 |                 | switch is       |
|                 |                 |                 | pressed.        |
+-----------------+-----------------+-----------------+-----------------+
| ``.roi_set``    | ``.request``    | switch          | Press this      |
|                 |                 |                 | switch to       |
|                 |                 |                 | configure with  |
|                 |                 |                 | the target      |
|                 |                 |                 | values of the   |
|                 |                 |                 | .roi_region     |
|                 |                 |                 | \*\ ``.target`` |
|                 |                 |                 | elements above. |
+-----------------+-----------------+-----------------+-----------------+
| ``              | ``.request``    | switch          | Press this      |
| .roi_set_full`` |                 |                 | switch to       |
|                 |                 |                 | configure with  |
|                 |                 |                 | the full ROI of |
|                 |                 |                 | the camera.     |
+-----------------+-----------------+-----------------+-----------------+
| ``              | ``.request``    | switch          | Press this      |
| .roi_set_last`` |                 |                 | switch to       |
|                 |                 |                 | configure with  |
|                 |                 |                 | the previously  |
|                 |                 |                 | set ROI.        |
+-----------------+-----------------+-----------------+-----------------+
| ``.ro           | ``.request``    | switch          | Press this      |
| i_set_startup`` |                 |                 | switch to       |
|                 |                 |                 | configure with  |
|                 |                 |                 | the startup ROI |
|                 |                 |                 | (see options    |
|                 |                 |                 | below).         |
+-----------------+-----------------+-----------------+-----------------+

The default ROI can be configured with the following options. This ROI
will be set each time the camera software is re-started or the camera is
powered-on.

+-------+-----------------+-----------------+-------+-----------------+
| Short | Long            | Config-File     | Type  | Description     |
+=======+=================+=================+=======+=================+
|       | –c              | c               | float | The default ROI |
|       | amera.startup_x | amera.startup_x |       | x position.     |
+-------+-----------------+-----------------+-------+-----------------+
|       | –c              | c               | float | The default ROI |
|       | amera.startup_y | amera.startup_y |       | y position.     |
+-------+-----------------+-----------------+-------+-----------------+
|       | –c              | c               | int   | The default ROI |
|       | amera.startup_w | amera.startup_w |       | width.          |
+-------+-----------------+-----------------+-------+-----------------+
|       | –c              | c               | int   | The default ROI |
|       | amera.startup_h | amera.startup_h |       | height.         |
+-------+-----------------+-----------------+-------+-----------------+
|       | –camer          | camer           | int   | The default ROI |
|       | a.startup_bin_x | a.startup_bin_x |       | x binning.      |
+-------+-----------------+-----------------+-------+-----------------+
|       | –camer          | camer           | int   | The default ROI |
|       | a.startup_bin_y | a.startup_bin_y |       | y binning.      |
+-------+-----------------+-----------------+-------+-----------------+

Exposure Control
~~~~~~~~~~~~~~~~

All MagAO-X cameras operate in free-run, meaning images are taken
continuously with no user intervention needed. The exposure time is
either set directly, or by setting the frame rate, or both. In cases
where both options are given, see the camera specific documentation for
details of how they are related. The INDI properties for controlling
exposure time and frame rate are:

======== ============ ===== ============================================
Property Element      Type  Description
======== ============ ===== ============================================
.exptime ``.current`` float the current exposure time, in seconds.
\        ``.target``  float the target exposure time, in second.
.fps     ``.current`` float the current framerate, in frames per second.
\        ``.target``  float the target frame rate, in frames per second.
======== ============ ===== ============================================

Shutters
~~~~~~~~

If the camera has an associated shutter, it is controlled with the
following properties

+-----------------+-----------------+-----------------+-----------------+
| Property        | Element         | Type            | Description     |
+=================+=================+=================+=================+
| ``.s            | ``.status``     | string          | Status of the   |
| hutter_status`` |                 |                 | shutter,        |
|                 |                 |                 | e.g. POWEROFF,  |
|                 |                 |                 | READY, etc.     |
+-----------------+-----------------+-----------------+-----------------+
| ``.shutter``    | ``.toggle``     | toggle switch   | Current state   |
|                 |                 |                 | of the shutter: |
|                 |                 |                 | ON = SHUT       |
|                 |                 |                 | (``|X|``), OFF =|
|                 |                 |                 | OPEN (``|O|``). |
|                 |                 |                 | Toggling the    |
|                 |                 |                 | switch changes  |
|                 |                 |                 | state.          |
+-----------------+-----------------+-----------------+-----------------+

Uniblitz DSS Shutters
^^^^^^^^^^^^^^^^^^^^^

The cameras which use the Uniblitz DSS shutter control have the
following additional configuration options

+-------------+-------------+-------------+-------------+-------------+
| Short       | Long        | Config-File | Type        | Description |
+=============+=============+=============+=============+=============+
|             | ``-         | `           | string      | The device  |
|             | -shutter.po | `shutter.po |             | controlling |
|             | werDevice`` | werDevice`` |             | this        |
|             |             |             |             | shutter’s   |
|             |             |             |             | power       |
+-------------+-------------+-------------+-------------+-------------+
|             | ``--        | ``          | string      | The channel |
|             | shutter.pow | shutter.pow |             | controlling |
|             | erChannel`` | erChannel`` |             | this        |
|             |             |             |             | shutter’s   |
|             |             |             |             | power       |
+-------------+-------------+-------------+-------------+-------------+
|             | `           | ``shutter.  | string      | The device  |
|             | `--shutter. | dioDevice`` |             | controlling |
|             | dioDevice`` |             |             | this        |
|             |             |             |             | shutter’s   |
|             |             |             |             | digital     |
|             |             |             |             | I/O.        |
+-------------+-------------+-------------+-------------+-------------+
|             | ``--s       | ``s         | string      | The channel |
|             | hutter.sens | hutter.sens |             | reading     |
|             | orChannel`` | orChannel`` |             | this        |
|             |             |             |             | shutter’s   |
|             |             |             |             | sensor.     |
+-------------+-------------+-------------+-------------+-------------+
|             | ``--shu     | ``shu       | int         | The time to |
|             | tter.wait`` | tter.wait`` |             | pause       |
|             |             |             |             | between     |
|             |             |             |             | checks of   |
|             |             |             |             | the sensor  |
|             |             |             |             | state       |
|             |             |             |             | during      |
|             |             |             |             | open/shut   |
|             |             |             |             | [msec].     |
|             |             |             |             | Default is  |
|             |             |             |             | 100.        |
+-------------+-------------+-------------+-------------+-------------+
|             | ``--shutte  | ``shutte    | int         | Total time  |
|             | r.timeout`` | r.timeout`` |             | to wait for |
|             |             |             |             | sensor to   |
|             |             |             |             | change      |
|             |             |             |             | state       |
|             |             |             |             | before      |
|             |             |             |             | timing out  |
|             |             |             |             | [msec].     |
|             |             |             |             | Default is  |
|             |             |             |             | 2000.       |
+-------------+-------------+-------------+-------------+-------------+

Temperature
~~~~~~~~~~~

All current cameras provide a measurement of the detector temperature.
Most provide a way to control the temperature based on a set point.

+-----------------+-----------------+-----------------+-----------------+
| Property        | Element         | Type            | Description     |
+=================+=================+=================+=================+
| ``.temp_ccd``   | ``.current``    | float           | the current     |
|                 |                 |                 | detector        |
|                 |                 |                 | temperature, in |
|                 |                 |                 | C.              |
+-----------------+-----------------+-----------------+-----------------+
|                 | ``.target``     | float           | only if         |
|                 |                 |                 | temperature     |
|                 |                 |                 | control is      |
|                 |                 |                 | offered, the    |
|                 |                 |                 | target          |
|                 |                 |                 | temperature to  |
|                 |                 |                 | set.            |
+-----------------+-----------------+-----------------+-----------------+
| ``.te           | ``.toggle``     | toggle switch   | switch to turn  |
| mp_controller`` |                 |                 | on/off the      |
|                 |                 |                 | temperature     |
|                 |                 |                 | control system  |
|                 |                 |                 | for this        |
|                 |                 |                 | camera.         |
+-----------------+-----------------+-----------------+-----------------+
| ``              | ``.status``     | string          | the state of    |
| .temp_control`` |                 |                 | the temperature |
|                 |                 |                 | control,        |
|                 |                 |                 | indicating      |
|                 |                 |                 | whether it is   |
|                 |                 |                 | on target, etc. |
+-----------------+-----------------+-----------------+-----------------+

The following configuration options also affect temperature:

+-------------+-------------+-------------+-------------+-------------+
| Short       | Long        | Config-File | Type        | Description |
+=============+=============+=============+=============+=============+
|             | ``          | ``camera.st | float       | the         |
|             | --camera.st | artupTemp`` |             | temperature |
|             | artupTemp`` |             |             | setpoint to |
|             |             |             |             | set at      |
|             |             |             |             | startup     |
+-------------+-------------+-------------+-------------+-------------+

Framegrabber Interface
----------------------

The standard MagAO-X framegrabber system is used by any application
which collects images from hardware and writes them to a shared memory
stream. All cameras are framegrabbers. The following INDI properties
provide details about the framegrabber:

+-----------------+-----------------+-----------------+-----------------+
| Property        | Element         | Type            | Description     |
+=================+=================+=================+=================+
| ``              | ``.name``       | string          | The name of the |
| .fg_shmimname`` |                 |                 | ImageStreamIO   |
|                 |                 |                 | shared memory   |
|                 |                 |                 | image. Will be  |
|                 |                 |                 | seen as         |
|                 |                 |                 | /mi             |
|                 |                 |                 | lk/shm/.im.shm. |
+-----------------+-----------------+-----------------+-----------------+
| ``              | ``.width``      | int             | The width of    |
| .fg_framesize`` |                 |                 | the frame in    |
|                 |                 |                 | memory.         |
+-----------------+-----------------+-----------------+-----------------+
|                 | ``.height``     | int             | The height of   |
|                 |                 |                 | the frame in    |
|                 |                 |                 | memory.         |
+-----------------+-----------------+-----------------+-----------------+

The following configuration options will be available in any application
which is a framegrabber:

+-------------+-------------+-------------+-------------+-------------+
| Short       | Long        | Config-File | Type        | Description |
+=============+=============+=============+=============+=============+
|             | –f          | f           | int         | The         |
|             | ramegrabber | ramegrabber |             | real-time   |
|             | .threadPrio | .threadPrio |             | priority of |
|             |             |             |             | the         |
|             |             |             |             | f           |
|             |             |             |             | ramegrabber |
|             |             |             |             | thread.     |
+-------------+-------------+-------------+-------------+-------------+
|             | –           | framegrabbe | string      | The name of |
|             | framegrabbe | r.shmimName |             | the         |
|             | r.shmimName |             |             | Im          |
|             |             |             |             | ageStreamIO |
|             |             |             |             | shared      |
|             |             |             |             | memory      |
|             |             |             |             | image. Will |
|             |             |             |             | be used as  |
|             |             |             |             | /milk/s     |
|             |             |             |             | hm/.im.shm. |
+-------------+-------------+-------------+-------------+-------------+
|             | –frame      | frame       | int         | The length  |
|             | grabber.cir | grabber.cir |             | of the      |
|             | cBuffLength | cBuffLength |             | circular    |
|             |             |             |             | buffer.     |
|             |             |             |             | Sets        |
|             |             |             |             | m_circ      |
|             |             |             |             | BuffLength, |
|             |             |             |             | default is  |
|             |             |             |             | 1.          |
+-------------+-------------+-------------+-------------+-------------+

EDT Framegrabbers
~~~~~~~~~~~~~~~~~

A camera which uses an EDT framegrabber (PCIe card) will have the
following additional configuration options:

+-------------+-------------+-------------+-------------+-------------+
| Short       | Long        | Config-File | Type        | Description |
+=============+=============+=============+=============+=============+
|             | –framegrabb | framegrabb  | int         | The EDT PDV |
|             | er.pdv_unit | er.pdv_unit |             | f           |
|             |             |             |             | ramegrabber |
|             |             |             |             | unit        |
|             |             |             |             | number.     |
|             |             |             |             | Default is  |
|             |             |             |             | 0.          |
+-------------+-------------+-------------+-------------+-------------+
|             | –fr         | fr          | int         | The EDT PDV |
|             | amegrabber. | amegrabber. |             | f           |
|             | pdv_channel | pdv_channel |             | ramegrabber |
|             |             |             |             | channel     |
|             |             |             |             | number.     |
|             |             |             |             | Default is  |
|             |             |             |             | 0.          |
+-------------+-------------+-------------+-------------+-------------+
|             | –framegrabb | framegrabb  | int         | The EDT PDV |
|             | er.numBuffs | er.numBuffs |             | f           |
|             |             |             |             | ramegrabber |
|             |             |             |             | DMA buffer  |
|             |             |             |             | size        |
|             |             |             |             | [images].   |
|             |             |             |             | Default is  |
|             |             |             |             | 4.          |
+-------------+-------------+-------------+-------------+-------------+

baslerCtrl
----------

``baslerCtrl`` controls a Basler camera. It monitors and logs
temperatures, configures the camera for the desired mode of operation,
and manages the grabbing and processing of frames. It is a MagAO-X
`standard camera <#Standard-Camera-Interface>`__ and a `standard
framegrabber <#Framegrabber-Interface>`__.

.. _exposure-control-1:

Exposure Control
~~~~~~~~~~~~~~~~

The basler cameras use exposure time. Acquisition FPS can be set as an
upper limit. As long as exposure time and ROI can support the set FPS,
then it will be the framerate of the camera but actual exposure time
will not change. Setting ``{name}.fps.target=0`` causes the camera to
run at its maximum possible FPS for its configuration.

.. _regions-of-interest-1:

Regions of Interest
~~~~~~~~~~~~~~~~~~~

Basler cameras support `ROIs <#Regions-of-Interest>`__. Note that there
are restrictions on possible settings, which depend on camera model. For
instance, the width or height may only be settable in multiples of 2 or
4.

.. _temperature-1:

Temperature
~~~~~~~~~~~

Temperature is passively monitored only.

Options
~~~~~~~

Basler specific configuration options are:

+-------------+-------------+-------------+-------------+-------------+
| Short       | Long        | Config-File | Type        | Description |
+=============+=============+=============+=============+=============+
|             | ``-         | `           | string      | The         |
|             | -camera.ser | `camera.ser |             | identifying |
|             | ialNumber`` | ialNumber`` |             | serial      |
|             |             |             |             | number of   |
|             |             |             |             | the camera. |
|             |             |             |             | This is     |
|             |             |             |             | required to |
|             |             |             |             | connect.    |
+-------------+-------------+-------------+-------------+-------------+
|             | ``--ca      | ``ca        | int         | The number  |
|             | mera.bits`` | mera.bits`` |             | of bits     |
|             |             |             |             | used by the |
|             |             |             |             | camera.     |
|             |             |             |             | Default is  |
|             |             |             |             | 10.         |
+-------------+-------------+-------------+-------------+-------------+

ocam2KCtrl
----------

``ocam2KCtrl`` controls the OCAM 2K EMCCD, which serves as the pyramid
wavefront sensor detector in MagAO-X. It monitors and logs temperatures,
configures the camera for the desired mode of operation, and manages the
grabbing and processing of frames. It is a MagAO-X `standard
camera <#Standard-Camera-Interface>`__ and a `standard
framegrabber <#Framegrabber-Interface>`__ using the `EDT
interface <#EDT-Framegrabbers>`__.

.. _options-1:

Options
~~~~~~~

OCAM specific configuration options are:

+-------------+-------------+-------------+-------------+-------------+
| Short       | Long        | Config-File | Type        | Description |
+=============+=============+=============+=============+=============+
|             | ``--camer   | ``camer     | string      | The path of |
|             | a.ocamDescr | a.ocamDescr |             | the OCAM    |
|             | ambleFile`` | ambleFile`` |             | descramble  |
|             |             |             |             | file,       |
|             |             |             |             | relative to |
|             |             |             |             | Mag         |
|             |             |             |             | AOX/config. |
+-------------+-------------+-------------+-------------+-------------+
|             | ``--camera. | ``camera.   | unsigned    | The maximum |
|             | maxEMGain`` | maxEMGain`` | int         | EM gain     |
|             |             |             |             | which can   |
|             |             |             |             | be set by   |
|             |             |             |             | user.       |
|             |             |             |             | Default is  |
|             |             |             |             | 600. Min is |
|             |             |             |             | 1, max is   |
|             |             |             |             | 600.        |
+-------------+-------------+-------------+-------------+-------------+
