
import sys
import os
# Prevent Streamlit from auto-launching a browser (which may use the wrong port)
os.environ["BROWSER"] = "none"


# import the top-level streamlit package explicitly so PyInstaller
# recognises the dependency rather than only the `cli` submodule.
import streamlit
# newer streamlit versions expose the CLI under web.cli; import that
# path to ensure PyInstaller collects it, and then call its main().
try:
    import streamlit.cli as stcli
except ModuleNotFoundError:
    # fallback for newer releases
    import streamlit.web.cli as stcli

# A tiny wrapper that invokes Streamlit programmatically. This makes it easier
# to bundle with tools like PyInstaller.

if __name__ == "__main__":
    # mimic running `streamlit run app.py`
    sys.argv = ["streamlit", "run", "app.py"]
    sys.exit(stcli.main())
