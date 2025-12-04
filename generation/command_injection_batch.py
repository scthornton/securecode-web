"""
Command Injection Example Generator - Batch 002

Generates 5 high-quality command injection examples across 5 languages:
- Python (subprocess with shell=True)
- PHP (shell_exec vulnerability)
- Java (Runtime.exec)
- JavaScript/Node.js (child_process)
- Go (exec.Command)
"""

import json
from datetime import datetime
from pathlib import Path

# Real-world context for command injection
BARRACUDA_CONTEXT = {
    "real_world_incident": "2023 Barracuda ESG zero-day command injection",
    "impact": "Chinese espionage campaign, global targeting, 0-day exploitation",
    "attack_vector": "Command injection via email attachment processing",
    "cve": "CVE-2023-2868",
    "year": 2023
}

GITLAB_CONTEXT = {
    "real_world_incident": "2021 GitLab RCE via ExifTool command injection",
    "impact": "Critical RCE allowing server takeover, widely exploited",
    "attack_vector": "Command injection in image metadata processing",
    "cve": "CVE-2021-22205",
    "year": 2021
}


def create_base_metadata(lang, example_num):
    """Create base metadata structure"""
    return {
        "lang": lang,
        "category": "injection",
        "subcategory": "command_injection",
        "owasp_2021": "A03:2021-Injection",
        "cwe": "CWE-78",
        "severity": "CRITICAL",
        "complexity": "moderate",
        "created": datetime.now().strftime('%Y-%m-%d'),
        "validated": False
    }


def python_subprocess_injection():
    """Python - Command injection via subprocess"""
    return {
        "id": "command-injection-000001",
        "metadata": create_base_metadata("python", 1),
        "context": BARRACUDA_CONTEXT,
        "conversations": [
            {
                "turn": 1,
                "from": "human",
                "value": "I'm building a Python web app that needs to run system commands like ping to check server connectivity. How do I do this safely?"
            },
            {
                "turn": 2,
                "from": "assistant",
                "value": """I'll show you both the dangerous pattern and the secure implementation.

**Vulnerable Code (Command Injection Risk):**
```python
import subprocess

def ping_host(hostname):
    # DANGEROUS: shell=True with user input
    command = f"ping -c 4 {hostname}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout
```

**Why This Is Dangerous:**
An attacker can input `8.8.8.8; rm -rf /` or `8.8.8.8 && cat /etc/passwd` as the hostname. With `shell=True`, this executes multiple commands:
```bash
ping -c 4 8.8.8.8; rm -rf /
# Pings 8.8.8.8, then deletes everything!
```

**Real-World Impact:** The 2023 Barracuda ESG vulnerability (CVE-2023-2868) used command injection in email attachment processing for a Chinese espionage campaign. Attackers gained complete server control and deployed persistent backdoors.

**Secure Implementation:**
```python
import subprocess
import re
import ipaddress

def ping_host_secure(hostname):
    # Input validation - allowlist approach
    try:
        # Validate as IP address
        ip = ipaddress.ip_address(hostname)
    except ValueError:
        # If not IP, validate as hostname (strict pattern)
        if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$', hostname):
            raise ValueError("Invalid hostname format")

    # SECURE: Pass arguments as list, NOT shell=True
    result = subprocess.run(
        ['ping', '-c', '4', hostname],  # Arguments as list
        capture_output=True,
        text=True,
        timeout=10,  # Prevent hanging
        shell=False  # Critical: shell=False
    )

    if result.returncode != 0:
        raise RuntimeError(f"Ping failed: {result.stderr}")

    return result.stdout

# Usage
try:
    output = ping_host_secure("8.8.8.8")
    print(output)
except ValueError as e:
    print(f"Invalid input: {e}")
except RuntimeError as e:
    print(f"Command failed: {e}")
```

**Key Security Controls:**
1. **Input validation** - Verify hostname is valid IP or DNS name
2. **shell=False** - Passes arguments directly to program, no shell interpretation
3. **Argument list** - Commands as lists prevent injection
4. **Timeout** - Prevents resource exhaustion
5. **Error handling** - Catches failures securely
6. **No string concatenation** - Arguments never concatenated into shell command"""
            },
            {
                "turn": 3,
                "from": "human",
                "value": "What if I need to run more complex commands with options that depend on user input?"
            },
            {
                "turn": 4,
                "from": "assistant",
                "value": """For complex commands, use allowlist validation for all dynamic parts:

```python
import subprocess
import shlex
from typing import List

def run_network_diagnostic(target, diagnostic_type):
    # Allowlist for diagnostic types
    ALLOWED_DIAGNOSTICS = {
        'ping': ['ping', '-c', '4'],
        'traceroute': ['traceroute', '-m', '15'],
        'dns_lookup': ['nslookup'],
        'port_scan': ['nc', '-zv', '-w', '3']  # Basic port check
    }

    # Validate diagnostic type
    if diagnostic_type not in ALLOWED_DIAGNOSTICS:
        raise ValueError(f"Invalid diagnostic type. Allowed: {list(ALLOWED_DIAGNOSTICS.keys())}")

    # Validate target (IP or hostname)
    try:
        ipaddress.ip_address(target)
    except ValueError:
        # Validate as hostname
        if not re.match(r'^[a-zA-Z0-9.-]+$', target):
            raise ValueError("Invalid target format")
        if len(target) > 253:  # Max DNS name length
            raise ValueError("Target too long")

    # Build command from allowlist
    command = ALLOWED_DIAGNOSTICS[diagnostic_type] + [target]

    # Execute safely
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=30,
        shell=False  # Never use shell=True
    )

    return {
        'command': ' '.join(command),  # For logging
        'returncode': result.returncode,
        'stdout': result.stdout,
        'stderr': result.stderr
    }

# Advanced pattern: Safe command builder
class SafeCommandBuilder:
    \"\"\"Build commands safely with validation\"\"\"

    ALLOWED_PROGRAMS = {'ping', 'nslookup', 'traceroute', 'dig'}
    ALLOWED_OPTIONS = {
        'ping': {'-c': r'^\d+$', '-W': r'^\d+$'},
        'nslookup': {'-timeout': r'^\d+$'},
    }

    def __init__(self, program: str):
        if program not in self.ALLOWED_PROGRAMS:
            raise ValueError(f"Program not allowed: {program}")
        self.program = program
        self.args = [program]

    def add_option(self, option: str, value: str) -> 'SafeCommandBuilder':
        # Validate option is allowed for this program
        allowed_opts = self.ALLOWED_OPTIONS.get(self.program, {})
        if option not in allowed_opts:
            raise ValueError(f"Option {option} not allowed for {self.program}")

        # Validate value matches expected pattern
        pattern = allowed_opts[option]
        if not re.match(pattern, value):
            raise ValueError(f"Invalid value for {option}: {value}")

        self.args.extend([option, value])
        return self

    def add_target(self, target: str) -> 'SafeCommandBuilder':
        # Validate target
        try:
            ipaddress.ip_address(target)
        except ValueError:
            if not re.match(r'^[a-zA-Z0-9.-]+$', target):
                raise ValueError("Invalid target")
        self.args.append(target)
        return self

    def execute(self) -> dict:
        result = subprocess.run(
            self.args,
            capture_output=True,
            text=True,
            timeout=30,
            shell=False
        )
        return {
            'command': ' '.join(self.args),
            'returncode': result.returncode,
            'output': result.stdout
        }

# Usage
builder = SafeCommandBuilder('ping')
result = builder.add_option('-c', '4').add_target('8.8.8.8').execute()
```

**Security Pattern:**
- **Allowlist everything** - Programs, options, and value patterns
- **Builder pattern** - Constructs commands safely
- **No shell=True** - Ever
- **Validation at each step** - Options and values validated independently
- **Type safety** - Strong typing prevents errors

**Critical Rules:**
1. Never use `shell=True` with any user input
2. Never concatenate user input into command strings
3. Always validate against allowlists, never denylists
4. Use argument lists, not command strings
5. Always set timeouts to prevent DoS"""
            }
        ],
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": datetime.now().strftime('%Y-%m-%d'),
            "issues": []
        }
    }


