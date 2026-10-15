import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
process.env.RUNTIME_NODE_MODULES='C:/Users/antho/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const work=path.resolve('..'), repo=path.resolve('../../../../..');
const source=path.resolve('../../UnrealFirst20261013/output/Week_7_Python_in_Unreal_v13.pptx');
const p=await PresentationFile.importPptx(await FileBlob.load(source));
const original=[...p.slides.items], changes=[];
const C={ink:'#17151F',muted:'#777080',accent:'#505969',bg:'#F2F3F5'};
function text(sl,str,x,y,w,h,size=26,color=C.ink,bold=false,font='Arial') { const s=sl.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}}); s.text=str;s.text.style={typeface:font,fontSize:size,color,bold};return s; }
function note(n,words,refs='') {const sl=original[n-1],old=sl.speakerNotes.text;const at=old.indexOf('\n\nSource insight');sl.speakerNotes.text=(at<0?old:old.slice(0,at))+'\n\n'+words+(at<0?'':old.slice(at))+'\nAdditional sources: Karol Kowalczyk / Tech Art Corner, refined lessons '+refs;}
function replace(n,old,value){const s=original[n-1].shapes.items.find(s=>String(s.text)===old);if(!s)throw Error('Missing text '+n+': '+old);s.text=value;}
function change(n,reason){changes.push({source:n,reason});}
text(original[9],'Which expression names the class, and which retrieves its instance?',94,581,1092,36,23,'#245F99',true);
note(10,'We ask the editor for its managed subsystem instance. Older course screenshots construct EditorActorSubsystem directly; use the accessor shown here. The returned Unreal Array supports this loop directly. Converting it to a Python list is optional. What questions do you have about the class, instance or collection?','49 and 50.');change(10,'Keep table and takeaway. Add a class/instance question and explain direct array iteration.');
text(original[12],'Explore further: Import troubleshooting (K3)',94,573,1092,36,23,'#245F99',true);
note(13,'If an import fails, read the traceback first. Is our module missing, or did something it imports fail? The interpreter and package folder matter. The optional Import troubleshooting example walks through that distinction. Repeated imports are cached; replacing registered callbacks needs deliberate cleanup. What questions do you have about finding or running the file?','06–09, 17, 48.');change(13,'Keep run procedure. Add named K3 reference and import/reload guidance.');
note(21,'This checkpoint only reads properties. When you later write one, use its editor setter and compare the actual result with a manual edit. Karol’s source-color-space example needed a change notification to rebuild dependent values. Reading back one field alone would miss that problem. Saving and Undo are separate decisions.','12–13.');change(21,'Keep read-only code. Add narration distinguishing property readback from the resulting asset.');
note(23,'Our suffix and expected compression are project rules. Karol uses a different naming convention, and his square and allowed-size validators are separate checks. A skipped input is not a pass. A useful failure names the asset, its actual value and the expected rule.','12, 21–25.');change(23,'Keep validator and question. Clarify project-specific rules, skipped inputs and actionable failures.');
replace(29,'Recorded Blender UI reference. Geometry revision; materials stay in Unreal.','Publish files. Send request. Wait for acknowledgement. Inspect the asset.');
// Keep the existing reset instruction and all geometry-demo steps.
note(29,'Publishing writes FBX and JSON. Sending queues an import request. Wait for Unreal’s acknowledgement, then inspect both blue placements and their shared asset. Our bridge uses files for requests and acknowledgements. Karol’s example uses HTTP Remote Control. If the send is blocked or pending, Copy diagnostics records the environment, exchange folder and request/result identities without sending another request. What proves the revision reached the intended asset?','19, 46–48; week07_bridge/client.py.');change(29,'Keep selection, +0.4 m revision, two placements and reset. Explain each handoff stage and Copy diagnostics.');
original[42].images.items[0].position={left:94+(1092-1092*320/380)/2,top:220,width:1092*320/380,height:320};
text(original[42],'Bridge example: Copy diagnostics preserves the request and its evidence.',94,566,1092,33,22,'#6550A2',true);
note(43,'The bridge now offers Copy diagnostics. It copies the active environment, exchange folder, receiver identity and request result. It leaves the current operation in place. We can attach that report to reproduction steps before deciding whether to retry.','37, 46, 48; week07_bridge/client.py.');change(43,'Keep error screenshot. Add the implemented diagnostics example and its read-only purpose.');
note(44,'Cancellation stops future work at the next check. It does not undo changes already made. A transaction groups supported editor edits, while file export and import need their own recovery procedure. Explore further in Progress, cancellation and Undo, K5.','33–34.');change(44,'Keep accessibility content. Add cancellation versus Undo distinction and K5 pointer in narration.');
note(46,'For automated checks, also prove that a deliberately failing expectation is detected. A discovered file that never calls its checks gives no evidence about those checks. Explore further in Tests that detect failure, K6.','35–38.');change(46,'Keep peer-test visual and discussion. Connect to optional test-wiring example.');
text(original[60],'UI calls workflow logic; host adapters call the editor API.',94,562,1092,42,25,'#00796F',true);
note(61,'Reusable workflow logic should not import the window that calls it. That direction helps avoid circular imports and lets another interface reuse the operation. The bridge follows the same idea with shared Publisher logic and separate Blender and Maya adapters.','39, 48.');change(61,'Keep PySide/Slate table. Add dependency-direction caption.');
text(original[74],'Explore further: Python data to a Blueprint Map (K2)',94,562,1092,42,25,C.accent,true);change(75,'Keep Blueprint overview. Link by name to the optional Map example immediately following.');
note(97,'For the classroom bridge, attach Copy diagnostics with the steps that led to the problem. It preserves the active exchange, receiver project/session and last request/result identity. Review local paths before sharing the report. The report does not export or resend anything.','37, 48; week07_bridge/client.py.');change(97,'Keep production reference. Add concrete bridge reproduction evidence.');
note(105,'Parameter names must match the parent material. Check expected names before applying edits, inspect setter results, then read back the assigned values. Clearing all parameter overrides is a separate operation that can remove unrelated choices. Constructing MaterialParameterInfo only describes a parameter; it does not set one.','14, 50.');change(105,'Keep parameter readback. Add prerequisite and clear-all scope clarification.');
text(original[105],'Completed course: K2 Map · K3 imports · K4 Remote Control',94,571,1092,32,23,C.accent,true);
text(original[105],'K5 cancellation / Undo · K6 automated test evidence',94,616,1092,32,23,C.accent,true);
note(106,'The completed course adds a typed Map output example, import troubleshooting and runtime object-path discovery. The latter applies to Remote Control, while our classroom bridge uses file requests. The further examples separate cancellation from Undo and show how to prove a test is actually running. Which reference would help your own tool next?','46–50 and 33–38.');change(106,'Keep existing connection table. Add named references to the completed-course examples.');
const noteRoot='C:/Users/antho/OneDrive/Desktop/Notes/anthony/personal/Duke Tech Art Course Notes/16 Karol UE Python Course';
const additions=[];
function optional(id,title,after=null){const sl=p.slides.add({layoutId:'/ppt/slideLayouts/slideLayout6.xml'}); if(after){const order=p.slides.items.filter(s=>s.id!==sl.id);order.splice(order.findIndex(s=>s.id===after.id)+1,0,sl);p.slides.reorder(order.map(s=>'sl/'+s.id));}sl.hidden=true;sl.background.fill=C.bg;text(sl,'Explore further',94,60,1092,35,20,C.accent,true);text(sl,title,94,125,1092,95,46,C.ink,true);text(sl,'WEEK 7  /  '+id,94,677,850,23,15,C.muted);additions.push({id,title,slideId:sl.id});return sl;}
function notes(sl,narration,lessons,prep='Optional reference, outside the 150-minute live route.'){sl.speakerNotes.text=narration+'\n\nFacilitation (not narration): '+prep+'\n\nSources: Karol Kowalczyk / Tech Art Corner, Unreal Python course; refined lessons '+lessons+' under '+noteRoot;}
let sl=optional('K2','Python data to a Blueprint Map',original[74]);
const mapCode='import unreal\nmy_dict = {"a": 1, "b": 2}\nunreal_map = unreal.Map.cast(str, int, my_dict)';
text(sl,mapCode,94,227,1092,108,26,C.ink,false,'Consolas');
await fs.mkdir('../assets',{recursive:true});
const mapImg='C:/Users/antho/OneDrive/Desktop/Notes/anthony/personal/Pasted image 20261014213859.png';await fs.copyFile(mapImg,'../assets/karol-map-output.png');
sl.images.add({blob:new Uint8Array(await fs.readFile(mapImg)),contentType:'image/png',alt:'Karol course: unreal_map output wired to Config with String and Integer Map types',fit:'contain',position:{left:94,top:340,width:1092,height:220}});
text(sl,'Output: unreal_map     Config: Map<String, Integer>',94,566,1092,32,25,C.ink,true);
text(sl,'Karol Kowalczyk / Tech Art Corner · lesson 50',94,605,1092,24,16,C.muted);
text(sl,'What must match on both sides? What would you like clarified?',94,637,1092,35,23,C.accent,true);
notes(sl,'This script runs in Execute Python Script inside an editor utility Blueprint. Add an output named unreal_map. Create Config as a Map with String keys and Integer values. Connect the execution wire and the unreal_map output to Set Config. The Python variable name matches the output name. Return Value reports execution success; it is separate from the returned Map. Inspect Config: a should be 1 and b should be 2. Change b to 3 and check it again. What would you inspect if the receiving pin had the wrong type?','40, 50.','Optional reference. Enable editor scripting and Python. Code includes its import. Configure output and receiving variable before running. No scene edits; reset the variable to clear this example. Screenshot is the course demonstration. New current-engine execution remains to be rehearsed.');
await fs.mkdir(path.join(repo,'Week07UnrealPython/lesson_materials/week_07_api_checkpoints/ue'),{recursive:true});
await fs.writeFile(path.join(repo,'Week07UnrealPython/lesson_materials/week_07_api_checkpoints/ue/UE13_blueprint_map.py'),'"""Optional: Execute Python Script node output unreal_map; Config is Map<String,Integer>.\nRun inside an editor utility Blueprint. Inspect a=1, b=2; change b and rerun.\nNo scene edits. The execution-success Boolean is separate from the data.\n"""\n'+mapCode+'\n');
sl=optional('K3','Import troubleshooting');
text(sl,'Missing module, nested failure, or a circular import?',94,233,1092,46,28,C.accent,true);
text(sl,'import sys\nimport unreal\nprint(unreal.get_interpreter_executable_path())\nprint("\\n".join(sys.path))',94,294,1092,160,26,C.ink,false,'Consolas');
text(sl,'Read the traceback. Check the loaded module’s __file__.\nUse package-qualified imports from Content/Python.\nInstall dependencies with the host interpreter during preparation.',94,466,1092,120,27);
text(sl,'Return to: A saved example, run inside Unreal (RUN)',94,602,1092,28,19,C.muted);
text(sl,'Which interpreter ran the failing import? Questions about discovery?',94,637,1092,35,23,C.accent,true);
notes(sl,'Run this diagnostic in Unreal. The first path identifies its Python interpreter; the remaining lines show import search locations. An IDE’s successful autocomplete does not prove that Unreal can import the module. If an import succeeds, print that module’s __file__ to verify which copy loaded. Read nested tracebacks before installing anything. Package-qualified imports avoid relying on a script folder added only by the IDE. Repeated imports are cached, and a circular import needs a dependency change. Keep the UI dependent on shared operations, not the other way around.','06–09, 27, 48.');
sl=optional('K4','Remote Control object paths');
text(sl,'Inside Unreal, after registering the course class:',94,233,1092,40,26,C.accent,true);
text(sl,'from remote_control_demo_functions import RemoteControlDemo\nobject_path = RemoteControlDemo.get_default_object().get_path_name()\nprint(object_path)',94,292,1092,133,24,C.ink,false,'Consolas');
text(sl,'Use the printed value as objectPath in the HTTP request.\nCheck HTTP status and ReturnValue, then inspect the operation’s result.\nThe classroom FBX bridge uses file requests instead.',94,443,1092,140,27);
text(sl,'Return to: Blender bridge (10D) or Karol course connections (K1)',94,602,1092,28,19,C.muted);
text(sl,'What does a successful ping prove? What remains untested?',94,637,1092,35,23,C.accent,true);
notes(sl,'This fragment requires the RemoteControlDemo class from the course module, imported and registered inside Unreal. Ask that registered class for its default object path. A copied Engine/PythonTypes path may not describe a class imported from a module. Use the discovered string in the request and check the response. A ping confirms that callable, not the correctness of an asset import. Our file-based bridge does not require this Remote Control setup.','41–47.','Optional alternative transport. Requires the course class and Remote Control API plugin/server. Do not run this fragment as a standalone checkpoint without the supplied module.');
sl=optional('K5','Progress, cancellation and Undo');
const vals=[['Mechanism','What it establishes'],['Progress','Work completed relative to the declared total'],['Cancellation','Stops future work when the loop checks'],['Transaction / Undo','Restores supported editor changes'],['Restore and reimport','Recovers exported or imported asset revisions']];
let table=sl.tables.add({rows:5,columns:2,left:94,top:238,width:1092,height:305,values:vals});table.borders.assign({fill:'#8D8994',width:.8});for(let r=0;r<5;r++)for(let c=0;c<2;c++){let cell=table.getCell(r,c);cell.fill=r===0?C.bg:'#FFFFFF';cell.text.style={typeface:'Arial',fontSize:24,color:C.ink,bold:r===0};}
text(sl,'A Cancel button needs a cooperative check between work units.',94,568,1092,35,25);
text(sl,'Return to: Recovery and accessibility (15B)',94,608,1092,26,19,C.muted);
text(sl,'After item 3 of 10, what remains changed if the artist cancels?',94,641,1092,32,23,C.accent,true);
notes(sl,'ScopedSlowTask can display progress and a Cancel button. The loop still has to check should_cancel between work units. Cancelling leaves completed edits in place. Put supported batch edits inside one meaningful ScopedEditorTransaction when one Undo should cover them. Verify that the affected operation participates in transactions. FBX exports, imports and file writes require an explicit recovery procedure. In our bridge, publish the baseline under the same asset name. What questions do you have about the recovery your tool promises?','33–34, 45.');
sl=optional('K6','Tests that detect failure');
text(sl,'The discovered script must call its check.',94,232,1092,40,28,C.accent,true);
text(sl,'import unreal\n\ndef test_upper():\n    actual = "foo".upper()\n    if actual != "FOO":\n        unreal.log_error(f"Expected FOO, got {actual!r}")\n\nif __name__ == "__main__":\n    test_upper()',94,281,1092,280,24,C.ink,false,'Consolas');
text(sl,'Temporarily expect BAR. Confirm failure, then restore FOO.',94,567,1092,32,24);
text(sl,'Return to: A test produces the next question (16E)',94,606,1092,26,19,C.muted);
text(sl,'Would a green result prove that an uncalled check passed?',94,640,1092,32,23,C.accent,true);
notes(sl,'Save this as a test_ Python script in a discoverable folder for the course’s Python Automation Test setup. Defining the function alone does not run it; the final call matters. First confirm the successful expectation. Temporarily change the expected value to BAR and confirm the runner detects the logged failure. Restore FOO afterward. Keep normal, empty and failure cases isolated. An excluded check is skipped, not passed. Expected-log rules must match the real tested operation; emitting a synthetic matching warning would not prove that operation ran. What would your tool’s meaningful failure case be?','35–38.','Optional Unreal Python Automation Test setup. Do not leave the deliberate failure in the final script. This is an Unreal runner example, distinct from the bridge’s ordinary Python unittest suite.');
// Update physical numbers after inserting K2; original stable review anchors survive.
for(const [i,s] of p.slides.items.entries()){const num=s.shapes.items.find(t=>t.position.left===1130&&t.position.top===677);if(num)num.text=String(i+1);else if(additions.some(a=>a.slideId===s.id))text(s,String(i+1),1130,677,75,23,15,C.muted);}
await fs.mkdir('../previews',{recursive:true});await fs.mkdir('../output',{recursive:true});
const changedSet=new Set(changes.map(c=>original[c.source-1].id));for(const a of additions)changedSet.add(a.slideId);
for(const [i,s] of p.slides.items.entries()) {await fs.writeFile(`../previews/slide-${String(i+1).padStart(3,'0')}.png`,new Uint8Array(await (await s.export({format:'png',scale:1})).arrayBuffer()));if((i+1)%20===0)console.log('Rendered',i+1);}
const records=p.slides.items.map((s,i)=>({number:i+1,id:s.id,hidden:s.hidden,changed:changedSet.has(s.id),source:original.findIndex(o=>o.id===s.id)+1||null,text:s.shapes.items.map(t=>String(t.text)),notes:s.speakerNotes.text}));
await fs.writeFile('../slide-map.json',JSON.stringify({source,changes,additions,slides:records},null,2));
await (await PresentationFile.exportPptx(p)).save('candidate.pptx');
const skill='C:/Users/antho/.codex/plugins/cache/openai-primary-runtime/presentations/26.1011.11113/skills/presentations';
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const tableOwners=p.slides.items.flatMap((s,i)=>s.tables.items.length?[i+1]:[]);
const result=await finalizePresentation({workspaceDir:work,candidatePath:path.join(work,'.build/candidate.pptx'),finalPath:path.join(work,'output/Week_7_Python_in_Unreal_v14.pptx'),pythonExecutable:'C:/Users/antho/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit',...tableOwners.flatMap(n=>['--require-native-table-slide',String(n)])],fontPolicy:{basis:'reference',families:['Arial','Consolas'],referencePath:source,referenceSha256:crypto.createHash('sha256').update(await fs.readFile(source)).digest('hex')},requiredNativeTableOwnerSlides:tableOwners,verifyArtifactToolImport:true,receiptPath:path.join(work,'.build/validation.json')});console.log(JSON.stringify({slides:p.slides.items.length,live:p.slides.items.filter(s=>!s.hidden).length,output:result.finalPath}));





