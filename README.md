# CSV → Excel Scatter Chart Streamlit App

This small project contains a Streamlit application that:

1. Accepts a CSV or Excel (.xlsx/.xls) upload
2. Displays the data in a table
3. Exports an Excel workbook with a multi‑series smooth‑line chart (scatter data without markers)
   - column **A** is treated as the X axis
   - columns **B…** become separate Y series (e.g. A vs B, A vs C, etc.)
   - series line colors:
     * column F → red
     * column H → black
     * all others → **#FFC000** (orange hex code)
   - every line drawn at 1 pt width
   - legend completely removed (no legend appears)
   - no chart title is shown
   - horizontal axis labeled **2θ (°)**
   - vertical axis labeled **Intensity (a.u.)** with major gridlines hidden


## Getting started

1. **Clone or download** the repository and open it in VS Code.
2. **Create a virtual environment** (optional but recommended):

   ```powershell
   python -m venv .venv        # Windows
   # or `python3 -m venv .venv` on macOS/Linux
   .\.venv\Scripts\Activate  # Windows
   # or `source .venv/bin/activate` on macOS/Linux
   ```

3. **Install dependencies**:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

   > The `requirements.txt` now includes `openpyxl`, which is required to read Excel files.

4. **Run the app**:

   ```powershell
   python -m streamlit run app.py
   ```

   The Streamlit server will print a URL (usually `http://localhost:8501`) that you can open in your browser.

   Upload a file where the **first column is the X values** and any number of additional columns contain Y values. The generated workbook will plot A against each of B, C, D… as separate series on the same chart.


## Project structure

- `app.py` – main Streamlit application
- `requirements.txt` – Python dependencies
- `.gitignore` – files to exclude from version control


## Tips

- You can customize the chart or support additional CSV formats by editing `app.py`.
- Use the VS Code Python extension for linting, IntelliSense, and debugging.

### Packaging as an executable

If you'd like to distribute the tool as a standalone program (no Python install or
virtual environment required) you can bundle it with [PyInstaller](https://www.pyinstaller.org/).
A helper wrapper called `runner.py` is included which simply invokes Streamlit
programmatically; this is what you package instead of `app.py`.

1. Install PyInstaller into the same environment:
   ```powershell
   python -m pip install pyinstaller
   ```
2. Build the executable:
   ```powershell
   pyinstaller --onefile --name scatter_app runner.py \
       --hidden-import streamlit --hidden-import streamlit.cli \
       --hidden-import streamlit.web.cli \
       --collect-data streamlit \
       --copy-metadata streamlit
   ```
   *PyInstaller will analyze imports and, with `--collect-data` and
   `--copy-metadata`, bundle Streamlit's non‑code files and package metadata
   (required by `importlib.metadata`). Older PyInstaller versions don’t support
   `--collect-metadata`, so `--copy-metadata` is the compatible alternative.
   Without metadata you may see `PackageNotFoundError` at runtime.*
   
   If you still run into missing modules or metadata, add further
   `--hidden-import`, `--collect-data`, or additional `--copy-metadata` flags
   (e.g. `--copy-metadata pandas`). Delete the existing `dist` folder before
   rebuilding to ensure a clean bundle. The resulting executable will be
   `dist\scatter_app.exe`.

3. Run the generated `.exe`:
   ```powershell
   .\dist\scatter_app.exe
   ```
   It behaves exactly like `python -m streamlit run app.py` and will open the
   browser with the interface.

Troubleshooting:

- If some modules are missing at runtime, add `--hidden-import <module>` to
the PyInstaller command.
- You can also customize the spec file for icons, extra data files, etc.

This gives you an easily‑accessible application that your colleagues can launch
without needing to install Python or any dependencies.


---

*Created on February 25, 2026.*