# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

**Linting and Formatting:**

Pre-commit will run Ruff and pycheck automatically when committing. Don't
proceed until the commit is successful. Many Ruff issues will be fixed
automatically, so if that fails simply retry the commit.

## Architecture Overview

This is a Talon voice control extension that enables advanced cursor control using eye tracking and OCR (text recognition). The system allows users to click, select, and manipulate text by speaking words that appear on screen.

### Core Components

**Main Module (`gaze_ocr_talon.py`):**
- Central orchestrator that integrates eye tracking, OCR, and Talon APIs
- Manages settings, homophones, and punctuation mappings
- Handles disambiguation UI when multiple text matches are found
- Implements all user-facing actions for text manipulation

**Timestamped Captures (`timestamped_captures.py`):**
- Defines data structures for text with timing information (`TimestampedText`, `TextRange`, `TextPosition`)
- Provides Talon capture definitions for parsing spoken commands with timestamps
- Enables precise matching of spoken words to screen text using timing data

**Talon Command Files:**
- `gaze_ocr.talon` - Main voice commands for text interaction
- `gaze_ocr_disambiguation.talon` - Commands for choosing between multiple matches

### Key Architecture Patterns

**Generator-Based Async Operations:**
The system uses Python generators extensively for handling async operations that may require user disambiguation:
- Operations like `move_cursor_to_word_generator()` yield control when multiple matches need user input
- The `begin_generator()` function manages generator execution and disambiguation flow
- This pattern allows complex multi-step operations to pause for user input and resume

**Eye Tracking Integration:**
- Uses `.subtrees/gaze-ocr` and `.subtrees/screen-ocr` as embedded dependencies
- Integrates with Talon's experimental OCR API when available
- Falls back to external OCR when Talon OCR unavailable
- Eye tracker data filters OCR results to improve accuracy

**Homophone and Context Handling:**
- Integrates with community homophones.csv for smart word matching
- Maps digits and punctuation between spoken and written forms
- Supports fuzzy matching for improved recognition accuracy

### Dependencies Structure

The `.subtrees` directory contains git subtrees of required packages:
- `gaze-ocr` - Core OCR and eye tracking logic
- `screen-ocr` - Screen capture and text recognition
- `rapidfuzz` - Fast fuzzy string matching

Changes are automatically synced to upstream repos via GitHub Actions using git subtree.

## Settings and Configuration

Key settings are defined as Talon module settings:
- `ocr_use_talon_backend` - Whether to use Talon's OCR vs external
- `ocr_connect_tracker` - Auto-connect eye tracker on startup
- `ocr_gaze_*_padding` - Eye tracking search area configuration
- Various UI timing and display settings

## Important Notes

- Two branches are maintained: `main` and `beta`. Beta is used for any features
  which depend on the Talon Beta, but is otherwise kept in sync with main. Most
  commits should be applied first to main and then main should be merged into
  beta. Suggest switching to main before implementing a feature if not already
  on main. At commit time, if changes have been made already on the beta branch,
  stash these and switch to main to commit.
- Requires Talon restart when updated or settings changed (unlike most Talon scripts)
- Requires `community` repository as sibling directory for full functionality
- Only works on main screen due to current limitations
- Eye tracker is optional but significantly improves accuracy

## Talon documentation

@~/.claude/talon.md