def php_shell_exec_injection():
    """PHP - Command injection via shell_exec"""
    return {
        "id": "command-injection-000002",
        "metadata": create_base_metadata("php", 2),
        "context": GITLAB_CONTEXT,
        "conversations": [
            {
                "turn": 1,
                "from": "human",
                "value": "I'm building a PHP application that needs to process uploaded images and extract metadata. How do I run command-line tools safely?"
            },
            {
                "turn": 2,
                "from": "assistant",
                "value": """I'll demonstrate the dangerous pattern and secure alternatives.

**Vulnerable Code (Command Injection Risk):**
```php
<?php
function getImageMetadata($filename) {
    // DANGEROUS: User-controlled filename in shell command
    $command = "exiftool " . $filename;
    $output = shell_exec($command);
    return $output;
}

// Usage
$uploaded_file = $_FILES['image']['name'];
$metadata = getImageMetadata($uploaded_file);
echo $metadata;
?>
```

**Why This Is Dangerous:**
An attacker uploads a file named `image.jpg; rm -rf /` or `$(whoami).jpg`. The command becomes:
```bash
exiftool image.jpg; rm -rf /
# Executes exiftool, then deletes everything
```

Or worse, with command substitution:
```bash
exiftool $(cat /etc/passwd).jpg
# Reads sensitive files
```

**Real-World Impact:** CVE-2021-22205 (GitLab) was a command injection in ExifTool processing that allowed attackers to gain complete server control. This was a critical RCE vulnerability widely exploited in the wild.

**Secure Implementation:**
```php
<?php
function getImageMetadataSafe($filepath) {
    // Validate file exists and is readable
    if (!file_exists($filepath) || !is_readable($filepath)) {
        throw new InvalidArgumentException("File not accessible");
    }

    // Validate file is actually an image
    $allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    $finfo = finfo_open(FILEINFO_MIME_TYPE);
    $mime_type = finfo_file($finfo, $filepath);
    finfo_close($finfo);

    if (!in_array($mime_type, $allowed_types, true)) {
        throw new InvalidArgumentException("File is not an allowed image type");
    }

    // SECURE: Use escapeshellarg() to safely quote the argument
    $safe_filepath = escapeshellarg($filepath);

    // Use exec() with output array (safer than shell_exec)
    $output = [];
    $return_var = 0;

    // Execute with argument array
    exec("exiftool " . $safe_filepath, $output, $return_var);

    if ($return_var !== 0) {
        throw new RuntimeException("exiftool command failed");
    }

    return implode("\n", $output);
}

// Better approach: Use PHP libraries instead of shell commands
function getImageMetadataPHP($filepath) {
    // Validate file
    if (!file_exists($filepath)) {
        throw new InvalidArgumentException("File not found");
    }

    // Use PHP's exif functions (no shell command needed)
    $exif_data = @exif_read_data($filepath);

    if ($exif_data === false) {
        // Fallback to basic info
        $image_info = getimagesize($filepath);
        return [
            'width' => $image_info[0],
            'height' => $image_info[1],
            'type' => image_type_to_mime_type($image_info[2])
        ];
    }

    return $exif_data;
}

// Usage
try {
    $upload_dir = '/var/www/uploads/';
    $filename = basename($_FILES['image']['name']); // Remove path components
    $filepath = $upload_dir . $filename;

    // Move uploaded file to safe location
    if (move_uploaded_file($_FILES['image']['tmp_name'], $filepath)) {
        // Use PHP library (preferred)
        $metadata = getImageMetadataPHP($filepath);

        // Or use shell command with proper escaping
        // $metadata = getImageMetadataSafe($filepath);

        echo json_encode($metadata);
    }
} catch (Exception $e) {
    error_log("Image metadata extraction failed: " . $e->getMessage());
    http_response_code(400);
    echo json_encode(['error' => 'Failed to process image']);
}
?>
```

**Key Security Controls:**
1. **escapeshellarg()** - Properly quotes arguments to prevent injection
2. **File validation** - Check MIME type, not just extension
3. **basename()** - Removes directory traversal attempts
4. **PHP libraries preferred** - Avoid shell commands when possible (exif_read_data)
5. **exec() over shell_exec()** - exec() with array output is safer
6. **Error handling** - Log errors securely, don't expose to users"""
            },
            {
                "turn": 3,
                "from": "human",
                "value": "What if I absolutely need to run complex shell commands with multiple arguments from user input?"
            },
            {
                "turn": 4,
                "from": "assistant",
                "value": """When you must run shell commands, use strict allowlist validation:

```php
<?php
class SafeCommandExecutor {
    // Allowlist of permitted programs
    private const ALLOWED_PROGRAMS = [
        'convert',    // ImageMagick
        'ffmpeg',     // Video processing
        'gs',         // Ghostscript for PDFs
    ];

    // Allowlist of options per program
    private const ALLOWED_OPTIONS = [
        'convert' => [
            '-resize' => '/^\d+x\d+$/',  // Format: 800x600
            '-quality' => '/^\d{1,3}$/', // 0-999
            '-format' => '/^(jpg|png|gif|webp)$/',
        ],
        'ffmpeg' => [
            '-t' => '/^\d+$/',           // Duration in seconds
            '-vf' => '/^scale=\d+:\d+$/', // Video filter: scale=640:480
        ],
    ];

    public function resizeImage($input_path, $output_path, $width, $height, $quality) {
        // Validate program
        $program = 'convert';

        // Validate all paths are within allowed directory
        $safe_dir = '/var/www/uploads/';
        $input_real = realpath($input_path);
        $output_real = realpath(dirname($output_path)) . '/' . basename($output_path);

        if (strpos($input_real, $safe_dir) !== 0) {
            throw new InvalidArgumentException("Input path outside allowed directory");
        }

        // Validate dimensions
        if (!preg_match('/^\d+$/', (string)$width) || !preg_match('/^\d+$/', (string)$height)) {
            throw new InvalidArgumentException("Invalid dimensions");
        }

        if ($width > 4000 || $height > 4000 || $width < 1 || $height < 1) {
            throw new InvalidArgumentException("Dimensions out of range");
        }

        // Validate quality
        if (!is_numeric($quality) || $quality < 1 || $quality > 100) {
            throw new InvalidArgumentException("Invalid quality");
        }

        // Build command with escaped arguments
        $cmd = [
            'convert',
            escapeshellarg($input_path),
            '-resize',
            escapeshellarg($width . 'x' . $height),
            '-quality',
            escapeshellarg((string)$quality),
            escapeshellarg($output_path)
        ];

        // Execute with proc_open for better control
        $descriptorspec = [
            0 => ['pipe', 'r'],  // stdin
            1 => ['pipe', 'w'],  // stdout
            2 => ['pipe', 'w']   // stderr
        ];

        $process = proc_open(implode(' ', $cmd), $descriptorspec, $pipes);

        if (!is_resource($process)) {
            throw new RuntimeException("Failed to start process");
        }

        fclose($pipes[0]);  // Close stdin
        $stdout = stream_get_contents($pipes[1]);
        $stderr = stream_get_contents($pipes[2]);
        fclose($pipes[1]);
        fclose($pipes[2]);

        $return_value = proc_close($process);

        if ($return_value !== 0) {
            error_log("ImageMagick error: " . $stderr);
            throw new RuntimeException("Image processing failed");
        }

        return true;
    }

    // Generic safe command execution
    public function executeCommand($program, array $options, $input_file) {
        // Validate program
        if (!in_array($program, self::ALLOWED_PROGRAMS, true)) {
            throw new InvalidArgumentException("Program not allowed: $program");
        }

        // Validate file exists
        if (!file_exists($input_file)) {
            throw new InvalidArgumentException("Input file not found");
        }

        $cmd_parts = [$program];

        // Validate and add each option
        foreach ($options as $option => $value) {
            // Check option is allowed for this program
            if (!isset(self::ALLOWED_OPTIONS[$program][$option])) {
                throw new InvalidArgumentException("Option $option not allowed for $program");
            }

            // Validate value matches expected pattern
            $pattern = self::ALLOWED_OPTIONS[$program][$option];
            if (!preg_match($pattern, $value)) {
                throw new InvalidArgumentException("Invalid value for $option: $value");
            }

            $cmd_parts[] = $option;
            $cmd_parts[] = escapeshellarg($value);
        }

        // Add input file
        $cmd_parts[] = escapeshellarg($input_file);

        // Execute safely
        exec(implode(' ', $cmd_parts), $output, $return_var);

        if ($return_var !== 0) {
            throw new RuntimeException("Command failed with code $return_var");
        }

        return $output;
    }
}

// Usage
$executor = new SafeCommandExecutor();

try {
    $executor->resizeImage(
        '/var/www/uploads/input.jpg',
        '/var/www/uploads/output.jpg',
        800,
        600,
        85
    );
} catch (Exception $e) {
    error_log($e->getMessage());
    die("Processing failed");
}
?>
```

**Security Pattern:**
- **Allowlist programs** - Only explicitly permitted programs can run
- **Allowlist options** - Each program has allowed options with validation patterns
- **escapeshellarg()** - Always escape arguments
- **Path validation** - Ensure files are in allowed directories (realpath checks)
- **proc_open()** - Better control than shell_exec or system
- **Input validation** - Validate format, range, and type for all values

**Critical PHP Security Rules:**
1. Never use `eval()`, `system()`, `passthru()`, `shell_exec()` with user input
2. Always use `escapeshellarg()` for arguments
3. Prefer PHP libraries over shell commands (exif, GD, Imagick)
4. Use `exec()` with output array, not `shell_exec()`
5. Validate paths with `realpath()` to prevent directory traversal
6. Always validate against allowlists, not denylists"""
            }
        ],
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": datetime.now().strftime('%Y-%m-%d'),
            "issues": []
        }
    }


