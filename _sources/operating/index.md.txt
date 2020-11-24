# Operation of the MagAO-X instrument

The MagAO-X instrument has (at last count) several thousand controllable degrees of freedom, three computers, and dozens of processes. To manage that complexity, we have the guides and tools detailed herein.

Good starting points include the [startup](./startup.md) guide and the [troubleshooting](./troubleshooting.md) guide. Useful tools include [xctrl](./software/utils/xctrl.md), [cursesINDI](./software/utils/cursesINDI.md), and [logdump](./software/utils/logdump.md).

Viewing camera output and DM input (really, any shared memory image) uses `rtimv`, which is documented in its own [User Guide](https://github.com/jaredmales/rtimv/blob/master/doc/UserGuide.md).

```eval_rst
.. toctree::
    :maxdepth: 2

    startup
    shutdown
    software/apps/index
    software/utils/index
    troubleshooting
```
