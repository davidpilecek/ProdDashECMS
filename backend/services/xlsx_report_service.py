import io
from datetime import datetime

import xlsxwriter

from services.production_service import load_production_month
from services.statistics_service import calculate_production_statistics


class XlsxReportService:

    def generate_xlsx(self, month: int, year: int) -> bytes:
        data = load_production_month(month, year)

        production_units = data["productionUnits"]
        segments = data["segments"]

        output = io.BytesIO()

        workbook = xlsxwriter.Workbook(
            output,
            {
                "in_memory": True
            }
        )

        datetime_format = workbook.add_format({
            "border": 1,
            "num_format": "dd/mm/yyyy hh:mm:ss",
        })

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

        if segments:
            statistics = calculate_production_statistics(
                segments=segments,
                selected_segment_id=segments[-1]["segmentId"],
            )

            monthly_rate = statistics["month"]["rate"]
        else:
            monthly_rate = 0.0

        total_produced = sum(
            unit["statistics"]["realTotal"]
            for unit in production_units
        )

        total_waste = sum(
            unit["statistics"]["wasteTotal"]
            for unit in production_units
        )

        summary_data = [
            ["Metric", "Value"],
            ["Production Units", len(production_units)],
            ["Segments", len(segments)],
            ["Average Production Rate", monthly_rate],
            ["Total Produced", total_produced],
            ["Total Waste", total_waste],
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
            "Real Total (t)",
            "Waste Total (t)",
            "Runtime (hours)",
            "Rate (t/hour)",
            "Steam 2 Cond (t)",
            "Steam 2 Extr (t)",
            "Water 2 Cond (t)",
            "Oil 2 Cond Extr (t)",
            "Water 2 Extr (t)",
            "Add 2 Cond Extr (t)",
            "Add 5 (t)",
            "Add 6 (t)",
            "Steam 2 Cond (%)",
            "Steam 2 Extr (%)",
            "Water 2 Cond (%)",
            "Oil 2 Cond Extr (%)",
            "Water 2 Extr (%)",
            "Add 2 Cond Extr (%)",
            "Add 5 (%)",
            "Add 6 (%)",
        ]

        for col, header in enumerate(headers):
            production_sheet.write(
                0,
                col,
                header,
                header_format,
            )

        real_fields = [
            "realSteam2Cond",
            "realSteam2Extr",
            "realWater2Cond",
            "realOil2CondExtr",
            "realWater2Extr",
            "realAdd2CondExtr",
            "realAdd5",
            "realAdd6",
        ]

        for row, unit in enumerate(
            production_units,
            start=1,
        ):
            stats = unit["statistics"]

            production_sheet.write(
                row,
                0,
                unit["prodId"],
                cell_format,
            )

            production_sheet.write(
                row,
                1,
                unit["recipeName"],
                cell_format,
            )

            production_sheet.write(
                row,
                2,
                stats["realTotal"],
                number_format,
            )

            production_sheet.write(
                row,
                3,
                stats["wasteTotal"],
                number_format,
            )

            production_sheet.write(
                row,
                4,
                stats["hours"],
                number_format,
            )

            production_sheet.write(
                row,
                5,
                stats["rate"],
                number_format,
            )

            # Real material masses
            for index, field in enumerate(real_fields):
                production_sheet.write(
                    row,
                    6 + index,
                    stats["real"][field],
                    number_format,
                )

            # Real material percentages
            for index, field in enumerate(real_fields):
                production_sheet.write(
                    row,
                    14 + index,
                    stats["realPercentages"][field],
                    number_format,
                )

        production_sheet.freeze_panes(1, 0)

        production_sheet.autofilter(
            0,
            0,
            len(production_units),
            len(headers) - 1,
        )

        production_sheet.set_column("A:A", 18)
        production_sheet.set_column("B:B", 25)
        production_sheet.set_column("C:F", 18)
        production_sheet.set_column("G:V", 18)

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
            "Real Total (t)",
            "Waste Total (t)",
            "Steam 2 Cond (t)",
            "Steam 2 Extr (t)",
            "Water 2 Cond (t)",
            "Oil 2 Cond Extr (t)",
            "Water 2 Extr (t)",
            "Add 2 Cond Extr (t)",
            "Add 5 (t)",
            "Add 6 (t)",
        ]

        for col, header in enumerate(segment_headers):
            segment_sheet.write(
                0,
                col,
                header,
                header_format,
            )

        for row, segment in enumerate(
            segments,
            start=1,
        ):
            segment_sheet.write(
                row,
                0,
                segment["segmentId"],
                cell_format,
            )

            segment_sheet.write(
                row,
                1,
                segment["prodId"],
                cell_format,
            )

            segment_sheet.write_datetime(
                row,
                2,
                datetime.fromisoformat(
                    segment["startTime"]
                ),
                datetime_format,
            )

            if segment.get("stopTime"):
                segment_sheet.write_datetime(
                    row,
                    3,
                    datetime.fromisoformat(
                        segment["stopTime"]
                    ),
                    datetime_format,
                )
            else:
                segment_sheet.write(
                    row,
                    3,
                    "",
                    cell_format,
                )

            segment_sheet.write_number(
                row,
                4,
                segment["runTime"] / 3600,
                number_format,
            )

            segment_sheet.write_number(
                row,
                5,
                segment["realTotal"],
                number_format,
            )

            segment_sheet.write_number(
                row,
                6,
                segment["wasteTotal"],
                number_format,
            )

            segment_fields = [
                "realSteam2Cond",
                "realSteam2Extr",
                "realWater2Cond",
                "realOil2CondExtr",
                "realWater2Extr",
                "realAdd2CondExtr",
                "realAdd5",
                "realAdd6",
            ]

            for index, field in enumerate(segment_fields):
                segment_sheet.write_number(
                    row,
                    7 + index,
                    segment[field],
                    number_format,
                )

        segment_sheet.freeze_panes(1, 0)

        segment_sheet.autofilter(
            0,
            0,
            len(segments),
            len(segment_headers) - 1,
        )

        segment_sheet.set_column("A:B", 30)
        segment_sheet.set_column("C:D", 22)
        segment_sheet.set_column("E:O", 18)

        workbook.close()

        output.seek(0)

        return output.getvalue()