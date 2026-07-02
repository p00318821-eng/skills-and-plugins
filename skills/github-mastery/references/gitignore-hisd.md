# .gitignore — HISD Sensitive File Block

Append this block to any repo's `.gitignore`. Adjust per repo domain.

## Universal Block (all repos)

```gitignore
# ─── HISD SENSITIVE — DO NOT COMMIT ────────────────────────────────────────

# Environment & secrets
.env
.env.*
*.env
!.env.example

# Fabric / Azure credentials
*.pfx
*.pem
*.key
*.cer
fabrictoken.json
.azure/

# Connection strings & config with secrets
appsettings.*.json
!appsettings.json
local.settings.json
connectionstrings.json

# Student data — synthetic or real
*.csv
*.xlsx
*.parquet
data/raw/
data/real/
exports/

# Notebook outputs (may contain query results)
.ipynb_checkpoints/
**/.ipynb_checkpoints/

# ─── END HISD SENSITIVE ─────────────────────────────────────────────────────
```

## Rayfin-specific additions (`rayfin-apps`)

```gitignore
# Rayfin build & deploy artifacts
.rayfin/
dist/
node_modules/
*.tsbuildinfo
rayfin.lock
```

## Ed-Fi pipeline additions (`edfi-pipelines`)

```gitignore
# Notebook outputs & temp data
__pycache__/
*.pyc
spark-warehouse/
derby.log
metastore_db/
```

## Semantic model additions (`semantic-models`)

```gitignore
# Power BI Desktop temp files
*.pbix.lock
.pbi/
```

## PBI assets additions (`pbi-assets`)

```gitignore
# Theme drafts with embedded data
*.json.bak
```
