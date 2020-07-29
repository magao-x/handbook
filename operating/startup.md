# System startup

Once the instrument has been unpacked and cabled, the power-up process begins. Subsequent startup will look the same, with the exception of step 3 (devices that should stay on).

The following assumes you're sitting at the AOC workstation, but it could be done anywhere with appropriate network tunnels. When one must SSH to different hosts, the one where the command should be run will be indicated before the prompt, like `aoc$ ls` to run `ls` on AOC. (Don't type the `host$` prefix, or any comment lines starting with `#`.)

For simplicity, it's easiest to run these commands as the user `xsup` to ensure you can read shared memory images (shmims) and `ssh` around to RTC and ICC.

1. Ensure the MagAO-X apps are started on AOC to get power control (see the [guide to xctrl](./xctrl.md) for more detail)

    ```
    aoc$ xctrl startup
    # you'll see some output as the processes start, wait a little bit
    aoc$ xctrl status
    # verify processes are all green/running
    ```

2. You should have power control now. AOC talks over the instrument internal LAN to network-controlled power strips (PDUs), which you can control over INDI via several different interfaces: `sup`, `cursesINDI`, or `pwrGUI`.

    Since you're sitting at AOC, it's simplest to open `pwrGUI`. You should see switches appear.

    ```
    aoc$ pwrGUI &
    # window should pop open with switches
    ```

3. (Initial startup only) The following devices should be powered up, and never powered off (unless you know what you're doing):

    - swinst
    - compicc
    - comprtc
    - dcpwr
    - usbdu0
    - blower
    - fan1
    - fan2
    - instcool

4. If the tweeter is going to be used, turn on the dry air supply (N2 bottle for now) and wait for the relative humidity to drop below 15%. This will take a while, but while you wait...

5. Ensure MagAO-X processes are started on ICC and RTC

    ```
    aoc$ ssh icc
    icc$ xctrl startup
    icc$ xctrl status
    # verify processes are all green/running
    icc$ exit
    aoc$ ssh rtc
    rtc$ xctrl startup
    rtc$ xctrl status
    # verify processes are all green/running
    rtc$ exit
    ```

6. Power up the necessary components for what you want to do, e.g. for lab work using AO + camsci1:

    - pdu0: source (calibration light source)
    - pdu1: ttmmod (pyramid modulation mirror), ttmpupil (pupil tracking mirror), dmwoofer (low order upstream DM), dmncpc (low order non-common-path DM)
    - pdu2: camsci1
    - dcdu1: shsci1 (camera shutter)
    - usbdu0: camtip (Basler viewing pyramid tip)

    This is a minimal list. To adjust focus and filters on camsci1, you'll also need:

    - pdu2 and usbdu0: stagezaber
    - usbdu0 and dcdu0: fwscind
    - dcdu0: fwpupil, fwsci1
    - dcdu1: fwbs

    With even more things to power up for camsci2, etc. Be sure to home stages that need it before use! (They'll appear as `NOTHOMED` in their `fsm` INDI property.)

7. Launch dmCtrlGUI, hit "reload flat" and "set flat" to flatten the DMs

    ```
    aoc$ dmCtrlGUI dmncpc &
    aoc$ dmCtrlGUI dmwoofer &
    ```

8. Launch camera viewers, e.g. for `camtip` and `camsci1`:

    ```
    aoc$ rtimv camsci1 &
    aoc$ rtimv camtip &
    ```

    **Note:** This needs to read shmims, and should be run as `xsup` if you're not logged in as `xsup` already (i.e. `su xsup` before running `rtimv`).

9. Launch `pupilGuideGUI`

    ```
    aoc$ pupilGuideGUI
    ```

    Now `Set` the pupil TTM and `Set` the pyramid modulator TTM. If the PSF isn’t centered on camtip, use the arrows (bottom left of pupilGuideGUI interface) to change the voltage bias. The central button changes the voltage step size.

10. **Once the tweeter relative humidity is less than 15%**, power it on (it's on pdu1)
11. Start dmCtrlGUI for `dmtweeter`:

    ```
    aoc$ dmCtrlGUI dmtweeter
    ```

    Now `Reload flat` and `Set flat`.
12. Optimize PSF quality with [The Eye Doctor](eyedoctor.md), starting with the `camtip` PSF

    ```
    aoc$ ssh icc
    icc$ dm_eye_doctor 7626 wooferModes camtip 10 2 1.0
    icc$ dm_eye_doctor 7626 wooferModes camtip 10 2...10 0.5
    icc$ dm_eye_doctor 7626 wooferModes camtip 10 2...35 0.05
    ```

    If you want to save this optimized woofer flat, you can do that on RTC:

    ```
    aoc$ ssh rtc
    rtc$ dm_eye_doctor_update_flat dmwoofer
    ```
13. Optimize the non-common-path correction with The Eye Doctor and `camsci1`

    ```
    icc$ dm_eye_doctor 7624 ncpcModes camsci1 5 2 1.0
    icc$ dm_eye_doctor 7624 ncpcModes camsci1 5 2…10 0.5
    icc$ dm_eye_doctor 7624 ncpcModes camsci1 5 2...35 0.05
    # note: still on icc
    icc$ dm_eye_doctor_update_flat dmncpc
    ```

Now you're ready to do things with the instrument! 

Open http://localhost:8000/ (or tunnel it to your computer from AOC) to use the web UI for filter wheels, stage positions, streamwriter and shutter toggles, etc. You can also control the instrument via the AOC indiserver on port 7624 with your favorite tool (`cursesINDI`, [PurePyINDI](https://github.com/magao-x/purepyindi), or what have you).