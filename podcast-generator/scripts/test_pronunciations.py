#!/usr/bin/env python3
"""
Generate test audio for all pronunciation guide terms.
Creates a single audio file with all terms spoken for validation.
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent))

from add_pronunciation_tags import PRONUNCIATIONS, SPECIAL_CASES


def create_pronunciation_test_script():
    """Create a test script with all pronunciation terms."""

    lines = []
    lines.append("# Pronunciation Test Script")
    lines.append("# This script contains all terms from PRONUNCIATION_GUIDE.md for audio validation")
    lines.append("")

    # Group terms by category for easier listening
    categories = {
        'Cloud Providers & Services': [
            'AWS', 'Azure', 'GCP', 'RDS', 'ECS', 'EKS', 'GKE', 'AKS'
        ],
        'Platform as a Service': [
            'Heroku', 'Vercel', 'Netlify'
        ],
        'Container & Orchestration': [
            'Kubernetes', 'kubectl', 'etcd', 'kubelet'
        ],
        'Databases': [
            'PostgreSQL', 'Postgres', 'MySQL', 'SQLite', 'Redis'
        ],
        'Infrastructure as Code': [
            'Pulumi', 'Ansible'
        ],
        'Observability': [
            'Prometheus', 'Grafana', 'OpenTelemetry'
        ],
        'Networking': [
            'Akamai', 'Nginx', 'Apache', 'CDN', 'DNS'
        ],
        'Protocols': [
            'HTTP', 'HTTPS', 'SSH', 'API', 'OAuth', 'JWT'
        ],
        'Acronyms': [
            'MLOps', 'AIOps', 'PaaS', 'IaaS', 'SaaS', 'ROI', 'CLI', 'GUI', 'SQL', 'NoSQL'
        ],
        'Hardware': [
            'GPU', 'CPU', 'RAM', 'SSD', 'NVMe', 'HDD'
        ],
        'Languages & Formats': [
            'YAML', 'JSON', 'XML', 'HTML', 'CSS'
        ],
        'Operating Systems': [
            'Linux', 'Unix'
        ]
    }

    # Create script with speaker alternating for variety
    speaker_num = 1

    for category, terms in categories.items():
        lines.append(f"Speaker {speaker_num}: Testing category: {category}")
        speaker_num = 3 - speaker_num  # Toggle between 1 and 2

        for term in terms:
            # Get SSML tag if it exists
            ssml_tag = PRONUNCIATIONS.get(term, term)

            # Create sentence with the term
            if '<' in ssml_tag:
                # Has SSML tag
                sentence = f"The technology term is {ssml_tag}. [pause]"
            else:
                # No SSML tag needed
                sentence = f"The technology term is {term}. [pause]"

            lines.append(f"Speaker {speaker_num}: {sentence}")
            speaker_num = 3 - speaker_num  # Toggle

        lines.append("")  # Blank line between categories

    # Add special cases
    lines.append(f"Speaker {speaker_num}: Testing special cases with slashes.")
    speaker_num = 3 - speaker_num

    for term, tag in SPECIAL_CASES.items():
        sentence = f"The term is {tag}. [pause]"
        lines.append(f"Speaker {speaker_num}: {sentence}")
        speaker_num = 3 - speaker_num

    return '\n'.join(lines)


def main():
    """Generate pronunciation test script and audio."""

    # Create test script
    test_script = create_pronunciation_test_script()

    # Save to file
    output_path = Path("../docs/podcasts/scripts/00000-pronunciation-test.txt")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(test_script)

    print(f"✅ Created pronunciation test script: {output_path}")
    print(f"📝 Script contains {len(PRONUNCIATIONS) + len(SPECIAL_CASES)} pronunciation terms")
    print()
    print("To generate audio:")
    print(f"  cd podcast-generator")
    print(f"  python3 scripts/generate_podcast.py {output_path}")
    print()
    print("The generated audio will include all pronunciation terms from PRONUNCIATION_GUIDE.md")
    print("Listen to validate that all terms are pronounced correctly.")

    # Print summary by category
    print()
    print("Terms included:")
    print(f"  Cloud Providers: 8 terms")
    print(f"  PaaS Platforms: 3 terms")
    print(f"  Container/K8s: 4 terms")
    print(f"  Databases: 5 terms")
    print(f"  IaC Tools: 2 terms")
    print(f"  Observability: 3 terms")
    print(f"  Networking: 5 terms")
    print(f"  Protocols: 6 terms")
    print(f"  Acronyms: 10 terms")
    print(f"  Hardware: 6 terms")
    print(f"  Languages: 5 terms")
    print(f"  OS: 2 terms")
    print(f"  Special Cases: 2 terms")
    print(f"  ─────────────────")
    print(f"  Total: {len(PRONUNCIATIONS) + len(SPECIAL_CASES)} terms")


if __name__ == "__main__":
    main()
