# FUND - AUTOMATION

<br>

This project is a calculation and validation system designed to automatically process income, expense, and date data stored in an Excel file by any company or individual.

<br>

The user simply uploads their own Excel file. The system then performs the following operations in the background:


<br><br>



<p>- Automatic Calculation -</p>

<br>

Reads all income and expense values

Automatically calculates total income, total expenses, and net profit

Extracts the most recent date from the dataset.




<br><br>




<p>- PDF Export -</p>


Allows users to download a professionally formatted PDF report containing all calculated results.



<br><br>



<p>- Error Detection & Validation -</p>

<br>

If the user accidentally enters incorrect or invalid data into the Excel file, such as:

Invalid text

Incompatible numeric values

Missing or invalid dates

Empty or malformed fields

the system automatically detects these issues.


<br>


**In the interface it displays warnings including:**

The row number containing the error

The column name

The invalid value entered

This enables the user to easily locate and correct mistakes directly in the Excel file.

The only thing the user needs to do is enter their Date, Income, and Expense data into the Excel file.

The system handles everything else fully automatically.


<br><br>


**NOTE:** This project operates in the background through a combination of jQuery-Ajax on the frontend and Python Flask backend functions, ensuring that all data is processed and transferred correctly.

