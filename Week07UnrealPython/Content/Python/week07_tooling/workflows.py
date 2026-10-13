"""Bounded material and VFX workflows. Pure data; no graph editing or scattering."""
from copy import deepcopy
from math import dist, isfinite
import re

TEXTURES = {'BaseColor': 'BaseColorTexture', 'Normal': 'NormalTexture', 'ORM': 'ORMTexture'}
OUTPUT = '/Game/Week07/Generated/Materials'
MAX_BATCH = 8
MAX_SYSTEM = 16
MAX_LOADED_COMPONENTS = 32
MIN_SPACING_CM = 100.0


def require(condition, message):
    if not condition:
        raise ValueError(message)


def material_plan(request, snapshot):
    require(snapshot['master_valid'], 'Choose a prepared material with BaseColorTexture, NormalTexture and ORMTexture parameters.')
    require(re.fullmatch(r'MI_[A-Za-z0-9_]+', request['name']) is not None,
            'Use an instance name beginning MI_, with letters, digits and underscores.')
    require(not snapshot['target_exists'], 'That material instance already exists. Choose a new name; overwrite is disabled.')
    require(snapshot['targets'] and not snapshot['mixed_selection'],
            'Select mesh Actors with exactly one Static Mesh Component and a valid target slot.')
    textures, prefixes = {}, set()
    for texture in snapshot['textures']:
        require(texture['is_texture'], 'Content Browser selection must contain only the three textures.')
        match = re.fullmatch(r'(.+)_(BaseColor|Normal|ORM)', texture['name'])
        require(match is not None, 'Texture names must share a prefix and end _BaseColor, _Normal, or _ORM.')
        prefix, role = match.groups()
        require(role not in textures, f'More than one {role} texture selected. Resolve the ambiguity.')
        prefixes.add(prefix)
        textures[role] = texture
    require(set(textures) == set(TEXTURES) and len(prefixes) == 1,
            'Select one complete texture set with a shared filename prefix.')
    require(all(parameter in snapshot['parameters'] for parameter in TEXTURES.values()),
            'The prepared parent is missing a required texture parameter.')
    for role, texture in textures.items():
        require(texture['srgb'] == (role == 'BaseColor'),
                f'{role}: review the texture sRGB setting before continuing. This tool does not change shared textures.')
    require(textures['Normal']['normal_compression'], 'Normal texture must use Normalmap compression. Review its import settings.')
    return {'kind': 'material', 'output': f"{OUTPUT}/{request['name']}",
            'parent': request['master'],
            'mapping': {TEXTURES[role]: texture['path'] for role, texture in textures.items()},
            'targets': deepcopy(snapshot['targets']),
            'notes': ['Creates one instance; assigns component overrides only.',
                      'Does not edit material graphs, texture settings or shared mesh assets.',
                      'New asset and level changes are not automatically saved.']}


def vfx_plan(request, snapshot):
    profile = snapshot['profile']
    require(profile and profile.get('reviewed_for_demo') is True and profile.get('review_note'),
            'This effect has not been reviewed for the demo. Ask the instructor to prepare its preset.')
    require(snapshot['system_valid'] and snapshot['has_effect_type'],
            'Preset must reference a Niagara System with an assigned Effect Type for scalability.')
    anchors = snapshot['anchors']
    require(anchors and not snapshot['mixed_selection'], 'Select only Actors tagged W07_VFXAnchor.')
    require(len({a['path'] for a in anchors}) == len(anchors), 'Duplicate placement anchors are not allowed.')
    maximum = profile.get('max_new', MAX_BATCH)
    require(type(maximum) is int and 1 <= maximum <= MAX_BATCH, 'Preset batch limit must be between 1 and 8.')
    require(len(anchors) <= maximum, f'Batch limit: {maximum} effects. Reduce the selected anchors.')
    scale = request['scale']
    require(type(scale) in (int, float) and isfinite(scale) and 0.25 <= scale <= 1.0,
            'Scale must be between 0.25 and 1.0. Larger effects require a separate review.')
    existing = snapshot['existing']
    require(len(existing) + len(anchors) <= MAX_LOADED_COMPONENTS,
            'Loaded-world Niagara component limit (32) would be exceeded. Review existing effects.')
    same_system = sum(e['system'].split('.')[0].casefold() == profile['system'].split('.')[0].casefold() for e in existing)
    require(same_system + len(anchors) <= MAX_SYSTEM, 'This Niagara System would exceed 16 loaded placements.')
    sources = {e['source'] for e in existing if e['source']}
    positions = [e['location'] for e in existing]
    for anchor in anchors:
        require(anchor['path'] not in sources, 'An effect already occupies one of these anchors. Repeated placement is blocked.')
        location = anchor['location']
        require(len(location) == 3 and all(type(v) in (float, int) and isfinite(v) for v in location),
                'Anchor locations must contain three finite coordinates.')
        require(all(dist(location, p) >= MIN_SPACING_CM for p in positions),
                'Effects must be at least 100 cm apart. Move or reduce the selected anchors.')
        positions.append(location)
    projected = len(existing) + len(anchors)
    return {'kind': 'vfx', 'system': profile['system'], 'anchors': deepcopy(anchors), 'scale': scale,
            'projected_components': projected,
            'warnings': (['More than 8 loaded Niagara components after this batch. Review density before Apply.']
                         if projected > 8 else []),
            'notes': ['Placement checks passed; runtime performance has NOT been measured.',
                      'Counts cover the loaded editor world, not unloaded levels or runtime spawns.',
                      'No spawn-rate overrides, random scattering or Niagara graph edits.']}


class WorkflowSession:
    """Keep a reviewed request and its exact snapshot; recheck before any mutation."""
    def __init__(self, backend):
        self.backend = backend
        self.pending = None

    def clear(self):
        self.pending = None

    def preview(self, kind, request):
        self.clear()
        require(kind in ('material', 'vfx'), 'Unknown workflow.')
        snapshot = self.backend.snapshot(kind, request)
        plan = (material_plan if kind == 'material' else vfx_plan)(request, snapshot)
        self.pending = deepcopy((kind, request, snapshot, plan))
        return deepcopy(plan)

    def apply(self, warnings_reviewed=False):
        require(self.pending is not None, 'Preview and review changes first.')
        kind, request, snapshot, plan = self.pending
        self.clear()
        require(self.backend.snapshot(kind, request) == snapshot,
                'Selection, scene, preset or destination changed. Preview again.')
        (material_plan if kind == 'material' else vfx_plan)(request, snapshot)
        require(not plan.get('warnings') or warnings_reviewed is True,
                'Review the density warning and explicitly acknowledge it before applying.')
        return self.backend.execute(kind, deepcopy(plan))