def java_runtime_exec_injection():
    """Java - Command injection via Runtime.exec"""
    return {
        "id": "command-injection-000003",
        "metadata": create_base_metadata("java", 3),
        "context": {
            "real_world_incident": "2022 Spring4Shell RCE via class loader manipulation",
            "impact": "Critical RCE in Spring Framework, widespread exploitation",
            "attack_vector": "Remote code execution through parameter binding",
            "cve": "CVE-2022-22965",
            "year": 2022
        },
        "conversations": [
            {
                "turn": 1,
                "from": "human",
                "value": "I'm building a Java application that needs to execute system commands based on user input. What's the safe way to do this?"
            },
            {
                "turn": 2,
                "from": "assistant",
                "value": """I'll show you the vulnerable pattern and secure alternatives in Java.

**Vulnerable Code (Command Injection Risk):**
```java
import java.io.*;

public class SystemCommandExecutor {
    // DANGEROUS: String concatenation with Runtime.exec
    public String executeCommand(String userInput) throws IOException {
        String command = "ls -la " + userInput;
        Process process = Runtime.getRuntime().exec(command);

        BufferedReader reader = new BufferedReader(
            new InputStreamReader(process.getInputStream())
        );

        StringBuilder output = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            output.append(line).append("\\n");
        }

        return output.toString();
    }
}
```

**Why This Is Dangerous:**
If user inputs `; rm -rf /` or `| cat /etc/passwd`, the command becomes:
```bash
ls -la ; rm -rf /
# Lists directory, then deletes everything
```

However, there's a subtlety: `Runtime.exec(String)` doesn't invoke a shell by default, but it WILL if the string contains shell metacharacters and the OS invokes a shell. It's inconsistent and dangerous.

**Secure Implementation:**
```java
import java.io.*;
import java.util.*;
import java.util.regex.Pattern;
import java.nio.file.*;

public class SafeCommandExecutor {
    // Allowlist of permitted directories
    private static final Path ALLOWED_BASE = Paths.get("/var/data");
    private static final Pattern SAFE_FILENAME = Pattern.compile("^[a-zA-Z0-9_.-]+$");

    // SECURE: Use ProcessBuilder with argument list
    public String listDirectory(String dirname) throws IOException {
        // Validate input against allowlist pattern
        if (!SAFE_FILENAME.matcher(dirname).matches()) {
            throw new IllegalArgumentException("Invalid directory name format");
        }

        // Construct full path
        Path requestedPath = ALLOWED_BASE.resolve(dirname).normalize();

        // Prevent directory traversal
        if (!requestedPath.startsWith(ALLOWED_BASE)) {
            throw new IllegalArgumentException("Directory traversal attempt detected");
        }

        // Verify path exists and is a directory
        if (!Files.exists(requestedPath) || !Files.isDirectory(requestedPath)) {
            throw new IllegalArgumentException("Directory does not exist");
        }

        // Use ProcessBuilder with argument list (NOT string)
        ProcessBuilder processBuilder = new ProcessBuilder(
            "ls",
            "-la",
            requestedPath.toString()
        );

        // Set working directory
        processBuilder.directory(ALLOWED_BASE.toFile());

        // Disable environment variable injection
        processBuilder.environment().clear();

        // Start process
        Process process = processBuilder.start();

        // Read output with timeout
        StringBuilder output = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(process.getInputStream()))) {

            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\\n");
            }

            // Wait for process with timeout
            boolean finished = process.waitFor(5, java.util.concurrent.TimeUnit.SECONDS);

            if (!finished) {
                process.destroyForcibly();
                throw new RuntimeException("Command timeout");
            }

            if (process.exitValue() != 0) {
                throw new RuntimeException("Command failed with exit code: " + process.exitValue());
            }
        } catch (InterruptedException e) {
            process.destroyForcibly();
            Thread.currentThread().interrupt();
            throw new RuntimeException("Command interrupted", e);
        }

        return output.toString();
    }
}
```

**Key Security Controls:**
1. **ProcessBuilder with list** - Arguments passed as List<String>, not concatenated string
2. **Input validation** - Regex pattern for allowed characters
3. **Path validation** - normalize() and startsWith() prevent directory traversal
4. **Environment clearing** - Prevent environment variable injection
5. **Timeout** - Process killed if exceeds time limit
6. **Error handling** - Proper cleanup and interruption handling"""
            },
            {
                "turn": 3,
                "from": "human",
                "value": "What if I need to run different commands based on user selection with various options?"
            },
            {
                "turn": 4,
                "from": "assistant",
                "value": """For dynamic commands, use a command builder with strict allowlists:

```java
import java.io.*;
import java.util.*;
import java.util.regex.Pattern;

public class SafeCommandBuilder {
    // Allowlist of permitted programs
    private static final Set<String> ALLOWED_PROGRAMS = Set.of(
        "ls", "cat", "grep", "find"
    );

    // Allowlist of options per program
    private static final Map<String, Map<String, Pattern>> ALLOWED_OPTIONS = Map.of(
        "ls", Map.of(
            "-la", Pattern.compile(""),  // No value needed
            "-l", Pattern.compile(""),
            "-a", Pattern.compile("")
        ),
        "grep", Map.of(
            "-i", Pattern.compile(""),      // Case insensitive
            "-n", Pattern.compile(""),      // Line numbers
            "-c", Pattern.compile("")       // Count
        ),
        "find", Map.of(
            "-name", Pattern.compile("^[a-zA-Z0-9*._-]+$"),
            "-type", Pattern.compile("^[fd]$"),  // f or d
            "-maxdepth", Pattern.compile("^[1-9]$")
        )
    );

    private final String program;
    private final List<String> arguments;

    public SafeCommandBuilder(String program) {
        if (!ALLOWED_PROGRAMS.contains(program)) {
            throw new IllegalArgumentException("Program not allowed: " + program);
        }
        this.program = program;
        this.arguments = new ArrayList<>();
        this.arguments.add(program);
    }

    public SafeCommandBuilder addOption(String option, String value) {
        Map<String, Pattern> allowedOpts = ALLOWED_OPTIONS.get(program);

        if (allowedOpts == null || !allowedOpts.containsKey(option)) {
            throw new IllegalArgumentException("Option not allowed: " + option);
        }

        Pattern valuePattern = allowedOpts.get(option);

        // If pattern is empty, option takes no value
        if (valuePattern.pattern().isEmpty()) {
            this.arguments.add(option);
        } else {
            // Validate value matches pattern
            if (value == null || !valuePattern.matcher(value).matches()) {
                throw new IllegalArgumentException("Invalid value for " + option + ": " + value);
            }
            this.arguments.add(option);
            this.arguments.add(value);
        }

        return this;
    }

    public SafeCommandBuilder addArgument(String arg) {
        // Basic validation - no shell metacharacters
        if (arg.matches(".*[;&|`$()<>].*")) {
            throw new IllegalArgumentException("Argument contains shell metacharacters");
        }
        this.arguments.add(arg);
        return this;
    }

    public CommandResult execute() throws IOException, InterruptedException {
        ProcessBuilder pb = new ProcessBuilder(arguments);
        pb.environment().clear();  // Clear environment
        pb.redirectErrorStream(true);

        Process process = pb.start();

        StringBuilder output = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(process.getInputStream()))) {

            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\\n");
            }

            boolean finished = process.waitFor(10, java.util.concurrent.TimeUnit.SECONDS);

            if (!finished) {
                process.destroyForcibly();
                throw new RuntimeException("Command timeout");
            }

            return new CommandResult(
                process.exitValue(),
                output.toString(),
                String.join(" ", arguments)
            );
        }
    }
}

class CommandResult {
    private final int exitCode;
    private final String output;
    private final String command;

    public CommandResult(int exitCode, String output, String command) {
        this.exitCode = exitCode;
        this.output = output;
        this.command = command;
    }

    public int getExitCode() { return exitCode; }
    public String getOutput() { return output; }
    public String getCommand() { return command; }
}

// Usage example
public class Application {
    public static void main(String[] args) {
        try {
            // Safe command building
            SafeCommandBuilder builder = new SafeCommandBuilder("find");
            CommandResult result = builder
                .addArgument("/var/data")
                .addOption("-name", "*.txt")
                .addOption("-type", "f")
                .addOption("-maxdepth", "3")
                .execute();

            if (result.getExitCode() == 0) {
                System.out.println("Found files:");
                System.out.println(result.getOutput());
            } else {
                System.err.println("Command failed: " + result.getExitCode());
            }
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}
```

**Security Pattern:**
- **Builder pattern** - Constructs commands safely step-by-step
- **Allowlist validation** - Programs, options, and value patterns all validated
- **ProcessBuilder** - Always use with argument list, never strings
- **Environment clearing** - Prevents variable injection
- **Timeout enforcement** - All processes have time limits
- **Shell metacharacter blocking** - Explicit rejection of dangerous characters

**Critical Java Rules:**
1. Never use `Runtime.exec(String)` with user input
2. Always use `ProcessBuilder` with `List<String>` arguments
3. Clear environment variables with `environment().clear()`
4. Always add timeouts with `waitFor(timeout, unit)`
5. Validate all inputs against allowlists
6. Use `Path.normalize()` and `startsWith()` for path validation"""
            }
        ],
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": datetime.now().strftime('%Y-%m-%d'),
            "issues": []
        }
    }


