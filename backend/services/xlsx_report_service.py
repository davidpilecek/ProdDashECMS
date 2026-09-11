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

                summary.write(
                    row,
                    col,
                    value,
                    fmt,
                )

        summary.set_column("A:A", 28)
        summary.set_column("B:B", 20)

        # --------------------------------------------------
        # Production Units
        # --------------------------------------------------

        production_sheet = workbook.add_worksheet(
            "Production Units"
        )

        headers = [
            "Production ID",
            "Recipe",
            "Runtime (hours)",
            "Rate (t/hour)",

            "Real Total (t)",
            "Real Steam to Conditioner (t)",
            "Real Steam to Extruder (t)",
            "Real Water to Conditioner (t)",
            "Real Oil to Conditioner or Extruder (t)",
            "Real Water to Extruder (t)",
            "Real Add to Conditioner or Extruder (t)",
            "Real Additive 5 (t)",
            "Real Additive 6 (t)",

            "Waste Total (t)",
            "Waste Steam to Conditioner (t)",
            "Waste Steam to Extruder (t)",
            "Waste Water to Conditioner (t)",
            "Waste Oil to Conditioner or Extruder (t)",
            "Waste Water to Extruder (t)",
            "Waste Additive to Conditioner or Extruder (t)",
            "Waste Additive 5 (t)",
            "Waste Additive 6 (t)",
        ]

        for col, header in enumerate(headers):
            production_sheet.write(
                0,
                col,
                header,
                header_format,
            )

        real_fields = [
            "realTotal",
            "realSteam2Cond",
            "realSteam2Extr",
            "realWater2Cond",
            "realOil2CondExtr",
            "realWater2Extr",
            "realAdd2CondExtr",
            "realAdd5",
            "realAdd6",
        ]

        waste_fields = [
            "wasteTotal",
            "wasteSteam2Cond",
            "wasteSteam2Extr",
            "wasteWater2Cond",
            "wasteOil2CondExtr",
            "wasteWater2Extr",
            "wasteAdd2CondExtr",
            "wasteAdd5",
            "wasteAdd6",
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
                stats["hours"],
                number_format,
            )

            production_sheet.write(
                row,
                3,
                stats["rate"],
                number_format,
            )

            # REAL values
            for index, field in enumerate(real_fields):
                production_sheet.write(
                    row,
                    4 + index,
                    (
                        stats[field]
                        if field in stats
                        else stats["real"][field]
                    ),
                    number_format,
                )

            # WASTE values
            for index, field in enumerate(waste_fields):
                production_sheet.write(
                    row,
                    13 + index,
                    (
                        stats[field]
                        if field in stats
                        else stats["waste"][field]
                    ),
                    number_format,
                )

        production_sheet.freeze_panes(
            1,
            0,
        )

        production_sheet.autofilter(
            0,
            0,
            len(production_units),
            len(headers) - 1,
        )

        production_sheet.set_column(
            "A:A",
            18,
        )

        production_sheet.set_column(
            "B:B",
            25,
        )

        production_sheet.set_column(
            "C:D",
            18,
        )

        production_sheet.set_column(
            "E:V",
            20,
        )

        # --------------------------------------------------
        # Segments
        # --------------------------------------------------

        segment_sheet = workbook.add_worksheet(
            "Segments"
        )

        segment_headers = [
            "Segment ID",
            "Production ID",
            "Start",
            "Stop",
            "Runtime (hours)",

            "Real Total (t)",
            "Real Steam to Conditioner (t)",
            "Real Steam to Extruder (t)",
            "Real Water to Conditioner (t)",
            "Real Oil to Conditioner or Extruder (t)",
            "Real Water to Extruder (t)",
            "Real Add to Conditioner or Extruder (t)",
            "Real Additive 5 (t)",
            "Real Additive 6 (t)",

            "Waste Total (t)",
            "Waste Steam to Conditioner (t)",
            "Waste Steam to Extruder (t)",
            "Waste Water to Conditioner (t)",
            "Waste Oil to Conditioner or Extruder (t)",
            "Waste Water to Extruder (t)",
            "Waste Additive to Conditioner or Extruder (t)",
            "Waste Additive 5 (t)",
            "Waste Additive 6 (t)",
        ]

        for col, header in enumerate(segment_headers):
            segment_sheet.write(
                0,
                col,
                header,
                header_format,
            )

        real_segment_fields = [
            "realTotal",
            "realSteam2Cond",
            "realSteam2Extr",
            "realWater2Cond",
            "realOil2CondExtr",
            "realWater2Extr",
            "realAdd2CondExtr",
            "realAdd5",
            "realAdd6",
        ]

        waste_segment_fields = [
            "wasteTotal",
            "wasteSteam2Cond",
            "wasteSteam2Extr",
            "wasteWater2Cond",
            "wasteOil2CondExtr",
            "wasteWater2Extr",
            "wasteAdd2CondExtr",
            "wasteAdd5",
            "wasteAdd6",
        ]

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

            # REAL values
            for index, field in enumerate(
                real_segment_fields
            ):
                segment_sheet.write_number(
                    row,
                    5 + index,
                    segment[field],
                    number_format,
                )

            # WASTE values
            for index, field in enumerate(
                waste_segment_fields
            ):
                segment_sheet.write_number(
                    row,
                    14 + index,
                    segment[field],
                    number_format,
                )

        segment_sheet.freeze_panes(
            1,
            0,
        )

        segment_sheet.autofilter(
            0,
            0,
            len(segments),
            len(segment_headers) - 1,
        )

        segment_sheet.set_column(
            "A:B",
            30,
        )

        segment_sheet.set_column(
            "C:D",
            22,
        )

        segment_sheet.set_column(
            "E:W",
            20,
        )

        # --------------------------------------------------
        # Finalize workbook
        # --------------------------------------------------

        workbook.close()

        output.seek(0)

        return output.getvalue()