export interface DashboardMonth {
    value: string;
    label: string;
}

export interface OverviewMetric {
    label: string;
    value: string;
    trend: string;
    note: string;
    tone: "positive" | "neutral" | "warning";
}

export interface ProductionGraphPoint {
    label: string;
    actual: number;
    target: number;
}

export interface ProductionSegment {
    readonly segmentId: string;
    readonly prodId: string;
    readonly usrId: string;

    readonly startTime: Date;
    readonly stopTime: Date;
    readonly runTime: number;

    readonly realTotal: number;
    readonly realSteam2Cond: number;
    readonly realSteam2Extr: number;
    readonly realWater2Cond: number;
    readonly realOil2CondExtr: number;
    readonly realWater2Extr: number;
    readonly realAdd2CondExtr: number;
    readonly realAdd5: number;
    readonly realAdd6: number;

    readonly wasteTotal: number;
    readonly wasteSteam2Cond: number;
    readonly wasteSteam2Extr: number;
    readonly wasteWater2Cond: number;
    readonly wasteOil2CondExtr: number;
    readonly wasteWater2Extr: number;
    readonly wasteAdd2CondExtr: number;
    readonly wasteAdd5: number;
    readonly wasteAdd6: number;
}

export interface ProductionUnit {
    prodId: string;
    prodNum: string;
    prodDesc: string;
    recipeName: string;
    statistics: ProductionUnitStatistics;
}

export interface ProductionUnitStatistics {
    segmentCount: number;

    startTime: string;
    stopTime: string | null;

    runTime: number;
    hours: number;

    realTotal: number;
    wasteTotal: number;

    rate: number;

    real: {
        realSteam2Cond: number;
        realSteam2Extr: number;
        realWater2Cond: number;
        realOil2CondExtr: number;
        realWater2Extr: number;
        realAdd2CondExtr: number;
        realAdd5: number;
        realAdd6: number;
    };

    realPercentages: {
        realSteam2Cond: number;
        realSteam2Extr: number;
        realWater2Cond: number;
        realOil2CondExtr: number;
        realWater2Extr: number;
        realAdd2CondExtr: number;
        realAdd5: number;
        realAdd6: number;
    };

    waste: {
        wasteSteam2Cond: number;
        wasteSteam2Extr: number;
        wasteWater2Cond: number;
        wasteOil2CondExtr: number;
        wasteWater2Extr: number;
        wasteAdd2CondExtr: number;
        wasteAdd5: number;
        wasteAdd6: number;
    };
}

export interface ReportAction {
    label: string;
    description: string;
}

export interface ProductionMonth {
    readonly month: number;
    readonly year: number;

    readonly segments: ProductionSegment[];
    readonly productionUnits: ProductionUnit[];
}

export interface ProductionStatistics {
    readonly segment: ProductionStats;
    readonly day: ProductionStats;
    readonly month: ProductionStats;
}

export interface ProductionStats {
    readonly tonnes: number;
    readonly hours: number;
    readonly rate: number;
}