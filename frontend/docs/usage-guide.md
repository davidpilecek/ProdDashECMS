# Metris UI technical usage guide (AI-oriented)

This guide is for AI coding assistants generating or modifying code that consumes `@andritzot/metris-web-ui`.

Goal: produce implementation-ready code that matches library conventions.

## 1) Bootstrapping (required runtime setup)

### Install package and peer dependencies

```bash
pnpm add @andritzot/metris-web-ui
pnpm add @emotion/react @emotion/styled \
  @mui/material @mui/system @mui/icons-material \
  @andritzot/metris-web-utils zustand dayjs
```

Install optional peers only when importing related entries (map, DataGrid premium, date pickers, drag-and-drop, forms, etc.).

### Import the stylesheet once

```ts
// main.tsx / _app.tsx / app/layout.tsx
import "@andritzot/metris-web-ui/styles.css";
```

Without this, `MetrisUIProvider` reports missing stylesheet tokens.

### Mount `MetrisUIProvider` once near the app root

```tsx
import { MetrisUIProvider } from "@andritzot/metris-web-ui/context";

export function AppProviders({ children }: { children: React.ReactNode }) {
  return <MetrisUIProvider language="en">{children}</MetrisUIProvider>;
}
```

What this provider wires:

- MUI `ThemeProvider` (light/dark theme)
- `CssBaseline`
- snackbar provider (`notistack`)
- confirm dialog provider
- UI translation bundles under namespace `ui`

## 2) Import strategy (technical rules)

- Prefer subpath imports (tree-shakeable public entries).
- Do not import internal source paths.
- Use the package root (`@andritzot/metris-web-ui`) only for CSS side-effects and root-level exports.

Examples:

```ts
import { Button } from "@andritzot/metris-web-ui/inputs/button";
import { DataGrid } from "@andritzot/metris-web-ui/mui-x/data-grid";
import { Panels } from "@andritzot/metris-web-ui/layout/panels";
import { Form } from "@andritzot/metris-web-ui/form";
```

## 3) Entry-point map (high-value entries)

| Entry                                 | Use for                                                     |
| ------------------------------------- | ----------------------------------------------------------- |
| `./context`                           | App-level provider (`MetrisUIProvider`)                     |
| `./theme`                             | Theme objects/hooks (`lightTheme`, `darkTheme`, `useTheme`) |
| `./layout/app-platform`               | App launcher/platform pages                                 |
| `./layout/panels`                     | Resizable multi-panel workspaces                            |
| `./layout/navigation/*`               | Application navigation drawers/lists                        |
| `./inputs/*`                          | Input controls (`button`, `select`, `textfield`, etc.)      |
| `./form`                              | Typed form composition around `react-hook-form`             |
| `./feedback/*`                        | Dialogs, alerts, snackbar, progress, skeleton               |
| `./mui-x/data-grid`                   | Data-heavy table pages with toolbar patterns                |
| `./mui-x/date-*`, `./mui-x/time-*`    | Date/time inputs and ranges                                 |
| `./charts/*`                          | Chart primitives and chart-card compositions                |
| `./canvas/map`, `./canvas/react-flow` | Spatial/flow visualizations                                 |
| `./utils/drag-and-drop`               | Sortable/reorderable UI                                     |
| `./styles.css`                        | Global tokens + foundations (required import)               |

### Source-derived module inventory (`src/**/index.ts`)

The codebase currently exposes a broad, category-based API surface via index files:

- `layout`: 26 index modules
- `inputs`: 21 index modules
- `navigation`: 20 index modules
- `data-display`: 15 index modules
- `utils`: 11 index modules
- `charts`: 10 index modules
- `mui-x`: 10 index modules
- `feedback`: 9 index modules
- `surfaces`: 4 index modules
- `canvas`: 2 index modules
- `metris`: 2 index modules

Use this as the primary taxonomy when generating imports or scaffolding new pages.

## 4) Layout composition patterns (code-first)

### A) Platform shell

Use:

- `MetrisAppBar`
- `MetrisAppNavigationDrawer` (or platform drawer variant)
- content area with cards/tables/charts

Typical shell composition:

```tsx
<MetrisAppBar title="Metris Platform" />
<MetrisAppNavigationDrawer appNavItems={navItems} onItemClicked={onItemClicked}>
  <MainPageContent />
</MetrisAppNavigationDrawer>
```

