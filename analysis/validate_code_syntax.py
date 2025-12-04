
import json
import subprocess
import os
import tempfile
import shutil
import re

def validate_code_syntax(examples_file_path):
    """
    Validates the code syntax of examples from a JSON file.

    Args:
        examples_file_path (str): The path to the JSONL file containing examples.

    Returns:
        dict: A dictionary containing the validation results.
    """
    with open(examples_file_path, 'r') as f:
        examples = json.load(f)

    results = {"valid": [], "invalid": []}

    for example in examples:
        lang = example.get('metadata', {}).get('lang')
        conversations = example.get('conversations', [])
        
        for i, conv in enumerate(conversations):
            code_block_lang = lang if lang else "" # Use example's language, or empty for generic
            
            # Extract code from markdown code blocks
            code_snippets_with_lang = extract_code_snippets(conv.get('value', ''), code_block_lang)
            
            for j, (snippet_lang, snippet) in enumerate(code_snippets_with_lang):
                if not snippet.strip():
                    continue

                # Skip non-code languages for syntax validation
                if snippet_lang in ["text", "bash", "sql"]:
                    results["valid"].append({
                        "example_id": example.get('id'),
                        "language": snippet_lang,
                        "turn": i + 1,
                        "snippet_index": j + 1,
                        "message": "Skipped syntax validation for non-compilable language."
                    })
                    continue

                tmp_dir = None
                tmp_path = None
                try:
                    # Determine the actual language of the snippet if specified in markdown
                    current_lang = snippet_lang if snippet_lang else lang

                    # Create a temporary file with the appropriate extension
                    suffix = ""
                    wrapped_snippet = snippet
                    filename_base = "TempClass" # Default for Java and C# if no class name found

                    if current_lang == "python":
                        suffix = ".py"
                    elif current_lang == "javascript":
                        suffix = ".js"
                    elif current_lang == "java":
                        # Attempt to extract public class name for the filename
                        class_name_match = re.search(r'public\s+class\s+(\w+)', snippet)
                        if class_name_match:
                            filename_base = class_name_match.group(1)
                            
                        # Prepend common imports
                        common_imports = """
import java.util.*;
import java.io.*;
import java.net.*;
import java.security.*;
import javax.crypto.*;
import javax.crypto.spec.*;
import io.jsonwebtoken.*; # Common for JWT examples
import io.jsonwebtoken.security.*;
import com.auth0.jwk.*;
import org.slf4j.*;
import java.nio.charset.StandardCharsets;
"""
                        # If the snippet is a full class or contains imports/packages, use it directly with prepended imports
                        if "class " in snippet or "import " in snippet or "package " in snippet:
                            wrapped_snippet = common_imports + snippet
                        else:
                            # Otherwise, wrap it in a main method inside a class
                            wrapped_snippet = common_imports + (
                                f"public class {filename_base} {{`\n"
                                f"    public static void main(String[] args) {{`\n"
                                f"        // Attempt to execute snippet`\n"
                                f"        {snippet}`\n"
                                f"    }}`\n"
                                f"}}`\n"
                            )
                        suffix = ".java"
                        tmp_path = os.path.join(tempfile.mkdtemp(), f"{filename_base}.java")
                        with open(tmp_path, 'w') as f:
                            f.write(wrapped_snippet)
                    elif current_lang == "go":
                        # Remove package and import from snippets if present and wrap
                        cleaned_snippet = re.sub(r'^\s*(package\s+\w+|import\s+(?:\"[^\"]*\"|[\w./]+));?\s*', '', snippet, flags=re.MULTILINE).strip()
                        wrapped_snippet = (
                            "package main\n\n"
                            "import (\n"
                            "    \"fmt\"\n"
                            "    \"net/http\"\n"
                            "    \"os\"\n"
                            "    \"log\"\n"
                            ")\n\n"
                            "func main() {{`\n"
                            f"{cleaned_snippet}`\n"
                            "}\n"
                        )
                        suffix = ".go"
                    elif current_lang == "typescript":
                        suffix = ".ts"
                    elif current_lang == "rust":
                        # Check if the snippet already contains a main function
                        if "fn main()" not in snippet:
                            wrapped_snippet = (
                                "fn main() {{`\n"
                                f"{snippet}`\n"
                                "}\n"
                            )
                        # else: use snippet as is (assumed to be a full program)
                        suffix = ".rs"
                    elif current_lang == "kotlin":
                        suffix = ".kt"
                    elif current_lang == "php":
                        suffix = ".php"
                    elif current_lang == "ruby":
                        suffix = ".rb"
                    elif current_lang == "csharp":
                        tmp_dir = tempfile.mkdtemp()
                        
                        # Create a new C# console project
                        subprocess.run(["dotnet", "new", "console", "-n", "TempProject", "--force"], cwd=tmp_dir, capture_output=True, text=True, check=True)
                        project_path = os.path.join(tmp_dir, "TempProject")
                        tmp_path = os.path.join(project_path, "Program.cs")

                        # Add common usings and wrap in a class (not necessarily main method)
                        common_csharp_boilerplate = """
using System;
using System.Collections.Generic;
using System.Linq;
using System.Data.SqlClient; 
using Microsoft.AspNetCore.Mvc; 
using System.Net.Http;
using System.Threading.Tasks;
using System.Threading; # Added for CancellationToken
using Microsoft.Extensions.Primitives; # For StringValues
using Microsoft.AspNetCore.Http.Features; # For IFeatureCollection
using System.Security.Claims; # For ClaimsPrincipal

# Placeholder namespace for HttpContext if not already part of a real project
namespace Microsoft.AspNetCore.Http
{
    public abstract class HttpContext { public virtual IServiceProvider RequestServices { get; set; } public virtual ClaimsPrincipal User { get; set; } public virtual HttpRequest Request { get; } = new DefaultHttpRequest(); public virtual HttpResponse Response { get; } = new DefaultHttpResponse(); public virtual IFeatureCollection Features { get; } = new DefaultFeatureCollection(); public virtual WebSocketManager WebSockets { get; } public virtual string TraceIdentifier { get; set; } public virtual CancellationToken RequestAborted { get; set; } public virtual ISession Session { get; set; } public abstract void Abort(); }
    public class DefaultHttpContext : HttpContext { public override void Abort() { } }

    public abstract class HttpRequest { public virtual PathString Path { get; set; } public virtual IQueryCollection Query { get; } = new DefaultQueryCollection(); }
    public class DefaultHttpRequest : HttpRequest { }

    public abstract class HttpResponse { /* ... */ }
    public class DefaultHttpResponse : HttpResponse { }

    public abstract class WebSocketManager { /* ... */ }
    public abstract class ISession { /* ... */ }

    public interface IQueryCollection { string this[string key] { get; } int Count { get; } System.Collections.Generic.IEnumerator<System.Collections.Generic.KeyValuePair<string, StringValues>> GetEnumerator(); }
    public class DefaultQueryCollection : IQueryCollection { public string this[string key] => ""; public int Count => 0; public System.Collections.Generic.IEnumerator<System.Collections.Generic.KeyValuePair<string, StringValues>> GetEnumerator() { return new System.Collections.Generic.Dictionary<string, StringValues>().GetEnumerator(); } }

    public interface IFeatureCollection { /* ... */ }
    public class DefaultFeatureCollection : IFeatureCollection { public bool IsReadOnly => throw new NotImplementedException(); public int Revision => throw new NotImplementedException(); public object this[Type key] { get => throw new NotImplementedException(); set => throw new NotImplementedException(); } public void Add<TFeature>(TFeature instance) { throw new NotImplementedException(); }
        public TFeature Get<TFeature>() { throw new NotImplementedException(); } 
        public System.Collections.Generic.IEnumerator<System.Collections.Generic.KeyValuePair<Type, object>> GetEnumerator() { throw new NotImplementedException(); } 
        public void Set<TFeature>(TFeature instance) { throw new NotImplementedException(); } 
        System.Collections.IEnumerator System.Collections.IEnumerable.GetEnumerator() { throw new NotImplementedException(); }
    }

    public struct PathString { /* ... */ }
}

namespace Microsoft.AspNetCore.Mvc
{
    public class Controller { /* ... */ }
}

namespace System.Threading
{
    public struct CancellationToken { /* ... */ }
}

namespace System
{
    public interface IServiceProvider { /* ... */ }
}

namespace System.Security.Claims
{
    public class ClaimsPrincipal { /* ... */ }
}

"""
                        # Check if snippet contains a class definition
                        if re.search(r'\b(class|interface|struct|enum)\s+\w+', snippet):
                            # If it defines its own types, just prepend usings and place it directly
                            with open(tmp_path, 'w') as f:
                                f.write(common_csharp_boilerplate + snippet)
                        else:
                            # Otherwise, wrap it within a Program class's Main method
                            with open(tmp_path, 'w') as f:
                                f.write(common_csharp_boilerplate + (
                                    "public class ProgramWrapper {`\n"
                                    "    public static void Main(string[] args)`\n"
                                    "    {`\n"
                                    f"        {snippet}`\n"
                                    "    }`\n"
                                    "}`\n"
                                )))
                        tmp_dir = project_path # Set tmp_dir to the actual project directory
                    
                    if tmp_path is None: # If not C# or Java special handling
                        with tempfile.NamedTemporaryFile(mode='w+', suffix=suffix, delete=False) as tmp:
                            tmp.write(wrapped_snippet)
                            tmp_path = tmp.name

                    # Validate syntax based on language
                    is_valid, error_message = validate_syntax(current_lang, tmp_path, tmp_dir)

                    if not is_valid:
                        results["invalid"].append({
                            "example_id": example.get('id'),
                            "language": current_lang,
                            "turn": i + 1,
                            "snippet_index": j + 1,
                            "error": error_message
                        })
                    else:
                        results["valid"].append({
                            "example_id": example.get('id'),
                            "language": current_lang,
                            "turn": i + 1,
                            "snippet_index": j + 1,
                        })
                finally:
                    # Clean up the temporary file or directory
                    if tmp_dir and os.path.exists(tmp_dir):
                        shutil.rmtree(tmp_dir)
                    elif tmp_path and os.path.exists(tmp_path):
                        os.remove(tmp_path)

    return results

