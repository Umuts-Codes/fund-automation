$(document).ready(function () {

    let lastData = null;

    // File input change
    $("#file-input").on("change", function () {
        let fileName = $(this).val().split("\\").pop();
        $("#file-name").text(fileName || "No file selected");
    });

    // Form submit
    $("#upload-form").on("submit", function (e) {
        e.preventDefault();
        let fileInput = $("#file-input")[0].files[0];
        if (!fileInput) { alert("Please select an Excel file first!"); return; }

        let formData = new FormData();
        formData.append("file", fileInput);

        $("#summary-output").html("<p>Processing...</p>");
        $("#download-pdf").hide();
		$("#error-box").hide();
        $("#row-details").hide();

        $.ajax({
            url: "/upload",
            type: "POST",
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                if (response.errors) {
                    $("#error-table-body").empty();
                    response.errors.forEach(function(err){
                        $("#error-table-body").append(
                            "<tr><td>"+err.row+"</td><td>"+err.column+"</td><td>"+err.value+"</td></tr>"
                        );
                    });
                    $("#error-box").show();
                    $("#summary-output").html("");
                    lastData = null;
                    return;
                } else {
                    $("#error-box").hide();
                }

                if (response.error) {
                    $("#summary-output").html(`<p class="text-danger">${response.error}</p>`);
                    lastData = null;
                    return;
                }

                lastData = response;

                // Summary display
                let html = `
                    <div class="result-box">
                        <p><strong>Total Income:</strong> ${response.total_income}</p>
                        <p><strong>Total Expense:</strong> ${response.total_expense}</p>
                        <p><strong>Net Profit:</strong> ${response.net_profit}</p>
                        <p><strong>Date:</strong> ${response.date}</p>
                    </div>
                `;
                $("#summary-output").html(html);
                $("#download-pdf").show();

                // Row Details
                if(response.rows && response.rows.length > 0){
                    $("#row-details-body").empty();
                    response.rows.forEach(function(r){
                        let net = `$${(parseFloat(r.Income.replace(/[$,]/g,'')) - parseFloat(r.Expense.replace(/[$,]/g,''))).toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2})}`;
                        $("#row-details-body").append(`
                            <tr>
                                <td>${r.Row}</td>
                                <td>${r.Income}</td>
                                <td>${r.Expense}</td>
                                <td>${net}</td>
                                <td>${r.Date}</td>
                            </tr>
                        `);
                    });
                    $("#row-details").show();
                }

            },
            error: function () {
                $("#summary-output").html("<p class='text-danger'>Server error occurred.</p>");
                lastData = null;
            }
        });
    });

    // PDF download
    $("#download-pdf").on("click", function() {
        if (!lastData) return;

        $.ajax({
            url: "/download_pdf",
            type: "POST",
            data: JSON.stringify(lastData),
            contentType: "application/json",
            xhrFields: { responseType: 'blob' },
            success: function(blob) {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = "summary.pdf";
                document.body.appendChild(a);
                a.click();
                a.remove();
            },
            error: function() {
                alert("PDF download failed!");
            }
        });
    });

});
