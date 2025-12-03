import pandas as pd

def process_excel(file, start_date=None, end_date=None, header_row=1):
    """
    Processes an Excel file and returns summary and row-level details.

    Parameters:
        file: Uploaded Excel file
        start_date: Optional, filter rows from this date
        end_date: Optional, filter rows up to this date
        header_row: 0-based index of the row to use as header (default 1 → second row)

    Returns:
        dict containing total income, total expense, net profit, last date, row details,
        and optionally validation errors
    """
    try:
        # Read Excel with custom header row
        df = pd.read_excel(file, engine='openpyxl', header=0)

        required_cols = ['Date', 'Income', 'Expense']
        for col in required_cols:
            if col not in df.columns:
                return {'error': f"Excel must contain columns: {required_cols}"}



        # Convert Date column
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        all_errors = []
        rows = []




        # Helper function for safe float conversion
        def safe_float(x):
            try:
                return float(str(x).replace("$", "").replace(",", "").strip())
            except:
                return 0.0

        for idx, row in df.iterrows():
            row_errors = []




            # Date validation
            if pd.isna(row['Date']):
                row_errors.append({"row": idx + header_row + 1, "column": "Date", "value": "INVALID DATE"})




            # Income and Expense validation
            income_val = safe_float(row['Income'])
            expense_val = safe_float(row['Expense'])




            # Check for empty or invalid cells
            if pd.isna(row['Income']) or income_val == 0 and str(row['Income']).strip() != "0":
                row_errors.append({"row": idx + header_row + 1, "column": "Income", "value": str(row['Income'])})
            if pd.isna(row['Expense']) or expense_val == 0 and str(row['Expense']).strip() != "0":
                row_errors.append({"row": idx + header_row + 1, "column": "Expense", "value": str(row['Expense'])})




            # Store row-level details regardless of errors
            date_str = row['Date'].strftime('%m/%d/%Y') if not pd.isna(row['Date']) else "N/A"
            income_str = f"${income_val:,.2f}"
            expense_str = f"${expense_val:,.2f}"

            rows.append({
                "Row": idx + header_row + 1,
                "Date": date_str,
                "Income": income_str,
                "Expense": expense_str
            })

            all_errors.extend(row_errors)




        # Apply date filter for summary calculation
        filtered_df = df.copy()
        if start_date:
            start_date = pd.to_datetime(start_date)
            filtered_df = filtered_df[filtered_df['Date'] >= start_date]
        if end_date:
            end_date = pd.to_datetime(end_date)
            filtered_df = filtered_df[filtered_df['Date'] <= end_date]




        # Use safe_float for calculations to avoid crashes
        total_income = filtered_df['Income'].apply(safe_float).sum()
        total_expense = filtered_df['Expense'].apply(safe_float).sum()
        net_profit = total_income - total_expense
        last_date_str = filtered_df['Date'].max().strftime('%m/%d/%Y') if not filtered_df.empty else "N/A"

        result = {
            'total_income': f"${total_income:,.2f}",
            'total_expense': f"${total_expense:,.2f}",
            'net_profit': f"${net_profit:,.2f}",
            'date': last_date_str,
            'rows': rows
        }

        if all_errors:
            result['errors'] = all_errors

        return result

    except Exception as e:
        return {'error': str(e)}
