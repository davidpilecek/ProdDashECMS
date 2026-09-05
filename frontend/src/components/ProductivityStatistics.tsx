import { Box, Divider } from "@mui/material";

import { Typography } from "@andritzot/metris-web-ui/data-display/typography";

import type { ProductionStatistics } from "../types/Production";

interface ProductivityStatisticsProps {
    readonly statistics: ProductionStatistics | null;
}

export default function ProductivityStatistics({
    statistics,
}: ProductivityStatisticsProps) {
    if (!statistics) {
        return (
            <Box>
                <Typography
                    variant="subtitle1"
                    sx={{ fontWeight: 600, mb: 1.5 }}
                >
                    Statistics
                </Typography>

                <Typography
                    variant="body2"
                    color="text.secondary"
                >
                    No statistics available.
                </Typography>
            </Box>
        );
    }

    const rows = [
        {
            label: "Segment",
            ...statistics.segment,
        },
        {
            label: "Day",
            ...statistics.day,
        },
        {
            label: "Month",
            ...statistics.month,
        },
    ];

    return (
        <Box>
            <Typography
                variant="subtitle1"
                sx={{
                    fontWeight: 600,
                    mb: 1.5,
                }}
            >
                Statistics
            </Typography>

            <Box
                sx={{
                    display: "grid",
                    gridTemplateColumns:
                        "1.2fr 1fr 1fr 1fr",
                    alignItems: "center",
                    px: 1,
                    py: 0.75,
                }}
            >
                <Typography
                    variant="body2"
                    color="text.secondary"
                >
                    Period
                </Typography>

                <Typography
                    variant="body2"
                    color="text.secondary"
                    sx={{ textAlign: "right" }}
                >
                    Tonnes
                </Typography>

                <Typography
                    variant="body2"
                    color="text.secondary"
                    sx={{ textAlign: "right" }}
                >
                    Hours
                </Typography>

                <Typography
                    variant="body2"
                    color="text.secondary"
                    sx={{ textAlign: "right" }}
                >
                    Rate
                </Typography>
            </Box>

            <Divider />

            {rows.map((row) => (
                <Box
                    key={row.label}
                    sx={{
                        display: "grid",
                        gridTemplateColumns:
                            "1.2fr 1fr 1fr 1fr",
                        alignItems: "center",
                        px: 1,
                        py: 0.9,
                    }}
                >
                    <Typography
                        variant="body1"
                        sx={{
                            fontWeight: 600
                        }}
                    >
                        {row.label}
                    </Typography>

                    <Typography
                        variant="body1"
                        sx={{ textAlign: "right" }}
                    >
                        {row.tonnes.toFixed(1)} t
                    </Typography>

                    <Typography
                        variant="body1"
                        sx={{ textAlign: "right" }}
                    >
                        {row.hours.toFixed(1)} h
                    </Typography>

                    <Typography
                        variant="body1"
                        sx={{ textAlign: "right" }}
                    >
                        {row.rate.toFixed(1)} t/h
                    </Typography>
                </Box>
            ))}
        </Box>
    );
}