### B) Resizable analysis workspace with `Panels`

Use `Panels.Group`, `Panels.Item`, `Panels.Separator`, `Panels.SidebarPanel`.

```tsx
<Panels.Group
  orientation={{ xs: "vertical", md: "horizontal" }}
  autoSaveId="analysis-layout"
>
  <Panels.Item defaultSize="70%" minSize="40%" surface>
    <PrimaryContent />
  </Panels.Item>
  <Panels.Separator />
  <Panels.SidebarPanel defaultSize="30%" collapsedSize="56px">
    <SidebarContent />
  </Panels.SidebarPanel>
</Panels.Group>
```

Technical notes:

- Size units should be explicit strings (`"50%"`, `"200px"`, `"20rem"`).
- `autoSaveId` persists panel layout in local storage.
- For SSR/custom persistence, use explicit layout persistence hooks instead of `autoSaveId`.

## 5) Form system usage (`./form`)

The form module wraps `react-hook-form` with typed components and reduced boilerplate.

### Simplified API (default)

```tsx
const form = useForm<FormData>({ defaultValues });

<Form.Provider {...form}>
  <Form.Root onSubmit={form.handleSubmit(onSubmit)}>
    <Form.TextField
      control={form.control}
      name="email"
      label="Email"
      required
    />
    <Form.Select
      control={form.control}
      name="country"
      label="Country"
      options={countries}
    />
    <Button type="submit">Save</Button>
  </Form.Root>
</Form.Provider>;
```

### Schema validation

Use resolvers (for example, Zod) with `useForm`.

```tsx
const form = useForm<FormData>({
  resolver: zodResolver(schema),
  defaultValues,
});
```

### Compositional API (when layout is complex)

Use `Form.Field`, `Form.Item`, `Form.Label`, `Form.Control`, `Form.Message` when you need custom structural control.

## 6) Data Grid pattern (`./mui-x/data-grid`)

The library’s `DataGrid` stories demonstrate toolbar composition via compound subcomponents.

```tsx
const CustomToolbar = () => (
  <DataGrid.Toolbar>
    <DataGrid.Toolbar.QuickFilter />
    <DataGrid.Toolbar.Actions>
      <DataGrid.Toolbar.ColumnsButton />
      <DataGrid.Toolbar.FilterButton />
      <DataGrid.Toolbar.DensitySelector />
      <DataGrid.Toolbar.ExportButton />
    </DataGrid.Toolbar.Actions>
  </DataGrid.Toolbar>
);

<DataGrid
  rows={rows}
  columns={columns}
  showToolbar
  slots={{ toolbar: CustomToolbar }}
/>;
```

Use this for configurable admin/data-review pages.

Source-verified behavior from `DataGrid.tsx`:

- wraps `@mui/x-data-grid-premium` and is license-gated via `withLicense`
- installs a default toolbar when `props.slots?.toolbar` is not provided
- enables pagination by default (`pagination ?? true`)
- default page size config:
  - `DEFAULT_PAGE_SIZE = 25`
  - `DEFAULT_PAGE_SIZE_OPTIONS = [25, 50, 100, 500]`
- default loading overlay behavior:
  - rows exist: linear progress
  - no rows: circular progress
- normalizes toolbar labels (`localeText`) for icon-first toolbar controls

## 7) i18n and translation constraints

- In this ecosystem, use translation APIs from `@andritzot/metris-web-utils/translation`.
- Use namespace `ui` for library keys.
- Do not create a second i18n instance.
- Let `MetrisUIProvider` drive language changes (`language` prop).

Example:

```tsx
import { useTranslation } from "@andritzot/metris-web-utils/translation";

const { t } = useTranslation("ui");
return <span>{t("all-apps")}</span>;
```

## 8) Module federation requirements

If host + remotes both consume the library, share singleton-sensitive packages across all MF apps:

- `react`, `react-dom`
- `@emotion/react`, `@emotion/styled`
- `@mui/material`, `@mui/system`, `@mui/icons-material`
- `zustand`
- `@andritzot/metris-web-utils`
- `@andritzot/metris-web-ui`

Reason: avoid split theme stores and MUI duplication that break theme propagation.

## 9) Utilities and when to use them

