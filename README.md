# skills-and-plugins

My long-term personal skills library and "Dotfiles for AI" — a curated
collection of Claude Code skills and plugins, with tooling to pull updates from
upstream repos and distribute skills to multiple AI tool environments.

Each skill lives under `skills/` as a self-contained folder (a `SKILL.md` at its
root, plus any reference files it needs). Plugin packages live under `plugins/`.
Third-party skills are vendored here as flat copies; attribution and licensing
for each are listed below.

## Documentation

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Orientation, quickstart, skill catalog, attribution (this file) |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Repository conventions, skill-update mechanism, distribution system |
| [.ai/PLAN.md](.ai/PLAN.md) | Current goals and open decisions |
| [.ai/archive/](.ai/archive/) | Historical decisions and rationale |
| [.ai/rules/](.ai/rules/) | Agent gotcha/convention source of truth |
| [.ai/LINEAGE.md](.ai/LINEAGE.md) | Which memory-architecture Standard/rung this repo follows |
| [.claude/CLAUDE.md](.claude/CLAUDE.md) | AI-agent operating instructions + navigation map |
| [CHANGELOG.md](CHANGELOG.md) | What changed, by release |

This table mirrors `.claude/CLAUDE.md`'s Navigation Map (kept separately since agents
auto-load `.claude/CLAUDE.md` at session start, while humans land here via GitHub first)
— update both if the doc set changes.

## Skills

