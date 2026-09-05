import { BarChart as MuiBarChart } from "@mui/x-charts-pro";
import { Skeleton } from "@andritzot/metris-web-ui/feedback/skeleton";
import { Box } from "@andritzot/metris-web-ui/layout/content/Box";
import type { ProductionSegment, } from "../types/Production";

const AXIS_COLOR = 'var(--metris-gray-400)';
const SEGMENT_COLOR = 'var(--metris-gray-50)';
const SELECTED_SEGMENT_COLOR = 'var(--metris-blue-800)';
const SAME_PRODID_COLOR = 'var(--metris-blue-300)';
const STROKE_COLOR = 'var(--metris-gray-600)';

export interface BarChartProps {
  readonly data: ProductionSegment[];
  readonly selectedSegmentId: string | null;
  readonly selectedProductionId: string | null;
  readonly displayedMonth: number;
  readonly displayedYear: number;
  readonly yLabel?: string;
  readonly width?: number;
  readonly height?: number;
  readonly color?: string;
  readonly categoryGapRatio?: number;
  readonly loading?: boolean;
  readonly showGrid?: boolean;
}

export default function BarChart({
  data,
  selectedSegmentId,
  selectedProductionId,
  displayedMonth,
  displayedYear,
  yLabel = "Mass (t)",
  width,
  height = 440,
  categoryGapRatio = 0.2,
  loading = false,
  showGrid = true,

}: BarChartProps) {
  if (loading) {
    
    return (
      <Box>
        <Skeleton
          variant="rectangular"
          width={width ?? '100%'}
          height={height}
          sx={{
            borderRadius: 1,
          }}
        />
      </Box>
    );
  }

  if (!data || data.length === 0) {
    return (
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          height,
          width: width ?? '100%',
          color: 'text.secondary',
        }}
      >
        No data available
      </Box>
    );
  }
  
const daysInMonth = new Date(
    displayedYear,
    displayedMonth,
    0,
).getDate();

function createSeries(

    segment: ProductionSegment,

    selectedSegmentId: string | null,

) {

    const day = segment.startTime.getDate();

    const values = Array(daysInMonth).fill(null);

    const isSelected =
    segment.segmentId === selectedSegmentId;

    const isSameProduction =
        segment.prodId === selectedProductionId;
        
    
    values[day - 1] = segment.massTotal;

    return {

        id: segment.segmentId,

        stack: "production",

        data: values,

        color: isSelected
            ? SELECTED_SEGMENT_COLOR
            : isSameProduction
                ? SAME_PRODID_COLOR
                : SEGMENT_COLOR

    };

}

const series = data.map(segment =>
    createSeries(segment, selectedSegmentId)
);

const dayLabels = Array.from(
    { length: daysInMonth},
    (_, index) => String(index + 1)
);

  return (
    <MuiBarChart
    series={series}

      xAxis={[
        {
          scaleType: 'band',
          data: dayLabels,
          categoryGapRatio,
          tickLabelStyle: { fill: AXIS_COLOR },
        },
      ]}
      yAxis={[
        {
          label: yLabel,
          tickLabelStyle: { fill: AXIS_COLOR },
          labelStyle: { fill: AXIS_COLOR },
        },
      ]}
      width={width}
      height={height}
      
      grid={
        showGrid
          ? {
              vertical: true,
              horizontal: true,
            }
          : undefined
      }
      sx={{
        '& line.MuiChartsAxis-line': {
          stroke: AXIS_COLOR,
        },
        '& line.MuiChartsAxis-tick': {
          stroke: AXIS_COLOR,
        },
        "& .MuiBarChart-element": {
        stroke: STROKE_COLOR,
        strokeWidth: 0.8,
    },
        '& text.MuiChartsAxis-tickLabel': {
          fill: AXIS_COLOR,
        },
        '& text.MuiChartsAxis-label': {
          fill: AXIS_COLOR,
        },
        '& .MuiChartsGrid-line': {
          stroke: '#ccc',
          opacity: 0,
          strokeDasharray: '4 4',
        },
      }}
          slots={{
        tooltip: () => null,
    }}
    />
  );
}
