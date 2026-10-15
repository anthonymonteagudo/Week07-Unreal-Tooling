import fs from 'node:fs';
import {catalog,checkpoint} from '../../StudentFacing20261013/.build/content.mjs';
export {catalog,checkpoint};
const data=JSON.parse(fs.readFileSync(new URL('../../StudentFacing20261013/slide_sources.json',import.meta.url),'utf8'));
export const S={...data.sourceKeys},sections=structuredClone(data.sections);
const old=data.slides.map((s,i)=>({...structuredClone(s),sourceNumber:i+2}));
const by=id=>old.find(s=>s.id===id);
S.docs='https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/?application_version=5.7';
S.autocomplete='https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-autocomplete-for-unreal-editor-python-scripting?application_version=5.7';
S.vscode='https://code.visualstudio.com/docs/python/settings-reference';
const karol='C:/Users/antho/OneDrive/Desktop/Notes/anthony/personal/Duke Tech Art Course Notes/16 Karol UE Python Course/';
const noteSetup=karol+'01 Setup/02 VS Code Autocomplete Setup - REFINED.md';
const noteSelection=karol+'03 Automation Scripting/10 Getting User Selection and Listing Assets - REFINED.md';
const make=(id,title,body,notes,minutes=1)=>({id,title,question:'',caption:'',...body,notes,minutes,section:'python',tag:'01  Python in Unreal',facilitation:'Predict the result before execution. Compare the editor selection and output. New examples need classroom rehearsal.',refs:['docs'],local:[noteSelection]});
const additions=[
 make('DOCS','Unreal Python documentation',{
   links:[['Python API reference: choose Unreal 5.7','docs'],['EditorActorSubsystem: selected level actors','EditorActorSubsystem'],['EditorUtilityLibrary: selected assets','EditorUtilityLibrary']],
   caption:'Read the owning class, parameters, return type and deprecation notices.',
   question:'Find the return type of get_selected_level_actors().'
 },'Open the Python API reference and match the engine version. Search for the class, then the method. Read which object owns the call, the parameters, the return type and any deprecation notice. Array[Actor] tells us we can loop over actors. This is a lookup exercise: what comes back, and what can we do with it?',1),
 make('VSC1','VS Code: Python autocomplete',{
   bullets:['Open the Week07UnrealPython folder in VS Code. Install Microsoft Python and Pylance.', 'In Unreal: Editor Preferences > Plugins > Python > Developer Mode. Restart Unreal.', 'Confirm Intermediate/PythonStub/unreal.py exists in this project.'],
   question:'VS Code edits the script. Unreal executes the editor API.'
 },'Karol separates writing code from running the editor. Open the folder containing the uproject so the next slide uses the correct relative paths. Enable Developer Mode before class and restart Unreal to generate its stub. The stub describes the API for autocomplete. It does not supply a running editor. Older course captures put this setting in Project Settings; the linked Unreal 5.7 documentation uses Editor Preferences.',.75),
 make('VSC2','VS Code: workspace settings',{
   api:true,code:'{\n  "python.analysis.extraPaths": [\n    "${workspaceFolder}/Intermediate/PythonStub",\n    "${workspaceFolder}/Content/Python"\n  ]\n}',
   explain:'Save in .vscode/settings.json. Type unreal. in a Python file to check suggestions.',
   caption:'JSON settings for VS Code. Run Unreal scripts inside Unreal.',
   question:'Ctrl-click an API symbol, then compare its signature with the docs.'
 },'Merge these entries with existing workspace settings rather than replacing unrelated settings. Pylance reads the stub folder for Unreal names and Content/Python for our project modules. Use Python: Select Interpreter for your ordinary Python tools, but selecting an interpreter does not create an Unreal editor session. Never add the stub directory to runtime PYTHONPATH. If suggestions are absent, check the generated file and reload the VS Code window.',.75),
 make('CALL','An Unreal function call, explained',{
   table:[['Expression','Meaning'],['unreal.get_editor_subsystem(...)','Ask the running editor for a subsystem.'],['unreal.EditorActorSubsystem','Class argument: which subsystem we need.'],['editor.get_selected_level_actors()','Call on that instance. No explicit arguments.'],['actors = ...','Keep the returned Array[Actor] to inspect.']],
   question:'A class names a type. The returned editor object performs the operation.'
 },'Read this together with the selection example. Unreal is the module. EditorActorSubsystem names the type we request. get_editor_subsystem returns the existing editor-owned instance. We store that instance as editor and call its method. The empty parentheses mean no explicit arguments on this call. Its return is a collection, so len counts it and a for loop inspects each Actor. Karol highlights the distinction between static library calls and calls on subsystem instances.',1),
 make('UE02R','Selection example: expected output',{
   showcase:true,input:'Outliner: select only W07_Crate_Target.\nRun the complete UE02 example.',
   output:'Selected Actors: 1\nW07_Crate_Target StaticMeshActor',
   result:'The label matches the Outliner. The class identifies the Actor type.',
   experiment:'Clear the Outliner selection and rerun: Selected Actors: 0.\nReset: select W07_Crate_Target again. No scene edits.'
 },'This is expected output for the prepared classroom map, not a new captured run. UE02 reads the current selection each time. The Content Browser can stay unchanged while this result changes. If the count is wrong, inspect the selected Outliner rows before investigating the loop.',.5),
 make('UE04R','Asset example: expected output',{
   showcase:true,input:'Content Browser: select only T_Crate_BaseColor.\nRun the complete UE04 example.',
   output:'Selected assets: 1\nT_Crate_BaseColor Texture2D\n/Game/Week07/LiveDemo/Textures/\nT_Crate_BaseColor.T_Crate_BaseColor',
   result:'get_name() reads the name. get_class() identifies the type.\nget_path_name() gives the object path.',
   experiment:'Select another asset and rerun. Reset: reselect the texture.\nThe path above wraps for display; Unreal prints it as one line.'
 },'Karol makes selected objects and their identity distinct. get_selected_assets is a library call that returns loaded objects. We can ask each object for its name, class and path without loading it again. These methods return values; print displays them. Changing Content Browser selection does not change Outliner selection.',.5),
 make('UE05R','Texture example: input and result',{
   showcase:true,input:'Select T_Crate_BaseColor, then run UE05.\nRepeat with T_Crate_Normal.',
   output:'BaseColor: Textures: 1 skipped: 0\nsRGB: True; compression: TC_DEFAULT\n\nNormal: Textures: 1 skipped: 0\nsRGB: False; compression: TC_NORMALMAP',
   result:'get_editor_property("srgb") reads a Boolean.\n"compression_settings" reads a TextureCompressionSettings enum.',
   experiment:'Compare Texture Editor > Details > sRGB / Compression Settings.\nExpected values shown; enum formatting may differ. No reset needed.'
 },'The example filters selected assets with isinstance before reading texture properties. The string passed to get_editor_property names an exposed property. Its return type depends on that property. We are reading, not changing, the checkbox and compression setting. Select a mesh too to see the skipped count increase. This demonstration connects code output to the manual controls students can inspect.',.5),
 make('RUN','A saved example, run inside Unreal',{
   bullets:['Save the complete UE02 example as Content/Python/selection_demo.py.', 'In Unreal, choose Tools > Execute Python Script and select that file.', 'Read the Output Log. Change the Outliner selection and execute the file again.'],
   question:'Each execution reads the selection that exists at that moment.'
 },'Use the same small file shown in the deck. It contains its own import and subsystem lookup so no earlier script is needed. A normal VS Code Run Python File command does not run inside Unreal. Re-executing the saved script is also different from importing a cached module again. During tool development, reload a module explicitly when needed.',.5)
];
for(const id of ['VSC1','VSC2']){const s=additions.find(s=>s.id===id);s.refs=['autocomplete','vscode'];s.local=[noteSetup];}
by('04').title='Project readiness check: 3 minutes';
by('04').explain='Expected: Hello from Unreal, your engine version and your intended project folder.';
by('04').question='Wrong project or any error? Pause and ask for help.';
by('04').notes='Take three minutes to open the intended project, choose Python in the Output Log and run this complete snippet. Confirm the greeting, engine version and project directory. Your user folder can differ from mine. This checks the Python host and project only. It does not certify the Material/VFX fixture or bridge. Tell me if you see an error or a different project.';
by('04').facilitation='Allow the full three minutes. Use the provided Week07UnrealPython project for the prepared demos. Address setup errors before continuing.';
by('07').explain='get_selected_level_actors() returns Actor objects. len counts them; the loop reads each label and class.';
by('UE04').explain='get_selected_assets() returns loaded Content Browser objects. Each object supplies its name, class and path.';
by('09G').explain='isinstance filters Texture2D inputs. get_editor_property reads the named setting; it does not change it.';
by('02').table[1][1]='01 Unreal foundations, 02 Working tools, 03 Blender and bridge';
by('02').bullets=['Unreal examples first. Blender comparison follows the working tools.'];
sections.demos.name='02  Unreal API calls in working tools';sections.blender.name='03  Blender and the bridge';
by('S1A').title='Unreal API calls\nin working tools';
by('S1A').subtitle='Selection and properties become a material or VFX operation.';
by('S1A').next='Next: inspect inputs, preview one change, apply and verify.';
by('SB').title='Blender and\nthe bridge';by('SB').subtitle='Compare host APIs after the Unreal examples.';by('SB').next='Next: Blender selection, then Maya/Blender publishing to Unreal.';
const sequence=['02','S1','03','04','DOCS','VSC1','VSC2','CALL','07','UE02R','RUN','07C','06A','UE04','UE04R','MAT1','09G','UE05R','09H','07A','S1A','MAT2','09I','MAT3','09','09F','08A','09J','09D','SB','BL01','BL02','10','BR-PARITY','10C','10A','UE12','10D','09K'];
const merged=new Map([...old,...additions].map(s=>[s.id,s]));
export const slides=[...sequence.map(id=>merged.get(id)),...old.filter(s=>!sequence.includes(s.id)&&!s.hidden),...old.filter(s=>s.hidden)];
for(const s of slides){if(['10','10D','BR-PARITY','10C','10A','UE12'].includes(s.id))s.section='blender';if(s.section==='demos'||s.section==='blender')s.tag=sections[s.section].name;}
// Preserve the prior schedule as a reference; it is not a slide pacing prescription.
export const timing=data.timing;
for(const s of slides){delete s.minutes;s.facilitation=(s.facilitation||'').replace(/Time:.*$/,'');}
export const bindings=slides.flatMap((s,i)=>s.checkpoint?[{slide:i+2,anchor:s.id,...s.checkpoint,hidden:!!s.hidden}]:[]);
