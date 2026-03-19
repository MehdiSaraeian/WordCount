# WordCount Generator

A Pythonic word cloud generator with both a CLI and a Gradio-based Web UI. Built using [Pixi](https://pixi.sh) for dependency management.

## Demo

![WordCount UI Demonstration](demo.gif)


## Features
- **CLI Interface**: Process text files and generate word clouds/CSV frequencies from the terminal.
- **Web UI**: User-friendly Gradio interface for uploading files and viewing results.
- **Modern Packaging**: Uses Pixi for reproducible environments (Conda + PyPI).

## Installation

1. Install [Pixi](https://pixi.sh):
   ```powershell
   powershell -ExecutionPolicy Bypass -c "irm -useb https://pixi.sh/install.ps1 | iex"
   ```
2. Clone the repository and navigate to the directory.
3. Pixi will automatically handle dependencies when you run the project.

## Usage

### Web UI
Launch the interactive browser interface:
```bash
pixi run ui
```

### CLI
Generate a word cloud and CSV frequency list:
```bash
pixi run cli "your_file.txt" output.png frequencies.csv
```

## Configuration
Dependencies are managed in `pixi.toml`. It uses `conda-forge` for core libraries and `PyPI` for Gradio to ensure compatibility.
