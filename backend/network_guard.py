import socket
import logging
from config import ALLOWED_OUTBOUND_HOSTS

logger = logging.getLogger("network_guard")
logging.basicConfig(filename="/app/data/outputs/network_audit.log", level=logging.INFO)

_original_getaddrinfo = socket.getaddrinfo

def _guarded_getaddrinfo(host, *args, **kwargs):
    if host not in ALLOWED_OUTBOUND_HOSTS and host not in ("localhost", "127.0.0.1"):
        logger.warning(f"BLOCKED outbound resolution attempt to: {host}")
        raise OSError(f"Network guard: connections to '{host}' are not permitted (air-gapped mode).")
    logger.info(f"ALLOWED internal connection to: {host}")
    return _original_getaddrinfo(host, *args, **kwargs)

def install_guard():
    socket.getaddrinfo = _guarded_getaddrinfo
    logger.info("Network guard installed. Allowed hosts: %s", ALLOWED_OUTBOUND_HOSTS)