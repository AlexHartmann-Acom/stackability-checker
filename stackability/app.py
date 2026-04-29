from __future__ import annotations

from typing import Any
import json

from flask import Flask, render_template_string, request, send_from_directory, url_for

from stackability.factories import sx
from stackability import datatypes as dt


app = Flask(__name__)


SKU_TRAILER_CATALOG: dict[str, dict[str, Any]] = {'1.39.1.3501.90': {'model_name': 'BENAX-3 3500.405x203 Go-Getter',
  'axles': 3,
  'length': 405,
  'width': 203,
  'height': 30},
 '1.38.1.3501.90': {'model_name': 'BENAX-2 3500.405x203 Go-Getter',
  'axles': 2,
  'length': 405,
  'width': 203,
  'height': 30},
 '1.39.1.3501.00': {'model_name': 'BENAX-3 3500.405x203',
  'axles': 3,
  'length': 405,
  'width': 203,
  'height': 30},
 '1.38.1.3501.00': {'model_name': 'BENAX-2 3500.405x203',
  'axles': 2,
  'length': 405,
  'width': 203,
  'height': 30},
 '1.31.1.1106.01': {'model_name': 'KLT-2 2000.305x150 Pro',
  'axles': 2,
  'length': 305,
  'width': 150,
  'height': 30},
 '1.31.1.0906.01': {'model_name': 'KLT-2 1350.305x150 Pro',
  'axles': 2,
  'length': 305,
  'width': 150,
  'height': 30},
 '1.31.1.0306.01': {'model_name': 'KLT-2 750.305x150 Pro',
  'axles': 2,
  'length': 305,
  'width': 150,
  'height': 30},
 '1.31.1.0805.01': {'model_name': 'KLT-1 1350.251x150 Pro',
  'axles': 1,
  'length': 251,
  'width': 150,
  'height': 30},
 '1.10.1.0807.11': {'model_name': 'GTT 2500.301x151 VT3 Ultra Low',
  'axles': 2,
  'length': None,
  'width': None,
  'height': None},
 '1.10.1.1207.11': {'model_name': 'GTB 1500.301x151 VT3 Ultra Low',
  'axles': 1,
  'length': None,
  'width': None,
  'height': None},
 '1.10.1.1008.11': {'model_name': 'GTB 1350.251x151 VT3 Ultra Low',
  'axles': 1,
  'length': None,
  'width': None,
  'height': None},
 '1.31.1.0803.02': {'model_name': 'PLT-1 1350.251x150 Pro + Aktionsplane 150',
  'axles': 1,
  'length': 251,
  'width': 150,
  'height': 30},
 '1.31.1.0204.02': {'model_name': 'PLT-1 750.305x150 Pro + Aktionsplane 165',
  'axles': 1,
  'length': 305,
  'width': 150,
  'height': 30},
 '1.31.1.0203.02': {'model_name': 'PLT-1 750.251x150 Pro + Aktionsplane 150',
  'axles': 1,
  'length': 251,
  'width': 150,
  'height': 30},
 '1.31.1.1107.02': {'model_name': 'PLT-2 2000.330x180 Pro + Aktionsplane 180',
  'axles': 2,
  'length': 330,
  'width': 180,
  'height': 30},
 '1.31.1.1104.02': {'model_name': 'PLT-2 2000.305x150 Pro + Aktionsplane 165',
  'axles': 2,
  'length': 305,
  'width': 150,
  'height': 30},
 '1.31.1.1103.02': {'model_name': 'PLT-2 2000.251x150 Pro + Aktionsplane 150',
  'axles': 2,
  'length': 251,
  'width': 150,
  'height': 30},
 '1.31.1.0904.02': {'model_name': 'PLT-2 1350.305x150 Pro + Aktionsplane 165',
  'axles': 2,
  'length': 305,
  'width': 150,
  'height': 30},
 '1.31.1.0903.02': {'model_name': 'PLT-2 1350.251x150 Pro + Aktionsplane 150',
  'axles': 2,
  'length': 251,
  'width': 150,
  'height': 30},
 '1.31.1.1107.01': {'model_name': 'PLT-2 2000.330x180 Pro',
  'axles': 2,
  'length': 330,
  'width': 180,
  'height': 30},
 '1.31.1.1104.01': {'model_name': 'PLT-2 2000.305x150 Pro',
  'axles': 2,
  'length': 305,
  'width': 150,
  'height': 30},
 '1.31.1.1103.01': {'model_name': 'PLT-2 2000.251x150 Pro',
  'axles': 2,
  'length': 251,
  'width': 150,
  'height': 30},
 '1.31.1.0904.01': {'model_name': 'PLT-2 1350.305x150 Pro',
  'axles': 2,
  'length': 305,
  'width': 150,
  'height': 30},
 '1.31.1.0903.01': {'model_name': 'PLT-2 1350.251x150 Pro',
  'axles': 2,
  'length': 251,
  'width': 150,
  'height': 30},
 '1.31.1.0307.01': {'model_name': 'PLT-2 750.330x180 Pro',
  'axles': 2,
  'length': 330,
  'width': 180,
  'height': 30},
 '1.31.1.0304.01': {'model_name': 'PLT-2 750.305x150 Pro',
  'axles': 2,
  'length': 305,
  'width': 150,
  'height': 30},
 '1.31.1.0303.01': {'model_name': 'PLT-2 750.251x150 Pro',
  'axles': 2,
  'length': 251,
  'width': 150,
  'height': 30},
 '1.31.1.0803.01': {'model_name': 'PLT-1 1350.251x150 Pro',
  'axles': 1,
  'length': 251,
  'width': 150,
  'height': 30},
 '1.31.1.0204.01': {'model_name': 'PLT-1 750.305x150 Pro',
  'axles': 1,
  'length': 305,
  'width': 150,
  'height': 30},
 '1.31.1.0203.01': {'model_name': 'PLT-1 750.251x150 Pro',
  'axles': 1,
  'length': 251,
  'width': 150,
  'height': 30},
 '1.04.1.0803.00': {'model_name': 'ASX 3500.405x203',
  'axles': 2,
  'length': 405,
  'width': 203,
  'height': 30},
 '1.04.1.0703.90': {'model_name': 'ASX 3000.405x203 Go-Getter',
  'axles': 2,
  'length': 405,
  'width': 203,
  'height': 30},
 '1.04.1.0703.00': {'model_name': 'ASX 3000.405x203',
  'axles': 2,
  'length': 405,
  'width': 203,
  'height': 30},
 '1.00.1.0102.00': {'model_name': 'BSX 750.251x130',
  'axles': 1,
  'length': 251,
  'width': 130,
  'height': 35},
 '1.45.1.3504.01': {'model_name': 'Terrax-3 3500.469x195 LK',
  'axles': 3,
  'length': 469,
  'width': 195,
  'height': 27},
 '1.44.1.3504.01': {'model_name': 'Terrax-2 3500.469x195',
  'axles': 2,
  'length': 469,
  'width': 195,
  'height': 27},
 '1.44.1.3503.01': {'model_name': 'Terrax-2 3500.344x165',
  'axles': 2,
  'length': 344,
  'width': 165,
  'height': 27},
 '1.44.1.3003.01': {'model_name': 'Terrax-2 3000.344x165 LK',
  'axles': 2,
  'length': 344,
  'width': 165,
  'height': 27},
 '1.44.1.3003.00': {'model_name': 'Terrax-2 3000.344x165',
  'axles': 2,
  'length': 344,
  'width': 165,
  'height': 27},
 '1.03.1.0803.00': {'model_name': 'KSX 3500.355x178 E',
  'axles': 2,
  'length': 355,
  'width': 178,
  'height': 30},
 '1.03.1.0703.00': {'model_name': 'KSX 3000.355x178 E',
  'axles': 2,
  'length': 355,
  'width': 178,
  'height': 30},
 '1.45.1.3502.90': {'model_name': 'TERRAX-3 3500.394x180 LK Go-Getter',
  'axles': 3,
  'length': 394,
  'width': 180,
  'height': 27},
 '1.44.1.3502.90': {'model_name': 'TERRAX-2 3500.394x180 Go-Getter',
  'axles': 2,
  'length': 394,
  'width': 180,
  'height': 27},
 '1.43.1.3513.90': {'model_name': 'MEDAX-3 3500.611x223 Go-Getter',
  'axles': 3,
  'length': 611,
  'width': 223,
  'height': 30},
 '1.43.1.3503.90': {'model_name': 'MEDAX-3 3500.611x203 Go-Getter',
  'axles': 3,
  'length': 611,
  'width': 203,
  'height': 30},
 '1.42.1.3513.90': {'model_name': 'MEDAX-2 3500.611x223 Go-Getter',
  'axles': 2,
  'length': 611,
  'width': 223,
  'height': 30},
 '1.42.1.3503.90': {'model_name': 'MEDAX-2 3500.611x203 Go-Getter',
  'axles': 2,
  'length': 611,
  'width': 203,
  'height': 30},
 '1.48.1.3502.90': {'model_name': 'CARAX-3 3500.540x207 Go-Getter',
  'axles': 3,
  'length': 540,
  'width': 207,
  'height': 4},
 '1.47.1.3001.90': {'model_name': 'CARAX-2 3000.440x207 Go-Getter',
  'axles': 2,
  'length': 440,
  'width': 207,
  'height': 4},
 '1.01.1.0704.90': {'model_name': 'PSX 3000.405x178 Go-Getter',
  'axles': 2,
  'length': 405,
  'width': 178,
  'height': 30},
 '1.01.1.0703.90': {'model_name': 'PSX 3000.325x178 Go-Getter',
  'axles': 2,
  'length': 325,
  'width': 178,
  'height': 30},
 '1.01.1.0404.90': {'model_name': 'PSX 2500.405x178 Go-Getter',
  'axles': 2,
  'length': 405,
  'width': 178,
  'height': 30},
 '1.01.1.0403.90': {'model_name': 'PSX 2500.325x178 Go-Getter',
  'axles': 2,
  'length': 325,
  'width': 178,
  'height': 30},
 '1.01.1.0604.90': {'model_name': 'PSX 2000.405x178 Go-Getter',
  'axles': 2,
  'length': 405,
  'width': 178,
  'height': 30},
 '1.01.1.0603.90': {'model_name': 'PSX 2000.325x178 Go-Getter',
  'axles': 2,
  'length': 325,
  'width': 178,
  'height': 30},
 '1.02.1.0701.90': {'model_name': 'MSX 3000.405x200 Go-Getter',
  'axles': 2,
  'length': 405,
  'width': 200,
  'height': 4},
 '1.03.1.0701.90': {'model_name': 'KSX 3000.305x178 E Go-Getter',
  'axles': 2,
  'length': 305,
  'width': 178,
  'height': 30},
 '1.00.1.0302.90': {'model_name': 'BSX 1350.251x130 Go-Getter',
  'axles': 1,
  'length': 251,
  'width': 130,
  'height': 35},
 '1.43.1.3503.04': {'model_name': 'MEDAX-3 3500.611x203 + Aktionsplane 210',
  'axles': 3,
  'length': 611,
  'width': 203,
  'height': 30},
 '1.43.1.3502.04': {'model_name': 'MEDAX-3.3500.502x203 + Aktionsplane 210',
  'axles': 3,
  'length': 502,
  'width': 203,
  'height': 30},
 '1.43.1.3501.04': {'model_name': 'MEDAX-3 3500.405x203 + Aktionsplane 210',
  'axles': 3,
  'length': 405,
  'width': 203,
  'height': 30},
 '1.42.1.3530.00': {'model_name': 'MEDAX-2 3500.335x183',
  'axles': 2,
  'length': 335,
  'width': 183,
  'height': 30},
 '1.42.1.3002.04': {'model_name': 'MEDAX-2 3000.502x203 + Aktionsplane 210',
  'axles': 2,
  'length': 502,
  'width': 203,
  'height': 30},
 '1.42.1.3001.04': {'model_name': 'MEDAX-2 3000.405x203 + Aktionsplane 210',
  'axles': 2,
  'length': 405,
  'width': 203,
  'height': 30},
 '1.31.1.0803.00': {'model_name': 'PLTB 1350.251x150',
  'axles': 1,
  'length': 251,
  'width': 150,
  'height': 30},
 '1.31.1.0203.00': {'model_name': 'PLT 750.251x150',
  'axles': 1,
  'length': 251,
  'width': 150,
  'height': 30},
 '1.03.1.0602.01': {'model_name': 'KSX 2000.305x153 H',
  'axles': 2,
  'length': 305,
  'width': 153,
  'height': 30},
 '1.03.1.0402.00': {'model_name': 'KSX 2500.305x153 E',
  'axles': 2,
  'length': 305,
  'width': 153,
  'height': 30},
 '1.30.1.2221.31.202': {'model_name': 'PTS 1400.390x188 mit Toilette',
  'axles': 1,
  'length': 390,
  'width': 188,
  'height': 211},
 '1.47.1.3502.00': {'model_name': 'CARAX-2 3500.540x207',
  'axles': 2,
  'length': 540,
  'width': 207,
  'height': 4},
 '1.42.1.3003.04': {'model_name': 'MEDAX-2 3000.611x203 + Aktionsplane 210',
  'axles': 2,
  'length': 611,
  'width': 203,
  'height': 30},
 '1.42.1.2602.04': {'model_name': 'MEDAX-2 2600.502x203 + Aktionsplane 210',
  'axles': 2,
  'length': 502,
  'width': 203,
  'height': 30},
 '1.42.1.2601.04': {'model_name': 'MEDAX-2 2600.405x203 + Aktionsplane 210',
  'axles': 2,
  'length': 405,
  'width': 203,
  'height': 30},
 '1.48.1.3502.00': {'model_name': 'CARAX-3 3500.540x207',
  'axles': 3,
  'length': 540,
  'width': 207,
  'height': 4},
 '1.48.1.3501.00': {'model_name': 'CARAX-3 3500.440x207',
  'axles': 3,
  'length': 440,
  'width': 207,
  'height': 4},
 '1.47.1.3501.00': {'model_name': 'CARAX-2 3500.440x207',
  'axles': 2,
  'length': 440,
  'width': 207,
  'height': 4},
 '1.47.1.3002.00': {'model_name': 'CARAX-2 3000.540x207',
  'axles': 2,
  'length': 540,
  'width': 207,
  'height': 4},
 '1.47.1.3001.00': {'model_name': 'CARAX-2 3000.440x207',
  'axles': 2,
  'length': 440,
  'width': 207,
  'height': 4},
 '1.01.1.0101.00': {'model_name': 'PSX 750.251x153',
  'axles': 1,
  'length': 251,
  'width': 153,
  'height': 30},
 '1.10.1.0707.08': {'model_name': 'GTT 2000.301x151 + Aktionsplane 180',
  'axles': 2,
  'length': 301,
  'width': 151,
  'height': 30},
 '1.01.1.0602.01': {'model_name': 'PSX 2000.305x153',
  'axles': 2,
  'length': 305,
  'width': 153,
  'height': 30},
 '1.01.1.0602.02': {'model_name': 'PSX 2000.305x153 + Aktionsplane 180',
  'axles': 2,
  'length': 305,
  'width': 153,
  'height': 30},
 '1.10.1.0505.01': {'model_name': 'GTB 1200.251x126 R',
  'axles': 1,
  'length': 251,
  'width': 126,
  'height': 30},
 '1.02.1.0901.00': {'model_name': 'MSX 2700.405x200 Basic',
  'axles': 2,
  'length': 405,
  'width': 200,
  'height': 4},
 '1.20.1.0505.01': {'model_name': 'AMT 1300.340x180 Eco',
  'axles': 1,
  'length': 340,
  'width': 180,
  'height': 18},
 '1.30.1.2221.30.202': {'model_name': 'PTS 1400.390x188',
  'axles': 1,
  'length': 390,
  'width': 188,
  'height': 211},
 '1.31.1.0501.00': {'model_name': 'PLTB 1000.211x132',
  'axles': 1,
  'length': 211,
  'width': 132,
  'height': 30},
 '1.10.1.0101.02': {'model_name': 'GT 500.151x101 HT',
  'axles': 1,
  'length': 151,
  'width': 101,
  'height': 48},
 '1.31.1.0805.00': {'model_name': 'KLTB 1350.251x150',
  'axles': 1,
  'length': 251,
  'width': 150,
  'height': 30},
 '1.10.1.0505.05': {'model_name': 'GTB 1200.251x126 VT3',
  'axles': 1,
  'length': 251,
  'width': 126,
  'height': 153},
 '1.10.1.0203.01': {'model_name': 'GT 750.201x101 R',
  'axles': 1,
  'length': 201,
  'width': 101,
  'height': 30},
 '1.00.1.0101.00': {'model_name': 'BSX 750.205x120',
  'axles': 1,
  'length': 205,
  'width': 120,
  'height': 35},
 '2.39.0.9007.00': {'model_name': '24 Netzhaken (Satz) BSX/LT',
  'axles': 1,
  'length': None,
  'width': None,
  'height': None},
 '1.04.1.0702.01': {'model_name': 'ASX 3000.405x178 + Aktionsplane 180',
  'axles': 2,
  'length': 405,
  'width': 178,
  'height': 30},
 '1.04.1.0701.01': {'model_name': 'ASX 3000.325x178 + Aktionsplane 180',
  'axles': 2,
  'length': 325,
  'width': 178,
  'height': 30},
 '1.04.1.0602.01': {'model_name': 'ASX 2000.405x178 + Aktionsplane 180',
  'axles': 2,
  'length': 405,
  'width': 178,
  'height': 30},
 '1.04.1.0601.01': {'model_name': 'ASX 2000.325x178 + Aktionsplane 180',
  'axles': 2,
  'length': 325,
  'width': 178,
  'height': 30},
 '1.04.1.0402.01': {'model_name': 'ASX 2500.405x178 + Aktionsplane 180',
  'axles': 2,
  'length': 405,
  'width': 178,
  'height': 30},
 '1.10.1.0305.07': {'model_name': 'GTT 750.251x126 + Aktionsplane 150',
  'axles': 2,
  'length': 251,
  'width': 126,
  'height': 30},
 '1.10.1.0102.07': {'model_name': 'GT 500.181x101 + Aktionsplane 120',
  'axles': 1,
  'length': 181,
  'width': 101,
  'height': 30},
 '1.10.1.0205.02': {'model_name': 'GT 750.251x126 HT',
  'axles': 1,
  'length': 251,
  'width': 126,
  'height': 48},
 '1.31.1.0201.00': {'model_name': 'PLT 750.211x132',
  'axles': 1,
  'length': 211,
  'width': 132,
  'height': 30},
 '1.01.1.0402.00': {'model_name': 'PSX 2500.305x153',
  'axles': 2,
  'length': 305,
  'width': 153,
  'height': 30},
 '1.31.1.1106.00': {'model_name': 'KLTT 2000.305x150',
  'axles': 2,
  'length': 305,
  'width': 150,
  'height': 30},
 '1.10.1.0505.04': {'model_name': 'GTB 1200.251x126 VT2',
  'axles': 1,
  'length': 251,
  'width': 126,
  'height': 118},
 '1.01.1.0603.02': {'model_name': 'PSX 2000.325x178 + Aktionsplane 180',
  'axles': 2,
  'length': 325,
  'width': 178,
  'height': 30},
 '1.01.1.0404.02': {'model_name': 'PSX 2500.405x178 + Aktionsplane 180',
  'axles': 2,
  'length': 405,
  'width': 178,
  'height': 30},
 '1.01.1.0403.02': {'model_name': 'PSX 2500.325x178 + Aktionsplane 180',
  'axles': 2,
  'length': 325,
  'width': 178,
  'height': 30},
 '1.01.1.0402.02': {'model_name': 'PSX 2500.305x153 + Aktionsplane 180',
  'axles': 2,
  'length': 305,
  'width': 153,
  'height': 30},
 '1.10.1.0506.07': {'model_name': 'GTB 1200.301x126 + Aktionsplane 150',
  'axles': 1,
  'length': 301,
  'width': 126,
  'height': 30},
 '1.10.1.0205.07': {'model_name': 'GT 750.251x126 + Aktionsplane 150',
  'axles': 1,
  'length': 251,
  'width': 126,
  'height': 30},
 '1.01.1.0604.02': {'model_name': 'PSX 2000.405x178 + Aktionsplane 180',
  'axles': 2,
  'length': 405,
  'width': 178,
  'height': 30},
 '1.46.1.1801.02': {'model_name': 'TERRAX-1 1800.294x150 Basic',
  'axles': 1,
  'length': 294,
  'width': 150,
  'height': 27},
 '1.46.1.1501.02': {'model_name': 'TERRAX-1 1500.294x150 Basic',
  'axles': 1,
  'length': 294,
  'width': 150,
  'height': 27},
 '1.45.1.3502.01': {'model_name': 'TERRAX-3 3500.394x180 LK',
  'axles': 3,
  'length': 394,
  'width': 180,
  'height': 27},
 '1.45.1.3502.00': {'model_name': 'TERRAX-3 3500.394x180',
  'axles': 3,
  'length': 394,
  'width': 180,
  'height': 27},
 '1.44.1.3502.00': {'model_name': 'TERRAX-2 3500.394x180',
  'axles': 2,
  'length': 394,
  'width': 180,
  'height': 27},
 '1.44.1.3501.00': {'model_name': 'TERRAX-2 3500.294x150',
  'axles': 2,
  'length': 294,
  'width': 150,
  'height': 27},
 '1.44.1.3002.01': {'model_name': 'TERRAX-2 3000.394x180 LK',
  'axles': 2,
  'length': 394,
  'width': 180,
  'height': 27},
 '1.44.1.3002.00': {'model_name': 'TERRAX-2 3000.394x180',
  'axles': 2,
  'length': 394,
  'width': 180,
  'height': 27},
 '1.44.1.3001.01': {'model_name': 'TERRAX-2 3000.294x150 LK',
  'axles': 2,
  'length': 294,
  'width': 150,
  'height': 27},
 '1.44.1.3001.00': {'model_name': 'TERRAX-2 3000.294x150',
  'axles': 2,
  'length': 294,
  'width': 150,
  'height': 27},
 '1.44.1.2601.02': {'model_name': 'TERRAX-2 2600.294x150 Basic',
  'axles': 2,
  'length': 294,
  'width': 150,
  'height': 27},
 '1.43.1.3513.00': {'model_name': 'MEDAX-3 3500.611x223',
  'axles': 3,
  'length': 611,
  'width': 223,
  'height': 30},
 '1.43.1.3512.00': {'model_name': 'MEDAX-3 3500.502x223',
  'axles': 3,
  'length': 502,
  'width': 223,
  'height': 30},
 '1.43.1.3511.00': {'model_name': 'MEDAX-3 3500.405x223',
  'axles': 3,
  'length': 405,
  'width': 223,
  'height': 30},
 '1.43.1.3503.00': {'model_name': 'MEDAX-3 3500.611x203',
  'axles': 3,
  'length': 611,
  'width': 203,
  'height': 30},
 '1.43.1.3502.00': {'model_name': 'MEDAX-3 3500.502x203',
  'axles': 3,
  'length': 502,
  'width': 203,
  'height': 30},
 '1.43.1.3501.00': {'model_name': 'MEDAX-3 3500.405x203',
  'axles': 3,
  'length': 405,
  'width': 203,
  'height': 30},
 '1.42.1.3513.00': {'model_name': 'MEDAX-2 3500.611x223',
  'axles': 2,
  'length': 611,
  'width': 223,
  'height': 30},
 '1.42.1.3512.00': {'model_name': 'MEDAX-2 3500.502x223',
  'axles': 2,
  'length': 502,
  'width': 223,
  'height': 30},
 '1.42.1.3511.00': {'model_name': 'MEDAX-2 3500.405x223',
  'axles': 2,
  'length': 405,
  'width': 223,
  'height': 30},
 '1.42.1.3503.00': {'model_name': 'MEDAX-2 3500.611x203',
  'axles': 2,
  'length': 611,
  'width': 203,
  'height': 30},
 '1.42.1.3502.00': {'model_name': 'MEDAX-2 3500.502x203',
  'axles': 2,
  'length': 502,
  'width': 203,
  'height': 30},
 '1.42.1.3501.00': {'model_name': 'MEDAX-2 3500.405x203',
  'axles': 2,
  'length': 405,
  'width': 203,
  'height': 30},
 '1.42.1.3031.00': {'model_name': 'MEDAX-2 3000.405x183',
  'axles': 2,
  'length': 405,
  'width': 183,
  'height': 30},
 '1.42.1.3030.00': {'model_name': 'MEDAX-2 3000.335x183',
  'axles': 2,
  'length': 335,
  'width': 183,
  'height': 30},
 '1.42.1.3013.00': {'model_name': 'MEDAX-2 3000.611x223',
  'axles': 2,
  'length': 611,
  'width': 223,
  'height': 30},
 '1.42.1.3012.00': {'model_name': 'MEDAX-2 3000.502x223',
  'axles': 2,
  'length': 502,
  'width': 223,
  'height': 30},
 '1.42.1.3011.00': {'model_name': 'MEDAX-2 3000.405x223',
  'axles': 2,
  'length': 405,
  'width': 223,
  'height': 30},
 '1.42.1.3003.00': {'model_name': 'MEDAX-2 3000.611x203',
  'axles': 2,
  'length': 611,
  'width': 203,
  'height': 30},
 '1.42.1.3002.00': {'model_name': 'MEDAX-2 3000.502x203',
  'axles': 2,
  'length': 502,
  'width': 203,
  'height': 30},
 '1.42.1.3001.00': {'model_name': 'MEDAX-2 3000.405x203',
  'axles': 2,
  'length': 405,
  'width': 203,
  'height': 30},
 '1.42.1.2631.00': {'model_name': 'MEDAX-2 2600.405x183',
  'axles': 2,
  'length': 405,
  'width': 183,
  'height': 30},
 '1.42.1.2602.00': {'model_name': 'MEDAX-2 2600.502x203',
  'axles': 2,
  'length': 502,
  'width': 203,
  'height': 30},
 '1.42.1.2601.00': {'model_name': 'MEDAX-2 2600.405x203',
  'axles': 2,
  'length': 405,
  'width': 203,
  'height': 30},
 '1.31.1.0906.00': {'model_name': 'KLTT 1350.305x150',
  'axles': 2,
  'length': 305,
  'width': 150,
  'height': 30},
 '1.31.1.0904.00': {'model_name': 'PLTT 1350.305x150',
  'axles': 2,
  'length': 305,
  'width': 150,
  'height': 30},
 '1.31.1.0903.00': {'model_name': 'PLTT 1350.251x150',
  'axles': 2,
  'length': 251,
  'width': 150,
  'height': 30},
 '1.31.1.0502.00': {'model_name': 'PLTB 1000.231x132',
  'axles': 1,
  'length': 231,
  'width': 132,
  'height': 30},
 '1.31.1.0304.00': {'model_name': 'PLTT 750.305x150',
  'axles': 2,
  'length': 305,
  'width': 150,
  'height': 30},
 '1.31.1.0303.00': {'model_name': 'PLTT 750.251x150',
  'axles': 2,
  'length': 251,
  'width': 150,
  'height': 30},
 '1.31.1.0202.00': {'model_name': 'PLT 750.231x132',
  'axles': 1,
  'length': 231,
  'width': 132,
  'height': 30},
 '1.30.1.0602.00.003': {'model_name': 'PTH 2300 Ganador - schwarz metallic',
  'axles': 2,
  'length': 331,
  'width': 166,
  'height': 236},
 '1.30.1.0502.02.003': {'model_name': 'PTH 2000 Privaro - schwarz metallic',
  'axles': 2,
  'length': 331,
  'width': 166,
  'height': 236},
 '1.30.1.0502.01.005': {'model_name': 'PTH 2000 Excelente - weiß',
  'axles': 2,
  'length': 331,
  'width': 166,
  'height': 236},
 '1.30.1.0502.01.003': {'model_name': 'PTH 2000 Excelente - schwarz metallic',
  'axles': 2,
  'length': 331,
  'width': 166,
  'height': 236},
 '1.20.1.0506.01': {'model_name': 'AMT 1300.400x188 Eco',
  'axles': 1,
  'length': 400,
  'width': 188,
  'height': 18},
 '1.20.1.0501.00': {'model_name': 'AMT 1200.340x170',
  'axles': 1,
  'length': 340,
  'width': 170,
  'height': 18},
 '1.20.1.0404.00': {'model_name': 'AMT 3000.507x200',
  'axles': 2,
  'length': 507,
  'width': 200,
  'height': 18},
 '1.20.1.0305.00': {'model_name': 'AMT 2500.340x180',
  'axles': 2,
  'length': 340,
  'width': 180,
  'height': 18},
 '1.20.1.0303.00': {'model_name': 'AMT 2500.440x190',
  'axles': 2,
  'length': 440,
  'width': 190,
  'height': 18},
 '1.20.1.0302.00': {'model_name': 'AMT 2500.407x180',
  'axles': 2,
  'length': 407,
  'width': 180,
  'height': 18},
 '1.20.1.0206.01': {'model_name': 'AMT 2000.400x188 Eco',
  'axles': 2,
  'length': 400,
  'width': 188,
  'height': 18},
 '1.20.1.0106.01': {'model_name': 'AMT 1500.400x188 Eco',
  'axles': 2,
  'length': 400,
  'width': 188,
  'height': 18},
 '1.20.1.0101.00': {'model_name': 'AMT 1500.340x170',
  'axles': 2,
  'length': 340,
  'width': 170,
  'height': 18},
 '1.10.1.0807.06': {'model_name': 'GTT 2500.301x151 VT4',
  'axles': 2,
  'length': 301,
  'width': 151,
  'height': 188},
 '1.10.1.0807.05': {'model_name': 'GTT 2500.301x151 VT3',
  'axles': 2,
  'length': 301,
  'width': 151,
  'height': 153},
 '1.10.1.0707.07': {'model_name': 'GTT 2000.301x151 + Aktionsplane 150',
  'axles': 2,
  'length': 301,
  'width': 151,
  'height': 30},
 '1.10.1.0707.01': {'model_name': 'GTT 2000.301x151 R',
  'axles': 2,
  'length': 301,
  'width': 151,
  'height': 30},
 '1.10.1.0707.00': {'model_name': 'GTT 2000.301x151',
  'axles': 2,
  'length': 301,
  'width': 151,
  'height': 30},
 '1.10.1.0706.07': {'model_name': 'GTT 2000.301x126 + Aktionsplane 150',
  'axles': 2,
  'length': 301,
  'width': 126,
  'height': 30},
 '1.10.1.0706.01': {'model_name': 'GTT 2000.301x126 R',
  'axles': 2,
  'length': 301,
  'width': 126,
  'height': 30},
 '1.10.1.0706.00': {'model_name': 'GTT 2000.301x126',
  'axles': 2,
  'length': 301,
  'width': 126,
  'height': 30},
 '1.10.1.0705.07': {'model_name': 'GTT 2000.251x126 + Aktionsplane 150',
  'axles': 2,
  'length': 251,
  'width': 126,
  'height': 30},
 '1.10.1.0705.01': {'model_name': 'GTT 2000.251x126 R',
  'axles': 2,
  'length': 251,
  'width': 126,
  'height': 30},
 '1.10.1.0705.00': {'model_name': 'GTT 2000.251x126',
  'axles': 2,
  'length': 251,
  'width': 126,
  'height': 30},
 '1.10.1.0606.07': {'model_name': 'GTT 1500.301x126 + Aktionsplane 150',
  'axles': 2,
  'length': 301,
  'width': 126,
  'height': 30},
 '1.10.1.0606.04': {'model_name': 'GTT 1500.301x126 VT2',
  'axles': 2,
  'length': 301,
  'width': 126,
  'height': 118},
 '1.10.1.0606.01': {'model_name': 'GTT 1500.301x126 R',
  'axles': 2,
  'length': 301,
  'width': 126,
  'height': 30},
 '1.10.1.0606.00': {'model_name': 'GTT 1500.301x126',
  'axles': 2,
  'length': 301,
  'width': 126,
  'height': 30},
 '1.10.1.0605.07': {'model_name': 'GTT 1500.251x126 + Aktionsplane 150',
  'axles': 2,
  'length': 251,
  'width': 126,
  'height': 30},
 '1.10.1.0605.01': {'model_name': 'GTT 1500.251x126 R',
  'axles': 2,
  'length': 251,
  'width': 126,
  'height': 30},
 '1.10.1.0605.00': {'model_name': 'GTT 1500.251x126',
  'axles': 2,
  'length': 251,
  'width': 126,
  'height': 30},
 '1.10.1.0506.01': {'model_name': 'GTB 1200.301x126 R',
  'axles': 1,
  'length': 301,
  'width': 126,
  'height': 30},
 '1.10.1.0506.00': {'model_name': 'GTB 1200.301x126',
  'axles': 1,
  'length': 301,
  'width': 126,
  'height': 30},
 '1.10.1.0505.07': {'model_name': 'GTB 1200.251x126 + Aktionsplane 150',
  'axles': 1,
  'length': 251,
  'width': 126,
  'height': 30},
 '1.10.1.0505.03': {'model_name': 'GTB 1200.251x126 VT1',
  'axles': 1,
  'length': 251,
  'width': 126,
  'height': 83},
 '1.10.1.0505.02': {'model_name': 'GTB 1200.251x126 HT',
  'axles': 1,
  'length': 251,
  'width': 126,
  'height': 48},
 '1.10.1.0505.00': {'model_name': 'GTB 1200.251x126',
  'axles': 1,
  'length': 251,
  'width': 126,
  'height': 30},
 '1.10.1.0405.07': {'model_name': 'GTB 750.251x126 + Aktionsplane 150',
  'axles': 1,
  'length': 251,
  'width': 126,
  'height': 30},
 '1.10.1.0405.01': {'model_name': 'GTB 750.251x126 R',
  'axles': 1,
  'length': 251,
  'width': 126,
  'height': 30},
 '1.10.1.0405.00': {'model_name': 'GTB 750.251x126',
  'axles': 1,
  'length': 251,
  'width': 126,
  'height': 30},
 '1.10.1.0404.07': {'model_name': 'GTB 750.211x126 + Aktionsplane 150',
  'axles': 1,
  'length': 211,
  'width': 126,
  'height': 30},
 '1.10.1.0404.04': {'model_name': 'GTB 750.211x126 VT2',
  'axles': 1,
  'length': 211,
  'width': 126,
  'height': 118},
 '1.10.1.0404.03': {'model_name': 'GTB 750.211x126 VT1',
  'axles': 1,
  'length': 211,
  'width': 126,
  'height': 83},
 '1.10.1.0404.02': {'model_name': 'GTB 750.211x126 HT',
  'axles': 1,
  'length': 211,
  'width': 126,
  'height': 48},
 '1.10.1.0404.01': {'model_name': 'GTB 750.211x126 R',
  'axles': 1,
  'length': 211,
  'width': 126,
  'height': 30},
 '1.10.1.0404.00': {'model_name': 'GTB 750.211x126',
  'axles': 1,
  'length': 211,
  'width': 126,
  'height': 30},
 '1.10.1.0305.01': {'model_name': 'GTT 750.251x126 R',
  'axles': 2,
  'length': 251,
  'width': 126,
  'height': 30},
 '1.10.1.0305.00': {'model_name': 'GTT 750.251x126',
  'axles': 2,
  'length': 251,
  'width': 126,
  'height': 30},
 '1.10.1.0205.01': {'model_name': 'GT 750.251x126 R',
  'axles': 1,
  'length': 251,
  'width': 126,
  'height': 30},
 '1.10.1.0205.00': {'model_name': 'GT 750.251x126',
  'axles': 1,
  'length': 251,
  'width': 126,
  'height': 30},
 '1.10.1.0204.07': {'model_name': 'GT 750.211x126 + Aktionsplane 150',
  'axles': 1,
  'length': 211,
  'width': 126,
  'height': 30},
 '1.10.1.0204.02': {'model_name': 'GT 750.211x126 HT',
  'axles': 1,
  'length': 211,
  'width': 126,
  'height': 48},
 '1.10.1.0204.01': {'model_name': 'GT 750.211x126 R',
  'axles': 1,
  'length': 211,
  'width': 126,
  'height': 30},
 '1.10.1.0204.00': {'model_name': 'GT 750.211x126',
  'axles': 1,
  'length': 211,
  'width': 126,
  'height': 30},
 '1.10.1.0203.03': {'model_name': 'GT 750.201x101 VT1',
  'axles': 1,
  'length': 201,
  'width': 101,
  'height': 83},
 '1.10.1.0203.02': {'model_name': 'GT 750.201x101 HT',
  'axles': 1,
  'length': 201,
  'width': 101,
  'height': 48},
 '1.10.1.0203.00': {'model_name': 'GT 750.201x101',
  'axles': 1,
  'length': 201,
  'width': 101,
  'height': 30},
 '1.10.1.0102.03': {'model_name': 'GT 500.181x101 VT1',
  'axles': 1,
  'length': 181,
  'width': 101,
  'height': 83},
 '1.10.1.0102.02': {'model_name': 'GT 500.181x101 HT',
  'axles': 1,
  'length': 181,
  'width': 101,
  'height': 48},
 '1.10.1.0102.01': {'model_name': 'GT 500.181x101 R',
  'axles': 1,
  'length': 181,
  'width': 101,
  'height': 30},
 '1.10.1.0102.00': {'model_name': 'GT 500.181x101',
  'axles': 1,
  'length': 181,
  'width': 101,
  'height': 30},
 '1.10.1.0101.01': {'model_name': 'GT 500.151x101 R',
  'axles': 1,
  'length': 151,
  'width': 101,
  'height': 30},
 '1.04.1.0702.00': {'model_name': 'ASX 3000.405x178',
  'axles': 2,
  'length': 405,
  'width': 178,
  'height': 30},
 '1.04.1.0701.00': {'model_name': 'ASX 3000.325x178',
  'axles': 2,
  'length': 325,
  'width': 178,
  'height': 30},
 '1.04.1.0602.00': {'model_name': 'ASX 2000.405x178',
  'axles': 2,
  'length': 405,
  'width': 178,
  'height': 30},
 '1.04.1.0601.00': {'model_name': 'ASX 2000.325x178',
  'axles': 2,
  'length': 325,
  'width': 178,
  'height': 30},
 '1.04.1.0402.00': {'model_name': 'ASX 2500.405x178',
  'axles': 2,
  'length': 405,
  'width': 178,
  'height': 30},
 '1.04.1.0401.00': {'model_name': 'ASX 2500.325x178',
  'axles': 2,
  'length': 325,
  'width': 178,
  'height': 30},
 '1.03.1.0801.00': {'model_name': 'KSX 3500.305x178 E',
  'axles': 2,
  'length': 305,
  'width': 178,
  'height': 30},
 '1.03.1.0701.00': {'model_name': 'KSX 3000.305x178 E',
  'axles': 2,
  'length': 305,
  'width': 178,
  'height': 30},
 '1.03.1.0401.01': {'model_name': 'KSX 2500.305x178 H',
  'axles': 2,
  'length': 305,
  'width': 178,
  'height': 30},
 '1.03.1.0401.00': {'model_name': 'KSX 2500.305x178 E',
  'axles': 2,
  'length': 305,
  'width': 178,
  'height': 30},
 '1.02.1.0801.00': {'model_name': 'MSX 3500.405x200',
  'axles': 2,
  'length': 405,
  'width': 200,
  'height': 4},
 '1.02.1.0701.00': {'model_name': 'MSX 3000.405x200',
  'axles': 2,
  'length': 405,
  'width': 200,
  'height': 4},
 '1.01.1.0704.02': {'model_name': 'PSX 3000.405x178 + Aktionsplane 180',
  'axles': 2,
  'length': 405,
  'width': 178,
  'height': 30},
 '1.01.1.0704.00': {'model_name': 'PSX 3000.405x178',
  'axles': 2,
  'length': 405,
  'width': 178,
  'height': 30},
 '1.01.1.0703.02': {'model_name': 'PSX 3000.325x178 + Aktionsplane 180',
  'axles': 2,
  'length': 325,
  'width': 178,
  'height': 30},
 '1.42.1.2630.00': {'model_name': 'MEDAX-2 2600.335x183',
  'axles': 2,
  'length': 335,
  'width': 183,
  'height': 30},
 '1.01.1.0703.00': {'model_name': 'PSX 3000.325x178',
  'axles': 2,
  'length': 325,
  'width': 178,
  'height': 30},
 '1.01.1.0604.01': {'model_name': 'PSX 2000.405x178',
  'axles': 2,
  'length': 405,
  'width': 178,
  'height': 30},
 '1.01.1.0603.01': {'model_name': 'PSX 2000.325x178',
  'axles': 2,
  'length': 325,
  'width': 178,
  'height': 30},
 '1.01.1.0404.00': {'model_name': 'PSX 2500.405x178',
  'axles': 2,
  'length': 405,
  'width': 178,
  'height': 30},
 '1.01.1.0403.00': {'model_name': 'PSX 2500.325x178',
  'axles': 2,
  'length': 325,
  'width': 178,
  'height': 30},
 '1.01.1.0301.00': {'model_name': 'PSX 1350.251x153',
  'axles': 1,
  'length': 251,
  'width': 153,
  'height': 30},
 '1.00.1.0503.00': {'model_name': 'BSX 1500.301x150',
  'axles': 1,
  'length': 301,
  'width': 150,
  'height': 35},
 '1.00.1.0403.00': {'model_name': 'BSX 2500.301x150',
  'axles': 2,
  'length': 301,
  'width': 150,
  'height': 35},
 '1.00.1.0402.00': {'model_name': 'BSX 2500.251x130',
  'axles': 2,
  'length': 251,
  'width': 130,
  'height': 35},
 '1.00.1.0302.00': {'model_name': 'BSX 1350.251x130',
  'axles': 1,
  'length': 251,
  'width': 130,
  'height': 35},
 '1.00.1.0301.00': {'model_name': 'BSX 1350.205x120',
  'axles': 1,
  'length': 205,
  'width': 120,
  'height': 35},
 '1.60.1.4103.21': {'model_name': 'Hochplane mit Gestell ASX, Benax, Medax 405x203x210',
  'axles': 1,
  'length': None,
  'width': None,
  'height': None},
 '1.10.1.0101.00': {'model_name': 'GT 500.151x101',
  'axles': 1,
  'length': 151,
  'width': 101,
  'height': 30},
 '1.04.1.0401.01': {'model_name': 'ASX 2500.325x178 + Aktionsplane 180',
  'axles': 2,
  'length': 325,
  'width': 178,
  'height': 30},
 '1.10.1.0203.07': {'model_name': 'GT 750.201x101 + Aktionsplane 120',
  'axles': 1,
  'length': 201,
  'width': 101,
  'height': 30},
 '1.10.1.0101.07': {'model_name': 'GT 500.151x101 + Aktionsplane 120',
  'axles': 1,
  'length': 151,
  'width': 101,
  'height': 30}}