| Skill | Folder | Purpose |
|---|---|---|
| activator-authoring-cli | [`activator-authoring-cli/`](skills/activator-authoring-cli/) | Author Fabric activators and notification workflows using CLI patterns. |
| activator-consumption-cli | [`activator-consumption-cli/`](skills/activator-consumption-cli/) | Inspect and monitor Fabric activators and alert definitions. |
| airunway-aks-setup | [`airunway-aks-setup/`](skills/airunway-aks-setup/) | Set up AI Runway (KAITO/vLLM model serving) on AKS from bare cluster to running deployment. |
| appinsights-instrumentation | [`appinsights-instrumentation/`](skills/appinsights-instrumentation/) | Instrument webapps with Azure Application Insights telemetry, SDK setup, and configuration. |
| azure-ai | [`azure-ai/`](skills/azure-ai/) | Use Azure AI Search, Speech, OpenAI, and Document Intelligence for search, transcription, and OCR. |
| azure-aigateway | [`azure-aigateway/`](skills/azure-aigateway/) | Configure Azure API Management as an AI Gateway for models, MCP tools, and agent governance. |
| azure-cloud-migrate | [`azure-cloud-migrate/`](skills/azure-cloud-migrate/) | Assess and migrate cross-cloud workloads (AWS/GCP) to Azure with reports and code conversion. |
| azure-compliance | [`azure-compliance/`](skills/azure-compliance/) | Run Azure compliance/security audits (azqr, Key Vault expiration, orphaned resources). |
| azure-compute | [`azure-compute/`](skills/azure-compute/) | Route Azure VM/VMSS creation, sizing, connectivity troubleshooting, and capacity reservation. |
| azure-cost | [`azure-cost/`](skills/azure-cost/) | Query, forecast, and optimize Azure spending and resource costs. |
| azure-deploy | [`azure-deploy/`](skills/azure-deploy/) | Execute Azure deployments (azd up/deploy, terraform apply) for already-prepared applications. |
| azure-diagnostics | [`azure-diagnostics/`](skills/azure-diagnostics/) | Debug Azure production issues using AppLens, Azure Monitor, resource health, and safe triage. |
| azure-enterprise-infra-planner | [`azure-enterprise-infra-planner/`](skills/azure-enterprise-infra-planner/) | Architect enterprise Azure landing zones — networking, identity, security, WAF-aligned Bicep/Terraform. |
| azure-hosted-copilot-sdk | [`azure-hosted-copilot-sdk/`](skills/azure-hosted-copilot-sdk/) | Build, deploy, and modify GitHub Copilot SDK apps hosted on Azure. |
| azure-kubernetes | [`azure-kubernetes/`](skills/azure-kubernetes/) | Plan, create, and configure production-ready AKS clusters — SKU, networking, security, autoscaling. |
| azure-kusto | [`azure-kusto/`](skills/azure-kusto/) | Query and analyze Azure Data Explorer (Kusto/ADX) data with KQL for logs and telemetry. |
| azure-messaging | [`azure-messaging/`](skills/azure-messaging/) | Troubleshoot Azure Event Hubs and Service Bus SDK connection, auth, and message-processing issues. |
| azure-prepare | [`azure-prepare/`](skills/azure-prepare/) | Prepare Azure apps for deployment — Bicep/Terraform infra, azure.yaml, Dockerfiles. |
| azure-quotas | [`azure-quotas/`](skills/azure-quotas/) | Check and manage Azure quota/usage limits for deployment planning and capacity validation. |
| azure-rbac | [`azure-rbac/`](skills/azure-rbac/) | Find the right least-privilege Azure RBAC role for an identity and generate assignment code. |
| azure-reliability | [`azure-reliability/`](skills/azure-reliability/) | Assess and remediate reliability posture (zone redundancy, failover, health probes) for PaaS apps. |
| azure-resource-lookup | [`azure-resource-lookup/`](skills/azure-resource-lookup/) | List and find Azure resources across subscriptions, resource groups, and tags. |
| azure-resource-visualizer | [`azure-resource-visualizer/`](skills/azure-resource-visualizer/) | Generate Mermaid architecture diagrams from Azure resource group relationships. |
| azure-storage | [`azure-storage/`](skills/azure-storage/) | Guide Azure Storage services (Blob, Files, Queue, Table, Data Lake) and access-tier selection. |
| azure-upgrade | [`azure-upgrade/`](skills/azure-upgrade/) | Assess and upgrade Azure workload plans/tiers/SKUs and modernize Azure SDK dependencies. |
| azure-validate | [`azure-validate/`](skills/azure-validate/) | Run pre-deployment validation — config, infra, RBAC, managed identity — before deploying to Azure. |
| caveman | [`caveman/`](skills/caveman/) | Ultra-compressed communication mode that cuts token usage by dropping filler while preserving technical accuracy. |
| check-updates | [`check-updates/`](skills/check-updates/) | Check for upstream updates across Fabric skills and plugins. |
| continual-learning | [`continual-learning/`](skills/continual-learning/) | Guide for implementing continual learning (hooks, memory scoping, reflection) in AI coding agents. |
| create-pbi-report | [`create-pbi-report/`](skills/create-pbi-report/) | Generate Power BI PBIR report definitions for report authoring workflows. |
| databricks-migration | [`databricks-migration/`](skills/databricks-migration/) | Port Databricks notebooks and Hive workloads to Microsoft Fabric. |
| dataflows-authoring-cli | [`dataflows-authoring-cli/`](skills/dataflows-authoring-cli/) | Create and update Fabric Dataflows Gen2 definitions and refresh workflows. |
| dataflows-consumption-cli | [`dataflows-consumption-cli/`](skills/dataflows-consumption-cli/) | Inspect saved Fabric Dataflows, refresh history, and query metadata. |
| dataflows-save-as-authoring-cli | [`dataflows-save-as-authoring-cli/`](skills/dataflows-save-as-authoring-cli/) | Assess and migrate Power BI Dataflows Gen1 to Fabric Dataflows Gen2.1. |
| deneb-visuals | [`deneb-visuals/`](skills/deneb-visuals/) | Author Deneb/Vega visual assets and Power BI visual definitions. |
| e2e-medallion-architecture | [`e2e-medallion-architecture/`](skills/e2e-medallion-architecture/) | Implement Bronze/Silver/Gold lakehouse patterns in Microsoft Fabric. |
| entra-agent-id | [`entra-agent-id/`](skills/entra-agent-id/) | Provision Microsoft Entra Agent Identity Blueprints and configure OAuth 2.0 token exchange for agents. |
| entra-app-registration | [`entra-app-registration/`](skills/entra-app-registration/) | Guide Microsoft Entra ID app registration, OAuth 2.0 authentication, and MSAL integration. |
| eventhouse-authoring-cli | [`eventhouse-authoring-cli/`](skills/eventhouse-authoring-cli/) | Create and manage Fabric Eventhouse KQL schema and ingestion configurations. |
| eventhouse-consumption-cli | [`eventhouse-consumption-cli/`](skills/eventhouse-consumption-cli/) | Query and inspect Fabric Eventhouse schemas, ingestion, and table metadata. |
| eventstream-authoring-cli | [`eventstream-authoring-cli/`](skills/eventstream-authoring-cli/) | Build and publish Fabric Eventstream topologies for real-time pipelines. |
| eventstream-consumption-cli | [`eventstream-consumption-cli/`](skills/eventstream-consumption-cli/) | Inspect and monitor Fabric Eventstream topologies and runtime wiring. |
| fabric-cli | [`fabric-cli/`](skills/fabric-cli/) | Run Fabric CLI workflows for workspace, item, and REST API operations. |
| fabriciq | [`fabriciq/`](skills/fabriciq/) | Answer Power BI business questions by discovering and querying semantic models. |
| github-issue-creator | [`github-issue-creator/`](skills/github-issue-creator/) | Convert notes, error logs, or screenshots into structured GitHub issue reports. |
| github-mastery | [`github-mastery/`](skills/github-mastery/) | GitHub best-practices copilot — PR templates, commit messages, branch strategy, workflows. |
| grill-me | [`grill-me/`](skills/grill-me/) | Relentlessly interview a plan or design, one branch at a time, until reaching shared understanding. |
| grill-with-docs | [`grill-with-docs/`](skills/grill-with-docs/) | Grilling session that challenges a plan against the existing domain model and updates docs (CONTEXT.md, ADRs) inline. |
| handoff | [`handoff/`](skills/handoff/) | Compact the current conversation into a handoff document for another agent to pick up. |
| hdinsight-migration | [`hdinsight-migration/`](skills/hdinsight-migration/) | Port Azure HDInsight Spark and Hive workloads to Microsoft Fabric. |
| improve-codebase-architecture | [`improve-codebase-architecture/`](skills/improve-codebase-architecture/) | Surface architectural friction and propose deepening refactors for testability and AI-navigability. |
| k12-dashboard-mockup | [`k12-dashboard-mockup/`](skills/k12-dashboard-mockup/) | Design K-12 data reporting dashboards and React mockups for district audiences. |
| mbti-persona | [`mbti-persona/`](skills/mbti-persona/) | Switch the agent's reasoning and communication style across all 16 MBTI types. |
| mcp-builder | [`mcp-builder/`](skills/mcp-builder/) | Guide for creating high-quality MCP servers exposing external services as LLM tools. |
| memory-architect | [`memory-architect/`](skills/memory-architect/) | Audit, scaffold, and consolidate Hub-and-Spoke project memory architecture across repositories. |
| microsoft-docs | [`microsoft-docs/`](skills/microsoft-docs/) | Query official Microsoft documentation for concepts, config, limits, and best practices. |
| microsoft-foundry | [`microsoft-foundry/`](skills/microsoft-foundry/) | Deploy, evaluate, fine-tune, and manage Microsoft Foundry agents end-to-end with azd. |
| modifying-theme-json | [`modifying-theme-json/`](skills/modifying-theme-json/) | Edit Power BI theme JSON files and styling for report definitions. |
| one-skill-to-rule-them-all | [`one-skill-to-rule-them-all/`](skills/one-skill-to-rule-them-all/) | Meta-skill that watches your work to draft new skills and improve existing ones. |
| pbi-report-design | [`pbi-report-design/`](skills/pbi-report-design/) | Design Power BI report pages, layouts, and theme usage. |
| pbi-visual-rendering | [`pbi-visual-rendering/`](skills/pbi-visual-rendering/) | Power BI visual rendering engine for Deneb/Vega specs and HTML Content visual DAX measures. |
| pbir-cli | [`pbir-cli/`](skills/pbir-cli/) | Create and manage Power BI PBIR report files from the CLI. |
| ponytail | [`ponytail/`](skills/ponytail/) | Force the laziest solution that actually works — YAGNI-driven, stdlib/native first. |
| powerbi-report-authoring | [`powerbi-report-authoring/`](skills/powerbi-report-authoring/) | Author and modify Power BI reports in PBIR format. |
| powerbi-semantic-model-authoring | [`powerbi-semantic-model-authoring/`](skills/powerbi-semantic-model-authoring/) | Develop Power BI semantic models, DAX measures, and deployment definitions. |
| python-appservice-deploy | [`python-appservice-deploy/`](skills/python-appservice-deploy/) | Deploy Python (Flask/Django/FastAPI) code to Azure App Service Linux. |
| python-visuals | [`python-visuals/`](skills/python-visuals/) | Create Python-powered visuals for Power BI reports. |
| r-visuals | [`r-visuals/`](skills/r-visuals/) | Create R-powered visuals for Power BI reports. |
| rayfin-companion | [`rayfin-companion/`](skills/rayfin-companion/) | Code-generation and architecture guidance for Microsoft Fabric Apps on the Rayfin platform. |
| review-report | [`review-report/`](skills/review-report/) | Review Power BI report definitions and suggest improvements. |
| sdi-backlog-writer | [`sdi-backlog-writer/`](skills/sdi-backlog-writer/) | Convert an HISD SDI Discovery Summary into Azure DevOps Epic/Feature/User Story markdown. |
| search-consumption-cli | [`search-consumption-cli/`](skills/search-consumption-cli/) | Discover and inspect Fabric items and artifacts across workspaces. |
| semantic-model-authoring | [`semantic-model-authoring/`](skills/semantic-model-authoring/) | Develop and manage Power BI semantic models across Desktop, PBIP, and Fabric. |
| semantic-model-consumption | [`semantic-model-consumption/`](skills/semantic-model-consumption/) | Query Power BI semantic model metadata and execute DAX analysis. |
| semantic-modeling-prepforai | [`semantic-modeling-prepforai/`](skills/semantic-modeling-prepforai/) | **Deprecated** as an actively-invoked skill (2026-07-10) — HISD content now delivered via global hooks; see `references/hisd-power-bi-context.md`. |
| skill-creator | [`skill-creator/`](skills/skill-creator/) | Create, edit, evaluate, and optimize Claude Code skills. |
| spark-authoring-cli | [`spark-authoring-cli/`](skills/spark-authoring-cli/) | Author Fabric Spark notebooks and workloads with CLI workflows. |
| spark-consumption-cli | [`spark-consumption-cli/`](skills/spark-consumption-cli/) | Analyze Fabric Spark data using PySpark and Spark SQL workflows. |
| spark-operations-cli | [`spark-operations-cli/`](skills/spark-operations-cli/) | Diagnose Fabric Spark job failures and performance issues. |
| sqldw-authoring-cli | [`sqldw-authoring-cli/`](skills/sqldw-authoring-cli/) | Author Fabric Data Warehouse SQL schema and ingestion workflows. |
| sqldw-consumption-cli | [`sqldw-consumption-cli/`](skills/sqldw-consumption-cli/) | Query Fabric SQL warehouse and lakehouse endpoints for analytics. |
| sqldw-operations-cli | [`sqldw-operations-cli/`](skills/sqldw-operations-cli/) | Analyze Fabric warehouse performance and query behavior. |
| svg-visuals | [`svg-visuals/`](skills/svg-visuals/) | Generate SVG visuals and assets for Power BI reports. |
| synapse-migration | [`synapse-migration/`](skills/synapse-migration/) | Convert Synapse Spark workloads and linked services to Fabric equivalents. |
| wiki-ado-convert | [`wiki-ado-convert/`](skills/wiki-ado-convert/) | Convert VitePress/GFM wiki markdown to Azure DevOps Wiki-compatible format. |
| wiki-agents-md | [`wiki-agents-md/`](skills/wiki-agents-md/) | Generate AGENTS.md coding-agent context files for repository folders. |
| wiki-architect | [`wiki-architect/`](skills/wiki-architect/) | Analyze code repositories and generate hierarchical documentation structures with onboarding guides. |
| wiki-changelog | [`wiki-changelog/`](skills/wiki-changelog/) | Analyze git commit history and generate structured, categorized changelogs. |
| wiki-llms-txt | [`wiki-llms-txt/`](skills/wiki-llms-txt/) | Generate llms.txt / llms-full.txt LLM-friendly project documentation. |
| wiki-onboarding | [`wiki-onboarding/`](skills/wiki-onboarding/) | Generate audience-tailored onboarding guides (Contributor, Staff Engineer, Executive, PM). |
| wiki-page-writer | [`wiki-page-writer/`](skills/wiki-page-writer/) | Generate rich technical documentation pages with diagrams and source citations. |
| wiki-qa | [`wiki-qa/`](skills/wiki-qa/) | Answer questions about a code repository using source file analysis. |
| wiki-researcher | [`wiki-researcher/`](skills/wiki-researcher/) | Conduct multi-turn deep research on specific topics within a codebase. |
| wiki-vitepress | [`wiki-vitepress/`](skills/wiki-vitepress/) | Package generated wiki markdown into a VitePress static site. |

