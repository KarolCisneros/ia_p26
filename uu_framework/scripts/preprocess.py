#!/usr/bin/env python3
"""
uu_framework Preprocessing Script

Main orchestrator for preprocessing course content.
Runs all preprocessing steps in order:
1. Extract metadata from markdown files
2. Generate hierarchy tree
3. Aggregate tasks (homework, exams, projects)

Usage:
    python3 preprocess.py [--config CONFIG_PATH] [--content CONTENT_DIR]
"""

import os
import sys
import argparse
import json
from pathlib import Path

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from extract_metadata import extract_all_metadata
from generate_indices import generate_hierarchy
from aggregate_tasks import aggregate_all_tasks


def load_config(config_path: Path) -> dict:
    """Load site configuration from YAML file."""
    try:
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except ImportError:
        # Fallback if PyYAML not available
        print("Warning: PyYAML not installed, using defaults")
        return {}
    except FileNotFoundError:
        print(f"Warning: Config file not found at {config_path}, using defaults")
        return {}


def main():
    parser = argparse.ArgumentParser(description='uu_framework preprocessor')
    parser.add_argument('--config', type=Path,
                        default=Path('uu_framework/config/site.yaml'),
                        help='Path to site configuration')
    parser.add_argument('--content', type=Path,
                        default=Path('clase'),
                        help='Path to content directory')
    parser.add_argument('--output', type=Path,
                        default=Path('uu_framework/eleventy/_data'),
                        help='Path to output data directory')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Enable verbose output')

    args = parser.parse_args()

    # Ensure output directory exists
    args.output.mkdir(parents=True, exist_ok=True)

    # Load configuration
    config = load_config(args.config)
    if args.verbose:
        print(f"Loaded config from {args.config}")

    # Get exclude patterns from config
    exclude = config.get('source', {}).get('exclude', [])

    print("=" * 60)
    print("uu_framework Preprocessing")
    print("=" * 60)

    # Step 1: Extract metadata from all markdown files
    print("\n[1/3] Extracting metadata from markdown files...")
    metadata = extract_all_metadata(args.content, exclude, args.verbose)

    # Save metadata
    metadata_path = args.output / 'metadata.json'
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"      Saved {len(metadata)} file metadata records to {metadata_path}")

    # Step 2: Generate hierarchy tree
    print("\n[2/3] Generating hierarchy tree...")
    hierarchy = generate_hierarchy(args.content, metadata, exclude, args.verbose)

    # Save hierarchy
    hierarchy_path = args.output / 'hierarchy.json'
    with open(hierarchy_path, 'w', encoding='utf-8') as f:
        json.dump(hierarchy, f, indent=2, ensure_ascii=False)
    print(f"      Saved hierarchy to {hierarchy_path}")

    # Step 3: Aggregate tasks (homework, exams, projects)
    print("\n[3/3] Aggregating tasks...")
    tasks = aggregate_all_tasks(args.content, metadata, args.verbose)

    # Save tasks
    tasks_path = args.output / 'tasks.json'
    with open(tasks_path, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
    print(f"      Saved {sum(len(v) for v in tasks.values())} tasks to {tasks_path}")

    # Save site config for templates
    site_path = args.output / 'site.json'
    with open(site_path, 'w', encoding='utf-8') as f:
        json.dump(config.get('site', {}), f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print("Preprocessing complete!")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    sys.exit(main())