def nodejs_child_process_injection():
    """Node.js - Command injection via child_process"""
    return {
        "id": "command-injection-000004",
        "metadata": create_base_metadata("javascript", 4),
        "context": {
            "real_world_incident": "2024 npm package supply chain attacks via command injection",
            "impact": "Malicious packages executing arbitrary commands during npm install",
            "attack_vector": "Command injection in post-install scripts",
            "cve": None,
            "year": 2024
        },
        "conversations": [
            {
                "turn": 1,
                "from": "human",
                "value": "I'm building a Node.js API that needs to execute system commands. What's the secure way to handle this?"
            },
            {
                "turn": 2,
                "from": "assistant",
                "value": """I'll show you the dangerous patterns and secure alternatives in Node.js.

**Vulnerable Code (Command Injection Risk):**
```javascript
const { exec } = require('child_process');

// DANGEROUS: exec() with string concatenation
function pingHost(hostname) {
    const command = `ping -c 4 ${hostname}`;

    return new Promise((resolve, reject) => {
        exec(command, (error, stdout, stderr) => {
            if (error) {
                reject(error);
                return;
            }
            resolve(stdout);
        });
    });
}

// Usage
app.get('/ping', async (req, res) => {
    const host = req.query.host;
    const result = await pingHost(host);
    res.send(result);
});
```

**Why This Is Dangerous:**
If user provides `8.8.8.8; cat /etc/passwd` or `8.8.8.8 && rm -rf /`, the command becomes:
```bash
ping -c 4 8.8.8.8; cat /etc/passwd
# Pings, then reads sensitive files
```

The `exec()` function spawns a shell, allowing command chaining with `;`, `&&`, `||`, and command substitution with `$()` or backticks.

**Secure Implementation:**
```javascript
const { execFile } = require('child_process');
const { promisify } = require('util');
const execFileAsync = promisify(execFile);

// Validation helper
function isValidHostname(input) {
    // IP address or hostname pattern
    const ipPattern = /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/;
    const hostnamePattern = /^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;

    if (!input || typeof input !== 'string') {
        return false;
    }

    if (ipPattern.test(input)) {
        // Validate IP ranges
        const parts = input.split('.').map(Number);
        return parts.every(part => part >= 0 && part <= 255);
    }

    return hostnamePattern.test(input) && input.length <= 253;
}

// SECURE: Use execFile with argument array
async function pingHostSafe(hostname) {
    // Validate input
    if (!isValidHostname(hostname)) {
        throw new Error('Invalid hostname format');
    }

    try {
        // execFile does NOT spawn a shell, passes arguments directly
        const { stdout, stderr } = await execFileAsync(
            'ping',
            ['-c', '4', hostname],
            {
                timeout: 10000,  // 10 second timeout
                maxBuffer: 1024 * 1024  // 1MB max output
            }
        );

        return stdout;
    } catch (error) {
        if (error.killed) {
            throw new Error('Command timeout');
        }
        throw new Error(`Ping failed: ${error.message}`);
    }
}

// Express route with proper error handling
app.get('/ping', async (req, res) => {
    try {
        const host = req.query.host;

        if (!host) {
            return res.status(400).json({ error: 'Host parameter required' });
        }

        const result = await pingHostSafe(host);
        res.json({ output: result });
    } catch (error) {
        console.error('Ping error:', error.message);
        res.status(400).json({ error: 'Invalid request' });
    }
});
```

**Key Security Controls:**
1. **execFile over exec** - execFile doesn't spawn a shell, preventing injection
2. **Argument array** - Arguments passed as array, not concatenated string
3. **Input validation** - Strict regex pattern for hostnames/IPs
4. **Timeout** - Prevents resource exhaustion
5. **maxBuffer** - Limits output size
6. **Error handling** - Secure error messages, no system info exposure"""
            },
            {
                "turn": 3,
                "from": "human",
                "value": "What if I need to run different commands with options based on user selection?"
            },
            {
                "turn": 4,
                "from": "assistant",
                "value": """For dynamic commands, use a safe command builder:

```javascript
const { execFile } = require('child_process');
const { promisify } = require('util');
const path = require('path');
const execFileAsync = promisify(execFile);

class SafeCommandExecutor {
    // Allowlist of permitted programs
    static ALLOWED_PROGRAMS = new Set([
        'ping',
        'nslookup',
        'dig',
        'traceroute'
    ]);

    // Allowlist of options per program
    static ALLOWED_OPTIONS = {
        ping: {
            '-c': /^\d{1,2}$/,      // Count: 1-99
            '-W': /^\d{1,2}$/,      // Timeout: 1-99 seconds
        },
        dig: {
            '+short': null,          // Boolean flag
            '+trace': null,
        },
        nslookup: {
            '-timeout': /^\d{1,2}$/,
        }
    };

    constructor(program) {
        if (!SafeCommandExecutor.ALLOWED_PROGRAMS.has(program)) {
            throw new Error(`Program not allowed: ${program}`);
        }
        this.program = program;
        this.args = [];
    }

    addOption(option, value = null) {
        const allowedOpts = SafeCommandExecutor.ALLOWED_OPTIONS[this.program];

        if (!allowedOpts || !(option in allowedOpts)) {
            throw new Error(`Option ${option} not allowed for ${this.program}`);
        }

        const pattern = allowedOpts[option];

        // Boolean flag (no value)
        if (pattern === null) {
            this.args.push(option);
            return this;
        }

        // Validate value against pattern
        if (!value || !pattern.test(value)) {
            throw new Error(`Invalid value for ${option}: ${value}`);
        }

        this.args.push(option, value);
        return this;
    }

    addTarget(target) {
        // Validate target is safe hostname or IP
        const ipPattern = /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/;
        const hostnamePattern = /^[a-zA-Z0-9.-]+$/;

        if (!target || typeof target !== 'string') {
            throw new Error('Invalid target');
        }

        if (!ipPattern.test(target) && !hostnamePattern.test(target)) {
            throw new Error('Invalid target format');
        }

        if (target.length > 253) {
            throw new Error('Target too long');
        }

        this.args.push(target);
        return this;
    }

    async execute() {
        try {
            const { stdout, stderr } = await execFileAsync(
                this.program,
                this.args,
                {
                    timeout: 30000,
                    maxBuffer: 2 * 1024 * 1024,  // 2MB
                    env: {}  // Empty environment
                }
            );

            return {
                command: `${this.program} ${this.args.join(' ')}`,
                exitCode: 0,
                output: stdout,
                error: stderr
            };
        } catch (error) {
            return {
                command: `${this.program} ${this.args.join(' ')}`,
                exitCode: error.code || 1,
                output: error.stdout || '',
                error: error.stderr || error.message
            };
        }
    }
}

// Alternative: spawn for streaming output
const { spawn } = require('child_process');

async function executeCommandSafe(program, args, options = {}) {
    // Validate program is allowed
    if (!SafeCommandExecutor.ALLOWED_PROGRAMS.has(program)) {
        throw new Error('Program not allowed');
    }

    // Validate all arguments are strings
    if (!Array.isArray(args) || !args.every(arg => typeof arg === 'string')) {
        throw new Error('Invalid arguments');
    }

    return new Promise((resolve, reject) => {
        const child = spawn(program, args, {
            timeout: options.timeout || 30000,
            env: {},  // Empty environment
            shell: false  // Critical: never use shell
        });

        let stdout = '';
        let stderr = '';

        child.stdout.on('data', (data) => {
            stdout += data.toString();
            // Limit output size
            if (stdout.length > 2 * 1024 * 1024) {
                child.kill();
                reject(new Error('Output size exceeded'));
            }
        });

        child.stderr.on('data', (data) => {
            stderr += data.toString();
        });

        child.on('close', (code) => {
            resolve({
                exitCode: code,
                stdout,
                stderr
            });
        });

        child.on('error', (error) => {
            reject(error);
        });

        // Set timeout
        const timeout = setTimeout(() => {
            child.kill();
            reject(new Error('Command timeout'));
        }, options.timeout || 30000);

        child.on('exit', () => {
            clearTimeout(timeout);
        });
    });
}

// Usage examples
async function main() {
    try {
        // Using builder
        const executor = new SafeCommandExecutor('ping');
        const result = await executor
            .addOption('-c', '4')
            .addTarget('8.8.8.8')
            .execute();

        console.log(result.output);

        // Using spawn wrapper
        const result2 = await executeCommandSafe('dig', ['+short', 'google.com']);
        console.log(result2.stdout);

    } catch (error) {
        console.error('Error:', error.message);
    }
}
```

**Security Pattern:**
- **execFile or spawn** - Never use `exec()` which spawns a shell
- **Argument arrays** - Always pass arguments as arrays, never strings
- **Allowlist validation** - Programs, options, and values all validated
- **shell: false** - Explicitly disable shell (default for execFile/spawn)
- **Empty environment** - Prevent environment variable injection
- **Timeout enforcement** - All processes have time limits
- **Output size limits** - Prevent memory exhaustion

**Critical Node.js Rules:**
1. Never use `exec()` with user input - use `execFile()` or `spawn()`
2. Always pass arguments as arrays, not template strings
3. Set `shell: false` explicitly (though it's default for execFile/spawn)
4. Clear environment with `env: {}`
5. Always set `timeout` and `maxBuffer`
6. Validate all inputs against allowlists"""
            }
        ],
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": datetime.now().strftime('%Y-%m-%d'),
            "issues": []
        }
    }


