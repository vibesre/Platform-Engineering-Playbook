#!/usr/bin/env python3
"""
Add pronunciation tags to podcast scripts based on PRONUNCIATION_GUIDE.md.
"""

import re
from pathlib import Path
import argparse


# Pronunciation mapping from PRONUNCIATION_GUIDE.md
PRONUNCIATIONS = {
    # Cloud Providers (say-as characters)
    'AWS': '<say-as interpret-as="characters">AWS</say-as>',
    'GCP': '<say-as interpret-as="characters">GCP</say-as>',
    'RDS': '<say-as interpret-as="characters">RDS</say-as>',
    'ECS': '<say-as interpret-as="characters">ECS</say-as>',
    'EKS': '<say-as interpret-as="characters">EKS</say-as>',
    'GKE': '<say-as interpret-as="characters">GKE</say-as>',
    'AKS': '<say-as interpret-as="characters">AKS</say-as>',

    # Cloud Providers (phoneme)
    'Azure': '<phoneme alphabet="ipa" ph="ˈæʒɚ">Azure</phoneme>',

    # PaaS Platforms
    'Heroku': '<phoneme alphabet="ipa" ph="hɛˈroʊku">Heroku</phoneme>',
    'Vercel': '<phoneme alphabet="ipa" ph="ˈvɝsəl">Vercel</phoneme>',
    'Netlify': '<phoneme alphabet="ipa" ph="ˈnɛtlɪfaɪ">Netlify</phoneme>',

    # Container & Orchestration (Source: kubernetes.io official pronunciation)
    'Kubernetes': '<phoneme alphabet="ipa" ph="ˌkubɚˈnɛtiz">Kubernetes</phoneme>',
    'kubectl': '<phoneme alphabet="ipa" ph="ˈkubkənˌtroʊl">kubectl</phoneme>',
    'etcd': '<phoneme alphabet="ipa" ph="ɛt si di">etcd</phoneme>',
    'kubelet': '<phoneme alphabet="ipa" ph="ˈkublɪt">kubelet</phoneme>',

    # Databases
    'PostgreSQL': '<phoneme alphabet="ipa" ph="ˈpoʊstɡrɛs kju ɛl">PostgreSQL</phoneme>',
    'Postgres': '<phoneme alphabet="ipa" ph="ˈpoʊstɡrɛs">Postgres</phoneme>',
    # MySQL and SQLite: Let Chirp3-HD handle naturally (no custom pronunciation needed)
    # 'MySQL': 'MySQL',  # Commented out - use natural pronunciation
    # 'SQLite': 'SQLite',  # Commented out - use natural pronunciation
    'Redis': '<phoneme alphabet="ipa" ph="ˈrɛdɪs">Redis</phoneme>',

    # Infrastructure as Code
    'Pulumi': '<phoneme alphabet="ipa" ph="puˈlumi">Pulumi</phoneme>',
    'Ansible': '<phoneme alphabet="ipa" ph="ˈænsəbəl">Ansible</phoneme>',

    # Observability
    'Prometheus': '<phoneme alphabet="ipa" ph="prəˈmiθiəs">Prometheus</phoneme>',
    'Grafana': '<phoneme alphabet="ipa" ph="ɡrəˈfɑnə">Grafana</phoneme>',
    'OpenTelemetry': '<phoneme alphabet="ipa" ph="ˈoʊpən tɛˈlɛmɪtri">OpenTelemetry</phoneme>',

    # Networking
    'Akamai': '<phoneme alphabet="ipa" ph="ˈɑkəmaɪ">Akamai</phoneme>',
    'Nginx': '<phoneme alphabet="ipa" ph="ˈɛndʒɪn ˈɛks">Nginx</phoneme>',
    'Apache': '<phoneme alphabet="ipa" ph="əˈpætʃi">Apache</phoneme>',
    'CDN': '<say-as interpret-as="characters">CDN</say-as>',
    'DNS': '<say-as interpret-as="characters">DNS</say-as>',

    # Protocols
    'HTTP': '<say-as interpret-as="characters">HTTP</say-as>',
    'HTTPS': '<say-as interpret-as="characters">HTTPS</say-as>',
    'SSH': '<say-as interpret-as="characters">SSH</say-as>',
    'API': '<say-as interpret-as="characters">API</say-as>',
    'OAuth': '<phoneme alphabet="ipa" ph="ˈoʊɑθ">OAuth</phoneme>',
    'JWT': '<say-as interpret-as="characters">JWT</say-as>',

    # Acronyms
    'MLOps': '<phoneme alphabet="ipa" ph="ɛm ɛl ɑps">MLOps</phoneme>',
    'AIOps': '<phoneme alphabet="ipa" ph="ˌeɪ aɪ ɑps">AIOps</phoneme>',
    'PaaS': '<phoneme alphabet="ipa" ph="pæs">PaaS</phoneme>',
    'IaaS': '<phoneme alphabet="ipa" ph="ˈaɪæs">IaaS</phoneme>',
    'SaaS': '<phoneme alphabet="ipa" ph="sæs">SaaS</phoneme>',
    'ROI': '<say-as interpret-as="characters">ROI</say-as>',
    'CLI': '<say-as interpret-as="characters">CLI</say-as>',
    'GUI': '<phoneme alphabet="ipa" ph="ˈɡui">GUI</phoneme>',
    'SQL': '<phoneme alphabet="ipa" ph="ˌɛskjuː ˈɛl">SQL</phoneme>',
    'NoSQL': '<phoneme alphabet="ipa" ph="noʊ ˌɛskjuː ˈɛl">NoSQL</phoneme>',

    # Hardware
    'GPU': '<say-as interpret-as="characters">GPU</say-as>',
    'CPU': '<say-as interpret-as="characters">CPU</say-as>',
    'RAM': '<say-as interpret-as="characters">RAM</say-as>',
    'SSD': '<say-as interpret-as="characters">SSD</say-as>',
    'NVMe': '<say-as interpret-as="characters">NVMe</say-as>',
    'HDD': '<say-as interpret-as="characters">HDD</say-as>',

    # Languages
    'YAML': '<phoneme alphabet="ipa" ph="ˈjæməl">YAML</phoneme>',
    'JSON': '<phoneme alphabet="ipa" ph="ˈdʒeɪsən">JSON</phoneme>',
    'XML': '<say-as interpret-as="characters">XML</say-as>',
    'HTML': '<say-as interpret-as="characters">HTML</say-as>',
    'CSS': '<say-as interpret-as="characters">CSS</say-as>',

    # Operating Systems
    'Linux': '<phoneme alphabet="ipa" ph="ˈlɪnəks">Linux</phoneme>',
    'Unix': '<phoneme alphabet="ipa" ph="ˈjunɪks">Unix</phoneme>',
}

