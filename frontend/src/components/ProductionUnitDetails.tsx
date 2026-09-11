import { Box, Divider, Typography } from "@mui/material";

import type { ProductionUnit } from "../types/Production";

interface ProductionUnitDetailsProps {
    readonly productionUnit: ProductionUnit | null;
}

function formatRuntime(seconds: number): string {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = Math.floor(seconds % 60);

    return `${hours} h ${minutes} min ${remainingSeconds} s`;
}

function formatDateTime(value: string | null): string {
    if (!value) {
        return "-";
    }

    return new Date(value).toLocaleString("en-GB", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: false,
    });
}

export default function ProductionUnitDetails({
    productionUnit,
}: ProductionUnitDetailsProps) {
    if (!productionUnit) {
        return null;
    }

    const { statistics } = productionUnit;

    return (
        <Box sx={{ padding: 4 }}>
            <Typography variant="h5" sx={{ fontWeight: 600 }}>
                Production Unit
            </Typography>

            <Box
                sx={{
                    mt: 2,
                    mb: 2,
                    display: "grid",
                    gridTemplateColumns: "1fr 1fr",
                    gap: 2,
                }}
            >
                <Box>
                    <strong>Production ID</strong>
                    <div>{productionUnit.prodId}</div>
                </Box>

                <Box>
                    <strong>Production Number</strong>
                    <div>{productionUnit.prodNum}</div>
                </Box>

                <Box>
                    <strong>Description</strong>
                    <div>{productionUnit.prodDesc}</div>
                </Box>

                <Box>
                    <strong>Recipe Name</strong>
                    <div>{productionUnit.recipeName}</div>
                </Box>

                <Box>
                    <strong>Segments</strong>
                    <div>{statistics.segmentCount}</div>
                </Box>

                <Box>
                    <strong>Runtime</strong>
                    <div>
                        {formatRuntime(statistics.runTime)}
                    </div>
                </Box>

                <Box>
                    <strong>Start</strong>
                    <div>
                        {formatDateTime(statistics.startTime)}
                    </div>
                </Box>

                <Box>
                    <strong>Stop</strong>
                    <div>
                        {formatDateTime(statistics.stopTime)}
                    </div>
                </Box>

                <Box>
                    <strong>Real Total</strong>
                    <div>
                        {statistics.realTotal.toFixed(2)} t
                    </div>
                </Box>

                <Box>
                    <strong>Waste Total</strong>
                    <div>
                        {statistics.wasteTotal.toFixed(2)} t
                    </div>
                </Box>

            </Box>

            <Divider />

            <Box
                sx={{
                    display: "grid",
                    gridTemplateColumns: "1fr 1fr 1fr",
                    columnGap: 2,
                    rowGap: 1,
                }}
            >
                <strong>Material</strong>
                <strong>Real</strong>
                <strong>Waste</strong>

                <span>Total</span>
                <span>
                    {statistics.realTotal.toFixed(2)} t
                </span>
                <span>
                    {statistics.wasteTotal.toFixed(2)} t
                </span>


                <span>Steam To Conditioner</span>
                <span>
                    {statistics.real.realSteam2Cond.toFixed(2)} t
                </span>
                <span>
                    {statistics.waste.wasteSteam2Cond.toFixed(2)} t
                </span>

                <span>Steam To Extruder</span>
                <span>
                    {statistics.real.realSteam2Extr.toFixed(2)} t
                </span>
                <span>
                    {statistics.waste.wasteSteam2Extr.toFixed(2)} t
                </span>

                <span>Water to Conditioner</span>
                <span>
                    {statistics.real.realWater2Cond.toFixed(2)} t
                </span>
                <span>
                    {statistics.waste.wasteWater2Cond.toFixed(2)} t
                </span>

                <span>Oil to Cond. Extr.</span>
                <span>
                    {statistics.real.realOil2CondExtr.toFixed(2)} t
                </span>
                <span>
                    {statistics.waste.wasteOil2CondExtr.toFixed(2)} t
                </span>
                                
                <span>Water to Extruder</span>
                <span>
                    {statistics.real.realWater2Extr.toFixed(2)} t
                </span>
                <span>
                    {statistics.waste.wasteWater2Extr.toFixed(2)} t
                </span>
                                                
                <span>Add. to Cond. Extr.</span>
                <span>
                    {statistics.real.realAdd2CondExtr.toFixed(2)} t
                </span>
                <span>
                    {statistics.waste.wasteAdd2CondExtr.toFixed(2)} t
                </span>

                <span>Aditive 5</span>
                <span>
                    {statistics.real.realAdd5.toFixed(2)} t
                </span>
                <span>
                    {statistics.waste.wasteAdd5.toFixed(2)} t
                </span>

                <span>Aditive 6</span>
                <span>
                    {statistics.real.realAdd6.toFixed(2)} t
                </span>
                <span>
                    {statistics.waste.wasteAdd6.toFixed(2)} t
                </span>
            </Box>
        </Box>
    );
}