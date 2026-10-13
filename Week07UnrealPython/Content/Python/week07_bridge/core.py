"""Shared publisher and contract. Runs in ordinary Python, Maya and Blender.

An adapter implements inspect_selection() and export_fbx(path). The contract,
validation, revision naming and publication order are identical for both hosts.
"""
from pathlib import Path
import hashlib
import json
import math
import os
import re
import time
import uuid

DESTINATION = '/Game/Week07/Bridge'
NAME = re.compile(r'SM_[A-Za-z0-9_]+\Z')


def default_exchange():
    return Path(__file__).resolve().parents[3] / 'Saved' / 'BridgeExchange'


def atomic_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    try:
        temporary.write_text(json.dumps(data, indent=2, allow_nan=False) + '\n', encoding='utf-8')
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def checksum(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def validate_target(asset_name, destination):
    if not isinstance(asset_name, str) or not NAME.fullmatch(asset_name):
        raise ValueError('Use an asset name such as SM_BridgeProp (letters, digits, underscores).')
    if (not isinstance(destination, str) or
            not re.fullmatch(r'/Game/Week07/Bridge(?:/[A-Za-z0-9_]+)*', destination)):
        raise ValueError('Choose a destination within /Game/Week07/Bridge.')
    return destination + '/' + asset_name


def validate_source(info):
    if info.get('host') not in ('blender', 'maya'):
        raise ValueError('Unsupported source application.')
    if not isinstance(info.get('source_file'), str):
        raise ValueError('Source file must be a string; an empty string means unsaved.')
    if info.get('mesh_count') != 1 or info.get('face_count', 0) < 1:
        raise ValueError('Select exactly one polygon mesh with faces.')
    dims = info.get('dimensions_cm', [])
    if len(dims) != 3 or any(not math.isfinite(v) or v <= 0 for v in dims):
        raise ValueError('The mesh needs nonzero, finite dimensions on all three axes.')
    return info


def publish(adapter, exchange=None, asset_name='SM_BridgeProp', destination=DESTINATION):
    """Export to an immutable revision; JSON is committed only after a valid FBX."""
    validate_target(asset_name, destination)
    info = validate_source(adapter.inspect_selection())
    root = Path(exchange or default_exchange()).resolve()
    revision = uuid.uuid4().hex
    folder = root / 'publishes' / asset_name / revision
    folder.mkdir(parents=True, exist_ok=False)
    fbx = folder / (asset_name + '.fbx')
    adapter.export_fbx(fbx)
    if not fbx.is_file() or fbx.stat().st_size < 32:
        raise RuntimeError('Exporter produced no usable FBX. Nothing was sent to Unreal.')
    manifest = {
        'schema_version': 1, 'revision': revision, 'created_at': time.time(),
        'source_file': info['source_file'], 'source_host': info['host'],
        'source_object': info['object_name'], 'asset_name': asset_name,
        'destination_path': destination, 'filename': fbx.name,
        'sha256': checksum(fbx), 'dimensions_cm': info['dimensions_cm'],
        'asset_type': 'StaticMesh', 'origin_policy': 'source_pivot',
    }
    path = folder / 'manifest.json'
    atomic_json(path, manifest)
    return path


def load_manifest(path, exchange=None):
    path = Path(path).resolve()
    root = Path(exchange or default_exchange()).resolve()
    if not path.is_relative_to(root / 'publishes'):
        raise ValueError('Manifest must be inside this bridge exchange/publishes folder.')
    data = read_json(path)
    if type(data.get('schema_version')) is not int or data['schema_version'] != 1:
        raise ValueError('Unsupported manifest schema_version.')
    validate_target(data.get('asset_name'), data.get('destination_path'))
    if data.get('asset_type') != 'StaticMesh' or data.get('origin_policy') != 'source_pivot':
        raise ValueError('This bridge accepts static meshes with a source pivot only.')
    if data.get('source_host') not in ('maya', 'blender'):
        raise ValueError('Unknown publisher.')
    if not re.fullmatch(r'[0-9a-f]{32}', str(data.get('revision', ''))):
        raise ValueError('Invalid revision.')
    if data.get('filename') != data['asset_name'] + '.fbx':
        raise ValueError('FBX filename must match asset_name.')
    fbx = (path.parent / data['filename']).resolve()
    if not fbx.is_relative_to(root / 'publishes'):
        raise ValueError('FBX resolved outside the exchange.')
    if not fbx.is_file() or checksum(fbx) != data.get('sha256'):
        raise ValueError('FBX is missing or changed after publish. Publish again.')
    dims = data.get('dimensions_cm', [])
    if len(dims) != 3 or any(not isinstance(v, (float, int)) or not math.isfinite(v) or v <= 0 for v in dims):
        raise ValueError('Invalid expected dimensions.')
    return data, fbx