# Special cases that need context-aware handling
SPECIAL_CASES = {
    'CI/CD': '<say-as interpret-as="characters">CI</say-as>/<say-as interpret-as="characters">CD</say-as>',
    'TCP/IP': '<say-as interpret-as="characters">TCP</say-as>/IP',
}


def add_pronunciation_tags(text: str, verbose: bool = False) -> tuple:
    """
    Add pronunciation tags to text.

    Args:
        text: Script text
        verbose: Print replacements

    Returns:
        Tuple of (modified_text, replacements_count)
    """
    # Check if already has pronunciation tags
    if '<phoneme' in text or '<say-as' in text:
        if verbose:
            print("  ⚠️  Script already contains pronunciation tags, skipping")
        return text, 0

    replacements = {}
    modified_text = text

    # Handle special cases first (they contain /)
    for term, tag in SPECIAL_CASES.items():
        # Use word boundaries to avoid partial matches
        pattern = rf'\b{re.escape(term)}\b'
        matches = re.findall(pattern, modified_text)
        if matches:
            modified_text = re.sub(pattern, tag, modified_text)
            replacements[term] = len(matches)
            if verbose:
                print(f"    {term} → {len(matches)} occurrences")

    # Handle regular pronunciations
    for term, tag in PRONUNCIATIONS.items():
        # Use word boundaries to avoid partial matches
        # Case-sensitive to avoid false positives
        pattern = rf'\b{re.escape(term)}\b'
        matches = re.findall(pattern, modified_text)
        if matches:
            modified_text = re.sub(pattern, tag, modified_text)
            replacements[term] = len(matches)
            if verbose:
                print(f"    {term} → {len(matches)} occurrences")

    total_replacements = sum(replacements.values())
    return modified_text, total_replacements


