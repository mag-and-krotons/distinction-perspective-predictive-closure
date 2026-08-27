from __future__ import annotations
import csv
from pathlib import Path
p=Path(__file__).with_name('alpha_track_predictions.csv')
rows=list(csv.DictReader(p.open()))
vals={r['gas']:float(r['predicted_kinks_per_track']) for r in rows}
assert vals=={'helium':0.19,'air':0.95,'argon':6.1}
expected={g:200*v for g,v in vals.items()}
assert expected=={'helium':38.0,'air':190.0,'argon':1220.0}
late_fraction=0.78
assert 0<late_fraction<1
print('gas_ladder_table=PASS')
print('expected_counts_for_200_tracks',expected)
print('late_range_fraction_model=0.78')
print('experimental_status=UNTESTED_PREDICTION')
