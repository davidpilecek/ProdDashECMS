import {
    Box,
    Divider,
    MenuItem,
    Stack,
    TextField,
} from '@mui/material';

import { Skeleton } from "@andritzot/metris-web-ui/feedback/skeleton";

import { Button} from '@andritzot/metris-web-ui/inputs/button';
import { ButtonGroup} from '@andritzot/metris-web-ui/inputs/button-group';

import { Typography } from '@andritzot/metris-web-ui/data-display/typography';
import { Panels } from '@andritzot/metris-web-ui/layout/panels';

import ProductionGraph from '../components/ProductionGraph';
import SegmentDetails from "../components/SegmentDetails";
import ProductionUnitDetails from "../components/ProductionUnitDetails";
import ProductivityStatistics from "../components/ProductivityStatistics";

import {
    getProductionMonth,
    getProductionStatistics,
    generatePdfReport,
    generateExcelReport,
    downloadCsvExport,
} from "../api/productionApi";

import type {
    ProductionMonth,
    ProductionStatistics,
} from "../types/Production";

import {useEffect, useMemo, useState } from 'react';

const months = [
    { value: 1, label: "January" },
    { value: 2, label: "February" },
    { value: 3, label: "March" },
    { value: 4, label: "April" },
    { value: 5, label: "May" },
    { value: 6, label: "June" },
    { value: 7, label: "July" },
    { value: 8, label: "August" },
    { value: 9, label: "September" },
    { value: 10, label: "October" },
    { value: 11, label: "November" },
    { value: 12, label: "December" },
];

const years = [
    2025,
    2026,
];

