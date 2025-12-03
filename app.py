from flask import Flask, render_template, request, jsonify, send_file
import utils
from io import BytesIO
from reportlab.pdfgen import canvas




app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')




@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        result = utils.process_excel(file)  # Call the function in utils.py
        return jsonify(result)
    except Exception as e:
        # Print detailed error to console
        print("ERROR:", e)
        # Return the error as JSON to the frontend
        return jsonify({"error": str(e)})






@app.route("/download_pdf", methods=["POST"])
def download_pdf():
    data = request.get_json()
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    
    
    p.drawString(100, 800, f"Total Income: {data['total_income']}")
    p.drawString(100, 780, f"Total Expense: {data['total_expense']}")
    p.drawString(100, 760, f"Net Profit: {data['net_profit']}")
    p.drawString(100, 740, f"Date: {data.get('date', 'N/A')}")

    p.showPage()
    p.save()
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True, download_name="summary.pdf", mimetype="application/pdf")







if __name__ == '__main__':
    app.run(debug=True, port=5000)

