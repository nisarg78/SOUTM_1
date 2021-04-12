import logging
from typing import Tuple

from valve import rcon

logger = logging.getLogger(__name__)


def execute_rcon_cmd(cmd: str, server_address: Tuple[str, int], rcon_password: str, retry: bool = True):
    logger.debug(
        "Running command %s on server %s:%s", cmd, server_address[0], server_address[1]
    )
    try:
        with rcon.RCON(server_address, rcon_password) as server_rcon:
            return server_rcon(cmd)
    except TimeoutError:
        if retry:
            logger.debug("Command timedout, retrying")
            return execute_rcon_cmd(cmd, server_address, rcon_password, retry=False)
        return "Command timedout"
    except Exception as e:
        logger.exception("Unknown error during execution of rcon cmd")
        return str(e)
