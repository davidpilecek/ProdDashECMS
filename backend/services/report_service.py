from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Flowable,
    Image,
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

from reportlab.lib.styles import ParagraphStyle
from services.report_graph_service import generate_production_graph
from services.production_service import load_production_month
from services.statistics_service import calculate_production_statistics

from path_config import LOGO_PATH


# Report colors
PRIMARY = HexColor("#003a70")
SECONDARY = HexColor("#707070")
LIGHT_BACKGROUND = HexColor("#F3F5F6")
BORDER = HexColor("#dddddd")
TEXT = HexColor("#000f1a")
LIGHTGREY = HexColor("#f0f0f0")
GREY = HexColor("#dddddd")


def convert_runtime_to_days_hours(
    runtime: float,
) -> tuple[float, float, float, float]:

    time = runtime

    day = time // (24 * 3600)
    time = time % (24 * 3600)

    hour = time // 3600
    time %= 3600

    minutes = time // 60
    seconds = time % 60

    return day, hour, minutes, seconds

def formatRuntime(seconds: float) -> str:
    hours_new = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remainingSeconds = int(seconds % 60)

    return f"{hours_new} h {minutes} min {remainingSeconds} s"

class ReportHeader(Flowable):

    def __init__(
        self,
        logo_path: str,
        title: str,
        generated_text: str,
        logo_width: float,
        logo_height: float,
    ):
        super().__init__()

        self.logo_path = logo_path
        self.title = title
        self.generated_text = generated_text
        self.logo_width = logo_width
        self.logo_height = logo_height

        self.width = 180 * mm
        self.height = 40 * mm

    def draw(self):

        canvas = self.canv

        # Logo and Generation Date
        canvas.drawImage(
            self.logo_path,
            0,
            self.height - self.logo_height,
            width=self.logo_width,
            height=self.logo_height,
            preserveAspectRatio=True,
            mask="auto",
        )

        canvas.setFont(
            "Helvetica",
            10,
        )

        canvas.setFillColor(
            SECONDARY
        )

        canvas.drawRightString(
            self.width,
            self.height - 8 * mm,
            self.generated_text,
        )

        # Report Title
        canvas.setFont(
            "Helvetica-Bold",
            18,
        )

        canvas.setFillColor(
            PRIMARY
        )

        canvas.drawString(
            38 * mm,
            0 * mm,
            self.title,
        )

        # Decorative Separator Line
        canvas.setStrokeColor(
            PRIMARY
        )

        canvas.setLineWidth(1.5)

        canvas.line(
            0,
            -5 * mm,
            self.width,
            -5 * mm,
        )


