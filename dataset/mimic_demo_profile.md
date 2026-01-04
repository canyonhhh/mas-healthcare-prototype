# MIMIC-IV Demo Profile

Data dir: `/home/joris/dl/mimic-iv-clinical-database-demo-2.2`

## Files by Folder

### .

- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/demo_subject_id.csv` (rows: 100, columns: 1)

### hosp

- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/admissions.csv` (rows: 275, columns: 16)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/d_hcpcs.csv` (rows: 89200, columns: 4)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/d_icd_diagnoses.csv` (rows: 109775, columns: 3)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/d_icd_procedures.csv` (rows: 85257, columns: 3)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/d_labitems.csv` (rows: 1622, columns: 4)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/diagnoses_icd.csv` (rows: 4506, columns: 5)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/drgcodes.csv` (rows: 454, columns: 7)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/emar.csv` (rows: 35835, columns: 12)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/emar_detail.csv` (rows: 72018, columns: 33)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/hcpcsevents.csv` (rows: 61, columns: 6)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/labevents.csv` (rows: 107727, columns: 16)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/microbiologyevents.csv` (rows: 2899, columns: 25)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/omr.csv` (rows: 2964, columns: 5)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/patients.csv` (rows: 100, columns: 6)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/pharmacy.csv` (rows: 15306, columns: 27)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/poe.csv` (rows: 45154, columns: 12)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/poe_detail.csv` (rows: 3795, columns: 5)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/prescriptions.csv` (rows: 18087, columns: 21)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/procedures_icd.csv` (rows: 722, columns: 6)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/provider.csv` (rows: 40508, columns: 1)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/services.csv` (rows: 319, columns: 5)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/transfers.csv` (rows: 1190, columns: 7)

### icu

- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/caregiver.csv` (rows: 15468, columns: 1)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/chartevents.csv` (rows: 668862, columns: 11)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/d_items.csv` (rows: 4014, columns: 9)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/datetimeevents.csv` (rows: 15280, columns: 10)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/icustays.csv` (rows: 140, columns: 8)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/ingredientevents.csv` (rows: 25728, columns: 17)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/inputevents.csv` (rows: 20404, columns: 26)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/outputevents.csv` (rows: 9362, columns: 9)
- `/home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/procedureevents.csv` (rows: 1468, columns: 22)

## Key Columns and Time Columns (Sample-based)

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/demo_subject_id.csv

- Primary keys (guess): ['subject_id']
- Join keys (guess): ['subject_id']
- Time columns: []

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/admissions.csv

- Primary keys (guess): ['hadm_id']
- Join keys (guess): ['subject_id', 'hadm_id', 'admit_provider_id']
- Time columns: ['admittime', 'dischtime', 'deathtime', 'edregtime', 'edouttime']
  - admittime: 2111-01-15 14:55:00 to 2201-12-11 12:00:00
  - dischtime: 2111-01-25 15:00:00 to 2201-12-17 13:45:00
  - deathtime: 2111-11-15 17:20:00 to 2185-01-22 14:25:00
  - edregtime: 2116-02-27 15:33:00 to 2201-03-23 12:04:00
  - edouttime: 2116-02-27 22:03:00 to 2201-03-26 14:24:00

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/d_hcpcs.csv

- Primary keys (guess): []
- Join keys (guess): []
- Time columns: []

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/d_icd_diagnoses.csv

- Primary keys (guess): []
- Join keys (guess): []
- Time columns: []

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/d_icd_procedures.csv

- Primary keys (guess): []
- Join keys (guess): []
- Time columns: []

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/d_labitems.csv

- Primary keys (guess): ['itemid']
- Join keys (guess): ['itemid']
- Time columns: []

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/diagnoses_icd.csv

- Primary keys (guess): []
- Join keys (guess): ['subject_id', 'hadm_id']
- Time columns: []

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/drgcodes.csv

- Primary keys (guess): []
- Join keys (guess): ['subject_id', 'hadm_id']
- Time columns: []

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/emar.csv

- Primary keys (guess): ['emar_id']
- Join keys (guess): ['subject_id', 'hadm_id', 'emar_id', 'poe_id', 'pharmacy_id', 'enter_provider_id']
- Time columns: ['charttime', 'scheduletime', 'storetime']
  - charttime: 2113-08-16 18:08:00 to 2196-06-14 23:16:00
  - scheduletime: 2113-08-16 18:08:00 to 2196-06-14 23:16:00
  - storetime: 2113-08-16 18:08:00 to 2196-06-14 23:17:00

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/emar_detail.csv

- Primary keys (guess): ['emar_id']
- Join keys (guess): ['subject_id', 'emar_id', 'pharmacy_id']
- Time columns: []

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/hcpcsevents.csv

- Primary keys (guess): []
- Join keys (guess): ['subject_id', 'hadm_id']
- Time columns: ['chartdate']
  - chartdate: 2113-07-17 00:00:00 to 2201-03-23 00:00:00

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/labevents.csv

- Primary keys (guess): ['labevent_id']
- Join keys (guess): ['labevent_id', 'subject_id', 'hadm_id', 'specimen_id', 'itemid', 'order_provider_id']
- Time columns: ['charttime', 'storetime']
  - charttime: 2110-12-07 03:05:00 to 2201-12-13 03:08:00
  - storetime: 2110-12-07 03:49:00 to 2201-12-13 03:44:00

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/microbiologyevents.csv

- Primary keys (guess): ['microevent_id']
- Join keys (guess): ['microevent_id', 'subject_id', 'hadm_id', 'micro_specimen_id', 'order_provider_id']
- Time columns: ['chartdate', 'charttime', 'storedate', 'storetime']
  - chartdate: 2110-04-14 00:00:00 to 2202-01-10 00:00:00
  - charttime: 2110-04-14 12:37:00 to 2201-11-16 13:04:00
  - storedate: 2110-04-16 00:00:00 to 2202-01-12 00:00:00
  - storetime: 2110-04-16 12:55:00 to 2202-01-12 12:22:00

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/omr.csv

- Primary keys (guess): []
- Join keys (guess): ['subject_id']
- Time columns: ['chartdate']
  - chartdate: 2113-10-16 00:00:00 to 2198-04-22 00:00:00

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/patients.csv

- Primary keys (guess): ['subject_id']
- Join keys (guess): ['subject_id']
- Time columns: []

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/pharmacy.csv

- Primary keys (guess): ['pharmacy_id']
- Join keys (guess): ['subject_id', 'hadm_id', 'pharmacy_id', 'poe_id']
- Time columns: ['starttime', 'stoptime', 'entertime', 'verifiedtime']
  - starttime: 2111-11-15 08:00:00 to 2201-10-31 12:00:00
  - stoptime: 2111-11-15 08:00:00 to 2193-11-26 22:00:00
  - entertime: 2111-11-14 08:32:03 to 2201-10-31 12:02:42
  - verifiedtime: 2111-11-14 08:32:03 to 2193-11-26 16:49:21

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/poe.csv

- Primary keys (guess): ['poe_id']
- Join keys (guess): ['poe_id', 'subject_id', 'hadm_id', 'discontinue_of_poe_id', 'discontinued_by_poe_id', 'order_provider_id']
- Time columns: ['ordertime']
  - ordertime: 2116-12-03 06:17:29 to 2201-03-26 11:05:54

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/poe_detail.csv

- Primary keys (guess): []
- Join keys (guess): ['poe_id', 'subject_id']
- Time columns: []

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/prescriptions.csv

- Primary keys (guess): ['pharmacy_id']
- Join keys (guess): ['subject_id', 'hadm_id', 'pharmacy_id', 'poe_id', 'order_provider_id']
- Time columns: ['starttime', 'stoptime']
  - starttime: 2113-08-27 17:00:00 to 2201-10-31 12:00:00
  - stoptime: 2113-08-30 18:00:00 to 2201-07-11 14:00:00

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/procedures_icd.csv

- Primary keys (guess): []
- Join keys (guess): ['subject_id', 'hadm_id']
- Time columns: ['chartdate']
  - chartdate: 2111-11-15 00:00:00 to 2200-09-17 00:00:00

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/provider.csv

- Primary keys (guess): ['provider_id']
- Join keys (guess): ['provider_id']
- Time columns: []

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/services.csv

- Primary keys (guess): []
- Join keys (guess): ['subject_id', 'hadm_id']
- Time columns: ['transfertime']
  - transfertime: 2110-04-11 15:09:36 to 2201-10-30 12:07:45

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/transfers.csv

- Primary keys (guess): ['transfer_id']
- Join keys (guess): ['subject_id', 'hadm_id', 'transfer_id']
- Time columns: ['intime', 'outtime']
  - intime: 2110-11-30 18:18:45 to 2201-12-13 18:46:17
  - outtime: 2110-12-05 16:48:24 to 2201-12-17 13:48:45

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/caregiver.csv

- Primary keys (guess): ['caregiver_id']
- Join keys (guess): ['caregiver_id']
- Time columns: []

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/chartevents.csv

- Primary keys (guess): []
- Join keys (guess): ['subject_id', 'hadm_id', 'stay_id', 'caregiver_id', 'itemid']
- Time columns: ['charttime', 'storetime']
  - charttime: 2111-11-14 16:00:00 to 2201-07-10 23:00:00
  - storetime: 2111-11-14 16:35:00 to 2201-07-11 00:57:00

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/d_items.csv

- Primary keys (guess): ['itemid']
- Join keys (guess): ['itemid']
- Time columns: []

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/datetimeevents.csv

- Primary keys (guess): []
- Join keys (guess): ['subject_id', 'hadm_id', 'stay_id', 'caregiver_id', 'itemid']
- Time columns: ['charttime', 'storetime']
  - charttime: 2111-11-14 01:00:00 to 2201-12-11 22:12:00
  - storetime: 2111-11-14 05:34:00 to 2201-12-11 22:18:00

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/icustays.csv

- Primary keys (guess): ['stay_id']
- Join keys (guess): ['subject_id', 'hadm_id', 'stay_id']
- Time columns: ['intime', 'outtime']
  - intime: 2110-11-30 17:11:36 to 2201-07-10 10:10:47
  - outtime: 2110-12-05 16:48:24 to 2201-07-11 13:48:02

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/ingredientevents.csv

- Primary keys (guess): []
- Join keys (guess): ['subject_id', 'hadm_id', 'stay_id', 'caregiver_id', 'itemid', 'orderid', 'linkorderid']
- Time columns: ['starttime', 'endtime', 'storetime']
  - starttime: 2111-01-18 20:40:00 to 2201-11-08 08:30:00
  - endtime: 2111-01-18 20:41:00 to 2201-11-08 08:31:00
  - storetime: 2111-01-18 21:41:00 to 2201-11-08 09:01:00

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/inputevents.csv

- Primary keys (guess): []
- Join keys (guess): ['subject_id', 'hadm_id', 'stay_id', 'caregiver_id', 'itemid', 'orderid', 'linkorderid']
- Time columns: ['starttime', 'endtime', 'storetime']
  - starttime: 2111-01-17 18:38:00 to 2196-02-27 22:24:00
  - endtime: 2111-01-17 20:16:00 to 2196-02-27 22:25:00
  - storetime: 2111-01-17 18:41:00 to 2196-02-27 22:24:00

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/outputevents.csv

- Primary keys (guess): []
- Join keys (guess): ['subject_id', 'hadm_id', 'stay_id', 'caregiver_id', 'itemid']
- Time columns: ['charttime', 'storetime']
  - charttime: 2111-01-18 02:00:00 to 2201-11-10 12:00:00
  - storetime: 2111-01-18 04:51:00 to 2201-11-10 12:17:00

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/procedureevents.csv

- Primary keys (guess): ['orderid', 'linkorderid']
- Join keys (guess): ['subject_id', 'hadm_id', 'stay_id', 'caregiver_id', 'itemid', 'orderid', 'linkorderid']
- Time columns: ['starttime', 'endtime', 'storetime']
  - starttime: 2110-12-05 04:37:00 to 2201-10-30 12:30:00
  - endtime: 2110-12-05 04:38:00 to 2201-11-07 13:40:00
  - storetime: 2110-12-05 04:37:00 to 2201-11-07 13:43:00

## Join Sanity Checks (Sample-based)

- patients ↔ admissions: ok
  - keys: ['subject_id']
  - matched: 0
  - left_unmatched_rate: 1.0
  - right_unmatched_rate: 1.0

- admissions ↔ diagnoses_icd: ok
  - keys: ['hadm_id']
  - matched: 0
  - left_unmatched_rate: 1.0
  - right_unmatched_rate: 1.0

- labevents ↔ d_labitems: ok
  - keys: ['itemid']
  - matched: 0
  - left_unmatched_rate: 1.0
  - right_unmatched_rate: 1.0

- icustays ↔ chartevents: ok
  - keys: ['subject_id', 'stay_id']
  - matched: 0
  - left_unmatched_rate: 1.0
  - right_unmatched_rate: 1.0

- icustays ↔ admissions: ok
  - keys: ['hadm_id']
  - matched: 0
  - left_unmatched_rate: 1.0
  - right_unmatched_rate: 1.0

## Example Rows (5 per file)

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/demo_subject_id.csv

| subject_id |
| --- |
| 10000032 |
| 10001217 |
| 10001725 |
| 10002428 |
| 10002495 |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/admissions.csv

| subject_id | hadm_id | admittime | dischtime | deathtime | admission_type | admit_provider_id | admission_location | discharge_location | insurance | language | marital_status | race | edregtime | edouttime | hospital_expire_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10004235 | 24181354 | 2196-02-24 14:38:00 | 2196-03-04 14:02:00 |  | URGENT | P03YMR | TRANSFER FROM HOSPITAL | SKILLED NURSING FACILITY | Medicaid | ENGLISH | SINGLE | BLACK/CAPE VERDEAN | 2196-02-24 12:15:00 | 2196-02-24 17:07:00 | 0 |
| 10009628 | 25926192 | 2153-09-17 17:08:00 | 2153-09-25 13:20:00 |  | URGENT | P41R5N | TRANSFER FROM HOSPITAL | HOME HEALTH CARE | Medicaid | ? | MARRIED | HISPANIC/LATINO - PUERTO RICAN |  |  | 0 |
| 10018081 | 23983182 | 2134-08-18 02:02:00 | 2134-08-23 19:35:00 |  | URGENT | P233F6 | TRANSFER FROM HOSPITAL | SKILLED NURSING FACILITY | Medicare | ENGLISH | MARRIED | WHITE | 2134-08-17 16:24:00 | 2134-08-18 03:15:00 | 0 |
| 10006053 | 22942076 | 2111-11-13 23:39:00 | 2111-11-15 17:20:00 | 2111-11-15 17:20:00 | URGENT | P38TI6 | TRANSFER FROM HOSPITAL | DIED | Medicaid | ENGLISH |  | UNKNOWN |  |  | 1 |
| 10031404 | 21606243 | 2113-08-04 18:46:00 | 2113-08-06 20:57:00 |  | URGENT | P07HDB | TRANSFER FROM HOSPITAL | HOME | Other | ENGLISH | WIDOWED | WHITE |  |  | 0 |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/d_hcpcs.csv

| code | category | long_description | short_description |
| --- | --- | --- | --- |
| TD    |  | Rn | Rn |
| A0428 |  | Ambulance service, basic life support, non-emergency transport, (bls) | Bls |
| V5272 |  | Assistive listening device, tdd | Tdd |
| S2080 |  | Laser-assisted uvulopalatoplasty (laup) | Laup |
| S8037 |  | Magnetic resonance cholangiopancreatography (mrcp) | Mrcp |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/d_icd_diagnoses.csv

| icd_code | icd_version | long_title |
| --- | --- | --- |
| 90 | 9 | Infectious colitis, enteritis, and gastroenteritis |
| 1160 | 9 | Tuberculous pneumonia [any form], unspecified |
| 1186 | 9 | Other specified pulmonary tuberculosis, tubercle bacilli not found by bacteriological or histological examination, but tuberculosis confirmed by other methods [inoculation of animals] |
| 1200 | 9 | Tuberculous pleurisy, unspecified |
| 1236 | 9 | Tuberculous laryngitis, tubercle bacilli not found by bacteriological or histological examination, but tuberculosis confirmed by other methods [inoculation of animals] |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/d_icd_procedures.csv

| icd_code | icd_version | long_title |
| --- | --- | --- |
| 39 | 9 | Other computer assisted surgery |
| 48 | 9 | Insertion of four or more vascular stents |
| 74 | 9 | Hip bearing surface, metal-on-polyethylene |
| 77 | 9 | Hip bearing surface, ceramic-on-polyethylene |
| 126 | 9 | Insertion of catheter(s) into cranial cavity or tissue |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/d_labitems.csv

| itemid | label | fluid | category |
| --- | --- | --- | --- |
| 50808 | Free Calcium | Blood | Blood Gas |
| 50826 | Tidal Volume | Blood | Blood Gas |
| 50813 | Lactate | Blood | Blood Gas |
| 52029 | % Ionized Calcium | Blood | Blood Gas |
| 50801 | Alveolar-arterial Gradient | Blood | Blood Gas |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/diagnoses_icd.csv

| subject_id | hadm_id | seq_num | icd_code | icd_version |
| --- | --- | --- | --- | --- |
| 10035185 | 22580999 | 3 | 4139 | 9 |
| 10035185 | 22580999 | 10 | V707 | 9 |
| 10035185 | 22580999 | 1 | 41401 | 9 |
| 10035185 | 22580999 | 9 | 3899 | 9 |
| 10035185 | 22580999 | 11 | V8532 | 9 |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/drgcodes.csv

| subject_id | hadm_id | drg_type | drg_code | description | drg_severity | drg_mortality |
| --- | --- | --- | --- | --- | --- | --- |
| 10004235 | 22187210 | HCFA | 864 | FEVER |  |  |
| 10026255 | 22059910 | HCFA | 180 | RESPIRATORY NEOPLASMS W MCC |  |  |
| 10032725 | 20611640 | HCFA | 54 | NERVOUS SYSTEM NEOPLASMS W MCC |  |  |
| 10005866 | 21636229 | HCFA | 393 | OTHER DIGESTIVE SYSTEM DIAGNOSES W MCC |  |  |
| 10008454 | 20291550 | HCFA | 956 | LIMB REATTACHMENT, HIP & FEMUR PROC FOR MULTIPLE SIGNIFICANT TRAUMA |  |  |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/emar.csv

| subject_id | hadm_id | emar_id | emar_seq | poe_id | pharmacy_id | enter_provider_id | charttime | medication | event_txt | scheduletime | storetime |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10005909 | 2.01994e+07 | 10005909-74 | 74 | 10005909-97 | 9.61104e+07 |  | 2144-10-31 05:56:00 | Magnesium Sulfate |  | 2144-10-31 05:56:00 | 2144-10-31 05:56:00 |
| 10005909 | 2.01994e+07 | 10005909-79 | 79 | 10005909-97 | 9.61104e+07 |  | 2144-10-31 08:00:00 | Magnesium Sulfate |  | 2144-10-31 08:00:00 | 2144-10-31 08:15:00 |
| 10008287 | 2.21684e+07 | 10008287-32 | 32 | 10008287-58 |  | P26PKF | 2145-09-28 20:15:00 | Potassium Chloride Replacement (Critical Care and Oncology) |  | 2145-09-28 20:15:00 | 2145-09-28 20:38:00 |
| 10010471 | 2.13225e+07 | 10010471-33 | 33 | 10010471-51 | 5.21318e+07 |  | 2155-05-08 21:45:00 | Metoprolol Tartrate |  | 2155-05-08 21:45:00 | 2155-05-08 22:40:00 |
| 10015272 | 2.79935e+07 | 10015272-31 | 31 | 10015272-48 | 8.87589e+07 |  | 2137-06-13 08:36:00 | Metoprolol Tartrate |  | 2137-06-13 08:36:00 | 2137-06-13 08:36:00 |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/emar_detail.csv

| subject_id | emar_id | emar_seq | parent_field_ordinal | administration_type | pharmacy_id | barcode_type | reason_for_no_barcode | complete_dose_not_given | dose_due | dose_due_unit | dose_given | dose_given_unit | will_remainder_of_dose_be_given | product_amount_given | product_unit | product_code | product_description | product_description_other | prior_infusion_rate | infusion_rate | infusion_rate_adjustment | infusion_rate_adjustment_amount | infusion_rate_unit | route | infusion_complete | completion_interval | new_iv_bag_hung | continued_infusion_in_other_location | restart_interval | side | site | non_formulary_visual_verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10039708 | 10039708-1750 | 1750 | 1.1 |  | 8.04008e+07 |  |  |  |  |  | 0.25 | mg |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 10015860 | 10015860-565 | 565 | 1.1 |  | 9.81787e+07 |  |  |  |  |  | ___ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 10005866 | 10005866-571 | 571 | 1.1 |  |  |  |  |  |  |  |  | mL/hr |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 10014354 | 10014354-2295 | 2295 | 1.1 |  | 7.88991e+06 |  |  |  |  |  | 50 | mcg |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 10029291 | 10029291-140 | 140 |  | IV Infusion |  |  |  |  |  | mcg/kg/min |  |  |  |  |  |  |  |  |  |  |  |  |  |  | N |  |  |  | PRN |  |  |  |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/hcpcsevents.csv

| subject_id | hadm_id | chartdate | hcpcs_cd | seq_num | short_description |
| --- | --- | --- | --- | --- | --- |
| 10005348 | 29176490 | 2129-05-22 | 93454 | 1 | Cardiovascular |
| 10005348 | 29176490 | 2129-05-22 | 92921 | 2 | Cardiovascular |
| 10004457 | 21039249 | 2140-09-17 | 92980 | 1 | Cardiovascular |
| 10004457 | 25559382 | 2148-09-14 | 93455 | 1 | Cardiovascular |
| 10039708 | 27504040 | 2142-07-06 | 64415 | 2 | Nervous system |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/labevents.csv

| labevent_id | subject_id | hadm_id | specimen_id | itemid | order_provider_id | charttime | storetime | value | valuenum | valueuom | ref_range_lower | ref_range_upper | flag | priority | comments |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 172061 | 10014354 | 2.96003e+07 | 1808066 | 51277 |  | 2148-08-16 00:00:00 | 2148-08-16 01:30:00 | 15.4 | 15.4 | % | 10.5 | 15.5 |  | ROUTINE |  |
| 172062 | 10014354 | 2.96003e+07 | 1808066 | 51279 |  | 2148-08-16 00:00:00 | 2148-08-16 01:30:00 | 3.35 | 3.35 | m/uL | 4.6 | 6.1 | abnormal | ROUTINE |  |
| 172068 | 10014354 | 2.96003e+07 | 1808066 | 52172 |  | 2148-08-16 00:00:00 | 2148-08-16 01:30:00 | 49.7 | 49.7 | fL | 35.1 | 46.3 | abnormal | ROUTINE |  |
| 172063 | 10014354 | 2.96003e+07 | 1808066 | 51301 |  | 2148-08-16 00:00:00 | 2148-08-16 01:30:00 | 20.3 | 20.3 | K/uL | 4 | 10 | abnormal | ROUTINE |  |
| 172050 | 10014354 | 2.96003e+07 | 1808066 | 51249 |  | 2148-08-16 00:00:00 | 2148-08-16 01:30:00 | 31.1 | 31.1 | g/dL | 32 | 37 | abnormal | ROUTINE |  |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/microbiologyevents.csv

| microevent_id | subject_id | hadm_id | micro_specimen_id | order_provider_id | chartdate | charttime | spec_itemid | spec_type_desc | test_seq | storedate | storetime | test_itemid | test_name | org_itemid | org_name | isolate_num | quantity | ab_itemid | ab_name | dilution_text | dilution_comparison | dilution_value | interpretation | comments |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 36 | 10000032 | 2.57429e+07 | 7814634 |  | 2180-08-06 00:00:00 | 2180-08-06 20:35:00 | 70070 | SWAB | 1 | 2180-08-08 00:00:00 | 2180-08-08 08:03:00 | 90115 | R/O VANCOMYCIN RESISTANT ENTEROCOCCUS |  |  |  |  |  |  |  |  |  |  | No VRE isolated.   |
| 15 | 10000032 | 2.25959e+07 | 5717063 |  | 2180-05-07 00:00:00 | 2180-05-07 00:19:00 | 70070 | SWAB | 1 | 2180-05-09 00:00:00 | 2180-05-09 07:57:00 | 90115 | R/O VANCOMYCIN RESISTANT ENTEROCOCCUS |  |  |  |  |  |  |  |  |  |  | No VRE isolated.   |
| 32 | 10000032 | 2.9079e+07 | 5901894 |  | 2180-07-24 00:00:00 | 2180-07-24 00:55:00 | 70070 | SWAB | 1 | 2180-07-27 00:00:00 | 2180-07-27 11:15:00 | 90115 | R/O VANCOMYCIN RESISTANT ENTEROCOCCUS |  |  |  |  |  |  |  |  |  |  | No VRE isolated.   |
| 7013 | 10020944 | 2.99746e+07 | 4646730 |  | 2131-02-27 00:00:00 | 2131-02-27 17:41:00 | 70070 | SWAB | 1 | 2131-03-03 00:00:00 | 2131-03-03 13:09:00 | 90115 | R/O VANCOMYCIN RESISTANT ENTEROCOCCUS | 80053 | ENTEROCOCCUS SP. | 1 |  | 90015 | VANCOMYCIN | >256 |  |  | R |  |
| 12898 | 10037975 | 2.76179e+07 | 1636367 |  | 2185-01-17 00:00:00 | 2185-01-17 21:32:00 | 70070 | SWAB | 1 | 2185-01-20 00:00:00 | 2185-01-20 07:56:00 | 90115 | R/O VANCOMYCIN RESISTANT ENTEROCOCCUS |  |  |  |  |  |  |  |  |  |  | No VRE isolated.   |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/omr.csv

| subject_id | chartdate | seq_num | result_name | result_value |
| --- | --- | --- | --- | --- |
| 10011398 | 2146-12-01 | 1 | Height (Inches) | 63 |
| 10011398 | 2147-01-22 | 1 | Weight (Lbs) | 127 |
| 10011398 | 2146-12-01 | 1 | Weight (Lbs) | 135 |
| 10011398 | 2147-07-24 | 1 | Weight (Lbs) | 136 |
| 10011398 | 2147-03-26 | 1 | Weight (Lbs) | 136 |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/patients.csv

| subject_id | gender | anchor_age | anchor_year | anchor_year_group | dod |
| --- | --- | --- | --- | --- | --- |
| 10014729 | F | 21 | 2125 | 2011 - 2013 |  |
| 10003400 | F | 72 | 2134 | 2011 - 2013 | 2137-09-02 |
| 10002428 | F | 80 | 2155 | 2011 - 2013 |  |
| 10032725 | F | 38 | 2143 | 2011 - 2013 | 2143-03-30 |
| 10027445 | F | 48 | 2142 | 2011 - 2013 | 2146-02-09 |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/pharmacy.csv

| subject_id | hadm_id | pharmacy_id | poe_id | starttime | stoptime | medication | proc_type | status | entertime | verifiedtime | route | frequency | disp_sched | infusion_type | sliding_scale | lockout_interval | basal_rate | one_hr_max | doses_per_24_hrs | duration | duration_interval | expiration_value | expiration_unit | expirationdate | dispensation | fill_quantity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10027602 | 28166872 | 24340150 |  | 2201-10-30 12:00:00 |  | Midazolam | Miscellaneous Charges | Inactive (Due to a change order) | 2201-10-30 12:32:11 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 10027602 | 28166872 | 14435820 |  | 2201-10-30 12:00:00 |  | Midazolam | Miscellaneous Charges | Inactive (Due to a change order) | 2201-10-30 12:54:34 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 10027602 | 28166872 | 40720238 |  | 2201-10-30 12:00:00 |  | Fentanyl Citrate | Miscellaneous Charges | Inactive (Due to a change order) | 2201-10-30 12:32:11 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 10027602 | 28166872 | 27168639 |  | 2201-10-30 12:00:00 |  | Fentanyl Citrate | Miscellaneous Charges | Inactive (Due to a change order) | 2201-10-30 12:54:34 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 10027602 | 28166872 | 62845687 |  | 2201-10-31 12:00:00 |  | Lorazepam | Miscellaneous Charges | Inactive (Due to a change order) | 2201-10-31 12:02:42 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/poe.csv

| poe_id | poe_seq | subject_id | hadm_id | ordertime | order_type | order_subtype | transaction_type | discontinue_of_poe_id | discontinued_by_poe_id | order_provider_id | order_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10002930-456 | 456 | 10002930 | 20282368 | 2201-03-23 19:14:33 | General Care | Other | New |  |  | P04TDP | Inactive |
| 10002930-454 | 454 | 10002930 | 20282368 | 2201-03-23 19:14:33 | General Care | Vitals/Monitoring | New |  |  | P04TDP | Inactive |
| 10002930-455 | 455 | 10002930 | 20282368 | 2201-03-23 19:14:33 | General Care | Activity | New |  |  | P04TDP | Inactive |
| 10002930-453 | 453 | 10002930 | 20282368 | 2201-03-23 19:14:33 | IV therapy | IV access | New |  |  | P04TDP | Inactive |
| 10002930-452 | 452 | 10002930 | 20282368 | 2201-03-23 19:14:33 | ADT orders | Admit | New |  |  | P04TDP | Inactive |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/poe_detail.csv

| poe_id | poe_seq | subject_id | field_name | field_value |
| --- | --- | --- | --- | --- |
| 10011398-23 | 23 | 10011398 | Admit to | Surgery |
| 10011398-103 | 103 | 10011398 | Transfer to | Surgery |
| 10011398-163 | 163 | 10011398 | Discharge Planning | Finalized |
| 10011398-109 | 109 | 10011398 | Tubes & Drains type | Chest tube |
| 10011398-35 | 35 | 10011398 | Tubes & Drains type | Chest tube |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/prescriptions.csv

| subject_id | hadm_id | pharmacy_id | poe_id | poe_seq | order_provider_id | starttime | stoptime | drug_type | drug | formulary_drug_cd | gsn | ndc | prod_strength | form_rx | dose_val_rx | dose_unit_rx | form_val_disp | form_unit_disp | doses_per_24_hrs | route |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10027602 | 28166872 | 27168639 |  |  |  | 2201-10-30 12:00:00 |  | MAIN | Fentanyl Citrate | FENT2I |  |  |  |  |  |  |  |  |  |  |
| 10027602 | 28166872 | 40720238 |  |  |  | 2201-10-30 12:00:00 |  | MAIN | Fentanyl Citrate | FENT2I |  |  |  |  |  |  |  |  |  |  |
| 10027602 | 28166872 | 62845687 |  |  |  | 2201-10-31 12:00:00 |  | MAIN | Lorazepam | LORA2I |  |  |  |  |  |  |  |  |  |  |
| 10027602 | 28166872 | 24340150 |  |  |  | 2201-10-30 12:00:00 |  | MAIN | Midazolam | MIDA2I |  |  |  |  |  |  |  |  |  |  |
| 10027602 | 28166872 | 14435820 |  |  |  | 2201-10-30 12:00:00 |  | MAIN | Midazolam | MIDA2I |  |  |  |  |  |  |  |  |  |  |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/procedures_icd.csv

| subject_id | hadm_id | seq_num | chartdate | icd_code | icd_version |
| --- | --- | --- | --- | --- | --- |
| 10011398 | 27505812 | 3 | 2146-12-15 | 3961 | 9 |
| 10011398 | 27505812 | 2 | 2146-12-15 | 3615 | 9 |
| 10011398 | 27505812 | 1 | 2146-12-15 | 3614 | 9 |
| 10014729 | 23300884 | 4 | 2125-03-23 | 3897 | 9 |
| 10014729 | 23300884 | 1 | 2125-03-20 | 3403 | 9 |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/provider.csv

| provider_id |
| --- |
| P003F3 |
| P005JG |
| P005MB |
| P00707 |
| P009IB |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/services.csv

| subject_id | hadm_id | transfertime | prev_service | curr_service |
| --- | --- | --- | --- | --- |
| 10001725 | 25563031 | 2110-04-11 15:09:36 |  | GYN |
| 10019003 | 28003918 | 2148-12-21 03:32:53 |  | GYN |
| 10007818 | 22987108 | 2146-06-10 16:38:18 |  | MED |
| 10004235 | 24181354 | 2196-02-24 14:39:31 |  | MED |
| 10026255 | 22059910 | 2201-07-07 18:16:14 |  | MED |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/hosp/transfers.csv

| subject_id | hadm_id | transfer_id | eventtype | careunit | intime | outtime |
| --- | --- | --- | --- | --- | --- | --- |
| 10009049 | 2.29955e+07 | 30030230 | discharge |  | 2174-05-31 14:21:47 |  |
| 10025612 | 2.34037e+07 | 32533329 | discharge |  | 2125-10-03 12:25:27 |  |
| 10020786 | 2.34884e+07 | 37922399 | discharge |  | 2189-06-13 17:25:44 |  |
| 10014078 | 2.58099e+07 | 34694622 | discharge |  | 2166-08-26 14:49:42 |  |
| 10039831 | 2.6925e+07 | 37155928 | discharge |  | 2116-01-02 14:35:02 |  |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/caregiver.csv

| caregiver_id |
| --- |
| 444 |
| 1016 |
| 1135 |
| 1172 |
| 1353 |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/chartevents.csv

| subject_id | hadm_id | stay_id | caregiver_id | charttime | storetime | itemid | value | valuenum | valueuom | warning |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10005817 | 20626031 | 32604416 | 6770 | 2132-12-16 00:00:00 | 2132-12-15 23:45:00 | 225054 | On  |  |  | 0 |
| 10005817 | 20626031 | 32604416 | 6770 | 2132-12-16 00:00:00 | 2132-12-15 23:43:00 | 223769 | 100 | 100 | % | 0 |
| 10005817 | 20626031 | 32604416 | 6770 | 2132-12-16 00:00:00 | 2132-12-15 23:47:00 | 223956 | Atrial demand |  |  | 0 |
| 10005817 | 20626031 | 32604416 | 6770 | 2132-12-16 00:00:00 | 2132-12-15 23:47:00 | 224866 | Yes |  |  | 0 |
| 10005817 | 20626031 | 32604416 | 6770 | 2132-12-16 00:00:00 | 2132-12-15 23:45:00 | 227341 | No | 0 |  | 0 |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/d_items.csv

| itemid | label | abbreviation | linksto | category | unitname | param_type | lownormalvalue | highnormalvalue |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 226228 | Gender | Gender | chartevents | ADT |  | Text |  |  |
| 226545 | Race | Race | chartevents | ADT |  | Text |  |  |
| 229877 | Suction events (CH) | Suction events (CH) | chartevents | ECMO |  | Text |  |  |
| 229875 | Oxygenator visible (CH) | Oxygenator visible (CH) | chartevents | ECMO |  | Text |  |  |
| 229266 | Cannula sites visually inspected (ECMO) | Cannula sites visually inspected (ECMO) | chartevents | ECMO |  | Text |  |  |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/datetimeevents.csv

| subject_id | hadm_id | stay_id | caregiver_id | charttime | storetime | itemid | value | valueuom | warning |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10002428 | 23473524 | 35479615 | 29441 | 2156-05-15 10:50:00 | 2156-05-15 10:50:00 | 225343 | 2156-05-11 00:00:00 | Date | 0 |
| 10002428 | 23473524 | 35479615 | 29441 | 2156-05-15 10:50:00 | 2156-05-15 10:50:00 | 225348 | 2156-05-11 00:00:00 | Date | 0 |
| 10002428 | 23473524 | 35479615 | 29441 | 2156-05-15 10:50:00 | 2156-05-15 10:50:00 | 225345 | 2156-05-14 09:00:00 | Date and Time | 0 |
| 10002428 | 23473524 | 35479615 | 29441 | 2156-05-15 09:00:00 | 2156-05-15 10:51:00 | 224186 | 2156-05-15 09:00:00 | Date and Time | 0 |
| 10002428 | 23473524 | 35479615 | 29441 | 2156-05-15 09:00:00 | 2156-05-15 10:51:00 | 224187 | 2156-05-15 10:50:00 | Date | 0 |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/icustays.csv

| subject_id | hadm_id | stay_id | first_careunit | last_careunit | intime | outtime | los |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10018328 | 23786647 | 31269608 | Neuro Stepdown | Neuro Stepdown | 2154-04-24 23:03:44 | 2154-05-02 15:55:21 | 7.70251 |
| 10020187 | 24104168 | 37509585 | Neuro Surgical Intensive Care Unit (Neuro SICU) | Neuro Stepdown | 2169-01-15 04:56:00 | 2169-01-20 15:47:50 | 5.45266 |
| 10020187 | 26842957 | 32554129 | Neuro Intermediate | Neuro Intermediate | 2170-02-24 18:18:46 | 2170-02-25 15:15:26 | 0.872685 |
| 10012853 | 27882036 | 31338022 | Trauma SICU (TSICU) | Trauma SICU (TSICU) | 2176-11-26 02:34:49 | 2176-11-29 20:58:54 | 3.76672 |
| 10020740 | 25826145 | 32145159 | Trauma SICU (TSICU) | Trauma SICU (TSICU) | 2150-06-03 20:12:32 | 2150-06-04 21:05:58 | 1.03711 |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/ingredientevents.csv

| subject_id | hadm_id | stay_id | caregiver_id | starttime | endtime | storetime | itemid | amount | amountuom | rate | rateuom | orderid | linkorderid | statusdescription | originalamount | originalrate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10005817 | 20626031 | 32604416 | 4793 | 2132-12-17 05:00:00 | 2132-12-17 06:00:00 | 2132-12-17 06:01:00 | 227074 | 50 | ml | 50 | mL/hour | 7330951 | 7330951 | FinishedRunning | 0 | 50 |
| 10005817 | 20626031 | 32604416 | 4793 | 2132-12-17 05:00:00 | 2132-12-17 06:00:00 | 2132-12-17 06:01:00 | 220490 | 50 | ml | 50 | mL/hour | 7330951 | 7330951 | FinishedRunning | 0 | 50 |
| 10005817 | 20626031 | 32604416 | 20310 | 2132-12-17 12:00:00 | 2132-12-17 13:00:00 | 2132-12-17 12:48:00 | 220490 | 250 | ml | 250 | mL/hour | 5334154 | 5334154 | FinishedRunning | 0 | 250 |
| 10005817 | 20626031 | 32604416 | 20310 | 2132-12-17 12:00:00 | 2132-12-17 13:00:00 | 2132-12-17 12:48:00 | 226509 | 250 | ml | 250 | mL/hour | 5334154 | 5334154 | FinishedRunning | 0 | 250 |
| 10005817 | 20626031 | 32604416 | 92805 | 2132-12-15 16:35:00 | 2132-12-15 18:00:00 | 2132-12-15 16:42:00 | 220490 | 38.8527 | ml | 27.4254 | mL/hour | 1386365 | 3042892 | ChangeDose/Rate | 0 | 47.0803 |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/inputevents.csv

| subject_id | hadm_id | stay_id | caregiver_id | starttime | endtime | storetime | itemid | amount | amountuom | rate | rateuom | orderid | linkorderid | ordercategoryname | secondaryordercategoryname | ordercomponenttypedescription | ordercategorydescription | patientweight | totalamount | totalamountuom | isopenbag | continueinnextdept | statusdescription | originalamount | originalrate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10005817 | 20626031 | 32604416 | 4793 | 2132-12-16 19:50:00 | 2132-12-16 19:51:00 | 2132-12-16 19:50:00 | 225798 | 1 | dose |  |  | 3316866 | 3316866 | 08-Antibiotics (IV) | 02-Fluids (Crystalloids) | Main order parameter | Drug Push | 91 | 500 | ml | 0 | 0 | FinishedRunning | 1 | 1 |
| 10005817 | 20626031 | 32604416 | 92805 | 2132-12-15 20:15:00 | 2132-12-15 20:16:00 | 2132-12-15 20:11:00 | 225798 | 1 | dose |  |  | 8515923 | 8515923 | 08-Antibiotics (IV) | 02-Fluids (Crystalloids) | Main order parameter | Drug Push | 91 | 500 | ml | 0 | 0 | FinishedRunning | 1 | 1 |
| 10005817 | 20626031 | 32604416 | 20310 | 2132-12-17 09:15:00 | 2132-12-17 09:16:00 | 2132-12-17 09:28:00 | 225798 | 1 | dose |  |  | 8912103 | 8912103 | 08-Antibiotics (IV) | 02-Fluids (Crystalloids) | Main order parameter | Drug Push | 91 | 500 | ml | 0 | 0 | FinishedRunning | 1 | 1 |
| 10005817 | 20626031 | 32604416 | 79166 | 2132-12-16 09:36:00 | 2132-12-16 09:37:00 | 2132-12-16 09:37:00 | 225798 | 1 | dose |  |  | 4059842 | 4059842 | 08-Antibiotics (IV) | 02-Fluids (Crystalloids) | Main order parameter | Drug Push | 91 | 500 | ml | 0 | 0 | FinishedRunning | 1 | 1 |
| 10005817 | 20626031 | 32604416 | 92805 | 2132-12-15 20:10:00 | 2132-12-15 21:10:00 | 2132-12-15 20:10:00 | 221456 | 2 | grams |  |  | 6323189 | 6323189 | 02-Fluids (Crystalloids) | Additive (Crystalloid) | Additives                                         Ampoule                                            | Continuous IV | 91 | 100 | ml | 0 | 0 | FinishedRunning | 2 | 0.0333333 |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/outputevents.csv

| subject_id | hadm_id | stay_id | caregiver_id | charttime | storetime | itemid | value | valueuom |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10002428 | 23473524 | 35479615 | 29441 | 2156-05-15 18:00:00 | 2156-05-15 17:42:00 | 226583 | 600 | ml |
| 10002428 | 23473524 | 35479615 | 29441 | 2156-05-15 12:00:00 | 2156-05-15 12:08:00 | 226559 | 60 | ml |
| 10002428 | 23473524 | 35479615 | 29441 | 2156-05-15 13:00:00 | 2156-05-15 13:00:00 | 226559 | 45 | ml |
| 10002428 | 23473524 | 35479615 | 29441 | 2156-05-15 08:00:00 | 2156-05-15 08:39:00 | 226559 | 125 | ml |
| 10002428 | 23473524 | 35479615 | 29441 | 2156-05-15 14:00:00 | 2156-05-15 13:56:00 | 226559 | 60 | ml |

### /home/joris/dl/mimic-iv-clinical-database-demo-2.2/icu/procedureevents.csv

| subject_id | hadm_id | stay_id | caregiver_id | starttime | endtime | storetime | itemid | value | valueuom | location | locationcategory | orderid | linkorderid | ordercategoryname | ordercategorydescription | patientweight | isopenbag | continueinnextdept | statusdescription | ORIGINALAMOUNT | ORIGINALRATE |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10027445 | 26275841 | 34499716 | 10712 | 2142-07-31 01:54:00 | 2142-08-02 10:44:00 | 2142-08-02 10:44:00 | 225792 | 3410 | min |  |  | 532221 | 532221 | Ventilation | ContinuousProcess | 103 | 1 | 0 | FinishedRunning | 3410 | 1 |
| 10027445 | 26275841 | 34499716 | 80518 | 2142-07-31 08:18:00 | 2142-08-03 15:10:00 | 2142-08-03 15:23:00 | 224263 | 4732 | min |  |  | 401769 | 401769 | Invasive Lines | ContinuousProcess | 103 | 1 | 0 | FinishedRunning | 4732 | 1 |
| 10027445 | 26275841 | 34499716 | 96407 | 2142-07-31 06:00:00 | 2142-08-03 06:03:00 | 2142-08-03 08:16:00 | 224275 | 4323 | min | Right Antecubital | Peripheral | 9714245 | 9714245 | Peripheral Lines | ContinuousProcess | 103 | 1 | 0 | FinishedRunning | 4323 | 1 |
| 10027445 | 26275841 | 34499716 | 96407 | 2142-07-31 02:00:00 | 2142-08-03 05:57:00 | 2142-08-03 08:15:00 | 224275 | 4557 | min | Left Basilic Lower Arm | Peripheral | 2870557 | 2870557 | Peripheral Lines | ContinuousProcess | 103 | 1 | 0 | FinishedRunning | 4557 | 1 |
| 10027445 | 26275841 | 34499716 |  | 2142-08-03 08:00:00 | 2142-08-03 21:06:00 | 2142-08-03 21:06:00.090 | 224277 | 786 | min |  |  | 4920092 | 4920092 | Peripheral Lines | ContinuousProcess | 103 | 1 | 0 | FinishedRunning | 786 | 1 |
