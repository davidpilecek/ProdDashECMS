from flask import Blueprint, jsonify, request, send_file
from io import BytesIO

from services.report_service import ReportService
from services.xlsx_report_service import XlsxReportService
from services.csv_report_service import CsvService

from pathlib import Path

report_bp = Blueprint(
    "report",
    __name__,
    url_prefix="/api",
)

report_service = ReportService()
xlsx_report_service = XlsxReportService()

@report_bp.post("/report")
def generate_report():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "error": "Request body is required.",
        }), 400

    month = data.get("month")
    year = data.get("year")

    if not isinstance(month, int) or not 1 <= month <= 12:
        return jsonify({
            "success": False,
            "error": "Invalid month.",
        }), 400

    if not isinstance(year, int):
        return jsonify({
            "success": False,
            "error": "Invalid year.",
        }), 400

    try:

        pdf_bytes = report_service.generate_pdf(
            month=month,
            year=year,
        )

        return send_file(
            BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=(
                f"production_report_"
                f"{year}_{month:02d}.pdf"
            ),
        )

    except Exception as error:
        print(error)
        return jsonify({
            "success": False,
            "error": "Failed to generate report.",
        }), 500

@report_bp.post("/report/xlsx")
def generate_xlsx_report():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "error": "Request body is required.",
        }), 400

    month = data.get("month")
    year = data.get("year")

    if not isinstance(month, int) or not 1 <= month <= 12:
        return jsonify({
            "success": False,
            "error": "Invalid month.",
        }), 400

    if not isinstance(year, int):
        return jsonify({
            "success": False,
            "error": "Invalid year.",
        }), 400

    try:

        xlsx_bytes = xlsx_report_service.generate_xlsx(
            month=month,
            year=year,
        )

        return send_file(
            BytesIO(xlsx_bytes),
            mimetype=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            as_attachment=True,
            download_name=(
                f"production_report_"
                f"{year}_{month:02d}.xlsx"
            ),
        )

    except Exception as error:
        print(error)
        return jsonify({
            "success": False,
            "error": "Failed to generate XLSX report.",
        }), 500

csv_service = CsvService(
    Path(r"C:\ProgramData\Andritz\ProdDashMCMS\data")
)


@report_bp.post("/report/csv")
def download_csv():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "error": "Request body is required.",
        }), 400

    month = data.get("month")
    year = data.get("year")

    if not isinstance(month, int) or not 1 <= month <= 12:
        return jsonify({
            "success": False,
            "error": "Invalid month.",
        }), 400

    if not isinstance(year, int):
        return jsonify({
            "success": False,
            "error": "Invalid year.",
        }), 400

    try:

        file_path = csv_service.get_production_csv(
            month=month,
            year=year,
        )

        return send_file(
            file_path,
            as_attachment=True,
            download_name=file_path.name,
            mimetype="text/csv",
        )

    except FileNotFoundError:
        return jsonify({
            "success": False,
            "error": "CSV file not found.",
        }), 404

    except Exception as error:
        print(error)

        return jsonify({
            "success": False,
            "error": "Failed to download CSV.",
        }), 500