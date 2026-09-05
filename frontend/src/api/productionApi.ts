import type {
    ProductionMonth,
    ProductionSegment,
    ProductionStatistics,
} from "../types/Production";

// const API_BASE_URL = "http://127.0.0.1:5000";

interface ProductionSegmentResponse
    extends Omit<ProductionSegment, "startTime" | "stopTime"> {
    startTime: string;
    stopTime: string;
}

export async function getProductionMonth(
    month: number,
    year: number,
): Promise<ProductionMonth> {

    const response = await fetch(
        `/api/production?month=${month}&year=${year}`,
    );

    if (!response.ok) {
        throw new Error(
            `Failed to load production data: ${response.status}`,
        );
    }

    const data: {
        month: number;
        year: number;
        segments: ProductionSegmentResponse[];
        productionUnits: ProductionMonth["productionUnits"];
    } = await response.json();

    return {
        month: data.month,
        year: data.year,

        segments: data.segments.map(
            (segment): ProductionSegment => ({
                ...segment,
                startTime: new Date(segment.startTime),
                stopTime: new Date(segment.stopTime),
            }),
        ),

        productionUnits: data.productionUnits,
    };
}

export async function getProductionStatistics(
    month: number,
    year: number,
    segmentId: string,
): Promise<ProductionStatistics> {

    const response = await fetch(
        `/api/production/statistics` +
        `?month=${month}` +
        `&year=${year}` +
        `&segmentId=${encodeURIComponent(segmentId)}`,
    );

    if (!response.ok) {
        throw new Error(
            `Failed to load production statistics: ${response.status}`,
        );
    }

    return response.json();
}

export async function generatePdfReport(
    displayedMonth: number,
    displayedYear: number,
) {
    try {
        const response = await fetch(
            "/api/report",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    month: displayedMonth,
                    year: displayedYear,
                }),
            },
        );

        if (!response.ok) {
            throw new Error(
                `Report generation failed: ${response.status}`,
            );
        }

        const blob = await response.blob();

        const url = window.URL.createObjectURL(blob);

        const link = document.createElement("a");

        link.href = url;
        link.download =
            `production_report_${displayedYear}_${String(displayedMonth).padStart(2, "0")}.pdf`;

        document.body.appendChild(link);

        link.click();

        link.remove();

        window.URL.revokeObjectURL(url);

    } catch (error) {
        console.error(
            "Failed to generate PDF report:",
            error,
        );
    }
}


export async function generateExcelReport(
    displayedMonth: number,
    displayedYear: number,
) {
    try {
        const response = await fetch(
            "/api/report/xlsx",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    month: displayedMonth,
                    year: displayedYear,
                }),
            },
        );

        if (!response.ok) {
            throw new Error(
                `Report generation failed: ${response.status}`,
            );
        }

        const blob = await response.blob();

        const url = window.URL.createObjectURL(blob);

        const link = document.createElement("a");

        link.href = url;
        link.download =
            `production_report_${displayedYear}_${String(displayedMonth).padStart(2, "0")}.xlsx`;

        document.body.appendChild(link);

        link.click();

        link.remove();

        window.URL.revokeObjectURL(url);

    } catch (error) {
        console.error(
            "Failed to generate Excel report:",
            error,
        );
    }
}

export async function downloadCsvExport(
    displayedMonth: number,
    displayedYear: number,
) {
    try {
        const response = await fetch(
            "/api/report/csv",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    month: displayedMonth,
                    year: displayedYear,
                }),
            },
        );

        if (!response.ok) {
            throw new Error(
                `CSV export failed: ${response.status}`,
            );
        }

        const blob = await response.blob();

        const url = window.URL.createObjectURL(blob);

        const link = document.createElement("a");

        link.href = url;
        link.download =
            `production_log_${displayedYear}_${String(displayedMonth).padStart(2, "0")}.csv`;

        document.body.appendChild(link);
        link.click();
        link.remove();

        window.URL.revokeObjectURL(url);

    } catch (error) {
        console.error(
            "Failed to export CSV:",
            error,
        );
    }
}