- `./utils/drag-and-drop`: reorderable list UIs (built on dnd-kit)
- `./utils/click-away-listener`: dismiss-on-outside-click interactions
- `./utils/transitions/*`: standardized transition wrappers (`collapse`, `fade`, `grow`, `slide`, `zoom`)
- `./utils/media-query`: responsive branching helpers

Source-verified re-export behavior:

- `./utils/click-away-listener` re-exports MUI `ClickAwayListener`
- `./canvas/map` exports `LeafletMap` / `Map` and re-exports `react-leaflet`
- `./canvas/react-flow` re-exports `@xyflow/system`, selected `@xyflow/react` APIs, plus Metris context/hooks/components

## 10) Capability matrix (what AI can safely assemble)

- Platform shell: app bar + nav drawer + content
- CRUD page: `Form` + `DataGrid` + dialog/snackbar feedback
- Master/detail workspace: `Panels` + list/grid + detail pane
- Analytics page: chart-card + line/bar/donut/trend charts
- Tree-driven explorer: project treeview + side panel
- Selection workflows: tag-selector/item-picker dialog

## 11) AI generation rules (strict)

When generating code for this package:

1. Import `@andritzot/metris-web-ui/styles.css` once at app entry.
2. Ensure app is wrapped with `MetrisUIProvider`.
3. Prefer package wrappers over raw MUI components when equivalents exist.
4. Prefer Storybook composition patterns over ad-hoc layouts.
5. Use subpath imports from public exports only.
6. Preserve shared i18n/theme patterns; do not instantiate parallel providers/stores.
7. For panel layouts, use explicit size units and `Panels` primitives.
8. For data tables, prefer `DataGrid` with toolbar compound components.
9. When using premium MUI X entries, provide `PUBLIC_MUI_X_LICENSE_KEY` in runtime env.
10. Use package exports for map/flow wrappers instead of importing `react-leaflet` or `@xyflow/*` directly.

## 12) Source-backed implementation details to preserve

### Panels

- `Panels` exposes:
  - `Group`, `Item`, `Separator`, `SidebarPanel`
  - hooks forwarded from `react-resizable-panels`: `useGroupRef`, `usePanelRef`, `useDefaultLayout`
- `Panels.Group` resolves responsive orientation via MUI breakpoints (`xs`..`xl`)
- `autoSaveId` uses local storage persistence; omit it to avoid persistence I/O

### Form

- `Form` exposes both simplified and base APIs:
  - simplified: `TextField`, `Select`, `Autocomplete`, `Switch`, `Checkbox`, `DatePicker`, `DateTimePicker`, `TimePicker`, `InputNumber`, `RichTextEditor`
  - base: `*Base` variants for custom layouts
- `Form.RichTextEditor` and `Form.RichTextEditorBase` are lazy-loaded
- `./form/index.ts` re-exports core `react-hook-form` types for consumer convenience

### Context/theme

- `MetrisUIProvider`:
  - toggles light/dark theme via shared theme store
  - applies `document.documentElement.dataset.theme`
  - changes language through shared i18n instance
  - wraps snackbar and confirm-dialog providers
  - performs missing stylesheet detection in development

### App layout compound API

- `AppLayout` is a compound component:
  - `AppLayout.SideNavigation`
  - `AppLayout.Content`
- internally computes grid columns from navigation drawer state

## 13) Minimal end-to-end page example

```tsx
import "@andritzot/metris-web-ui/styles.css";

import { MetrisUIProvider } from "@andritzot/metris-web-ui/context";
import { Form } from "@andritzot/metris-web-ui/form";
import { Panels } from "@andritzot/metris-web-ui/layout/panels";
import { DataGrid } from "@andritzot/metris-web-ui/mui-x/data-grid";

export function App() {
  return (
    <MetrisUIProvider language="en">
      <Panels.Group
        orientation={{ xs: "vertical", md: "horizontal" }}
        autoSaveId="main"
      >
        <Panels.Item defaultSize="35%" minSize="25%" surface>
          <MyFilterForm />
        </Panels.Item>
        <Panels.Separator />
        <Panels.Item defaultSize="65%" minSize="40%" surface>
          <DataGrid rows={rows} columns={columns} showToolbar />
        </Panels.Item>
      </Panels.Group>
    </MetrisUIProvider>
  );
}
```
