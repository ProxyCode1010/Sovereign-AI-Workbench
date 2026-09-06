import docker
import uuid
import os
from config import SANDBOX_IMAGE

_client = docker.from_env()

# This must be the path on the HOST machine, since docker.sock talks to the host daemon.
# Set this to match wherever your project folder actually sits on Windows.
HOST_SANDBOX_DIR = os.getenv("HOST_SANDBOX_DIR", "/app/data/sandbox_tmp")
CONTAINER_SANDBOX_DIR = "/app/data/sandbox_tmp"

def run_code_in_sandbox(code: str, timeout: int = 20) -> dict:
    job_id = str(uuid.uuid4())
    script_name = f"script_{job_id}.py"
    container_script_path = os.path.join(CONTAINER_SANDBOX_DIR, script_name)

    with open(container_script_path, "w") as f:
        f.write(code)

    host_script_dir = os.getenv("HOST_SANDBOX_DIR_ABS")  # set via .env, see below

    try:
        container = _client.containers.run(
            SANDBOX_IMAGE,
            command=["python3", f"/workspace/{script_name}"],
            volumes={host_script_dir: {"bind": "/workspace", "mode": "ro"}},
            network_disabled=True,
            mem_limit="256m",
            nano_cpus=1_000_000_000,
            detach=True,
            remove=False,
            stdout=True,
            stderr=True,
        )
        try:
            result = container.wait(timeout=timeout)
            logs = container.logs().decode("utf-8", errors="ignore")
            exit_code = result.get("StatusCode", -1)
        finally:
            container.remove(force=True)
            os.remove(container_script_path)

        return {"exit_code": exit_code, "output": logs}
    except Exception as e:
        return {"exit_code": -1, "output": f"Sandbox error: {e}"}