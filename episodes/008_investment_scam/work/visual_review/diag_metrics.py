# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'C:/Codex/260829_youtube-anshin/scripts')
sys.stdout.reconfigure(encoding='utf-8')
from scene_renderer_metrics import measure, bands
from pathlib import Path
import numpy as np
from PIL import Image
old = Path(r'C:/Codex/260829_youtube-anshin/episodes/008_investment_scam/work/visual_review/before_render/scene_003.png')
new = Path(r'C:/Codex/260829_youtube-anshin/episodes/008_investment_scam/work/rendered_final_scenes/scene_003.png')
for tag, p in [('OLD', old), ('NEW', new)]:
    m = measure(p)
    a = np.asarray(Image.open(p).convert('RGB'))[:900]
    dark = (a[:,:,0]<105)&(a[:,:,1]<155)&(a[:,:,2]<215)
    bs = bands(dark)
    print(tag, 'raster_h:', m['headline_raster_height_px'], 'bands:', len(bs), 'top3:', [(b['top'], b['bottom'], b['pixels']) for b in bs[:3]])