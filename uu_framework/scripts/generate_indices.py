#!/usr/bin/env python3
"""
Hierarchy Generation Script

Generates a hierarchical tree structure from the content directory.
Respects the file naming convention:
- 00_ = index files
- 01_, 02_ = chapters/sections (numeric order)
- 01_a_, 01_b_ = sub-sections (alphabetical)
- A_, B_ = appendices (after numbered content)
- code/ = special code directory
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional


def get_sort_key(name: str) -> tuple:
    """
    Generate sort key for a file/directory name.

    Returns tuple for proper sorting:
    - (0, num, 0, '') for numbered items (01_, 02_)
    - (0, num, 1, letter) for lettered sub-items (01_a_, 01_b_)
    - (1, ord, 0, '') for appendices (A_, B_)
    - (2, 999, 0, name) for other items
    """
    # Numbered items: 01_, 02_, etc.
    match = re.match(r'^(\d+)_', name)
    if match:
        num = int(match.group(1))
        # Check for letter suffix: 01_a_, 01_b_
        letter_match = re.match(r'^\d+_([a-z])_', name)
        if letter_match:
            return (0, num, 1, letter_match.group(1))
        return (0, num, 0, '')

    # Appendices: A_, B_, etc.
    match = re.match(r'^([A-Z])_', name)
    if match:
        return (1, ord(match.group(1)), 0, '')

    # Special directories (code, etc.)
    if name.lower() == 'code':
        return (3, 0, 0, '')

    # Everything else
    return (2, 999, 0, name.lower())


def build_tree(
    dir_path: Path,
    metadata: Dict[str, Any],
    base_path: Path,
    exclude: List[str],
    depth: int = 0
) -> Dict[str, Any]:
    """
    Recursively build hierarchy tree from directory.

    Returns:
        Dict with structure:
        {
            'name': 'dirname',
            'path': 'relative/path',
            'type': 'directory' | 'file',
            'title': 'Human Title',
            'order': 1,
            'has_index': True,
            'children': [...]
        }
    """
    rel_path = dir_path.relative_to(base_path)
    name = dir_path.name

    # Check exclusions
    for excl in exclude:
        if excl in str(rel_path):
            return None

    node = {
        'name': name,
        'path': str(rel_path),
        'type': 'directory',
        'order': get_sort_key(name),
        'children': [],
        'has_index': False,
    }

    # Get title from index file if exists
    index_path = dir_path / '00_index.md'
    rel_index = str(rel_path / '00_index.md')

    if index_path.exists() and rel_index in metadata:
        node['has_index'] = True
        node['title'] = metadata[rel_index].get('title', name)
    else:
        # Generate title from directory name
        node['title'] = title_from_dirname(name)

    # Process children
    children = []

    for item in sorted(dir_path.iterdir(), key=lambda x: get_sort_key(x.name)):
        # Skip hidden files
        if item.name.startswith('.'):
            continue

        # Check exclusions
        rel_item = item.relative_to(base_path)
        skip = False
        for excl in exclude:
            if excl in str(rel_item):
                skip = True
                break
        if skip:
            continue

        if item.is_dir():
            child = build_tree(item, metadata, base_path, exclude, depth + 1)
            if child:
                children.append(child)
        elif item.suffix == '.md':
            # Skip index files in children (they're part of parent)
            if item.name == '00_index.md':
                continue

            rel_file = str(rel_item)
            file_meta = metadata.get(rel_file, {})

            children.append({
                'name': item.name,
                'path': rel_file,
                'type': 'file',
                'title': file_meta.get('title', title_from_filename(item.stem)),
                'order': get_sort_key(item.name),
                'summary': file_meta.get('summary'),
            })
        elif item.suffix == '.py':
            # Python files
            children.append({
                'name': item.name,
                'path': str(rel_item),
                'type': 'code',
                'title': item.name,
                'order': get_sort_key(item.name),
            })

    # Sort children
    node['children'] = sorted(children, key=lambda x: x['order'])

    return node


def title_from_dirname(name: str) -> str:
    """Generate human-readable title from directory name."""
    # Remove prefix
    clean = re.sub(r'^\d+[_-]?', '', name)
    clean = re.sub(r'^[a-zA-Z]_', '', clean)

    # Convert to title case
    clean = clean.replace('_', ' ').replace('-', ' ')
    return ' '.join(word.capitalize() for word in clean.split()) or name


def title_from_filename(name: str) -> str:
    """Generate human-readable title from filename."""
    # Remove prefix and extension
    clean = re.sub(r'^\d+[_-]?', '', name)
    clean = re.sub(r'^[a-z]_', '', clean)

    # Convert to title case
    clean = clean.replace('_', ' ').replace('-', ' ')
    return ' '.join(word.capitalize() for word in clean.split()) or name


def generate_hierarchy(
    content_dir: Path,
    metadata: Dict[str, Any],
    exclude: List[str] = None,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Generate complete hierarchy tree for content directory.
    """
    exclude = exclude or []
    content_path = Path(content_dir)

    if not content_path.exists():
        return {'children': []}

    # Build tree starting from content directory
    tree = {
        'name': content_path.name,
        'path': '',
        'type': 'root',
        'title': 'Contenido',
        'children': [],
    }

    for item in sorted(content_path.iterdir(), key=lambda x: get_sort_key(x.name)):
        if item.name.startswith('.'):
            continue

        # Check exclusions
        skip = False
        for excl in exclude:
            if excl in item.name:
                skip = True
                break
        if skip:
            continue

        if item.is_dir():
            child = build_tree(item, metadata, content_path, exclude)
            if child:
                tree['children'].append(child)
                if verbose:
                    print(f"      Added: {item.name}")

    # Sort top-level children
    tree['children'] = sorted(tree['children'], key=lambda x: x['order'])

    return tree


if __name__ == '__main__':
    import sys
    import json

    content_dir = sys.argv[1] if len(sys.argv) > 1 else 'clase'
    hierarchy = generate_hierarchy(Path(content_dir), {}, verbose=True)
    print(json.dumps(hierarchy, indent=2, ensure_ascii=False, default=str))
