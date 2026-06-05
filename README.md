# skills

My long-term personal skills library (repository renamed from `ben-skills`).

Each top-level directory is a single, self-contained skill (a `SKILL.md` at its
root, plus any reference files it needs). Skills are stored as plain folders —
this repo no longer uses Git submodules. Third-party skills are vendored here as
flat copies; attribution and licensing for each are listed below.

## Skills

| Skill | Folder | Purpose |
|---|---|---|
| activator-authoring-cli | [`activator-authoring-cli/`](activator-authoring-cli/) | Author Fabric activators and notification workflows using CLI patterns. |
| activator-consumption-cli | [`activator-consumption-cli/`](activator-consumption-cli/) | Inspect and monitor Fabric activators and alert definitions. |
| caveman | [`caveman/`](caveman/) | Ultra-compressed communication mode that cuts token usage by dropping filler while preserving technical accuracy. |
| check-updates | [`check-updates/`](check-updates/) | Check for upstream updates across Fabric skills and plugins. |
| create-pbi-report | [`create-pbi-report/`](create-pbi-report/) | Generate Power BI PBIR report definitions for report authoring workflows. |
| databricks-migration | [`databricks-migration/`](databricks-migration/) | Port Databricks notebooks and Hive workloads to Microsoft Fabric. |
| dataflows-authoring-cli | [`dataflows-authoring-cli/`](dataflows-authoring-cli/) | Create and update Fabric Dataflows Gen2 definitions and refresh workflows. |
| dataflows-consumption-cli | [`dataflows-consumption-cli/`](dataflows-consumption-cli/) | Inspect saved Fabric Dataflows, refresh history, and query metadata. |
| dataflows-save-as-authoring-cli | [`dataflows-save-as-authoring-cli/`](dataflows-save-as-authoring-cli/) | Assess and migrate Power BI Dataflows Gen1 to Fabric Dataflows Gen2.1. |
| deneb-visuals | [`deneb-visuals/`](deneb-visuals/) | Author Deneb/Vega visual assets and Power BI visual definitions. |
| e2e-medallion-architecture | [`e2e-medallion-architecture/`](e2e-medallion-architecture/) | Implement Bronze/Silver/Gold lakehouse patterns in Microsoft Fabric. |
| eventhouse-authoring-cli | [`eventhouse-authoring-cli/`](eventhouse-authoring-cli/) | Create and manage Fabric Eventhouse KQL schema and ingestion configurations. |
| eventhouse-consumption-cli | [`eventhouse-consumption-cli/`](eventhouse-consumption-cli/) | Query and inspect Fabric Eventhouse schemas, ingestion, and table metadata. |
| eventstream-authoring-cli | [`eventstream-authoring-cli/`](eventstream-authoring-cli/) | Build and publish Fabric Eventstream topologies for real-time pipelines. |
| eventstream-consumption-cli | [`eventstream-consumption-cli/`](eventstream-consumption-cli/) | Inspect and monitor Fabric Eventstream topologies and runtime wiring. |
| fabric-cli | [`fabric-cli/`](fabric-cli/) | Run Fabric CLI workflows for workspace, item, and REST API operations. |
| fabriciq | [`fabriciq/`](fabriciq/) | Answer Power BI business questions by discovering and querying semantic models. |
| grill-me | [`grill-me/`](grill-me/) | Relentlessly interview a plan or design, one branch at a time, until reaching shared understanding. |
| grill-with-docs | [`grill-with-docs/`](grill-with-docs/) | Grilling session that challenges a plan against the existing domain model and updates docs (CONTEXT.md, ADRs) inline. |
| handoff | [`handoff/`](handoff/) | Compact the current conversation into a handoff document for another agent to pick up. |
| hdinsight-migration | [`hdinsight-migration/`](hdinsight-migration/) | Port Azure HDInsight Spark and Hive workloads to Microsoft Fabric. |
| improve-codebase-architecture | [`improve-codebase-architecture/`](improve-codebase-architecture/) | Surface architectural friction and propose deepening refactors for testability and AI-navigability. |
| mbti-persona | [`mbti-persona/`](mbti-persona/) | Switch the agent's reasoning and communication style across all 16 MBTI types. |
| modifying-theme-json | [`modifying-theme-json/`](modifying-theme-json/) | Edit Power BI theme JSON files and styling for report definitions. |
| one-skill-to-rule-them-all | [`one-skill-to-rule-them-all/`](one-skill-to-rule-them-all/) | Meta-skill that watches your work to draft new skills and improve existing ones. |
| pbi-report-design | [`pbi-report-design/`](pbi-report-design/) | Design Power BI report pages, layouts, and theme usage. |
| pbi-visual-rendering | [`pbi-visual-rendering/`](pbi-visual-rendering/) | Power BI visual rendering engine for Deneb/Vega specs and HTML Content visual DAX measures. |
| pbir-cli | [`pbir-cli/`](pbir-cli/) | Create and manage Power BI PBIR report files from the CLI. |
| powerbi-report-authoring | [`powerbi-report-authoring/`](powerbi-report-authoring/) | Author and modify Power BI reports in PBIR format. |
| powerbi-semantic-model-authoring | [`powerbi-semantic-model-authoring/`](powerbi-semantic-model-authoring/) | Develop Power BI semantic models, DAX measures, and deployment definitions. |
| python-visuals | [`python-visuals/`](python-visuals/) | Create Python-powered visuals for Power BI reports. |
| r-visuals | [`r-visuals/`](r-visuals/) | Create R-powered visuals for Power BI reports. |
| review-report | [`review-report/`](review-report/) | Review Power BI report definitions and suggest improvements. |
| search-consumption-cli | [`search-consumption-cli/`](search-consumption-cli/) | Discover and inspect Fabric items and artifacts across workspaces. |
| semantic-model-authoring | [`semantic-model-authoring/`](semantic-model-authoring/) | Develop and manage Power BI semantic models across Desktop, PBIP, and Fabric. |
| semantic-model-consumption | [`semantic-model-consumption/`](semantic-model-consumption/) | Query Power BI semantic model metadata and execute DAX analysis. |
| semantic-modeling-prepforai | [`semantic-modeling-prepforai/`](semantic-modeling-prepforai/) | TMDL semantic model enhancement and Prep for AI configuration for Power BI Copilot / Fabric Data Agent. |
| spark-authoring-cli | [`spark-authoring-cli/`](spark-authoring-cli/) | Author Fabric Spark notebooks and workloads with CLI workflows. |
| spark-consumption-cli | [`spark-consumption-cli/`](spark-consumption-cli/) | Analyze Fabric Spark data using PySpark and Spark SQL workflows. |
| spark-operations-cli | [`spark-operations-cli/`](spark-operations-cli/) | Diagnose Fabric Spark job failures and performance issues. |
| sqldw-authoring-cli | [`sqldw-authoring-cli/`](sqldw-authoring-cli/) | Author Fabric Data Warehouse SQL schema and ingestion workflows. |
| sqldw-consumption-cli | [`sqldw-consumption-cli/`](sqldw-consumption-cli/) | Query Fabric SQL warehouse and lakehouse endpoints for analytics. |
| sqldw-operations-cli | [`sqldw-operations-cli/`](sqldw-operations-cli/) | Analyze Fabric warehouse performance and query behavior. |
| svg-visuals | [`svg-visuals/`](svg-visuals/) | Generate SVG visuals and assets for Power BI reports. |
| synapse-migration | [`synapse-migration/`](synapse-migration/) | Convert Synapse Spark workloads and linked services to Fabric equivalents. |