## Distributing skills

The distribution system pushes skill prompts into target files (CLAUDE.md,
copilot-instructions.md, etc.) for multiple AI tool environments.

**Setup:**
```
py -m pip install -r requirements.txt
```

**Configure destinations** in
[`manifests/destinations.json`](manifests/destinations.json) — each entry
specifies a `target_file` (with `{HOME}` expansion), `skills_assigned`, and an
`enabled` toggle.

**Run** [`skills-workflow.ipynb`](skills-workflow.ipynb) in VS Code — Phase 4
(Distribute):
1. **Build Cache** — copies SKILL.md files to `.cache/prompts/`.
2. **Distribute** — injects cached prompts into target files using idempotent
   HTML-comment boundary markers (`<!-- MANAGED-SKILLS:START/END -->`).
3. **Report** — prints a summary of what changed.

Manual content outside the boundary markers is always preserved.

## Updating sourced skills

The externally-sourced skills are tracked in
[`manifests/origins.json`](manifests/origins.json) and refreshed with
[`skills-workflow.ipynb`](skills-workflow.ipynb)'s Phase 2 (Update from
source). It shallow-clones each upstream repo, shows a per-skill change-list
(with diffs) when an update exists, and lets you apply or disregard each one.
Applying preserves local-only files (e.g. the vendored `LICENSE` copies) and
never deletes anything.