@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("stackability/static", filename)


HTML = """
<!doctype html>
<html lang="de">
<head>
    <meta charset="utf-8">
    <title>Stapellogik Anhänger</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        :root {
            --anssems-red: #c4001a;
            --anssems-red-dark: #a80016;
            --bg: #f5f5f5;
            --text: #222;
            --muted: #666;
            --border: #e6e6e6;
        }

        body {
            font-family: Arial, sans-serif;
            background: var(--bg);
            margin: 0;
            padding: 24px;
            color: var(--text);
        }

        .container {
            max-width: 1250px;
            margin: 0 auto;
        }

        .header {
            display: flex;
            align-items: center;
            gap: 22px;
            margin-bottom: 24px;
        }

        .logo {
            height: 52px;
            display: block;
        }

        h1 {
            margin: 0;
            color: var(--anssems-red);
        }

        .subtitle {
            color: var(--muted);
            margin-top: 4px;
        }

        .card {
            background: white;
            border-radius: 14px;
            padding: 22px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.07);
            margin-bottom: 20px;
        }

        .sku-add-row {
            display: grid;
            grid-template-columns: 1.5fr auto;
            gap: 10px;
            align-items: end;
            margin-bottom: 18px;
            padding-bottom: 18px;
            border-bottom: 2px solid var(--border);
        }

        .trailer-row {
            display: grid;
            grid-template-columns: 1.4fr 1fr 1fr 1fr 1fr 130px auto;
            gap: 10px;
            align-items: end;
            margin-bottom: 12px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border);
        }

        label {
            display: block;
            font-size: 12px;
            font-weight: bold;
            color: #444;
            margin-bottom: 4px;
        }

        input {
            width: 100%;
            box-sizing: border-box;
            padding: 9px 10px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 14px;
        }

        button {
            border: 0;
            border-radius: 8px;
            padding: 10px 14px;
            font-weight: bold;
            cursor: pointer;
            white-space: nowrap;
        }

        .btn-primary {
            background: var(--anssems-red);
            color: white;
        }

        .btn-primary:hover {
            background: var(--anssems-red-dark);
        }

        .btn-secondary {
            background: #fff0f0;
            color: var(--anssems-red);
        }

        .btn-danger {
            background: #ffe5e5;
            color: var(--anssems-red);
        }

        .btn-muted {
            background: #f0f0f0;
            color: #555;
        }

        .actions,
        .solution-nav {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            align-items: center;
            margin-top: 16px;
        }

        .quantity-control {
            display: grid;
            grid-template-columns: 36px 1fr 36px;
            gap: 6px;
        }

        .quantity-display {
            text-align: center;
            font-weight: bold;
            padding: 9px;
            background: #fafafa;
            border-radius: 8px;
            border: 1px solid #ddd;
        }

        .result-error {
            border-left: 6px solid var(--anssems-red);
            background: #fff5f5;
        }

        .hint {
            color: var(--muted);
            font-size: 13px;
            margin-bottom: 0;
        }

        .summary {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 8px;
        }

        .summary-pill {
            background: #fff0f0;
            color: var(--anssems-red);
            border-radius: 999px;
            padding: 7px 12px;
            font-size: 13px;
            font-weight: bold;
        }

        .solution-counter {
            font-weight: bold;
            color: #444;
        }

        .lorry-wrap {
            margin-top: 18px;
            overflow-x: auto;
            padding-bottom: 8px;
        }

        .lorry-scene {
            min-width: 900px;
            padding: 20px 10px 6px 10px;
        }

        .lorry-load-area {
            display: grid;
            gap: 14px;
            align-items: end;
            min-height: 470px;
            padding: 0 32px;
        }

        .lorry-position {
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            align-items: center;
            min-height: 435px;
            position: relative;
        }

        .position-label {
            font-size: 12px;
            color: #777;
            margin-bottom: 8px;
        }

        .stack-pile {
            width: 100%;
            display: flex;
            flex-direction: column-reverse;
            align-items: center;
            justify-content: flex-start;
        }

        .trailer-block {
            width: var(--box-width);
            height: var(--box-height);
            min-height: 62px;
            max-width: 100%;
            background: linear-gradient(180deg, #d5162e 0%, #b80018 100%);
            color: white;
            border: 2px solid #8f0013;
            border-radius: 10px 10px 6px 6px;
            box-shadow: 0 4px 9px rgba(0,0,0,0.18);
            margin-top: -1px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
            text-align: center;
            overflow: visible;
            box-sizing: border-box;
            padding: 8px 34px 18px 34px;
        }

        .trailer-block.has-contained {
            height: auto !important;
            min-height: 138px;
            padding-top: 12px;
            justify-content: flex-start;
        }

        .trailer-block::before,
        .trailer-block::after {
            content: "";
            position: absolute;
            bottom: 6px;
            width: 15px;
            height: 15px;
            border-radius: 50%;
            background: #333;
            border: 2px solid #111;
        }

        .trailer-block::before {
            left: 14px;
        }

        .trailer-block::after {
            right: 14px;
        }

        .trailer-model {
            font-size: 13px;
            font-weight: bold;
            line-height: 1.15;
            padding: 0 4px;
            max-width: 100%;
            overflow-wrap: anywhere;
        }

        .trailer-dims {
            margin-top: 4px;
            font-size: 11px;
            opacity: 0.95;
            white-space: nowrap;
        }

        .trailer-block.has-contained > .trailer-model {
            font-size: 13px;
            margin-bottom: 2px;
        }

        .trailer-block.has-contained > .trailer-dims {
            font-size: 10px;
            margin-bottom: 8px;
        }

        .contained-trailer {
            position: relative;
            left: auto;
            bottom: auto;
            transform: none;
            width: 74%;
            z-index: 5;
            pointer-events: none;
            margin-top: 6px;
        }

        .contained-trailer-block {
            width: 100% !important;
            height: auto !important;
            min-height: 62px;
            background: linear-gradient(180deg, #ffffff 0%, #eeeeee 100%);
            color: #333;
            border: 2px solid #555;
            box-shadow: 0 2px 8px rgba(0,0,0,0.28);
            padding: 8px 26px 16px 26px;
        }

        .contained-trailer-block::before,
        .contained-trailer-block::after {
            width: 10px;
            height: 10px;
            bottom: 4px;
            border-width: 1px;
        }

        .contained-trailer-block::before {
            left: 10px;
        }

        .contained-trailer-block::after {
            right: 10px;
        }

        .contained-trailer-block .trailer-model {
            font-size: 12px;
            color: #333;
        }

        .contained-trailer-block .trailer-dims {
            display: block;
            font-size: 10px;
            color: #555;
            opacity: 1;
        }

        .contained-label {
            display: inline-block;
            background: #333;
            color: white;
            font-size: 10px;
            line-height: 1;
            padding: 3px 7px;
            border-radius: 999px;
            white-space: nowrap;
            margin-bottom: 4px;
        }

        .flatbed {
            height: 34px;
            background: linear-gradient(180deg, #3a3a3a, #222);
            border-radius: 6px;
            margin: 0 22px;
            position: relative;
            box-shadow: 0 5px 14px rgba(0,0,0,0.25);
        }

        .flatbed::before {
            content: "";
            position: absolute;
            left: -28px;
            bottom: 0;
            width: 36px;
            height: 42px;
            background: #2c2c2c;
            border-radius: 8px 0 0 8px;
        }

        .wheel {
            position: absolute;
            bottom: -20px;
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: #111;
            border: 5px solid #444;
            box-sizing: border-box;
        }

        .wheel.w1 { left: 8%; }
        .wheel.w2 { left: 16%; }
        .wheel.w3 { right: 16%; }
        .wheel.w4 { right: 8%; }

        .lorry-caption {
            text-align: center;
            color: #555;
            margin-top: 28px;
            font-size: 13px;
        }

        @media (max-width: 950px) {
            body {
                padding: 16px;
            }

            .trailer-row,
            .sku-add-row {
                grid-template-columns: 1fr 1fr;
            }

            .header {
                flex-direction: column;
                align-items: flex-start;
            }

            .logo {
                height: 44px;
            }
        }
    </style>
</head>

<body>
<div class="container">

    <div class="header">
        <img src="{{ url_for('static_files', filename='anssems-logo.svg') }}" class="logo">
        <div>
            <h1>Anhänger-Stapelprüfung</h1>
            <div class="subtitle">Modelle eintragen, Stückzahlen anpassen und Stapelplan auf dem LKW-Tieflader visualisieren</div>
        </div>
    </div>

    <form method="post" class="card" id="stackForm">

        <div class="sku-add-row">
            <div>
                <label>Artikelnummer / SKU</label>
                <input id="skuInput" placeholder="z. B. 1.00.1.0102.00" onkeydown="handleSkuKeydown(event)">
            </div>

            <button type="button" class="btn-secondary" onclick="addTrailerBySku()">+ Per SKU hinzufügen</button>
        </div>

        <div id="trailerRows"></div>

        <div class="actions">
            <button type="button" class="btn-secondary" onclick="addTrailer()">+ Modell manuell hinzufügen</button>
            <button type="button" class="btn-muted" onclick="addExample()">Beispiel laden</button>
            <button type="button" class="btn-danger" onclick="clearTrailers()">Leeren</button>
            <button type="submit" class="btn-primary">Stapelplan berechnen</button>
        </div>

        <p class="hint">Maße bitte in cm eingeben. Die Visualisierung skaliert Länge und Höhe relativ zu den eingegebenen Anhängern. Eingeladene Anhänger werden hell innerhalb des äußeren Anhängers angezeigt.</p>

        <input type="hidden" name="trailers_json" id="trailersJson">
    </form>

    {% if error %}
        <div class="card result-error">
            <h2>Nicht stapelbar / Fehler</h2>
            <p>{{ error }}</p>
        </div>
    {% endif %}

    {% if stack_solutions %}
        <div class="card">
            <h2>Stapelplan auf LKW-Tieflader</h2>

            <div class="summary">
                <div class="summary-pill"><span id="stackCount">{{ stack_count }}</span> Stapelpositionen</div>
                <div class="summary-pill"><span id="trailerCount">{{ trailer_count }}</span> Anhänger</div>
                <div class="summary-pill">{{ solution_count }} mögliche Lösung{% if solution_count != 1 %}en{% endif %}</div>
            </div>

            {% if solution_count > 1 %}
                <div class="solution-nav">
                    <button type="button" class="btn-muted" onclick="previousSolution()">← Vorherige Lösung</button>
                    <span class="solution-counter" id="solutionCounter"></span>
                    <button type="button" class="btn-secondary" onclick="nextSolution()">Nächste Lösung →</button>
                </div>
            {% endif %}

            <div class="lorry-wrap">
                <div class="lorry-scene">
                    <div class="lorry-load-area" id="lorryLoadArea"></div>

                    <div class="flatbed">
                        <div class="wheel w1"></div>
                        <div class="wheel w2"></div>
                        <div class="wheel w3"></div>
                        <div class="wheel w4"></div>
                    </div>

                    <div class="lorry-caption">
                        Schematische Darstellung: Länge und Höhe der Boxen sind relativ skaliert, nicht maßstabsgetreu.
                    </div>
                </div>
            </div>
        </div>
    {% endif %}
</div>

<script>
let trailers = {{ trailers | tojson }};
let stackSolutions = {{ stack_solutions | tojson }};
let skuCatalog = {{ sku_catalog | tojson }};
let currentSolutionIndex = 0;

function normalizeSku(value) {
    return String(value || '').trim().toUpperCase();
}

function escapeHtml(value) {
    return String(value ?? '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#039;');
}

function sameTrailerDefinition(a, b) {
    return normalizeSku(a.sku) === normalizeSku(b.sku)
        || (
            String(a.model_name || '') === String(b.model_name || '')
            && Number(a.length) === Number(b.length)
            && Number(a.height) === Number(b.height)
            && Number(a.width) === Number(b.width)
            && Number(a.axles || 2) === Number(b.axles || 2)
        );
}

function addTrailerBySku() {
    const input = document.getElementById('skuInput');
    const sku = normalizeSku(input.value);

    if (!sku) {
        alert('Bitte eine SKU eingeben.');
        return;
    }

    const catalogItem = skuCatalog[sku];

    if (!catalogItem) {
        alert(`SKU nicht gefunden: ${sku}`);
        return;
    }

    const newTrailer = {
        sku: sku,
        model_name: catalogItem.model_name,
        length: catalogItem.length,
        height: catalogItem.height,
        width: catalogItem.width,
        axles: catalogItem.axles || 1,
        quantity: 1
    };

    const existingIndex = trailers.findIndex(t => sameTrailerDefinition(t, newTrailer));

    if (existingIndex >= 0) {
        trailers[existingIndex].quantity = Number(trailers[existingIndex].quantity || 1) + 1;
    } else {
        trailers.push(newTrailer);
    }

    input.value = '';
    renderTrailers();
}

function handleSkuKeydown(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        addTrailerBySku();
    }
}

function renderTrailers() {
    const container = document.getElementById('trailerRows');

    container.innerHTML = trailers.map((t, i) => `
        <div class="trailer-row">
            <div>
                <label>Modellname${t.sku ? ` · SKU ${escapeHtml(t.sku)}` : ''}</label>
                <input value="${escapeHtml(t.model_name || '')}" onchange="trailers[${i}].model_name=this.value">
            </div>

            <div>
                <label>Länge</label>
                <input type="number" value="${escapeHtml(t.length || '')}" onchange="trailers[${i}].length=this.value">
            </div>

            <div>
                <label>Höhe</label>
                <input type="number" value="${escapeHtml(t.height || '')}" onchange="trailers[${i}].height=this.value">
            </div>

            <div>
                <label>Breite</label>
                <input type="number" value="${escapeHtml(t.width || '')}" onchange="trailers[${i}].width=this.value">
            </div>

            <div>
                <label>Achsen</label>
                <input type="number" value="${escapeHtml(t.axles || 2)}" onchange="trailers[${i}].axles=this.value">
            </div>

            <div>
                <label>Stückzahl</label>
                <div class="quantity-control">
                    <button type="button" class="btn-muted" onclick="decreaseQuantity(${i})">−</button>
                    <div class="quantity-display">${t.quantity || 1}</div>
                    <button type="button" class="btn-muted" onclick="increaseQuantity(${i})">+</button>
                </div>
            </div>

            <button type="button" class="btn-danger" onclick="removeTrailer(${i})">Entfernen</button>
        </div>
    `).join('');

    document.getElementById('trailersJson').value = JSON.stringify(trailers);
}

function increaseQuantity(i) {
    trailers[i].quantity = Number(trailers[i].quantity || 1) + 1;
    renderTrailers();
}

function decreaseQuantity(i) {
    const q = Number(trailers[i].quantity || 1);

    if (q <= 1) {
        trailers.splice(i, 1);
    } else {
        trailers[i].quantity = q - 1;
    }

    if (trailers.length === 0) {
        addTrailer();
    } else {
        renderTrailers();
    }
}

function removeTrailer(i) {
    trailers.splice(i, 1);

    if (trailers.length === 0) {
        addTrailer();
    } else {
        renderTrailers();
    }
}

function addTrailer() {
    trailers.push({
        sku: '',
        model_name: '',
        length: '',
        height: '',
        width: '',
        axles: 2,
        quantity: 1
    });

    renderTrailers();
}

function clearTrailers() {
    trailers = [];
    addTrailer();
}

function addExample() {
    trailers = [
        {sku: '1.10.1.0807.05', model_name:'GTT 2500.301x151 VT3', length:301, height:153, width:151, axles:2, quantity:1},
        {sku: '1.10.1.0101.02', model_name:'GT 500.151x101 HT', length:151, height:48, width:101, axles:1, quantity:1},
        {sku: '1.00.1.0101.00', model_name:'BSX 750.205x120', length:205, height:35, width:120, axles:1, quantity:2}
    ];

    renderTrailers();
}

function renderTrailerBlock(trailer, contained = false) {
    const containedClass = contained ? ' contained-trailer-block' : '';
    const hasContainedClass = trailer.contained_trailer && !contained ? ' has-contained' : '';

    return `
        <div class="trailer-block${containedClass}${hasContainedClass}"
             style="--box-width: ${trailer.visual_width}%; --box-height: ${trailer.visual_height}px;">

            <div class="trailer-model">${escapeHtml(trailer.model_name)}</div>

            <div class="trailer-dims">
                ${escapeHtml(trailer.length)} × ${escapeHtml(trailer.width)} × ${escapeHtml(trailer.height)} cm
            </div>

            ${
                trailer.contained_trailer
                    ? `<div class="contained-trailer">
                        <div class="contained-label">eingeladen</div>
                        ${renderTrailerBlock(trailer.contained_trailer, true)}
                       </div>`
                    : ''
            }
        </div>
    `;
}

function renderStack(stack, stackIndex) {
    return `
        <div class="lorry-position">
            <div class="position-label">Position ${stackIndex + 1}</div>

            <div class="stack-pile">
                ${stack.map(trailer => renderTrailerBlock(trailer)).join('')}
            </div>
        </div>
    `;
}

function renderCurrentSolution() {
    if (!stackSolutions || stackSolutions.length === 0) {
        return;
    }

    const solution = stackSolutions[currentSolutionIndex];
    const loadArea = document.getElementById('lorryLoadArea');

    loadArea.style.gridTemplateColumns = `repeat(${solution.length}, minmax(145px, 1fr))`;
    loadArea.innerHTML = solution.map((stack, stackIndex) => renderStack(stack, stackIndex)).join('');

    const solutionCounter = document.getElementById('solutionCounter');
    if (solutionCounter) {
        solutionCounter.innerText = `Lösung ${currentSolutionIndex + 1} von ${stackSolutions.length}`;
    }

    const stackCount = document.getElementById('stackCount');
    if (stackCount) {
        stackCount.innerText = solution.length;
    }

    const trailerCount = document.getElementById('trailerCount');
    if (trailerCount) {
        trailerCount.innerText = solution.reduce((sum, stack) => {
            return sum + stack.reduce((stackSum, trailer) => {
                return stackSum + 1 + (trailer.contained_trailer ? 1 : 0);
            }, 0);
        }, 0);
    }
}

function previousSolution() {
    if (!stackSolutions || stackSolutions.length === 0) {
        return;
    }

    currentSolutionIndex =
        (currentSolutionIndex - 1 + stackSolutions.length) % stackSolutions.length;

    renderCurrentSolution();
}

function nextSolution() {
    if (!stackSolutions || stackSolutions.length === 0) {
        return;
    }

    currentSolutionIndex =
        (currentSolutionIndex + 1) % stackSolutions.length;

    renderCurrentSolution();
}

document.getElementById('stackForm').addEventListener('submit', () => {
    document.getElementById('trailersJson').value = JSON.stringify(trailers);
});

if (trailers.length === 0) {
    addTrailer();
} else {
    renderTrailers();
}

renderCurrentSolution();
</script>

</body>
</html>
"""


