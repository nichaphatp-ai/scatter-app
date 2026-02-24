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
        # choose color based on specific columns
        if col_letter == 'F':
            color = 'red'
        elif col_letter == 'H':
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
    })
    # explicitly turn off legend
    chart.set_legend({'none': True})
    worksheet.insert_chart('D2', chart, {'x_offset': 25, 'y_offset': 10})

    workbook.close()
    output.seek(0)
    return output


def main():
    st.title("Data \u2192 Excel Scatter Chart")

    uploaded = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx", "xls"])
    if not uploaded:
        st.info("Please upload a CSV or Excel file to continue.")
        return

    # determine file type from extension (uploaded may not have a name field in some cases)
    filename = getattr(uploaded, "name", "")
    try:
        if filename.lower().endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded)
        else:
            df = pd.read_csv(uploaded)
    except Exception as exc:
        st.error(f"Failed to read file: {exc}")
        return

    st.subheader("Preview of data")
    st.dataframe(df)

    if df.shape[1] < 2:
        st.error("CSV needs at least two columns for X/Y data.")
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
