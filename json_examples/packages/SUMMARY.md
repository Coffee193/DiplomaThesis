# Civilian Baseline Scheduling — KPI Summary

**Scenario:** 100 % civilian vehicle assembly (0 % military mix)  
**Configs:** 3 IMPACT parameter sets × 3 workload sizes = 9 runs  
**Date:** 2026-06-10

---

## Parameters

| Config label | DH | MNA | SR | Description |
|---|---|---|---|---|
| DH2/MNA200/SR3 | 2 | 200 | 3 | Light — fast, shallow look-ahead |
| DH3/MNA200/SR5 | 3 | 200 | 5 | Medium — recommended baseline |
| DH4/MNA400/SR10 | 4 | 400 | 10 | Heavy — wider search, higher quality |

---

## KPI Results

| Package | Config | Makespan (h) | Proc time (h) | Setup (h) | Switches |
|---|---|---:|---:|---:|---:|
| T10_CIV | DH2/MNA200/SR3  | 116.00 | 447.00 | 0.00 | 0 |
| T10_CIV | DH3/MNA200/SR5  | 116.00 | 445.00 | 0.00 | 0 |
| T10_CIV | DH4/MNA400/SR10 | 117.00 | 451.00 | 0.00 | 0 |
| T25_CIV | DH2/MNA200/SR3  | 237.00 | 1125.00 | 0.00 | 0 |
| T25_CIV | DH3/MNA200/SR5  | 237.00 | 1127.00 | 0.00 | 0 |
| T25_CIV | DH4/MNA400/SR10 | 238.00 | 1128.00 | 0.00 | 0 |
| T50_CIV | DH2/MNA200/SR3  | 438.00 | 2250.00 | 0.00 | 0 |
| T50_CIV | DH3/MNA200/SR5  | 437.00 | 2246.00 | 0.00 | 0 |
| T50_CIV | DH4/MNA400/SR10 | 437.00 | 2244.00 | 0.00 | 0 |

**Definitions**

- **Makespan** — wall-clock span from the first to the last non-INIT assignment
- **Proc time** — sum of all task operation durations (pure processing, excludes setup overhead)
- **Setup** — total reconfiguration cost accumulated from setup-code transitions across all resources
- **Switches** — total number of setup-code transitions across all resources

---

## Observations

### Setup cost and switches
All runs show **0 setup cost and 0 switches**. This is expected for a 100 % civilian baseline: every job shares identical setup codes (`KIT_CIV`, `CHS_CIV`, `RUN_CIV`, …), so no reconfiguration is ever triggered. This establishes the zero-penalty reference point against which mixed military scenarios can be compared.

### Makespan scaling
Makespan grows roughly linearly with job count, reflecting the sequential assembly line structure:

| Jobs | Avg makespan (h) | Ratio vs T10 |
|---|---:|---:|
| 10 | 116.3 | 1.0× |
| 25 | 237.3 | 2.04× |
| 50 | 437.3 | 3.76× |

The sub-linear growth at T50 suggests the scheduler is achieving slightly better resource utilisation at higher load.

### Config sensitivity
Differences across DH/MNA/SR configurations are minimal (≤ 1 h per workload). With a homogeneous civilian job mix there is no setup tension to resolve, so the heavier search configurations (DH4/MNA400/SR10) offer no advantage over the light config. Config sensitivity is expected to become significant once military jobs — with longer operation times and different setup codes — are introduced.

---

## Package Structure

```
packages/
  T10_CIV/
    input/   VEHICLE_T10_MIL_000PERCENT.json          (10 civilian vehicles)
    output/  VEHICLE_T10_MIL_000PERCENT_DH2_MNA200_SR3.json
             VEHICLE_T10_MIL_000PERCENT_DH3_MNA200_SR5.json
             VEHICLE_T10_MIL_000PERCENT_DH4_MNA400_SR10.json
  T25_CIV/
    input/   VEHICLE_T25_MIL_000PERCENT.json          (25 civilian vehicles)
    output/  VEHICLE_T25_MIL_000PERCENT_DH2_MNA200_SR3.json
             VEHICLE_T25_MIL_000PERCENT_DH3_MNA200_SR5.json
             VEHICLE_T25_MIL_000PERCENT_DH4_MNA400_SR10.json
  T50_CIV/
    input/   VEHICLE_T50_MIL_000PERCENT.json          (50 civilian vehicles)
    output/  VEHICLE_T50_MIL_000PERCENT_DH2_MNA200_SR3.json
             VEHICLE_T50_MIL_000PERCENT_DH3_MNA200_SR5.json
             VEHICLE_T50_MIL_000PERCENT_DH4_MNA400_SR10.json
```
