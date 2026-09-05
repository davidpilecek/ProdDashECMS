import io

import xlsxwriter
from datetime import datetime

from services.production_service import load_production_month
from services.statistics_service import calculate_production_statistics

class XlsxReportService:

    def generate_xlsx(self, month: int, year: int) -> bytes:
        data = load_production_month(month, year)

        production_units = data["productionUnits"]
        segments = data["segments"]

        output = io.BytesIO()

        workbook = xlsxwriter.Workbook(output, {
            "in_memory": True
        })

        datetime_format = workbook.add_format({
            "border": 1,
            "num_format": "dd/mm/yyyy hh:mm:ss",
        })

        # Formats
        header_format = workbook.add_format({
            "bold": True,
            "border": 1,
        })

        cell_format = workbook.add_format({
            "border": 1,
        })

        number_format = workbook.add_format({
            "border": 1,
            "num_format": "0.00",
        })

        # --------------------------------------------------
        # Summary
        # --------------------------------------------------

        summary = workbook.add_worksheet("Summary")

        statistics = calculate_production_statistics(
            segments=segments,
            selected_segment_id=segments[-1]["segmentId"],
        )

        monthly_rate = statistics["month"]["rate"]
        total_produced = sum(
            unit["statistics"]["mass"]
            for unit in production_units
        )

        summary_data = [
            ["Metric", "Value"],
            ["Production Units", len(production_units)],
            ["Segments", len(segments)],
            ["Average Production Rate", monthly_rate],
            ["Total Produced", total_produced],
        ]

        for row, values in enumerate(summary_data):
            for col, value in enumerate(values):
                fmt = header_format if row == 0 else cell_format

                if row > 0 and col == 1:
                    fmt = number_format

                summary.write(row, col, value, fmt)

        summary.set_column("A:A", 28)
        summary.set_column("B:B", 20)

        # --------------------------------------------------
        # Production Units
        # --------------------------------------------------

        production_sheet = workbook.add_worksheet("Production Units")

        headers = [
            "Production ID",
            "Recipe",
            "Produced (t)",
            "Produced incl. Additives (t)",
            "Runtime (hours)",
            "Rate (tons/hour)",
            "Additive 1 (t)",
            "Additive 2 (t)",
            "Additive 3 (t)",
            "Additive 4 (t)",
            "Additive 5 (t)",
            "Additive 1 (%)",
            "Additive 2 (%)",
            "Additive 3 (%)",
            "Additive 4 (%)",
            "Additive 5 (%)",
        ]

        for col, header in enumerate(headers):
            production_sheet.write(0, col, header, header_format)

        for row, unit in enumerate(production_units, start=1):
            stats = unit["statistics"]
            additives = stats["additives"]

            production_sheet.write(row, 0, unit["prodId"], cell_format)
            production_sheet.write(row, 1, unit["recipeName"], cell_format)
            production_sheet.write(row, 2, stats["mass"], number_format)
            production_sheet.write(
                row, 3, stats["totalInclAdditives"], number_format
            )
            production_sheet.write(row, 4, stats["hours"], number_format)
            production_sheet.write(row, 5, stats["rate"], number_format)

            for i in range(1, 6):
                production_sheet.write(
                    row,
                    5 + i,
                    additives[f"add{i}"]["mass"],
                    number_format,
                )

            for i in range(1, 6):
                production_sheet.write(
                    row,
                    10 + i,
                    additives[f"add{i}"]["percent"],
                    number_format,
                )

        production_sheet.freeze_panes(1, 0)
        production_sheet.autofilter(
            0, 0, len(production_units), len(headers) - 1
        )

        production_sheet.set_column("A:A", 18)
        production_sheet.set_column("B:B", 25)
        production_sheet.set_column("C:F", 18)
        production_sheet.set_column("G:P", 15)

        # --------------------------------------------------
        # Segments
        # --------------------------------------------------

        segment_sheet = workbook.add_worksheet("Segments")

        segment_headers = [
            "Segment ID",
            "Production ID",
            "Start",
            "Stop",
            "Runtime (hours)",
            "Mass (t)",
        ]

        for col, header in enumerate(segment_headers):
            segment_sheet.write(0, col, header, header_format)

        for row, segment in enumerate(segments, start=1):
            segment_sheet.write(
                row, 0,
                segment["segmentId"],
                cell_format,
            )

            segment_sheet.write(
                row, 1,
                segment["prodId"],
                cell_format,
            )

            segment_sheet.write_datetime(
                row, 2,
                datetime.fromisoformat(segment["startTime"]),
                datetime_format,
            )

            segment_sheet.write_datetime(
                row, 3,
                datetime.fromisoformat(segment["stopTime"]),
                datetime_format,
            )

            segment_sheet.write_number(
                row, 4,
                segment["runTime"] / 3600,
                number_format,
            )

            segment_sheet.write_number(
                row, 5,
                segment["massTotal"],
                number_format,
            )

        segment_sheet.freeze_panes(1, 0)
        segment_sheet.autofilter(
            0, 0, len(segments), len(segment_headers) - 1
        )

        segment_sheet.set_column("A:B", 30)
        segment_sheet.set_column("C:D", 22)
        segment_sheet.set_column("E:F", 15)

        workbook.close()

        output.seek(0)
        return output.getvalue()