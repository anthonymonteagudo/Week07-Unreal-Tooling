"""Assemble actual UE renders into a labelled step comparison, not a screen recording."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
root = Path(__file__).resolve().parent / 'Captures'
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 28)
small = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 17)
frames = []
for name, label in [('01_baseline', 'BEFORE  /  scattered placement + temporary labels'),
                    ('02_organized', 'APPLY  /  six selected Actors organized'),
                    ('03_reset', 'RESET  /  return to the rehearsal baseline')]:
    raw = Image.open(root / (name + '.png')).convert('RGB')
    raw.thumbnail((1200, 675))
    frame = Image.new('RGB', (1200, 765), '#171b24')
    frame.paste(raw, (0, 0))
    draw = ImageDraw.Draw(frame)
    draw.text((24, 686), label, font=font, fill='white')
    draw.text((24, 728), 'Week 7 Unreal Python | Actual Unreal renders | Discrete state comparison, not live recording', font=small, fill='#c1cbd9')
    frames.append(frame)
frames[0].save(root / 'week07_unreal_python_comparison.gif', save_all=True,
               append_images=frames[1:], duration=[2200, 2600, 1800], loop=0, disposal=2)
print(root / 'week07_unreal_python_comparison.gif')
