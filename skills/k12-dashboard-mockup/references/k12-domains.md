# K–12 Domain Reference — Metrics, Ranges & Grain

## Attendance

| Metric | Definition | Typical Range (HISD) | Status Thresholds |
|---|---|---|---|
| Average Daily Attendance (ADA) | % of enrolled students present daily | 93–97% | ≥95% Good; 90–94.9% Caution; <90% Bad |
| Chronic Absenteeism Rate | % of students missing ≥10% of school days | 8–18% | ≤10% Good; 10–15% Caution; >15% Bad |
| Unexcused Absence Rate | % of total absences that are unexcused | 20–40% of absences | — |
| Tardiness Rate | % of students with ≥3 tardies/month | 5–15% | — |

**Grain**: District → School → Grade → Student  
**Time**: Daily, Weekly rolling, Monthly, YTD, Year-over-year  
**Disaggregation**: Race/Ethnicity, ELL, SPED, Econ. Disadvantaged, Grade Band

---

## Academic Achievement

| Metric | Definition | Typical Range | Status Thresholds |
|---|---|---|---|
| STAAR Approaches Grade Level | % meeting minimum passing standard | 55–80% | ≥70% Good; 55–69% Caution; <55% Bad |
| STAAR Meets Grade Level | % meeting grade-level standard | 35–60% | ≥50% Good; 35–49% Caution; <35% Bad |
| STAAR Masters Grade Level | % demonstrating advanced understanding | 15–30% | ≥25% Good; 15–24% Caution; <15% Bad |
| Interim Assessment Proficiency | % proficient on district benchmarks | 50–75% | District-defined |
| Reading on Grade Level (K–3) | % reading at/above grade level by grade | 45–70% | — |
| Algebra I by 8th Grade | % of 8th graders enrolled/passing Algebra I | 30–60% | — |

**Grain**: District → School → Grade → Subject → Student  
**Time**: Assessment windows (typically 3× per year), STAAR once annually  
**Subjects**: Reading/ELA, Math, Science (5th/8th), Social Studies (8th), EOC (HS)

---

## Behavior & Discipline

| Metric | Definition | Typical Range | Notes |
|---|---|---|---|
| Disciplinary Action Rate | % of students with ≥1 disciplinary action | 5–15% | Disaggregate to check disproportionality |
| In-School Suspension (ISS) Rate | ISS incidents per 100 students | 3–10 | — |
| Out-of-School Suspension (OSS) Rate | OSS incidents per 100 students | 2–8 | Federal reporting required |
| Expulsion Rate | Expulsions per 1,000 students | <1 | IDEA compliance concern |
| Referral-to-Action Ratio | % of referrals resulting in formal action | 40–70% | — |

**Compliance note**: IDEA requires disproportionality analysis for SPED students in discipline. Flag schools where SPED OSS rate > 2× non-SPED rate.

---

## Graduation & College Readiness

| Metric | Definition | Typical Range | Status |
|---|---|---|---|
| 4-Year Graduation Rate | % graduating within 4 years | 80–92% | ≥90% Good; 80–89% Caution; <80% Bad |
| 5-Year Graduation Rate | % graduating within 5 years | 85–95% | — |
| College Readiness Rate | % of graduates meeting TSI readiness in ELA+Math | 40–65% | — |
| AP Participation Rate | % of students taking ≥1 AP course | 30–55% (HS) | — |
| AP Pass Rate | % of AP exams with score ≥3 | 50–70% | — |
| Dual Credit Enrollment | % of HS students enrolled in dual credit | 20–40% | — |
| FAFSA Completion Rate | % of 12th graders completing FAFSA | 60–85% | State target: 80% |

---

## Enrollment & Mobility

| Metric | Definition | Notes |
|---|---|---|
| Enrollment Count | Headcount by school/grade/program | Snapshot date matters |
| Mobility Rate | % of students who transfer in or out mid-year | High mobility = data instability |
| Withdrawal Reason Codes | Reason for departure | Track "unknown" rates |
| Program Participation | % enrolled in SPED, ESL/Bilingual, GT, CTE, etc. | — |

---

## Program Compliance (Federal/State)

### Title I
- Schoolwide vs. Targeted Assistance designation
- Parent involvement activity compliance
- Highly Qualified Teacher requirements

