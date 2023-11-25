import logging

import pytest

from saltfactories.daemons.container import SaltMinion
from saltfactories.utils import random_string

docker = pytest.importorskip("docker")

log = logging.getLogger(__name__)


pytestmark = [
    # We can't pass ``extra_cli_arguments_after_first_start_failure``, but this is solvable,
    # but we also rely on container volume binds, which, when running against the system,
    # means trying to bind `/`, which is not possible, hence, we're skipping this test.
    pytest.mark.skip_on_salt_system_service,
    pytest.mark.skip_on_darwin,
    pytest.mark.skip_on_windows,
]


@pytest.fixture(scope="session")
def docker_client(salt_factories, docker_client):
    if salt_factories.system_service:  # pragma: no cover
        msg = "Test should not run against system install of Salt"
        raise pytest.skip.Exception(msg, _use_item_location=True)
    return docker_client


@pytest.fixture
def minion_id(salt_version):
    return random_string(f"salt-minion-{salt_version}-", uppercase=False)


@pytest.fixture(scope="module")
def salt_master(salt_factories, host_docker_network_ip_address):
    config_overrides = {
        "interface": host_docker_network_ip_address,
        "log_level_logfile": "quiet",
        # We also want to scrutinize the key acceptance
        "open_mode": True,
    }
    factory = salt_factories.salt_master_daemon(
        random_string("master-"),
        overrides=config_overrides,
    )
    with factory.started():
        yield factory


@pytest.fixture
def salt_minion(
    minion_id,
    salt_master,
    docker_client,
    host_docker_network_ip_address,
):
    config_overrides = {
        "master": salt_master.config["interface"],
        "user": "root",
        "pytest-minion": {
            "log": {"host": host_docker_network_ip_address},
            "returner_address": {"host": host_docker_network_ip_address},
        },
        # We also want to scrutinize the key acceptance
        "open_mode": False,
    }
    factory = salt_master.salt_minion_daemon(
        minion_id,
        overrides=config_overrides,
        factory_class=SaltMinion,
        extra_cli_arguments_after_first_start_failure=["--log-level=debug"],
        # SaltMinion kwargs
        name=minion_id,
        image="ghcr.io/saltstack/salt-ci-containers/salt:3005",
        docker_client=docker_client,
        start_timeout=120,
        pull_before_start=False,
    )
    with factory.started():
        yield factory


@pytest.fixture
def salt_cli(salt_master, salt_cli_timeout):
    return salt_master.salt_cli(timeout=salt_cli_timeout)


def test_minion(salt_minion, salt_cli):
    assert salt_minion.is_running()
    ret = salt_cli.run("test.ping", minion_tgt=salt_minion.id)
    assert ret.returncode == 0, ret
    assert ret.data is True
