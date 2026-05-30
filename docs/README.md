# Documentation for Umbra

This directory contains the Sphinx-based documentation for the Umbra neuromuscular interface project.

## Quick Start

### Building Documentation Locally

1. **Install documentation dependencies**:

   ```bash
   pip install -r requirements-docs.txt
   ```

2. **Build HTML documentation**:

   ```bash
   cd docs
   make html
   ```

   The built documentation will be in `docs/build/html/`.

3. **View documentation locally**:

   ```bash
   open docs/build/html/index.html
   ```

   Or start a local server:

   ```bash
   cd docs/build/html
   python -m http.server 8000
   ```

   Then visit `http://localhost:8000` in your browser.

## Documentation Structure

```
docs/
├── source/                    # Sphinx source files
│   ├── conf.py               # Sphinx configuration
│   ├── index.rst             # Main documentation index
│   ├── setup.rst             # Installation and setup guide
│   ├── usage.rst             # Usage guide
│   ├── architecture.rst      # Project architecture overview
│   ├── beta_test_plan.rst    # Beta testing documentation
│   ├── api/                  # API reference
│   │   ├── emg_movement.rst     # EMG→Movement module API
│   │   ├── eeg_emg.rst          # EEG→EMG module API
│   │   └── dashboard.rst        # Dashboard module API
│   └── guides/               # Detailed how-to guides
│       ├── preprocessing.rst    # Preprocessing guide
│       ├── model_training.rst   # Model training guide
│       └── dashboard.rst        # Dashboard usage guide
├── build/                    # Built documentation (auto-generated)
│   └── html/                 # HTML output
├── Makefile                  # Build automation
├── make.bat                  # Windows batch for builds
└── requirements-docs.txt     # Documentation dependencies
```

## Documentation Sections

### Getting Started

- **[Setup Guide](source/setup.rst)**: Installation, environment configuration, system requirements
- **[Usage Guide](source/usage.rst)**: Running preprocessing, training, and dashboard
- **[Architecture](source/architecture.rst)**: Project structure and design overview

### Detailed Guides

- **[Preprocessing Guide](source/guides/preprocessing.rst)**: EMG signal processing, windowing, normalization
- **[Model Training Guide](source/guides/model_training.rst)**: CNN-LSTM training, hyperparameters, evaluation
- **[Dashboard Guide](source/guides/dashboard.rst)**: Using the Streamlit interface and analysis tools

### API Reference

- **[EMG Movement API](source/api/emg_movement.rst)**: Preprocessing, model, training utilities
- **[EEG-EMG API](source/api/eeg_emg.rst)**: EEG signal translation (in development)
- **[Dashboard API](source/api/dashboard.rst)**: Streamlit interface components

### Project Information

- **[Beta Test Plan](source/beta_test_plan.rst)**: Testing features, success criteria, results

## Building Different Formats

### HTML (Default)

```bash
cd docs
make html
```

### PDF (requires LaTeX)

```bash
cd docs
make latex
cd build/latex
pdflatex -interaction=nonstopmode Umbra.tex
```

### Other formats

```bash
cd docs
make help  # List all available builders
```

## Deployment

### GitHub Pages

1. **Build documentation**:

   ```bash
   cd docs
   make html
   ```

2. **Commit built docs** (if using `gh-pages` branch):

   ```bash
   git add docs/build/html/
   git commit -m "docs: rebuild documentation"
   git push origin main
   ```

3. **Configure GitHub Pages**:
   - Go to repository Settings → Pages
   - Set source to `docs/build/html` or `gh-pages` branch
   - Enable GitHub Pages

### Streamlit Cloud

1. Add `.streamlit/config.toml` if needed
2. Commit to GitHub
3. Deploy from https://share.streamlit.io

### ReadTheDocs

1. Sign up at [readthedocs.org](https://readthedocs.org)
2. Import repository
3. Configure webhook for automatic builds on push

## Development

### Adding New Documentation Pages

1. Create a new `.rst` file in `source/` or subdirectories
2. Add reference to `index.rst` toctree
3. Rebuild: `make html`

### Modifying Configuration

Edit `source/conf.py` to change:

- Theme settings
- Extension configuration
- Logo, colors, layout
- HTML output options

### Building with Auto-Rebuild

```bash
pip install sphinx-autobuild
cd docs
sphinx-autobuild source build/html
```

This watches for changes and rebuilds automatically. Open `http://localhost:8000` in your browser.

## Troubleshooting

### Import Errors During Build

The documentation build may show warnings about missing dependencies (numpy, tensorflow, streamlit). This is normal and doesn't prevent documentation generation. To fix:

```bash
pip install -r requirements.txt  # Install full project dependencies
```

### Build Fails with "make" Not Found

On Windows, use:

```bash
./make.bat html
```

Or install Make:

```bash
brew install make  # macOS
choco install make  # Windows (via Chocolatey)
apt install make   # Linux
```

### Autodoc Not Finding Modules

Ensure the project root is in `sys.path`. Check `source/conf.py`:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
```

## Contributing to Documentation

1. Write clear, concise documentation
2. Use examples and code blocks
3. Follow reStructuredText (RST) syntax
4. Cross-reference related pages with `:doc:` role
5. Build locally before committing
6. Test links and navigation

## Resources

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [reStructuredText Guide](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html)
- [Sphinx RTD Theme](https://sphinx-rtd-theme.readthedocs.io/)
- [MyST Parser](https://myst-parser.readthedocs.io/) (Markdown support)

## License

This documentation is part of the Umbra project. See [LICENSE](../LICENSE) for details.