def process_script_file(script_path: Path, dry_run: bool = False, verbose: bool = False) -> dict:
    """
    Add pronunciation tags to a script file.

    Args:
        script_path: Path to script file
        dry_run: If True, don't write changes
        verbose: Print detailed replacements

    Returns:
        Dict with processing stats
    """
    print(f"\nProcessing: {script_path.name}")

    # Read original content
    with open(script_path, 'r') as f:
        original = f.read()

    # Add pronunciation tags
    modified, count = add_pronunciation_tags(original, verbose=verbose)

    stats = {
        'file': script_path.name,
        'replacements': count,
        'changed': original != modified
    }

    print(f"  Pronunciations added: {count}")

    # Write changes if not dry run
    if not dry_run and stats['changed']:
        # Backup original
        backup_path = script_path.with_suffix('.txt.pronunciation_bak')
        with open(backup_path, 'w') as f:
            f.write(original)
        print(f"  ✓ Backup created: {backup_path.name}")

        # Write modified
        with open(script_path, 'w') as f:
            f.write(modified)
        print(f"  ✓ Updated with pronunciation tags")
    elif dry_run and stats['changed']:
        print(f"  (Dry run - no changes written)")

    return stats


def main():
    """Process podcast scripts to add pronunciation tags."""
    parser = argparse.ArgumentParser(
        description="Add pronunciation tags to podcast scripts for proper TTS"
    )

    parser.add_argument(
        "scripts_dir",
        type=Path,
        default=Path("../docs/podcasts/scripts"),
        nargs='?',
        help="Directory containing podcast scripts (default: ../docs/podcasts/scripts)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without writing files"
    )

    parser.add_argument(
        "--file",
        type=str,
        help="Process a specific file instead of entire directory"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed replacement information"
    )

    args = parser.parse_args()

    if args.file:
        # Process single file
        script_path = Path(args.file)
        if not script_path.exists():
            print(f"Error: File not found: {script_path}")
            return

        stats = process_script_file(script_path, dry_run=args.dry_run, verbose=args.verbose)

        print("\n" + "="*80)
        print(f"Summary: Added {stats['replacements']} pronunciation tags")

    else:
        # Process directory
        if not args.scripts_dir.exists():
            print(f"Error: Directory not found: {args.scripts_dir}")
            return

        scripts = sorted(args.scripts_dir.glob("*.txt"))
        if not scripts:
            print(f"No script files found in {args.scripts_dir}")
            return

        print(f"Found {len(scripts)} script files")

        all_stats = []
        for script_path in scripts:
            stats = process_script_file(script_path, dry_run=args.dry_run, verbose=args.verbose)
            all_stats.append(stats)

        # Print summary
        print("\n" + "="*80)
        print("Summary:")
        total_replacements = sum(s['replacements'] for s in all_stats)
        print(f"  Total files: {len(all_stats)}")
        print(f"  Total pronunciation tags added: {total_replacements}")

        if args.dry_run:
            print("\n  This was a dry run. Use without --dry-run to apply changes.")


if __name__ == "__main__":
    main()
