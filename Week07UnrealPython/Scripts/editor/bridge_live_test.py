"""Keep a separate test editor alive for actual DCC Publish & Send requests."""
from pathlib import Path
import time
import traceback
import unreal
from week07_bridge import core, unreal_receiver, transport

root = Path(unreal.Paths.project_dir()).resolve()
exchange = root / 'Saved/BridgeLiveTest'
unreal.EditorPythonScripting.set_keep_python_script_alive(True)
unreal_receiver.install_menu()
unreal_receiver.start(exchange)
session = transport.receiver_status(exchange)['session']
started = time.monotonic()
report = {'status': 'WAITING', 'engine': unreal.SystemLibrary.get_engine_version()}
core.atomic_json(exchange / 'ready.json', report)


def finish(delta):
    try:
        responses = [core.read_json(p) for p in (exchange / 'responses').glob('*.json')]
        responses = [r for r in responses if r.get('session') == session]
        if len(responses) < 4 and time.monotonic() - started < 180:
            return
        if len(responses) < 4:
            raise TimeoutError('Expected four actual DCC publish requests.')
        assert all(item['ok'] for item in responses), responses
        evidence = {}
        for host in ('Blender', 'Maya'):
            mesh = unreal.load_asset('/Game/Week07/Bridge/SM_Live_' + host)
            # Read actual imported vertices to verify orientation, not just dimensions.
            verts = unreal.ProceduralMeshLibrary.get_section_from_static_mesh(mesh, 0, 0)[0]
            positions = sorted(set(tuple(round(v, 2) for v in (p.x, p.y, p.z)) for p in verts))
            assert min(p[2] for p in positions) == 0, positions
            assert max(p[2] for p in positions if p[0] > 0) == 140, positions
            assert max(p[2] for p in positions if p[0] < 0) == 220, positions
            evidence[host] = positions
        assert evidence['Blender'] == evidence['Maya'], evidence
        report.update(status='PASS', responses=responses, matching_vertices_cm=evidence)
    except Exception:
        report.update(status='FAIL', error=traceback.format_exc())
    finally:
        if report['status'] != 'WAITING':
            core.atomic_json(exchange / 'result.json', report)
            unreal_receiver.stop()
            unreal.unregister_slate_post_tick_callback(handle)
            unreal.SystemLibrary.quit_editor()


handle = unreal.register_slate_post_tick_callback(finish)