class ReportService:

    def generate_pdf(
        self,
        month: int,
        year: int,
    ) -> bytes:

        data = load_production_month(
            month,
            year,
        )

        production_units = data["productionUnits"]
        segments = data["segments"]

        graph_bytes = generate_production_graph(
            segments=segments,
            month=month,
            year=year,
        )

        buffer = BytesIO()

        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=15 * mm,
            leftMargin=15 * mm,
            topMargin=8 * mm,
            bottomMargin=15 * mm,
        )

        styles = getSampleStyleSheet()

        table_style = ParagraphStyle(
                    "TableText",
                    parent=styles["BodyText"],
                    fontSize=10,
                    leading=10,
                    wordWrap="CJK",
                )
        
        elements = []

        # --------------------------------------------------
        # Header
        # --------------------------------------------------

        header = ReportHeader(
            logo_path=str(LOGO_PATH),
            title=f"Production Report for {month:02d}/{year}",
            generated_text=(
                f"Generated on "
                f"{datetime.now().strftime('%d.%m.%Y %H:%M')}"
            ),
            logo_width=35 * mm,
            logo_height=18 * mm,
        )

        elements.append(header)
        elements.append(
            Spacer(1, 25 * mm)
        )

        # --------------------------------------------------
        # Graph
        # --------------------------------------------------

        elements.append(
            Image(
                BytesIO(graph_bytes),
                width=175 * mm,
                height=70 * mm,
            )
        )

        elements.append(
            Spacer(1, 15 * mm)
        )

        # --------------------------------------------------
        # Monthly Summary
        # --------------------------------------------------

        elements.append(
            Paragraph(
                "Monthly Summary",
                styles["Heading2"],
            )
        )

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
            [
                "Production Units",
                str(len(production_units)),
            ],
            [
                "Segments",
                str(len(segments)),
            ],
            [
                "Average Production Rate",
                f"{monthly_rate:.2f} t/h",
            ],
            [
                "Total Produced",
                f"{total_produced:.2f} t",
            ],
            [
                "Total Waste",
                f"{total_waste:.2f} t",
            ],
        ]

        summary_table = Table(
            summary_data,
            colWidths=[
                70 * mm,
                40 * mm,
            ],
        )

        summary_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    PRIMARY,
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.whitesmoke,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (1, -1),
                    "RIGHT",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    BORDER,
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        LIGHT_BACKGROUND,
                    ],
                ),
            ])
        )

        elements.append(summary_table)
        elements.append(PageBreak())

        # --------------------------------------------------
        # Production Units
        # --------------------------------------------------

        elements.append(
            Paragraph(
                "Production Units",
                styles["Heading2"],
            )
        )

        production_rows = [
            [
                "Production ID",
                "Recipe",
                "Start / Stop",
                "Produced",
                "Avg Rate",
                "Production Real (Waste)",
            ]
        ]

        production_fields = [
            (
                "Steam 2 Cond",
                "realSteam2Cond",
                "wasteSteam2Cond",
            ),
            (
                "Steam 2 Extr",
                "realSteam2Extr",
                "wasteSteam2Extr",
            ),
            (
                "Water 2 Cond",
                "realWater2Cond",
                "wasteWater2Cond",
            ),
            (
                "Oil 2 Cond Extr",
                "realOil2CondExtr",
                "wasteOil2CondExtr",
            ),
            (
                "Water 2 Extr",
                "realWater2Extr",
                "wasteWater2Extr",
            ),
            (
                "Add 2 Cond Extr",
                "realAdd2CondExtr",
                "wasteAdd2CondExtr",
            ),
            (
                "Add 5",
                "realAdd5",
                "wasteAdd5",
            ),
            (
                "Add 6",
                "realAdd6",
                "wasteAdd6",
            ),
        ]

        for unit in production_units:

            stats = unit["statistics"]

            if stats["stopTime"]:
                stop_time = stats["stopTime"].replace(
                    "T",
                    " ",
                )
            else:
                stop_time = "-"

            real_lines = [
                (
                    f"{label}: "
                    f"{stats['real'][real_field]:.2f} t "
                    f"({stats['waste'][waste_field]:.2f} t)"
                )
                for label, real_field, waste_field
                in production_fields
            ]

            production_rows.append([
                Paragraph(
                    str(unit["prodId"]),
                    table_style,
                ),

                Paragraph(
                    str(unit["recipeName"]),
                    table_style,
                ),

                Paragraph(
                    "<br/>".join([
                        stats["startTime"].replace(
                            "T",
                            " ",
                        ),
                        stop_time,
                    ]),
                    table_style,
                ),

                Paragraph(
                    f"{stats['realTotal']:.2f} t "
                    f"({stats['wasteTotal']:.2f} t)",
                    table_style,
                ),

                Paragraph(
                    f"{stats['rate']:.2f} t/h",
                    table_style,
                ),

                Paragraph(
                    "<br/>".join(real_lines),
                    table_style,
                ),
            ])

        production_table = Table(
            production_rows,
            colWidths=[
                30 * mm,
                23 * mm,
                40 * mm,
                25 * mm,
                22 * mm,
                63 * mm,
            ],
            repeatRows=1,
        )

        production_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    PRIMARY,
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.whitesmoke,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "ALIGN",
                    (2, 1),
                    (5, -1),
                    "RIGHT",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    BORDER,
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        LIGHT_BACKGROUND,
                    ],
                ),
            ])
        )

        elements.append(production_table)
        elements.append(PageBreak())

        # --------------------------------------------------
        # Segments
        # --------------------------------------------------

        elements.append(
            Paragraph(
                "Segments",
                styles["Heading2"],
            )
        )

        segment_rows = [
            [
                "Segment ID",
                "Production ID",
                "Start",
                "Stop",
                "Runtime",
                "Real Total",
                "Waste",
            ]
        ]

        for segment in segments:

            runtime_hours = (
                segment["runTime"] / 3600
            )

            start_time = (
                segment["startTime"]
                .replace("T", " ")
            )

            stop_time = (
                segment["stopTime"].replace("T", " ")
                if segment.get("stopTime")
                else "-"
            )

            segment_rows.append([
                segment["segmentId"],
                segment["prodId"],
                start_time,
                stop_time,
                f"{runtime_hours:.1f} h",
                f"{segment['realTotal']:.2f} t",
                f"{segment['wasteTotal']:.2f} t",
            ])

        segment_table = Table(
            segment_rows,
            repeatRows=1,
        )

        segment_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    PRIMARY,
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.whitesmoke,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "ALIGN",
                    (4, 1),
                    (-1, -1),
                    "RIGHT",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    BORDER,
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        LIGHT_BACKGROUND,
                    ],
                ),
            ])
        )

        elements.append(segment_table)

        document.build(elements)

        return buffer.getvalue()