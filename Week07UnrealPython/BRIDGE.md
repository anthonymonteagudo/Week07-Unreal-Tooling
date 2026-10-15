# Optional Maya or Blender bridge

Use the same extracted demo project. No additional plugin build or pip install is needed. The rehearsed hosts are Blender 5.1.1, Maya 2027 and Unreal 5.7.4. Static meshes only.

1. In Unreal, open `Content/Week07/Bridge/W07_BridgeComparison`.
2. In Output Log > Python, run:
   ```python
   from week07_bridge import unreal_receiver
   unreal_receiver.install_menu()
   unreal_receiver.start()
   ```
3. In Blender, open `Samples/Bridge/BridgeCompare.blend`. In its Text Editor, open the saved `Scripts/bridge/open_blender.py` and choose Run Script. The publisher is in the 3D View's **N sidebar > Week 7**.
4. Or in Maya, open `Samples/Bridge/BridgeCompare.ma` and run this in the Python Script Editor, replacing the example path with your extracted folder:
   ```python
   import runpy
   runpy.run_path(r'C:\Teaching\Week07UnrealPython\Scripts\bridge\open_maya.py')
   ```
5. Use **Publish & Send**, then inspect the imported mesh in Unreal. Both apps exchange files through this project's `Saved/BridgeExchange`; no network service is required.

After moving the project, publish again to establish the new local FBX source path. To reset a changed source mesh, reopen the original sample without saving, then publish it under the same asset name. Files under `Samples/Bridge/Handoffs` are inspectable reference copies. They are not a substitute for publishing a new revision.

Return to `W07_MaterialVFXLab` for the Material/VFX demonstration.
