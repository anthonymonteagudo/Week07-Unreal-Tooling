"""Shared student-facing preview language, independent of Qt and Unreal."""


def describe_plan(plan):
    """Return table rows, action label and scope summary for either interface."""
    if plan['kind'] == 'material':
        count = len(plan['targets'])
        rows = [('Material instance', 'Not created', plan['output']),
                ('Parent material', 'N/A', plan['parent'])]
        roles = {'BaseColorTexture': 'Base color texture', 'NormalTexture': 'Normal texture',
                 'ORMTexture': 'ORM texture'}
        rows += [(roles.get(parameter, parameter), 'Not assigned', path)
                 for parameter, path in plan['mapping'].items()]
        rows += [(f"{t.get('label', t['path'])} · slot {t['slot']}", t['material'] or 'No material', plan['output'])
                 for t in plan['targets']]
        return {'rows': rows, 'action': 'Apply: create instance',
                'summary': f'1 new material instance · {count} component assignment' + ('' if count == 1 else 's'),
                'next': 'Check the texture mapping and destination below. Existing material assets will not be overwritten.'}
    count = len(plan['anchors'])
    rows = [('Prepared effect', 'N/A', plan['system']), ('Uniform scale', 'N/A', f"{plan['scale']:g}×"),
            ('Loaded Niagara components', str(plan['projected_components'] - count), str(plan['projected_components']))]
    rows += [(a.get('label', a['path']), 'No tool placement',
              f"Position (cm): {', '.join(f'{v:g}' for v in a['location'])}\n"
              f"Rotation (degrees): {', '.join(f'{v:g}' for v in a['rotation'])}") for a in plan['anchors']]
    return {'rows': rows, 'action': f'Apply: place {count} effect' + ('' if count == 1 else 's'),
            'summary': f'{count} anchors → {count} new effects · {plan["projected_components"]} total components',
            'next': 'Check each placement below. Placement limits passed; runtime performance has not been measured.'}


def display_cell(value):
    """Compact asset labels; full paths remain available in tooltips."""
    text = str(value)
    if text.startswith(("/Game/", "/Engine/", "sample://")) and "\n" not in text:
        return text.rsplit("/", 1)[-1].split(".")[0]
    return text
