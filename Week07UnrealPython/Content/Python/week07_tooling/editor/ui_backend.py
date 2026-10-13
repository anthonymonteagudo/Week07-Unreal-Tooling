"""Thin live adapter. Import only when the instructor explicitly opens the UE UI."""
import unreal
from week07_tooling.editor import demo


class UnrealBackend:
    is_live = True

    def snapshot(self):
        records = []
        for actor in demo.fixture():  # Also guards world, fixture identity and PIE.
            state = demo._state(actor)
            mesh = actor.get_component_by_class(unreal.StaticMeshComponent)
            records.append(dict(state, has_mesh=bool(mesh and mesh.static_mesh)))
        return {'world': demo.world().get_path_name(), 'records': records,
                'selected': sorted(a.get_path_name() for a in demo.actors().get_selected_level_actors())}

    def select_demo(self):
        return demo.select_demo()

    def preview(self):
        return demo.preview()

    def apply(self, plan):
        return demo.apply(plan)

    def check(self):
        return demo.check()

    def reset_demo(self):
        return demo.reset_demo()
