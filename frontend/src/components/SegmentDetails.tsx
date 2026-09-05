import { Box } from "@mui/material";

import { Typography } from "@andritzot/metris-web-ui/data-display/typography";

import type { ProductionSegment } from "../types/Production";

interface SegmentDetailsProps {
    readonly segment: ProductionSegment | null;
}

function formatRuntime(seconds: number): string {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor(
        (seconds % 3600) / 60,
    );
    const remainingSeconds = seconds % 60;

    return `${hours} h ${minutes} min ${remainingSeconds} s`;
}

interface DetailItemProps {
    readonly label: string;
    readonly value: string;
}

function DetailItem({
    label,
    value,
}: DetailItemProps) {
    return (
        <Box>
            <Typography
                variant="body1"
                color="text.primary"
                sx={{ mb: 0.25 }}
            >
                {label}
            </Typography>

            <Typography variant="body2">
                {value}
            </Typography>
        </Box>
    );
}

export default function SegmentDetails({
    segment,
}: SegmentDetailsProps) {
    if (!segment) {
        return (
            <Box>
                <Typography
                    variant="h5"
                    sx={{ fontWeight: 600, mb: 1.5 }}
                >
                    Selected Segment
                </Typography>

                <Typography
                    variant="body2"
                    color="text.secondary"
                >
                    No segment selected.
                </Typography>
            </Box>
        );
    }

    return (
        <Box>

            <Box
                sx={{
                    display: "grid",
                    gridTemplateColumns:
                        "1fr 1fr",
                    columnGap: 3,
                    rowGap: 1.5,
                }}
            >
                <DetailItem
                    label="Runtime"
                    value={formatRuntime(
                        segment.runTime,
                    )}
                />

                <DetailItem
                    label="Start"
                    value={segment.startTime.toLocaleString()}
                />

                <DetailItem
                    label="Stop"
                    value={segment.stopTime.toLocaleString()}
                />

                <DetailItem
                    label="Mass"
                    value={`${segment.massTotal.toFixed(2)} t`}
                />
            </Box>
        </Box>
    );
}