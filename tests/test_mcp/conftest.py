import os

import pytest

os.environ["ORRERY_TELEMETRY_ENABLED"] = "false"


@pytest.fixture(scope="module")
def anyio_backend() -> str:
    return "asyncio"
