# System Maintenance & Administration

## Adding a new user or developer account

User accounts on the RTC, ICC, and AOC machines are members of `magaox`. Developer accounts are additionally members of `magaox-dev` and `wheel`.

`/opt/MagAOX/source/MagAOX/setup/` contains scripts to help you remember which groups and what permissions the `~/.ssh` folder should have.

### `add_a_user.sh`

Creates a new user account in the group `magaox`, creates `.ssh` (`u=rwx,g=r,o=r`), and `.ssh/authorized_keys` (`u=rw,g=,o=`).

Example:

```
$ /opt/MagAOX/source/MagAOX/setup/add_a_user.sh klmiller
```

### `add_a_developer.sh`

Just like `add_a_user.sh` (in fact, uses it). Additionally adds the new account to the `wheel` (RTC/ICC) or `sudo` (AOC) group and `magaox-dev` groups.

## Configuring git for a new user account

We use GitHub Personal Access Tokens coupled with HTTPS push to synchronize changes on the instrument. Configuration is required for your credentials to be remembered.

1. Log in to the computer (AOC, RTC, ICC, vm, etc) where you want to configure git
2. Change directories to a repository (e.g. `cd /opt/MagAOX/calib`) and verify it is set up for HTTPS push:
   ```
   $ cd /opt/MagAOX/calib
   $ git remote -v
   origin	https://github.com/magao-x/calib.git (fetch)
   origin	https://github.com/magao-x/calib.git (push)
   ```
3. If you haven't already for this machine, configure your name and email address:
   ```
   $ git config --global user.email "youremailusernamehere@youremaildomainhere.com"
   $ git config --global user.name "Your Name Here"
   ```
4. Configure the 'store' credential helper, which will store your credentials so you do not have to re-enter them:
   ```
   $ git config --global credential.helper store
   ```
5. Create (or retrieve from your password manager) a GitHub Personal Access Token. If you don't have one, log in to GitHub and visit [https://github.com/settings/tokens](https://github.com/settings/tokens).
6. Attempt to push, and enter/paste your username and **personal access token as password**:
   ```
   $ git push
   Username for 'https://github.com/magao-x/calib.git': your-github-user-name
   Password for 'https://your-github-user-name@github.com/magao-x/calib.git':
   ```
   (Note that even if you don't see it, your key is being entered.)
7. Attempt to push again. You should not be prompted for credentials a second time.

## Upgrading NVIDIA CUDA and drivers

The CUDA install script at https://github.com/magao-x/MagAOX/blob/master/setup/steps/install_cuda.sh will install CUDA on a new system (provided that [pre_provision.sh](https://github.com/magao-x/MagAOX/blob/master/setup/pre_provision.sh) is run first, and the system is rebooted).

Upgrading CUDA is more involved, as the systems stubbornly insist on loading the driver even when asked nicely not to, and the installer won't work if the driver is loaded.

1. (on AOC only) Default to text-based boot: `systemctl set-default multi-user.target`
2. Disable all the driver modules.

   Open `/etc/default/grub` and append the following to the line beginning `GRUB_CMDLINE_LINUX_DEFAULT` (inside the quotes):

   ```
   nvidia_modeset.blacklist=1 nvidia_uvm.blacklist=1 nvidia.blacklist=1 rd.driver.blacklist=nvidia_modeset,nvidia_uvm,nvidia
   ```
3. Install the new config with `sudo grub2-mkconfig -o /boot/grub2/grub.cfg`
4. Reboot, verify with `lsmod | grep nv` that no driver modules loaded
5. Use `sudo /usr/bin/nvidia-uninstall` to uninstall the driver
6. Use `sudo /usr/local/cuda/bin/cuda-uninstaller` to uninstall CUDA
7. Remove the options to disable the driver.

   Open `/etc/default/grub` and remove the added options from `GRUB_CMDLINE_LINUX_DEFAULT`.
8. Install the new config with `sudo grub2-mkconfig -o /boot/grub2/grub.cfg`
9. Reboot again! Verify no driver is loaded again!
10. Install CUDA using `sudo bash -x /opt/MagAOX/source/MagAOX/setup/steps/install_cuda.sh`
11. (on AOC only) Default to graphical boot again with  `systemctl set-default multi-user.target` and complete boot to graphical desktop with  `systemctl isolate graphical.target`
