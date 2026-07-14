# Discovery Summary Contract

The Discovery Summary is the single handoff artifact between the SDI Request Intake Agent (producer) and the SDI Azure DevOps Backlog Writer Agent (consumer). It uses exactly nine sections, with these exact names, in this order.

This file is canonical at the repo root. Each agent's Knowledge folder carries a copy; if they ever differ, the root copy wins.

## Rules

- **All nine sections always present.** A section with no confirmed content is included with the single line `Unresolved — see Section 9.` Never omit a section; never fabricate content to fill one.
- **Exact headings.** The Backlog Writer's decomposition logic keys on these section names verbatim.
- **Technical pass-through.** Table names, DAX, SQL, file/OneLake paths, and configuration strings appear verbatim as the requester supplied them — never altered, abbreviated, or truncated.
- **Plain business language** for narrative content; this artifact is what the requester signs off, so they must be able to read it.
- **Title line:** `# Discovery Summary: [request name]`, followed by requester name and date.

## Sections

### 1. Business Objective & Audience
Who consumes the deliverable and why. Personas (executives, campus staff, analysts, external), the core business questions it must answer, where the request originated (spec document, tracking list, legacy Excel, verbal), and any regulatory or compliance drivers.
→ Backlog Writer maps to: Epic Strategic Objective; User Story personas.

### 2. Data Sources & Lineage
Every data origin with its transport and target path: live core systems (SIS, ERP, HRIS), flat-file/SFTP feeds, ad-hoc business sources (SharePoint/OneDrive files). Source-to-target lineage across Bronze/Silver/Gold layers.
→ Epic Source Systems & Data Lineage; Feature Data Sources.

### 3. Business Rules & Logic Location
Where calculation logic currently lives (Excel formulas, document prose, backend views, stored procedures, tribal knowledge), hidden quirks and manual overrides, and conditional logic by time period, campus, or student population.
→ Feature Business Rules; Story Technical Notes.

### 4. Dimensional Model
Target semantic structure: schema type (Star/Snowflake/hybrid), fact grain, dimensions and hierarchies (e.g., School → Region → District), slowly changing dimension strategy, relationship cardinalities, flat-file normalization needs.
→ Epic Target Architecture; Feature Functional Scope.

### 5. Metrics & Calculations
Every metric with calculation method and edge-case handling: aggregations, semi-additive measures, ratios/weighted averages, time intelligence (YoY, YTD, fiscal/school-day calendars), missing-data handling (NULLs, late-arriving records, absence codes).
→ Feature Business Rules; Story Acceptance Criteria + Technical Notes.

### 6. Security & Governance
RLS rules mapped to roles/campuses/regions, OLS for sensitive columns, PII/PHI fields and protections, governance tier, audit requirements.
→ Epic Security & Governance; Story Acceptance Criteria (RLS/OLS).

### 7. Pipeline & Refresh
Refresh frequency targets, triggers (scheduled, event-driven, live connection, manual), row volume estimates and growth, downstream SLA dependencies.
→ Feature Pipeline & Refresh; Story Acceptance Criteria (refresh).

### 8. Validation Anchors
Baselines for correctness: legacy report numbers, source-of-truth queries, manual spreadsheets; reconciliation strategy; acceptable variance and quality thresholds.
→ Story Validation Anchors.

### 9. Unresolved Items
Every open question, each with: what is missing, why it could not be resolved, and the owner or next step. The only legitimate destination for unconfirmed content.
→ Epic Open Items / Risks. Never backfilled into acceptance criteria.
