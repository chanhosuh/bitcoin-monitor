import pydevd


def set_trace():
    """
    To use Eclipse's Pydev debugging in the Django docker
    container:

    1. in the docker container:

        pip install pydevd

    or add it to container's requirements.

    2. set this in environment-dev-local.env:

        PYTHONBREAKPOINT=bitcoin_monitor.pydevd.set_trace

    The reason we don't use pydevd.settrace directly is
    that it requires the host argument so Docker knows
    the IP to reach out to from the container, but
    it's annoying to have to always do:

        breakpoint('docker.for.mac.localhost')

    An alternative is to use a PyDev editor template,
    which is how the above 'pydev' autocomplete works.

    3. set a Python breakpoint in your code, start
    up the Pydev debug server in Eclipse, debug away!
    """
    pydevd.settrace('docker.for.mac.localhost')
