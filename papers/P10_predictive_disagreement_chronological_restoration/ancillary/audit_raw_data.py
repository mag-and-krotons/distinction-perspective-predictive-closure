from __future__ import annotations
import io,json,zipfile
from pathlib import Path
import numpy as np
import pandas as pd
zpath=Path(__file__).with_name('air+quality.zip')
with zipfile.ZipFile(zpath) as z:
    name=next(n for n in z.namelist() if n.lower().endswith('.csv'))
    df=pd.read_csv(io.BytesIO(z.read(name)),sep=';',decimal=',')
blank=int(df.isna().all(axis=1).sum())
empty=[c for c in df.columns if df[c].isna().all()]
d=df.dropna(how='all').dropna(axis=1,how='all')
num=d.select_dtypes(include=[np.number])
result={
    'raw_rows':len(df),'nonblank_rows':len(d),'blank_trailer_rows':blank,
    'all_empty_columns':len(empty),'numeric_channels':num.shape[1],
    'sentinel_cells':int((num==-200).sum().sum()),
    'complete_rows':int((num!=-200).all(axis=1).sum()),
}
expected={'raw_rows':9471,'nonblank_rows':9357,'blank_trailer_rows':114,'all_empty_columns':2,'numeric_channels':13,'sentinel_cells':16701,'complete_rows':827}
assert result==expected,(result,expected)
print(json.dumps(result,sort_keys=True))
print('raw_environmental_audit=PASS')
print('downstream_constructor_metrics=SOURCE_REPORTED')