def parse_int(value: Any, field_name: str) -> int:
    if value is None or value == "":
        raise ValueError(f"{field_name} ist erforderlich")

    try:
        return int(value)
    except ValueError:
        raise ValueError(f"{field_name} muss eine ganze Zahl sein")


def build_trailers(raw_trailers: list[dict[str, Any]]) -> list[dt.Trailer]:
    trailers: list[dt.Trailer] = []
    sku_counter = 1

    for idx, raw in enumerate(raw_trailers, start=1):
        model_name = str(raw.get("model_name", "")).strip()

        if not model_name:
            raise ValueError(f"Anhänger {idx}: Modellname ist erforderlich")

        quantity = parse_int(raw.get("quantity", 1), f"Anhänger {idx}: Stückzahl")

        if quantity < 1:
            raise ValueError(f"Anhänger {idx}: Stückzahl muss mindestens 1 sein")

        width = parse_int(raw.get("width"), f"Anhänger {idx}: Breite")
        height = parse_int(raw.get("height"), f"Anhänger {idx}: Höhe")
        length = parse_int(raw.get("length"), f"Anhänger {idx}: Länge")
        axles = parse_int(raw.get("axles"), f"Anhänger {idx}: Achsen")
        sku = str(raw.get("sku") or f"trailer-{sku_counter}")

        for _ in range(quantity):
            trailers.append(
                dt.Trailer(
                    sku=f"{sku}-{sku_counter}",
                    width=width,
                    height=height,
                    length=length,
                    axles=axles,
                    model_name=model_name,
                )
            )
            sku_counter += 1

    return trailers

