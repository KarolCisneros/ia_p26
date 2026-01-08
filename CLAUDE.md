# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a course repository for ITAM's Artificial Intelligence class (Primavera 2026). It contains course materials, guides, and student assignments.

## Repository Structure

- `clase/` - Course materials and guides
  - `a_stack/` - Technical stack documentation (LLMs, OS setup, IDE, Git, Python)
  - `b_libros/` - Book references
  - `certificaciones/` - Certification guides
  - `flow.sh` - Git workflow automation script
- `estudiantes/` - Student work directories (each student has their own folder)

## Key Commands

### Git Workflow Script (flow.sh)

The course uses a custom script at `clase/flow.sh` to manage git operations:

```bash
./clase/flow.sh setup    # Initial setup (configure upstream, create student folder)
./clase/flow.sh sync     # Sync with upstream (professor's repo)
./clase/flow.sh start <task-name>  # Start new task (creates branch)
./clase/flow.sh save "message"     # Save changes (git add + commit)
./clase/flow.sh upload   # Push branch to GitHub
./clase/flow.sh finish   # Clean up after PR is merged
./clase/flow.sh copy <src> <dest>  # Safe copy (won't overwrite existing files)
```

The upstream repository is `git@github.com:sonder-art/ia_p26.git`.

## Language

Course materials are in Spanish. When creating or editing documentation, maintain Spanish unless explicitly asked otherwise.

## Student Workflow

Students work in their own directories under `estudiantes/<username>/`. The typical workflow is:
1. `./clase/flow.sh start tarea-X` - Create a task branch
2. Work in `estudiantes/<username>/` directory
3. `./clase/flow.sh save "message"` - Commit changes
4. `./clase/flow.sh upload` - Push and create PR to upstream