Skills under `excluded` in the manifest are never auto-updated — this includes
locally-modified skills, my own skills, and skills extracted from a plugin
package (those update via the plugin's parent manifest entry instead).

## Attribution

This library bundles skills authored by others. Credit and licenses below; each
external skill folder retains its upstream license file.

### My own skills

Authored by Benjamin Hanna (Houston ISD):

- **pbi-visual-rendering**, **semantic-modeling-prepforai**
- **github-mastery**, **k12-dashboard-mockup**, **rayfin-companion**
- **sdi-backlog-writer**

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
(see [`skills/mbti-persona/LICENSE`](skills/mbti-persona/LICENSE))

- **mbti-persona**

### Eoghan Henn / rebelytics.com — One Skill to Rule Them All

Source: <https://github.com/rebelytics/one-skill-to-rule-them-all> ·
License: CC BY 4.0 (see [`skills/one-skill-to-rule-them-all/LICENSE.txt`](skills/one-skill-to-rule-them-all/LICENSE.txt))

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

### Microsoft — `microsoft/skills`

Source: <https://github.com/microsoft/skills> · License: MIT. Includes two
plugin packages ([`plugins/azure-skills/`](plugins/azure-skills/),
[`plugins/deep-wiki/`](plugins/deep-wiki/)) whose skills are also flattened
into `skills/` per [ARCHITECTURE.md § Repository conventions](ARCHITECTURE.md#repository-conventions),
plus three individually-tracked skills.

- **azure-skills plugin:** airunway-aks-setup, appinsights-instrumentation,
  azure-ai, azure-aigateway, azure-cloud-migrate, azure-compliance,
  azure-compute, azure-cost, azure-deploy, azure-diagnostics,
  azure-enterprise-infra-planner, azure-hosted-copilot-sdk, azure-kubernetes,
  azure-kusto, azure-messaging, azure-prepare, azure-quotas, azure-rbac,
  azure-reliability, azure-resource-lookup, azure-resource-visualizer,
  azure-storage, azure-upgrade, azure-validate, entra-agent-id,
  entra-app-registration, microsoft-foundry, python-appservice-deploy
- **deep-wiki plugin:** wiki-ado-convert, wiki-agents-md, wiki-architect,
  wiki-changelog, wiki-llms-txt, wiki-onboarding, wiki-page-writer, wiki-qa,
  wiki-researcher, wiki-vitepress
- **Individually tracked:** microsoft-docs, continual-learning, github-issue-creator

### Anthropic — `anthropics/skills`

Source: <https://github.com/anthropics/skills> · License: MIT

- **skill-creator**
- **mcp-builder**

### Dietrich Gebert — ponytail

Source: <https://github.com/DietrichGebert/ponytail> · License: MIT

- **ponytail**