def serialize_trailer(trailer: dt.Trailer, visual_width, visual_height) -> dict:
    return {
        "sku": trailer.sku,
        "model_name": trailer.model_name,
        "length": trailer.length,
        "height": trailer.height,
        "width": trailer.width,
        "axles": trailer.axles,
        "contained_trailer": (
            serialize_trailer(trailer.contained_trailer, 58, 42)
            if trailer.contained_trailer is not None
            else None
        ),
        "visual_width": round(visual_width, 1),
        "visual_height": round(visual_height, 1),
    }

def serialize_stack_result(stacks: list[dt.Stack]) -> list[list[dict[str, Any]]]:
    all_trailers = [trailer for stack in stacks for trailer in stack.trailers]

    max_length = max((trailer.length for trailer in all_trailers), default=1)
    max_height = max((trailer.height for trailer in all_trailers), default=1)

    serialized: list[list[dict[str, Any]]] = []

    for stack in stacks:
        serialized_stack = []

        for trailer in stack.trailers:
            visual_width = 58 + (trailer.length / max_length) * 42
            visual_height = 42 + (trailer.height / max_height) * 48

            serialized_stack.append(
                serialize_trailer(trailer, visual_width, visual_height)
            )

        serialized.append(serialized_stack)

    return serialized


def serialize_stack_solutions(
    solutions: list[list[dt.Stack]],
) -> list[list[list[dict[str, Any]]]]:
    return [
        serialize_stack_result(solution)
        for solution in solutions
    ]


@app.route("/", methods=["GET", "POST"])
def index():
    trailers_for_ui: list[dict[str, Any]] = []
    stack_solutions: list[list[list[dict[str, Any]]]] = []
    error = None
    stack_count = 0
    trailer_count = 0
    solution_count = 0

    if request.method == "POST":
        try:
            trailers_for_ui = json.loads(request.form.get("trailers_json", "[]"))
            trailers = build_trailers(trailers_for_ui)

            results = sx.stack_all(trailers, max_results=25)

            if not results:
                error = "Für diese Anhänger wurde kein gültiger Stapelplan gefunden."
            else:
                stack_solutions = serialize_stack_solutions(results)
                solution_count = len(stack_solutions)
                stack_count = len(stack_solutions[0])
                trailer_count = sum(len(stack) for stack in stack_solutions[0])

        except Exception as exc:
            error = str(exc)

    return render_template_string(
        HTML,
        trailers=trailers_for_ui,
        stack_solutions=stack_solutions,
        error=error,
        stack_count=stack_count,
        trailer_count=trailer_count,
        solution_count=solution_count,
        sku_catalog=SKU_TRAILER_CATALOG,
    )