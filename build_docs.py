#!/usr/bin/env python3
"""Build documentation using MkDocs with the strip-number-prefix plugin."""

import subprocess
import sys
from pathlib import Path
import shutil


def main():
    """Build the documentation."""
    # Ensure we're in the project root
    project_root = Path(__file__).parent
    
    # Check if mkdocs.yml exists
    config_file = project_root / "mkdocs.yml"
    if not config_file.exists():
        print(f"Error: {config_file} not found!")
        sys.exit(1)
    
    # Clean previous build if it exists
    docs_dir = project_root / "docs"
    if docs_dir.exists():
        print(f"Cleaning existing docs directory: {docs_dir}")
        shutil.rmtree(docs_dir)
    
    # Build the documentation
    print("Building documentation with MkDocs...")
    cmd = ["mkdocs", "build", "--site-dir", "docs"]
    
    try:
        result = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Documentation built successfully!")
            print(f"Output directory: {docs_dir}")
            
            # Optionally serve the docs
            if len(sys.argv) > 1 and sys.argv[1] == "--serve":
                print("\nStarting development server...")
                subprocess.run(["mkdocs", "serve"], cwd=project_root)
        else:
            print("❌ Build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            sys.exit(1)
            
    except FileNotFoundError:
        print("Error: mkdocs not found. Please install it with: pip install mkdocs mkdocs-material")
        sys.exit(1)
    except Exception as e:
        print(f"Error running mkdocs: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()