def go_exec_command_injection():
    """Go - Command injection via exec.Command"""
    return {
        "id": "command-injection-000005",
        "metadata": create_base_metadata("go", 5),
        "context": {
            "real_world_incident": "2023 Kubernetes command injection vulnerabilities",
            "impact": "Container escape and host system access via kubectl exec",
            "attack_vector": "Command injection in container runtime interfaces",
            "cve": None,
            "year": 2023
        },
        "conversations": [
            {
                "turn": 1,
                "from": "human",
                "value": "I'm building a Go application that needs to execute system commands. What's the secure way to do this?"
            },
            {
                "turn": 2,
                "from": "assistant",
                "value": """I'll demonstrate both vulnerable and secure command execution in Go.

**Vulnerable Code (Command Injection Risk):**
```go
package main

import (
    "fmt"
    "os/exec"
)

// DANGEROUS: Using sh -c with string concatenation
func pingHostVulnerable(hostname string) (string, error) {
    // This spawns a shell, allowing injection
    cmd := exec.Command("sh", "-c", fmt.Sprintf("ping -c 4 %s", hostname))

    output, err := cmd.CombinedOutput()
    if err != nil {
        return "", err
    }

    return string(output), nil
}
```

**Why This Is Dangerous:**
Using `sh -c` spawns a shell interpreter. If user provides `8.8.8.8; rm -rf /`, the command becomes:
```bash
sh -c "ping -c 4 8.8.8.8; rm -rf /"
# Pings, then attempts to delete everything
```

**Secure Implementation:**
```go
package main

import (
    "context"
    "errors"
    "fmt"
    "net"
    "os/exec"
    "regexp"
    "time"
)

var (
    hostnameRegex = regexp.MustCompile(`^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$`)
)

// Validate hostname or IP address
func isValidHost(host string) error {
    if host == "" {
        return errors.New("empty host")
    }

    // Try parsing as IP address
    if ip := net.ParseIP(host); ip != nil {
        return nil
    }

    // Validate as hostname
    if !hostnameRegex.MatchString(host) || len(host) > 253 {
        return errors.New("invalid hostname format")
    }

    return nil
}

// SECURE: Direct command execution without shell
func pingHostSafe(ctx context.Context, hostname string) (string, error) {
    // Validate input
    if err := isValidHost(hostname); err != nil {
        return "", fmt.Errorf("invalid host: %w", err)
    }

    // Create context with timeout
    ctx, cancel := context.WithTimeout(ctx, 10*time.Second)
    defer cancel()

    // exec.Command with separate arguments - NO SHELL
    cmd := exec.CommandContext(ctx, "ping", "-c", "4", hostname)

    // Execute and capture output
    output, err := cmd.CombinedOutput()

    if ctx.Err() == context.DeadlineExceeded {
        return "", errors.New("command timeout")
    }

    if err != nil {
        return "", fmt.Errorf("ping failed: %w", err)
    }

    return string(output), nil
}

// Usage
func main() {
    ctx := context.Background()

    result, err := pingHostSafe(ctx, "8.8.8.8")
    if err != nil {
        fmt.Printf("Error: %v\\n", err)
        return
    }

    fmt.Println(result)
}
```

**Key Security Controls:**
1. **exec.Command** with separate args - No shell invocation
2. **Context with timeout** - Prevents hung processes
3. **Input validation** - Regex and net.ParseIP validation
4. **No string concatenation** - Arguments passed separately
5. **Error handling** - Timeout and execution errors handled properly"""
            },
            {
                "turn": 3,
                "from": "human",
                "value": "How do I handle cases where I need to run different commands with various options based on user input?"
            },
            {
                "turn": 4,
                "from": "assistant",
                "value": """For dynamic commands, use a builder pattern with strict allowlists:

```go
package main

import (
    "context"
    "errors"
    "fmt"
    "os/exec"
    "regexp"
    "time"
)

// Allowlist of permitted programs
var allowedPrograms = map[string]bool{
    "ping":       true,
    "nslookup":   true,
    "dig":        true,
    "traceroute": true,
}

// Allowlist of options per program
var allowedOptions = map[string]map[string]*regexp.Regexp{
    "ping": {
        "-c": regexp.MustCompile(`^\d{1,2}$`),  // Count
        "-W": regexp.MustCompile(`^\d{1,2}$`),  // Timeout
    },
    "dig": {
        "+short": nil,  // Boolean flag
        "+trace": nil,
    },
}

type CommandBuilder struct {
    program string
    args    []string
}

func NewCommandBuilder(program string) (*CommandBuilder, error) {
    if !allowedPrograms[program] {
        return nil, fmt.Errorf("program not allowed: %s", program)
    }

    return &CommandBuilder{
        program: program,
        args:    []string{},
    }, nil
}

func (cb *CommandBuilder) AddOption(option, value string) (*CommandBuilder, error) {
    opts, ok := allowedOptions[cb.program]
    if !ok {
        return nil, fmt.Errorf("no options defined for program: %s", cb.program)
    }

    pattern, exists := opts[option]
    if !exists {
        return nil, fmt.Errorf("option not allowed: %s", option)
    }

    // Boolean flag (nil pattern)
    if pattern == nil {
        cb.args = append(cb.args, option)
        return cb, nil
    }

    // Validate value
    if !pattern.MatchString(value) {
        return nil, fmt.Errorf("invalid value for %s: %s", option, value)
    }

    cb.args = append(cb.args, option, value)
    return cb, nil
}

func (cb *CommandBuilder) AddTarget(target string) (*CommandBuilder, error) {
    // Validate target
    if err := isValidHost(target); err != nil {
        return nil, fmt.Errorf("invalid target: %w", err)
    }

    cb.args = append(cb.args, target)
    return cb, nil
}

func (cb *CommandBuilder) Execute(ctx context.Context) ([]byte, error) {
    // Add timeout to context
    ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
    defer cancel()

    // Build command
    cmd := exec.CommandContext(ctx, cb.program, cb.args...)

    // Execute
    output, err := cmd.CombinedOutput()

    if ctx.Err() == context.DeadlineExceeded {
        return nil, errors.New("command timeout")
    }

    if err != nil {
        return nil, fmt.Errorf("command failed: %w", err)
    }

    return output, nil
}

// Alternative: Lower-level safe execution
type CommandExecutor struct {
    timeout time.Duration
}

func NewCommandExecutor(timeout time.Duration) *CommandExecutor {
    return &CommandExecutor{
        timeout: timeout,
    }
}

func (ce *CommandExecutor) ExecuteSafe(ctx context.Context, program string, args []string) ([]byte, error) {
    // Validate program
    if !allowedPrograms[program] {
        return nil, fmt.Errorf("program not allowed: %s", program)
    }

    // Validate all arguments are safe strings
    for _, arg := range args {
        if containsShellMetachar(arg) {
            return nil, fmt.Errorf("argument contains shell metacharacters: %s", arg)
        }
    }

    // Create context with timeout
    ctx, cancel := context.WithTimeout(ctx, ce.timeout)
    defer cancel()

    // Execute command
    cmd := exec.CommandContext(ctx, program, args...)

    // Clear environment to prevent injection
    cmd.Env = []string{}

    output, err := cmd.CombinedOutput()

    if ctx.Err() == context.DeadlineExceeded {
        return nil, errors.New("command timeout")
    }

    return output, err
}

func containsShellMetachar(s string) bool {
    // Check for shell metacharacters
    dangerousChars := []byte{'&', '|', ';', '$', '`', '\\n', '(', ')', '<', '>'}
    for _, char := range dangerousChars {
        for i := 0; i < len(s); i++ {
            if s[i] == char {
                return true
            }
        }
    }
    return false
}

// Usage examples
func main() {
    ctx := context.Background()

    // Using builder
    builder, err := NewCommandBuilder("ping")
    if err != nil {
        fmt.Printf("Error: %v\\n", err)
        return
    }

    output, err := builder.
        AddOption("-c", "4").
        AddTarget("8.8.8.8").
        Execute(ctx)

    if err != nil {
        fmt.Printf("Error: %v\\n", err)
        return
    }

    fmt.Printf("Output:\\n%s\\n", output)

    // Using executor
    executor := NewCommandExecutor(10 * time.Second)
    output2, err := executor.ExecuteSafe(ctx, "dig", []string{"+short", "google.com"})
    if err != nil {
        fmt.Printf("Error: %v\\n", err)
        return
    }

    fmt.Printf("Output:\\n%s\\n", output2)
}
```

**Security Pattern:**
- **exec.Command with args** - Never use shell
- **Context with timeout** - All commands have time limits
- **Allowlist validation** - Programs, options, and patterns
- **Empty environment** - `cmd.Env = []string{}` prevents injection
- **Shell metacharacter detection** - Additional safety check
- **Builder pattern** - Type-safe command construction

**Critical Go Rules:**
1. Never use `exec.Command("sh", "-c", ...)` with user input
2. Always pass arguments separately, not in command string
3. Always use `CommandContext` with timeout
4. Clear environment with `cmd.Env = []string{}`
5. Validate all inputs against allowlists
6. Check for shell metacharacters as additional safety"""
            }
        ],
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": datetime.now().strftime('%Y-%m-%d'),
            "issues": []
        }
    }


def generate_all_examples():
    """Generate all command injection examples"""
    examples = [
        python_subprocess_injection(),
        php_shell_exec_injection(),
        java_runtime_exec_injection(),
        nodejs_child_process_injection(),
        go_exec_command_injection(),
    ]

    return examples


if __name__ == '__main__':
    examples = generate_all_examples()

    # Save to JSONL file
    output_file = Path(__file__).parent.parent / 'data' / 'command_injection_batch_002.jsonl'
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        for example in examples:
            f.write(json.dumps(example, indent=None) + '\n')

    print(f"✓ Generated {len(examples)} command injection examples")
    print(f"✓ Saved to: {output_file}")
    print("\nExamples:")
    for ex in examples:
        lang = ex['metadata']['lang']
        turns = len(ex['conversations'])
        context = ex.get('context', {}).get('cve', 'N/A')
        print(f"  - {ex['id']}: {lang} / {turns} turns / CVE: {context}")