export default function Dashboard() {

    // --------------------------------------------------
    // State
    // --------------------------------------------------

    const [displayedMonth, setDisplayedMonth] =
        useState(1);

    const [displayedYear, setDisplayedYear] =
        useState(2026);

    const [productionMonth, setProductionMonth] =
        useState<ProductionMonth | null>(null);

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState<string | null>(null);

    const [selectedSegmentId, setSelectedSegmentId] =
        useState<string | null>(null);


    // --------------------------------------------------
    // Load production data
    // --------------------------------------------------

    useEffect(() => {

        async function loadMonth() {

            setLoading(true);
            setError(null);

            try {

                const data = await getProductionMonth(
                    displayedMonth,
                    displayedYear,
                );

                setProductionMonth(data);

            } catch (err) {

                console.error(
                    "Failed to load production data:",
                    err,
                );

                setError(
                    "Failed to load production data.",
                );

            } finally {

                setLoading(false);

            }
        }

        loadMonth();

    }, [displayedMonth, displayedYear]);


    // --------------------------------------------------
    // Derived data
    // --------------------------------------------------

    const segments =
        productionMonth?.segments ?? [];

    const orderedSegmentIds = useMemo(
        () =>
            [...segments]
                .sort(
                    (a, b) =>
                        a.startTime.getTime() -
                        b.startTime.getTime(),
                )
                .map(
                    segment =>
                        segment.segmentId,
                ),
        [segments],
    );


    // --------------------------------------------------
    // Reset selection when month/data changes
    // --------------------------------------------------

    useEffect(() => {

        if (orderedSegmentIds.length === 0) {
            setSelectedSegmentId(null);
            return;
        }

        setSelectedSegmentId(
            orderedSegmentIds[0],
        );

    }, [orderedSegmentIds]);


    // --------------------------------------------------
    // Selected segment
    // --------------------------------------------------

    const selectedSegment =
        segments.find(
            segment =>
                segment.segmentId ===
                selectedSegmentId,
        ) ?? null;


    const selectedProductionUnit =
        productionMonth?.productionUnits.find(
            productionUnit =>
                productionUnit.prodId ===
                selectedSegment?.prodId,
        ) ?? null;

    const selectedProductionId =
    segments.find(
        segment =>
            segment.segmentId === selectedSegmentId,
    )?.prodId ?? null;


    // --------------------------------------------------
    // Statistics
    // --------------------------------------------------

const [statistics, setStatistics] =
    useState<ProductionStatistics | null>(null);

useEffect(() => {
    if (!selectedSegmentId) {
        setStatistics(null);
        return;
    }

    const segmentId = selectedSegmentId;

    async function loadStatistics() {
        try {
            const data =
                await getProductionStatistics(
                    displayedMonth,
                    displayedYear,
                    segmentId,
                );

            setStatistics(data);

        } catch (error) {
            console.error(
                "Failed to load production statistics:",
                error,
            );
            setStatistics(null);
        }
    }

    loadStatistics();

}, [
    displayedMonth,
    displayedYear,
    selectedSegmentId,
]);

    // --------------------------------------------------
    // Navigation
    // --------------------------------------------------

    const selectedIndex =
        orderedSegmentIds.indexOf(
            selectedSegmentId ?? "",
        );


    function selectNextSegment() {

        if (
            selectedIndex < 0 ||
            selectedIndex >=
                orderedSegmentIds.length - 1
        ) {
            return;
        }

        setSelectedSegmentId(
            orderedSegmentIds[
                selectedIndex + 1
            ],
        );
    }


    function selectPreviousSegment() {

        if (selectedIndex <= 0) {
            return;
        }

        setSelectedSegmentId(
            orderedSegmentIds[
                selectedIndex - 1
            ],
        );
    }


    // --------------------------------------------------
    // Loading / error states
    // --------------------------------------------------




    // --------------------------------------------------
    // UI
    // --------------------------------------------------

return (
    <Box sx={{ p: 1.5 }}>

        {/* Toolbar */}
        <Box
            sx={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                mb: 2,
            }}
        >
            {/* Month / Year */}
            <Box
                sx={{py:2,
                    display: "flex",
                    alignItems: "center",
                    gap: 2,
                }}
            >
                <TextField
                    select
                    size="small"
                    label="Month"
                    value={displayedMonth}
                    onChange={(event) => {
                        setDisplayedMonth(
                            Number(event.target.value),
                        );
                    }}
                    sx={{ minWidth: 150 }}
                >
                    {months.map((month) => (
                        <MenuItem
                            key={month.value}
                            value={month.value}
                        >
                            {month.label}
                        </MenuItem>
                    ))}
                </TextField>

                <TextField
                    select
                    size="small"
                    label="Year"
                    value={displayedYear}
                    onChange={(event) => {
                        setDisplayedYear(
                            Number(event.target.value),
                        );
                    }}
                    sx={{ minWidth: 120 }}
                >
                    {years.map((year) => (
                        <MenuItem
                            key={year}
                            value={year}
                        >
                            {year}
                        </MenuItem>
                    ))}
                </TextField>
            </Box>

            {/* Reports */}
            <Box
                sx={{
                    display: "flex",
                    alignItems: "center",
                    gap: 1,
                }}
            >
                <Button
                    variant="outlined"
                    size="small"
                    onClick={() => generatePdfReport(displayedMonth, displayedYear)}
                >
                    PDF Report
                </Button>

                <Button
                    variant="contained"
                    size="small"
                    onClick={() => generateExcelReport(displayedMonth, displayedYear)}
                >
                    Excel Report
                </Button>

                <Button
                    variant="outlined"
                    size="small"
                    onClick={() => downloadCsvExport(displayedMonth, displayedYear)}
                >
                    CSV Export
                </Button>
            </Box>
        </Box>
        {error && (
            <Box
                sx={{
                    mb: 2,
                    px: 2,
                    py: 1,
                    borderRadius: 1,
                    backgroundColor: "error.light",
                }}
            >
                <Typography
                    variant="body2"
                    color="error.dark"
                >
                    {error}
                </Typography>
            </Box>
        )}

            <Panels.Group orientation="horizontal" autoSaveId="production-dashboard-layout">

<Panels.Item
    defaultSize="70%"
    minSize="55%"
    surface
>
    <Stack
        spacing={0}
        sx={{ height: "100%" }}
    >

        {/* Production Overview heading */}
        <Box
            sx={{
                px: 2,
                pt: 2,
                pb: 1,
            }}
        >
            <Stack
                direction="row"
                alignItems="baseline"
                justifyContent="space-between"
            >
                <Typography variant="h5" sx={{ fontWeight: 600 }}>
                    Production Overview
                </Typography>

                {/* <Typography
                    variant="body2"
                    color="text.secondary"
                >
                    {months.find(
                        month =>
                            month.value ===
                            displayedMonth
                    )?.label}{" "}
                    {displayedYear}
                </Typography> */}
            </Stack>
        </Box>

        {/* Graph */}
        <Box
            sx={{
                px: 1.5,
                pb: 1,
            }}
        >
            <ProductionGraph
                data={segments}
                selectedSegmentId={
                    selectedSegmentId
                }
                selectedProductionId={
                    selectedProductionId
                }
                displayedMonth={displayedMonth}
                displayedYear={displayedYear}
                loading={loading}
            />
        </Box>

        <Box sx={{ display: "flex", flexDirection: "column" }}>
    <Divider />          

    <Box sx={{ display: "flex", alignItems: "stretch" }}>
        {/* Left Column: Segment Details & Navigation */}
        <Box sx={{ flex: 1.25, px: 2, py: 1.5, pr: 3 }}>
            
            {/* Unified Panel Header */}
            <Stack 
                direction="row" 
                alignItems="center" 
                justifyContent="space-between" 
                sx={{ mb: 2 }}
            >
                <Typography variant="h5" sx={{ fontWeight: 600 }}>
                    Selected Segment
                </Typography>

                <Stack direction="row" spacing={2} alignItems="center">
                    <Typography variant="body2" color="text.secondary">
                        {selectedIndex >= 0
                            ? `Segment ${selectedIndex + 1} of ${orderedSegmentIds.length}`
                            : "No segment selected"}
                    </Typography>

                    <ButtonGroup size="small">
                        <Button
                            onClick={selectPreviousSegment}
                            disabled={selectedIndex <= 0}
                        >
                            ◀ Prev
                        </Button>
                        <Button
                            onClick={selectNextSegment}
                            disabled={
                                selectedIndex < 0 ||
                                selectedIndex >= orderedSegmentIds.length - 1
                            }
                        >
                            Next ▶
                        </Button>
                    </ButtonGroup>
                </Stack>
            </Stack>

            {/* Component Details */}
            <SegmentDetails segment={selectedSegment} />
        </Box>

        <Divider orientation="vertical" flexItem />

        {/* Right Column: Statistics */}
        <Box sx={{ flex: 1, px: 2, py: 1.5, pl: 3 }}>
            <ProductivityStatistics statistics={statistics} />
        </Box>
    </Box>
</Box>

    </Stack>
</Panels.Item>

                <Panels.Separator disableDrag />

                <Panels.Item defaultSize="30%" minSize="25%" surface>
                    <Stack
                        spacing={0}
                        sx={{ height: "100%" }}
                    >
                    
                        <ProductionUnitDetails
                            productionUnit={selectedProductionUnit}
                        />

                    </Stack>
                </Panels.Item>
            </Panels.Group>
        </Box>
    );
}