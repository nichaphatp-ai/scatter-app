import streamlit as st
import pandas as pd
import io
from xlsxwriter.workbook import Workbook


def create_excel_bytes(df: pd.DataFrame) -> io.BytesIO:
    """Create an in-memory Excel workbook containing the dataframe and a
    scatter chart (smooth lines) based on the first two columns.

    Returns a :class:`io.BytesIO` containing the .xlsx data.
    """
    output = io.BytesIO()
    # use in_memory option so XlsxWriter writes to bytes buffer
    workbook = Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('Data')

    # write headers
    for c, header in enumerate(df.columns):
        worksheet.write(0, c, header)

    # write data rows
    for r, row in enumerate(df.itertuples(index=False, name=None), start=1):
        for c, val in enumerate(row):
            worksheet.write(r, c, val)

    # build scatter chart using first column as X axis and each subsequent column as a Y series
    max_row = len(df)
    chart = workbook.add_chart({'type': 'scatter', 'subtype': 'smooth'})

    # add one series per column after the first
    for col_idx in range(1, len(df.columns)):
        col_letter = chr(ord('A') + col_idx)
        # Set color rules:
        # Column C (col_idx==2) -> Red
        # Column J (col_idx==9) -> Black
        # Column H (col_idx==7) -> Orange (same as others)
        if col_letter == 'C':
            color = 'red'
        elif col_letter == 'J':
            color = 'black'
        else:
            color = '#FFC000'  # use specified orange hex

        chart.add_series({
            'name':       f'=Data!${col_letter}$1',
            'categories': f'=Data!$A$2:$A${max_row+1}',
            'values':     f'=Data!${col_letter}$2:${col_letter}${max_row+1}',
            # use smooth line without markers for a continuous curve
            'marker':     {'type': 'none'},
            'line':       {'smooth': True, 'color': color, 'width': 1},
        })

    # no chart title as requested
    # set custom axis titles and remove vertical major gridlines
    chart.set_x_axis({'name': '2\u03B8 (°)'})
    chart.set_y_axis({
        'name': 'Intensity (a.u.)',
        'major_gridlines': {'visible': False},
        'min': 0,
    })
    # explicitly turn off legend
    chart.set_legend({'none': True})
    worksheet.insert_chart('D2', chart, {'x_offset': 25, 'y_offset': 10})

    workbook.close()
    output.seek(0)
    return output


def main():
    st.title(".dat to Excel Scatter Chart")

    uploaded = st.file_uploader("Upload a .dat, CSV, or Excel file", type=["dat", "csv", "xlsx", "xls"])
    if not uploaded:
        st.info("Please upload a .dat, CSV, or Excel file to continue.")
        return

    filename = getattr(uploaded, "name", "")
    try:
        if filename.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded)
        elif filename.lower().endswith(".csv"):
            df = pd.read_csv(uploaded)
        elif filename.lower().endswith(".dat"):
            # Try to parse .dat file (assume whitespace or tab delimited, skip comment lines)
            content = uploaded.read().decode(errors="ignore")
            # Remove comment lines (starting with # or ";")
            lines = [line for line in content.splitlines() if line.strip() and not line.strip().startswith(("#", ";"))]
            # Try to detect delimiter (tab or whitespace)
            import csv
            import io as _io
            sample = "\n".join(lines[:10])
            dialect = csv.Sniffer().sniff(sample, delimiters="\t ,;")
            delimiter = dialect.delimiter
            df = pd.read_csv(_io.StringIO("\n".join(lines)), delimiter=delimiter)
        else:
            st.error("Unsupported file type.")
            return
    except Exception as exc:
        st.error(f"Failed to read file: {exc}")
        return

    st.subheader("Preview of data")
    st.dataframe(df)

    if df.shape[1] < 2:
        st.error("Data needs at least two columns for X/Y data.")
        return

    excel_bytes = create_excel_bytes(df)

    st.download_button(
        label="Download Excel workbook",
        data=excel_bytes,
        file_name="scatter.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


if __name__ == "__main__":
    main()