## Updating sourced skills

The externally-sourced skills are tracked in
[`skill-plugin-sources.json`](skill-plugin-sources.json) and refreshed with
[`update-sourced-skills.ipynb`](update-sourced-skills.ipynb). The notebook
shallow-clones each upstream repo, shows a per-skill change-list (with diffs)
when an update exists, and lets you apply or disregard each one. Applying
preserves local-only files (e.g. the vendored `LICENSE` copies) and never
deletes anything.

Skills under `excluded` in the manifest are never auto-updated:

- **caveman** — locally modified to suit my own use.
- **pbi-visual-rendering**, **semantic-modeling-prepforai** — my own skills.

## Attribution

This library bundles skills authored by others. Credit and licenses below; each
external skill folder retains its upstream license file.

### My own skills

- **pbi-visual-rendering** and **semantic-modeling-prepforai** — authored by
  Benjamin Hanna (Houston ISD).

### Matt Pocock — Skills for Real Engineers

Source: <https://github.com/mattpocock/skills> · License: MIT (a `LICENSE` copy
is included in each folder below)

- **caveman** (locally modified)
- **grill-me**
- **grill-with-docs**
- **handoff**
- **improve-codebase-architecture**

### ChangyuanYU — MBTI Persona Skill

Source: <https://github.com/ChangyuanYU/mbti-persona-skill> · License: MIT
(see [`mbti-persona/LICENSE`](mbti-persona/LICENSE))

- **mbti-persona**

### Eoghan Henn / rebelytics.com — One Skill to Rule Them All

Source: <https://github.com/rebelytics/one-skill-to-rule-them-all> ·
License: CC BY 4.0 (see [`one-skill-to-rule-them-all/LICENSE.txt`](one-skill-to-rule-them-all/LICENSE.txt))

- **task-observer**

### Microsoft / Skills for Fabric

Source: <https://github.com/microsoft/skills-for-fabric> · License: MIT

- **activator-authoring-cli**
- **activator-consumption-cli**
- **check-updates**
- **databricks-migration**
- **dataflows-authoring-cli**
- **dataflows-consumption-cli**
- **dataflows-save-as-authoring-cli**
- **e2e-medallion-architecture**
- **eventhouse-authoring-cli**
- **eventhouse-consumption-cli**
- **eventstream-authoring-cli**
- **eventstream-consumption-cli**
- **fabriciq**
- **hdinsight-migration**
- **semantic-model-authoring**
- **semantic-model-consumption**
- **spark-authoring-cli**
- **spark-consumption-cli**
- **spark-operations-cli**
- **sqldw-authoring-cli**
- **sqldw-consumption-cli**
- **sqldw-operations-cli**
- **synapse-migration**

### Rui Romano — Power BI Agentic Plugins

Source: <https://github.com/RuiRomano/powerbi-agentic-plugins> · License: MIT

- **powerbi-report-authoring**
- **powerbi-semantic-model-authoring**
- **fabric-cli**

### data-goblin — Power BI Agentic Development

Source: <https://github.com/data-goblin/power-bi-agentic-development> · License: MIT

- **create-pbi-report**
- **deneb-visuals**
- **modifying-theme-json**
- **pbi-report-design**
- **pbir-cli**
- **python-visuals**
- **r-visuals**
- **review-report**
- **svg-visuals**
