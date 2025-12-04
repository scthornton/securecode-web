#!/usr/bin/env python3
"""
SecureCode v2.0 API-Driven Example Generator

Generates secure code training examples using Claude and OpenAI APIs.
Supports batch generation, automatic validation, and retry logic.

Usage:
    python3 api_generator.py --batch 011 --provider claude
    python3 api_generator.py --batch 016-025 --provider claude --parallel 5
    python3 api_generator.py --all --dry-run
"""

import anthropic
import openai
import json
import yaml
import argparse
import sys
from pathlib import Path
from datetime import date
from typing import Dict, List, Optional, Tuple
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SecureCodeGenerator:
    """Main generator class for API-driven example creation"""

    def __init__(self, provider: str = "claude", api_key: Optional[str] = None):
        """
        Initialize generator with API provider

        Args:
            provider: "claude", "openai", or "gemini"
            api_key: API key (or will read from environment)
        """
        self.provider = provider
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'retries': 0,
            'api_calls': 0,
            'tokens_used': 0
        }

        # Initialize API client
        if provider == "claude":
            self.client = anthropic.Anthropic(api_key=api_key)
            self.model = "claude-opus-4-5-20251101"  # Claude Opus 4.5 (best for complex tasks)
        elif provider == "openai":
            self.client = openai.OpenAI(api_key=api_key)
            self.model = "gpt-5.1-2025-11-13"
        elif provider == "gemini":
            # Placeholder for Gemini integration
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        else:
            raise ValueError(f"Unknown provider: {provider}")

        # Load configuration
        self.config_dir = Path(__file__).parent.parent / 'config'
        self.prompts_dir = Path(__file__).parent.parent / 'prompts'
        self.output_dir = Path(__file__).parent.parent.parent / 'data'

        # Load generation plan (expanded version with individual batch definitions)
        with open(self.config_dir / 'generation_plan_expanded.yaml', 'r') as f:
            self.generation_plan = yaml.safe_load(f)

        # Load master prompt template
        with open(self.prompts_dir / 'master_prompt_template.txt', 'r') as f:
            self.master_prompt_template = f.read()

        # Load OWASP/CWE mappings
        self.owasp_cwe_mappings = self._load_owasp_cwe_mappings()

    def _load_owasp_cwe_mappings(self) -> Dict:
        """Load OWASP to CWE mappings"""
        return {
            'sql_injection': {'owasp': 'A03:2021-Injection', 'cwe': 'CWE-89'},
            'command_injection': {'owasp': 'A03:2021-Injection', 'cwe': 'CWE-78'},
            'xss': {'owasp': 'A03:2021-Injection', 'cwe': 'CWE-79'},
            'nosql_injection': {'owasp': 'A03:2021-Injection', 'cwe': 'CWE-943'},
            'template_injection': {'owasp': 'A03:2021-Injection', 'cwe': 'CWE-94'},
            'xxe': {'owasp': 'A03:2021-Injection', 'cwe': 'CWE-611'},
            'ldap_injection': {'owasp': 'A03:2021-Injection', 'cwe': 'CWE-90'},
            'authentication': {'owasp': 'A07:2021-Identification and Authentication Failures', 'cwe': 'CWE-287'},
            'authorization': {'owasp': 'A01:2021-Broken Access Control', 'cwe': 'CWE-284'},
            'misconfiguration': {'owasp': 'A05:2021-Security Misconfiguration', 'cwe': 'CWE-16'},
            'cryptography': {'owasp': 'A02:2021-Cryptographic Failures', 'cwe': 'CWE-327'},
            'design_flaws': {'owasp': 'A04:2021-Insecure Design', 'cwe': 'CWE-840'},
            'dependencies': {'owasp': 'A06:2021-Vulnerable and Outdated Components', 'cwe': 'CWE-1035'},
            'integrity': {'owasp': 'A08:2021-Software and Data Integrity Failures', 'cwe': 'CWE-502'},
            'logging': {'owasp': 'A09:2021-Security Logging and Monitoring Failures', 'cwe': 'CWE-778'},
            'ssrf': {'owasp': 'A10:2021-Server-Side Request Forgery', 'cwe': 'CWE-918'},
            'ai_security': {'owasp': 'AI/ML Security Threats', 'cwe': 'CWE-1357'},
        }

    def build_prompt(self, batch_config: Dict, example_num: int, language: str) -> str:
        """
        Build generation prompt from template

        Args:
            batch_config: Batch configuration from generation_plan.yaml
            example_num: Example number within batch
            language: Programming language for this example

        Returns:
            Complete prompt string
        """
        subcategory = batch_config['subcategory']
        category = batch_config['category']

        # Get OWASP/CWE mappings
        mapping = self.owasp_cwe_mappings.get(subcategory, {})
        owasp_mapping = mapping.get('owasp', 'Unknown')
        cwe = mapping.get('cwe', 'CWE-000')

        # Generate example ID
        example_id = f"{subcategory.replace('_', '-')}-{str(example_num).zfill(6)}"

        # Get technique (rotate through available techniques)
        techniques = batch_config.get('techniques', [])
        technique = techniques[example_num % len(techniques)] if techniques else "general"

        # Build prompt from template
        prompt = self.master_prompt_template.format(
            category=category,
            subcategory=subcategory,
            language=language,
            technique=technique,
            owasp_mapping=owasp_mapping,
            cwe=cwe,
            example_id=example_id,
            additional_context=""
        )

        return prompt

    def call_api(self, prompt: str, max_tokens: int = 4096) -> Tuple[str, Dict]:
        """
        Call API to generate example

        Args:
            prompt: Generation prompt
            max_tokens: Maximum response tokens

        Returns:
            (response_text, usage_stats)
        """
        self.stats['api_calls'] += 1

        try:
            if self.provider == "claude":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )

                text = response.content[0].text
                usage = {
                    'input_tokens': response.usage.input_tokens,
                    'output_tokens': response.usage.output_tokens
                }
                self.stats['tokens_used'] += usage['input_tokens'] + usage['output_tokens']

                return text, usage

            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    max_completion_tokens=max_tokens,
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )

                text = response.choices[0].message.content
                usage = {
                    'input_tokens': response.usage.prompt_tokens,
                    'output_tokens': response.usage.completion_tokens
                }
                self.stats['tokens_used'] += usage['input_tokens'] + usage['output_tokens']

                return text, usage

            elif self.provider == "gemini":
                response = self.model.generate_content(prompt)
                text = response.text
                usage = {'input_tokens': 0, 'output_tokens': 0}  # Gemini doesn't expose token counts easily

                return text, usage

        except Exception as e:
            logger.error(f"API call failed: {e}")
            raise

    def parse_response(self, response_text: str) -> Optional[Dict]:
        """
        Parse API response into example JSON

        Args:
            response_text: Raw API response

        Returns:
            Parsed example dict or None if parsing failed
        """
        try:
            # Try to extract JSON from response
            # Handle cases where model wraps JSON in markdown
            text = response_text.strip()

            # Remove markdown code fences if present
            if text.startswith('```json'):
                text = text[7:]
            if text.startswith('```'):
                text = text[3:]
            if text.endswith('```'):
                text = text[:-3]

            text = text.strip()

            # Strip any preamble text before the JSON object
            # (e.g., "Here is the secure code training example in JSON format:")
            if '{' in text:
                text = text[text.find('{'):]

            # Parse JSON
            example = json.loads(text)

            return example

        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}")
            logger.debug(f"Response text: {response_text[:500]}")
            return None

    def validate_example(self, example: Dict) -> Tuple[bool, List[str]]:
        """
        Validate generated example

        Args:
            example: Example dictionary

        Returns:
            (is_valid, list_of_issues)
        """
        issues = []

        # Check required fields
        required_fields = ['id', 'metadata', 'context', 'conversations', 'validation']
        for field in required_fields:
            if field not in example:
                issues.append(f"Missing required field: {field}")

        # Check conversation structure
        if 'conversations' in example:
            if len(example['conversations']) != 4:  # 4 turns = 4 messages
                issues.append(f"Expected 4 conversation messages (4 turns), got {len(example['conversations'])}")

            # Check turn numbers (should be 1, 2, 3, 4)
            for i, conv in enumerate(example['conversations']):
                expected_turn = i + 1
                if conv.get('turn') != expected_turn:
                    issues.append(f"Conversation {i}: expected turn {expected_turn}, got {conv.get('turn')}")

        # Check metadata
        if 'metadata' in example:
            required_metadata = ['lang', 'category', 'subcategory', 'owasp_2021', 'cwe']
            for field in required_metadata:
                if field not in example['metadata']:
                    issues.append(f"Missing metadata field: {field}")

        # Check validation field
        if 'validation' in example:
            val = example['validation']
            if val.get('syntax_check') == 'pending':
                issues.append("validation.syntax_check should be 'not_tested', not 'pending'")

        return len(issues) == 0, issues

    def generate_example(
        self,
        batch_config: Dict,
        example_num: int,
        language: str,
        max_retries: int = 3
    ) -> Optional[Dict]:
        """
        Generate a single example with retry logic

        Args:
            batch_config: Batch configuration
            example_num: Example number
            language: Programming language
            max_retries: Maximum retry attempts

        Returns:
            Generated example dict or None
        """
        for attempt in range(max_retries):
            try:
                logger.info(f"Generating example {example_num} ({language}) - attempt {attempt + 1}/{max_retries}")

                # Build prompt
                prompt = self.build_prompt(batch_config, example_num, language)

                # Call API (Claude Opus 4.5 supports up to 8192 output tokens)
                response_text, usage = self.call_api(prompt, max_tokens=8192)

                # Parse response
                example = self.parse_response(response_text)
                if not example:
                    logger.warning(f"Failed to parse response on attempt {attempt + 1}")
                    self.stats['retries'] += 1
                    continue

                # Validate
                is_valid, issues = self.validate_example(example)
                if not is_valid:
                    logger.warning(f"Validation failed on attempt {attempt + 1}: {issues}")
                    self.stats['retries'] += 1
                    continue

                # Success!
                self.stats['success'] += 1
                logger.info(f"✓ Generated {example['id']} (tokens: {usage['input_tokens']}/{usage['output_tokens']})")
                return example

            except Exception as e:
                logger.error(f"Generation failed on attempt {attempt + 1}: {e}")
                self.stats['retries'] += 1
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff

        # All retries failed
        self.stats['failed'] += 1
        logger.error(f"✗ Failed to generate example {example_num} after {max_retries} attempts")
        return None

    def generate_batch(
        self,
        batch_id: str,
        dry_run: bool = False,
        parallel: int = 1
    ) -> List[Dict]:
        """
        Generate a complete batch of examples

        Args:
            batch_id: Batch ID (e.g., "011" or "016-025")
            dry_run: If True, only show what would be generated
            parallel: Number of parallel API calls

        Returns:
            List of generated examples
        """
        # Find batch config
        batch_config = None
        for batch in self.generation_plan['batches']:
            if batch['batch_id'] == batch_id:
                batch_config = batch
                break

        if not batch_config:
            logger.error(f"Batch {batch_id} not found in generation plan")
            return []

        logger.info(f"\n{'='*60}")
        logger.info(f"Batch {batch_id}: {batch_config['name']}")
        logger.info(f"{'='*60}")
        logger.info(f"Category: {batch_config['category']}")
        logger.info(f"Subcategory: {batch_config['subcategory']}")
        logger.info(f"Count: {batch_config['count']}")
        logger.info(f"Provider: {batch_config['provider']}")
        logger.info(f"Languages: {', '.join(batch_config['languages'])}")

        if dry_run:
            logger.info("\n[DRY RUN] Would generate these examples:")
            for i in range(batch_config['count']):
                lang = batch_config['languages'][i % len(batch_config['languages'])]
                logger.info(f"  {i+1:3d}. {batch_config['subcategory']}-{str(i+1).zfill(6)} ({lang})")
            return []

        # Generate examples
        examples = []
        count = batch_config['count']
        languages = batch_config['languages']

        if parallel > 1:
            # Parallel generation
            with ThreadPoolExecutor(max_workers=parallel) as executor:
                futures = []
                for i in range(count):
                    lang = languages[i % len(languages)]
                    future = executor.submit(
                        self.generate_example,
                        batch_config,
                        i + 1,
                        lang
                    )
                    futures.append(future)

                for future in as_completed(futures):
                    example = future.result()
                    if example:
                        examples.append(example)
        else:
            # Sequential generation
            for i in range(count):
                self.stats['total'] += 1
                lang = languages[i % len(languages)]

                example = self.generate_example(batch_config, i + 1, lang)
                if example:
                    examples.append(example)

        # Save to file
        if examples:
            output_file = self.output_dir / f"{batch_config['subcategory']}_batch_{batch_id}.jsonl"
            with open(output_file, 'w', encoding='utf-8') as f:
                for example in examples:
                    f.write(json.dumps(example, ensure_ascii=False) + '\n')

            logger.info(f"\n✓ Saved {len(examples)} examples to {output_file}")

        # Print stats
        logger.info(f"\nBatch {batch_id} Stats:")
        logger.info(f"  Success: {len(examples)}/{count}")
        logger.info(f"  Failed: {count - len(examples)}")
        logger.info(f"  API Calls: {self.stats['api_calls']}")
        logger.info(f"  Retries: {self.stats['retries']}")

        return examples

    def print_final_stats(self):
        """Print final generation statistics"""
        logger.info(f"\n{'='*60}")
        logger.info("FINAL STATISTICS")
        logger.info(f"{'='*60}")
        logger.info(f"Total Examples: {self.stats['total']}")
        if self.stats['total'] > 0:
            logger.info(f"Successful: {self.stats['success']} ({self.stats['success']/self.stats['total']*100:.1f}%)")
        else:
            logger.info(f"Successful: {self.stats['success']}")
        logger.info(f"Failed: {self.stats['failed']}")
        logger.info(f"Total API Calls: {self.stats['api_calls']}")
        logger.info(f"Total Retries: {self.stats['retries']}")
        logger.info(f"Total Tokens: {self.stats['tokens_used']:,}")

        # Estimate cost
        if self.provider == "claude":
            cost = (self.stats['tokens_used'] / 1_000_000) * 9  # Rough avg: $9/M tokens
            logger.info(f"Estimated Cost: ${cost:.2f}")
        elif self.provider == "openai":
            cost = (self.stats['tokens_used'] / 1_000_000) * 20  # Rough avg: $20/M tokens
            logger.info(f"Estimated Cost: ${cost:.2f}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate SecureCode v2.0 examples using AI APIs'
    )
    parser.add_argument(
        '--batch',
        type=str,
        help='Batch ID (e.g., "011" or "016-025")'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Generate all batches'
    )
    parser.add_argument(
        '--provider',
        type=str,
        choices=['claude', 'openai', 'gemini'],
        default='claude',
        help='API provider to use'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        help='API key (or set ANTHROPIC_API_KEY/OPENAI_API_KEY env var)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be generated without calling APIs'
    )
    parser.add_argument(
        '--parallel',
        type=int,
        default=1,
        help='Number of parallel API calls (1-10)'
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.batch and not args.all:
        parser.error("Must specify either --batch or --all")

    # Initialize generator
    try:
        generator = SecureCodeGenerator(
            provider=args.provider,
            api_key=args.api_key
        )
    except Exception as e:
        logger.error(f"Failed to initialize generator: {e}")
        logger.error("Make sure to set ANTHROPIC_API_KEY or OPENAI_API_KEY environment variable")
        sys.exit(1)

    # Generate batches
    if args.batch:
        generator.generate_batch(
            batch_id=args.batch,
            dry_run=args.dry_run,
            parallel=args.parallel
        )
    elif args.all:
        for batch in generator.generation_plan['batches']:
            batch_id = batch['batch_id']
            # Skip already completed batches (001-010)
            if batch_id in ['001', '002', '003', '005', '006', '007', '008', '009', '010']:
                continue

            generator.generate_batch(
                batch_id=batch_id,
                dry_run=args.dry_run,
                parallel=args.parallel
            )

            if not args.dry_run:
                time.sleep(5)  # Rate limiting between batches

    # Print final stats
    if not args.dry_run:
        generator.print_final_stats()


if __name__ == '__main__':
    main()
