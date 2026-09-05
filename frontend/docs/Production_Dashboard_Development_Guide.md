# Production Dashboard Development Guide

## Overview

This project aims to develop a historical production dashboard for the
Metris ecosystem using **Flask**, **React**, and the **Metris Web UI**
component library.

The application is intended to visualize historical production data for
a selected month, allowing users to explore production segments, inspect
associated batch information, and generate reports from the displayed
data.

The documentation and export of the storybook are included in the llms_documentation.txt file.

The initial focus is entirely on building the user interface. Backend
integration and communication with production data sources will be
addressed in a later phase.

------------------------------------------------------------------------

# Guiding Principles

The dashboard should be developed according to the following principles:

-   Build reusable, modular components.
-   Keep the frontend focused on presentation rather than business
    logic.
-   Use Metris Web UI components wherever appropriate.
-   Prioritize clarity and maintainability over premature optimization.
-   Develop against mock data until the backend interface is defined.

These principles should guide decisions throughout the project.

------------------------------------------------------------------------

# Project Scope

The first version of the application should provide:

-   A monthly production overview
-   A production graph
-   Summary KPI cards
-   Segment and batch information
-   Basic production statistics
-   Report generation controls

The application is intended for historical analysis only and should not
include live production monitoring.

------------------------------------------------------------------------

# Development Roadmap

## Phase 1 -- Foundation

Establish the project and development environment.

**Goals:**

-   Create the project structure.
-   Integrate the Metris Web UI library.
-   Build the basic page layout.
-   Create placeholder components for the main sections.

At the end of this phase, the application should resemble the intended
dashboard structure without requiring real data.

------------------------------------------------------------------------

## Phase 2 -- UI Development

Develop the individual interface components.

Focus on:

-   Toolbar
-   KPI cards
-   Production graph
-   Information panels
-   Navigation between production segments

Use mock data throughout this phase to enable independent frontend
development.

------------------------------------------------------------------------

## Phase 3 -- Polish

Improve usability and consistency.

Typical tasks include:

-   Responsive layout improvements
-   Visual refinement
-   Loading and empty states
-   Consistent spacing and styling
-   Component reuse and cleanup

The objective is a polished, coherent interface before backend
integration begins.

------------------------------------------------------------------------

## Phase 4 -- Backend Integration

Once the backend architecture is defined, replace mock data with real
data sources.

This phase should require minimal changes to the UI thanks to the
separation between presentation and data.

------------------------------------------------------------------------

# Architecture

Maintain a clear separation between responsibilities.

## Frontend

Responsible for:

-   Rendering the interface
-   Managing UI state
-   Displaying data
-   Handling user interactions

## Backend

Responsible for:

-   Retrieving production data
-   Processing business logic
-   Generating reports
-   Providing data to the frontend

The frontend should avoid embedding business logic whenever possible.

------------------------------------------------------------------------

# User Workflow

The dashboard follows a simple interaction model:

1.  Select a month.
2.  Review the production overview.
3.  Explore production segments.
4.  Inspect related batch information.
5.  Generate reports if required.

The selected month defines the context for the entire application.

------------------------------------------------------------------------

# Design Philosophy

The interface should emphasize simplicity and readability.

The production graph is the primary focus of the page, while supporting
information is presented through clearly organized detail panels.

Consistency with other Metris applications is more important than
introducing custom visual styles.

------------------------------------------------------------------------

# Success Criteria

The first milestone is complete when:

-   The dashboard layout is fully implemented.
-   All major UI components exist.
-   Components use mock data.
-   The interface resembles the intended design.
-   The application is ready for backend integration.
