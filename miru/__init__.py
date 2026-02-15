import sys
from importlib.machinery import EXTENSION_SUFFIXES
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


def _maybe_extend_package_path_for_meson() -> None:
    """
    Meson places the compiled native extension in the build directory.

    When importing from the source tree, we extend this package's search path so
    `from . import _miru` can resolve the extension from the build output.
    """

    package_dir = Path(__file__).resolve().parent

    try:
        miru_library_dir = Path(__file__).resolve().parents[3]
    except IndexError:
        return

    build_package_dir = miru_library_dir / "build" / "subprojects" / "miru-python" / "miru"
    if not build_package_dir.is_dir() or build_package_dir == package_dir:
        return

    has_extension = any(
        (build_package_dir / "_miru" / ("_miru" + suffix)).is_file()
        or (build_package_dir / ("_miru" + suffix)).is_file()
        for suffix in EXTENSION_SUFFIXES
    )
    if not has_extension:
        return

    build_dir = str(build_package_dir)
    if build_dir not in __path__:
        __path__.append(build_dir)


_maybe_extend_package_path_for_meson()

try:
    from . import _miru as _miru
    if not hasattr(_miru, "__version__"):
        from ._miru import _miru as _miru
        sys.modules[__name__ + "._miru"] = _miru
except Exception as ex:
    print("")
    print("***")
    if str(ex).startswith("No module named "):
        print("Miru native extension not found")
        print("Please check your PYTHONPATH.")
    else:
        print(f"Failed to load the Miru native extension: {ex}")
        print("Please ensure that the extension was compiled correctly")
    print("***")
    print("")
    raise ex
from . import core

__version__: str = _miru.__version__

get_device_manager = core.get_device_manager
Relay = _miru.Relay
PortalService = core.PortalService
EndpointParameters = core.EndpointParameters
Compiler = core.Compiler
PackageManager = core.PackageManager
FileMonitor = _miru.FileMonitor
Cancellable = core.Cancellable

ServerNotRunningError = _miru.ServerNotRunningError
ExecutableNotFoundError = _miru.ExecutableNotFoundError
ExecutableNotSupportedError = _miru.ExecutableNotSupportedError
ProcessNotFoundError = _miru.ProcessNotFoundError
ProcessNotRespondingError = _miru.ProcessNotRespondingError
InvalidArgumentError = _miru.InvalidArgumentError
InvalidOperationError = _miru.InvalidOperationError
PermissionDeniedError = _miru.PermissionDeniedError
AddressInUseError = _miru.AddressInUseError
TimedOutError = _miru.TimedOutError
NotSupportedError = _miru.NotSupportedError
ProtocolError = _miru.ProtocolError
TransportError = _miru.TransportError
OperationCancelledError = _miru.OperationCancelledError


def query_system_parameters() -> Dict[str, Any]:
    """
    Returns a dictionary of information about the host system
    """

    return get_local_device().query_system_parameters()


def spawn(
    program: Union[str, List[Union[str, bytes]], Tuple[Union[str, bytes]]],
    argv: Union[None, List[Union[str, bytes]], Tuple[Union[str, bytes]]] = None,
    envp: Optional[Dict[str, str]] = None,
    env: Optional[Dict[str, str]] = None,
    cwd: Optional[str] = None,
    stdio: Optional[str] = None,
    **kwargs: Any,
) -> int:
    """
    Spawn a process into an attachable state
    """

    return get_local_device().spawn(program=program, argv=argv, envp=envp, env=env, cwd=cwd, stdio=stdio, **kwargs)


def resume(target: core.ProcessTarget) -> None:
    """
    Resume a process from the attachable state
    :param target: the PID or name of the process
    """

    get_local_device().resume(target)


def kill(target: core.ProcessTarget) -> None:
    """
    Kill a process
    :param target: the PID or name of the process
    """

    get_local_device().kill(target)


def attach(
    target: core.ProcessTarget, realm: Optional[str] = None, persist_timeout: Optional[int] = None
) -> core.Session:
    """
    Attach to a process
    :param target: the PID or name of the process
    """

    return get_local_device().attach(target, realm=realm, persist_timeout=persist_timeout)


def inject_library_file(target: core.ProcessTarget, path: str, entrypoint: str, data: str) -> int:
    """
    Inject a library file to a process.
    :param target: the PID or name of the process
    """

    return get_local_device().inject_library_file(target, path, entrypoint, data)


def inject_library_blob(target: core.ProcessTarget, blob: bytes, entrypoint: str, data: str) -> int:
    """
    Inject a library blob to a process
    :param target: the PID or name of the process
    """

    return get_local_device().inject_library_blob(target, blob, entrypoint, data)


def get_local_device() -> core.Device:
    """
    Get the local device
    """

    return get_device_manager().get_local_device()


def get_remote_device() -> core.Device:
    """
    Get the first remote device in the devices list
    """

    return get_device_manager().get_remote_device()


def get_usb_device(timeout: int = 0) -> core.Device:
    """
    Get the first device connected over USB in the devices list
    """

    return get_device_manager().get_usb_device(timeout)


def get_device(id: Optional[str], timeout: int = 0) -> core.Device:
    """
    Get a device by its id
    """

    return get_device_manager().get_device(id, timeout)


def get_device_matching(predicate: Callable[[core.Device], bool], timeout: int = 0) -> core.Device:
    """
    Get device matching predicate.
    :param predicate: a function to filter the devices
    :param timeout: operation timeout in seconds
    """

    return get_device_manager().get_device_matching(predicate, timeout)


def enumerate_devices() -> List[core.Device]:
    """
    Enumerate all the devices from the device manager
    """

    return get_device_manager().enumerate_devices()


@core.cancellable
def shutdown() -> None:
    """
    Shutdown the main device manager
    """

    get_device_manager()._impl.close()