### IDEA (Special Education)
- Child Find obligations
- IEP timelines (annual review within 365 days; evaluation within 60 days)
- Least Restrictive Environment (LRE) percentage targets
- Disproportionality in identification and discipline

### English Learner / Bilingual
- EL identification rate
- Annual LPAC committee review completion
- ACCESS/TELPAS participation rate
- Reclassification rate (monitoring required 2 years post-exit)

### Attendance (State)
- Texas: ADA must be ≥90% for FSP funding
- Schools below 90% ADA trigger intervention and funding adjustments

---

## Teacher Effectiveness

| Metric | Definition | Notes |
|---|---|---|
| T-TESS Average Score | Mean score on Texas Teacher Evaluation | 3.0–4.0 scale |
| Observation Completion Rate | % of required observations completed on time | ≥95% target |
| Teacher Retention Rate | % of teachers returning year over year | 80–90% healthy range |
| Vacancies / Days Unfilled | Critical for planning | Track by subject and school |

---

## SEL / School Climate

| Metric | Definition | Notes |
|---|---|---|
| Survey Response Rate | % of students/staff completing climate survey | ≥70% for validity |
| Belonging Score | Mean survey score on belonging/safety items | Scale varies |
| Bullying Incident Rate | Reported bullying incidents per 100 students | — |
| Counselor Caseload | Students per counselor | ASCA recommends ≤250:1 |

---

## Demographic Groups for Disaggregation

Standard groups for Texas accountability and equity reporting:

| Group | Abbreviation | Notes |
|---|---|---|
| All Students | ALL | Aggregate |
| African American | AA | |
| Hispanic | HIS | Largest group in HISD |
| White | WHI | |
| Asian | ASN | |
| Two or More Races | TWO | |
| English Learners | EL | Current EL only |
| Special Education | SPED | All students with IEPs |
| Economically Disadvantaged | ED | Free/reduced lunch eligible |
| Gifted & Talented | GT | Often excluded from gap analysis |

**Minimum cell size**: Texas suppresses subgroup data below n=5 (display as "n<5").

---

## Realistic Mock Data Ranges (use these for mockups)

```js
const mockSchools = [
  { name: 'Wheatley HS',   type: 'HS', attendance: 91.2, staarELA: 58, staarMath: 52, chronic: 18.4 },
  { name: 'Yates HS',      type: 'HS', attendance: 92.8, staarELA: 61, staarMath: 55, chronic: 16.1 },
  { name: 'Lamar HS',      type: 'HS', attendance: 95.4, staarELA: 74, staarMath: 68, chronic: 9.2  },
  { name: 'Reagan HS',     type: 'HS', attendance: 94.1, staarELA: 70, staarMath: 63, chronic: 11.8 },
  { name: 'Ortiz MS',      type: 'MS', attendance: 94.8, staarELA: 66, staarMath: 60, chronic: 12.3 },
  { name: 'Black MS',      type: 'MS', attendance: 96.2, staarELA: 72, staarMath: 67, chronic: 8.4  },
  { name: 'Stevenson MS',  type: 'MS', attendance: 93.5, staarELA: 63, staarMath: 58, chronic: 14.7 },
  { name: 'Poe ES',        type: 'ES', attendance: 96.8, staarELA: 78, staarMath: 74, chronic: 6.2  },
  { name: 'Helms ES',      type: 'ES', attendance: 95.3, staarELA: 70, staarMath: 69, chronic: 9.8  },
  { name: 'Shearn ES',     type: 'ES', attendance: 93.9, staarELA: 61, staarMath: 58, chronic: 13.6 },
  { name: 'De Zavala ES',  type: 'ES', attendance: 97.1, staarELA: 80, staarMath: 77, chronic: 5.9  },
  { name: 'Burbank ES',    type: 'ES', attendance: 94.4, staarELA: 65, staarMath: 63, chronic: 11.2 },
];

const districtAverages = { attendance: 94.6, staarELA: 68, staarMath: 63, chronic: 11.4 };

const demographicData = [
  { group: 'All Students',         rate: 68 },
  { group: 'Hispanic',             rate: 65 },
  { group: 'African American',     rate: 58 },
  { group: 'White',                rate: 79 },
  { group: 'Asian',                rate: 88 },
  { group: 'Econ. Disadvantaged',  rate: 62 },
  { group: 'English Learners',     rate: 54 },
  { group: 'Special Education',    rate: 47 },
];
```