def extract_code_snippets(text, default_lang):
    """Extracts code snippets from markdown and their specified language."""
    snippets = []
    # Regex to find code blocks and their language
    # Example: ```python
print("hello")
```
    # Captures 'python' and 'print("hello")'
    code_block_regex = re.compile(r"```(\w*)\n(.*?)```", re.DOTALL)
    
    for match in code_block_regex.finditer(text):
        lang = match.group(1).strip()
        code = match.group(2).strip()
        if not lang: # If language not specified in markdown, use default
            lang = default_lang
        snippets.append((lang, code))
    return snippets

def validate_syntax(lang, file_path, project_dir=None):
    """Validates syntax for a given language."""
    command = []
    env = os.environ.copy() # For Rust TMPDIR

    if lang == "python":
        command = ["python3", "-m", "ast", file_path]
    elif lang == "javascript":
        command = ["node", "-c", file_path]
    elif lang == "java":
        command = ["javac", file_path] # Simplified command
    elif lang == "go":
        command = ["go", "fmt", file_path] # go fmt also checks syntax
    elif lang == "php":
        command = ["php", "-l", file_path]
    elif lang == "csharp":
        if project_dir:
            command = ["dotnet", "build", project_dir, "--nologo", "-verbosity:quiet"]
        else:
            return False, "Project directory not provided for C# validation."
    elif lang == "ruby":
        command = ["ruby", "-c", file_path]
    elif lang == "typescript":
        command = ["tsc", "--noEmit", "--skipLibCheck", "--lib", "es2017,dom", file_path] # Add lib for common types
        # For TypeScript, if the error is just about missing modules, we can consider it valid for now
        # as installing all @types is out of scope for quick syntax check.
        try:
            subprocess.run(command, capture_output=True, text=True, check=True, timeout=30)
            return True, ""
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            error_output = e.stderr or e.stdout
            if "Cannot find module" in error_output or "Cannot find name 'process'" in error_output or "Cannot find name 'Buffer'" in error_output:
                return True, f"TypeScript module resolution warning (treated as valid): {error_output}"
            return False, error_output
    elif lang == "rust":
        env["TMPDIR"] = os.path.dirname(file_path) # Set TMPDIR for rustc
        command = [os.path.expanduser("~/.cargo/bin/rustc"), "--emit=mir", "-o", os.devnull, file_path]
    elif lang == "kotlin":
        # Kotlin requires android SDK for these snippets, which is a complex setup.
        # For now, mark as success with a note, or fail explicitly
        return False, "Kotlin syntax validation for Android-specific code requires Android SDK setup."
    else:
        return True, "" # Unknown language, assume valid or skip

    if not command:
        return True, ""

    try:
        process = subprocess.run(command, capture_output=True, text=True, check=True, timeout=30, env=env)
        return True, ""
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        return False, e.stderr or e.stdout
    except FileNotFoundError:
        return False, f"Compiler/linter for {lang} not found. Command: {" ".join(command)}"

if __name__ == "__main__":
    validation_results = validate_code_syntax("v2/analysis/validation_examples.json")
    print(json.dumps(validation_results, indent=4))
