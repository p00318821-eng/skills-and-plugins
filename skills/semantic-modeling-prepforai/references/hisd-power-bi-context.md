# HISD Power BI / Fabric Context

Consolidated HISD-specific and gap-filling content for Power BI semantic model AI-readiness
work. Delivered via two global Claude Code hooks (`SessionStart` + `PostToolUse` on
`.tmdl` files — see [global-hooks.md](global-hooks.md)) so it reaches Claude regardless of
which skill (vendored or first-party) is doing the actual editing. This file is the single
source; don't duplicate its content elsewhere.

**Org context:** Houston ISD (274 campuses). Power BI semantic models in Microsoft Fabric,
Direct Lake on medallion architecture (Bronze → Silver → Gold). Primary consumers:
district leadership analyzing student assessments, discipline, enrollment, and campus
performance.

## Dual Synonym Annotations

Two annotations required on every **visible** object (tables, visible columns, measures).
Both must contain identical terms — they serve different AI consumers and neither
substitutes for the other:

| Annotation | Consumer | Format |
|---|---|---|
| `annotation Synonyms` | Copilot Q&A in Report | `term1\|term2\|term3` |
| `annotation SynonymCollection` | FDA + Copilot in Service | `["term1","term2","term3"]` |

**Quantity:** 3–7 per object (target 5).

**Priority order:**
1. Business terms users naturally say ("how many kids", "which school")
2. HISD/TEA acronyms (ISS, OSS, DAEP, SPED, ELL, STAAR)
3. Related concepts for query expansion
4. Legacy field names still referenced

**Do not add synonyms to:** hidden columns, relationships.

## AI-Consumer Compatibility

Which metadata each AI surface actually reads — invest accordingly:

| Metadata | Copilot Q&A in Report | Copilot in Service | FDA DAX Tool |
|---|---|---|---|
| `annotation Synonyms` | ✅ Read | ❌ Not read | ❌ Not read |
| `annotation SynonymCollection` | ❌ Not read | ✅ Read | ✅ Read |
| `///` descriptions | ✅ Read | ✅ Read | ✅ Read |
| AI Instructions (Prep for AI) | ❌ Not read | ✅ Read | ✅ Read |

**Q&A Deprecation Note (December 2026):** Power BI Q&A-in-Report is on Microsoft's
retirement path. Don't over-invest in `Synonyms`-only tuning for that surface alone —
prioritize `SynonymCollection` and AI Instructions, which serve the surfaces staying live.

**Do not invest in** (phantom annotations — never add, not real, no consumer reads them):
`Copilot_QueryHints`, `Copilot_SampleQuestions`, `FDA_TechnicalContext`, `AI_Category`,
`AI_CommonFilters`, `AI_TypicalMeasures`, `AI_RelationshipContext`, or any custom
annotation not present in the source file.

## Relationship Naming

TMDL does **not** support `///` descriptions on relationship objects, and no comparison
skill (including `fabric-skills:semantic-model-authoring`) covers relationship naming at
all — this is a genuine gap-fill, not redundant guidance.

**Pattern:** `{FromTable}_to_{ToTable}_via_{KeyDescription}` — use business terms for
`KeyDescription`, not technical column names.

✅ `Students_to_Campuses_via_HomeCampus`
❌ `Relationship1` / `fk_student_campus_id` / `0d78ca4c-dd11-1fe8`

**Complex relationship semantics** (e.g., "use home campus, not serving campus") belong in
AI Instructions via Prep for AI, not on the relationship object itself.

## Worked Example

```tmdl
/// Student demographics, enrollment status, and grade level. One row per active student.
table Students
    lineageTag: a1b2c3d4-e5f6-7890-abcd-ef1234567890

    /// Full legal name (Last, First Middle). Primary display field for student identification.
    column StudentName
        dataType: string
        lineageTag: c3d4e5f6-a7b8-9012-cdef-345678901234
        sourceColumn: StudentName

        annotation Synonyms = name|student name|pupil name|full name|legal name
        annotation SynonymCollection = ["name","student name","pupil name","full name","legal name"]

    annotation Synonyms = Students|Student Demographics|Learners|Pupils|Kids
    annotation SynonymCollection = ["Students","Student Demographics","Learners","Pupils","Kids"]

relationship Students_to_Campuses_via_HomeCampus
    fromColumn: Students.HomeCampusID
    toColumn: Campuses.CampusID
    crossFilteringBehavior: oneDirection
```

## AI Instructions Template

Free-text instructions that guide the FDA DAX generation tool (**critical constraint**:
the FDA DAX tool ignores agent-level instructions for query generation — all
DAX-influencing guidance must go here, via Prep data for AI → AI Instructions):

```markdown
## Model Overview
[What the model covers, grain of fact tables, key relationships]

## Default Filters
- Always apply CurrentSchoolYearIndicator = TRUE for current-year queries
- Always apply YearToDateIndicator = 1 for fair year-over-year comparisons
- Apply both defaults unless the user explicitly specifies a different time scope

## Key Business Rules
[Critical logic — e.g., "Incident Count measures events, Occurrence Count measures student-incident interactions"]

## Term Definitions
[Domain-specific terms with exact meaning in this model]
- "Campus" = an individual HISD school (not a university campus)
- "Feeder pattern" = a cluster of schools feeding into a single high school
- "SY" = School Year (e.g., SY 2024-25)

## When Asked About
[Query routing patterns with DAX hints]
- **Enrollment by campus**: Use [Student Count] from Fact_CampusEnrollmentSummary filtered by Dim_CampusInformationList
- **District-wide enrollment**: Use [Student Count] from Fact_DistrictEnrollmentSummary

## Example Column Values
[Help the AI match user language to actual column values]
- SchoolCategoryLong: "Elementary School", "Middle School", "High School", "Combined"
- FederalRaceEthnicity: "Hispanic", "African American", "White", "Asian", "Two or More"
```

## HISD Synonym Glossary

Use these synonyms and terms when enhancing HISD models.

| Concept | Synonyms to Include |
|---------|---------------------|
| Campus | school, building, site, location |
| Student | pupil, scholar, learner, child |
| Enrollment | registered, headcount, student count |
| STAAR | state assessment, Texas assessment |
| MAP | NWEA, growth assessment |
| Discipline | behavior, incident, referral |
| ISS | in-school suspension |
| OSS | out-of-school suspension |
| DAEP | disciplinary alternative education program |
| Attendance | present, absent, ADA |
| SPED | special education, special ed |
| ELL | English language learner, ESL, emergent bilingual, EB |
| TEA | Texas Education Agency |
| TEKS | Texas Essential Knowledge and Skills, standards |
| TELPAS | Texas English Language Proficiency Assessment System |
| Feeder Pattern | cluster, feeder, school cluster |
| School Year (SY) | academic year, SY |

## HISD Quality Gate

Beyond whatever generic validation the active editing skill already runs, confirm:

- [ ] Both `Synonyms` and `SynonymCollection` present on every visible table/column/measure,
      identical terms, 3–7 per object
- [ ] No phantom annotations added (see list above)
- [ ] Relationships follow `{FromTable}_to_{ToTable}_via_{KeyDescription}`
- [ ] AI Instructions (if authored) follow the template structure, with default filters
      (`CurrentSchoolYearIndicator`, `YearToDateIndicator`) documented
