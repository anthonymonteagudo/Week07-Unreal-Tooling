import fs from 'node:fs';
export {catalog,checkpoint} from '../../UnrealFoundations20261013/.build/content.mjs';
const prior=JSON.parse(fs.readFileSync(new URL('../../UnrealFoundations20261013/slide_sources.json',import.meta.url),'utf8'));
export const S={...prior.sourceKeys},sections=structuredClone(prior.sections),timing=prior.timing;
const all=prior.slides.map((s,i)=>({...structuredClone(s),sourceNumber:i+2}));
const by=id=>all.find(s=>s.id===id);
Object.assign(S,{
 crayta:'https://www.unrealengine.com/events/unreal-fest-europe-2019/using-python-to-streamline-asset-workflows-for-a-small-team',
 craytaVideo:'https://www.youtube.com/watch?v=FOSwlDQY6N0',
 m2:'https://www.youtube.com/watch?v=MjjkWH0eT3U',
 scriptEditor:'https://github.com/leixingyu/unrealScriptEditor',
 scriptEditorFork:'https://github.com/hannesdelbeke/unreal-script-editor',
 ayon:'https://help.ayon.app/en/help/articles/2228078-working-with-unreal-in-ayon',
 ayonCode:'https://github.com/ynput/ayon-unreal',
 ayonPython:'https://docs.ayon.dev/ayon-unreal/latest/autoapi/client/ayon_unreal/api/pipeline.html',
 samples:'https://github.com/EpicGames/PythonSamples'
});
const newSlide=(id,title,bullets,resource,label,notes,question)=>({id,title,bullets,resource,resourceLabel:label,notes,question,section:'python',tag:'01  Python in Unreal',refs:[resource],local:[],facilitation:'Open the linked primary source before class. Showcase only; no installation or new live host test was performed.'});
const extra=[
 newSlide('PROD1','Python in production: Crayta',[
  'Unit 2 Games needed an asset workflow that a small team could sustain.',
  'Marcus White describes Python-based importing and asset conditioning in Unreal.',
  'Our connection: a repeatable script can apply the same checks to many assets.'
 ],'crayta','Unreal Fest Europe 2019: talk and slides',
 'This is a game-production example from Unit 2 Games, presented by Marcus White at Unreal Fest Europe 2019. The documented problem is a small team facing large asset demands. The talk describes a Python workflow for importing and conditioning assets in Unreal. Our classroom connection is repeatability: the selection, properties and checks we are about to learn can become steps in an asset pipeline. That connection is our interpretation, not a claim that our classroom script reproduces their implementation.',
 'Which repeated asset task would you want a script to handle?'),
 newSlide('TOOL1','Available tool: Unreal Script Editor',[
  'A Python/Qt script editor with file and temporary-script support.',
  'Provides syntax highlighting and editing shortcuts inside an Unreal workflow.',
  'Study how a familiar artist interface launches and organizes Python operations.'
 ],'scriptEditor','Source and UI preview: leixingyu / unrealScriptEditor',
 'This is a downloadable open-source tool, rather than a short teaching snippet. The repository includes the UI preview and launch instructions. It credits the original script editor and links the related Hannes Delbeke plugin. Version 0.0.3 and later use PySide6. The README marks autocomplete as unfinished, so do not promise that feature. A Qt window is not proof of native Slate docking. Open the creator’s preview to show the interface. We have not installed or tested this tool against our Unreal 5.7 classroom project.',
 'What does a script editor add beyond a one-line console?'),
 newSlide('PROD2','Python in production: shot setup',[
  'M2 Animation uses Python to integrate Unreal into a studio pipeline.',
  'ShotGrid data drives automatic level and sequence creation.',
  'A custom interface manages Movie Render Queue presets and rendering.'
 ],'m2','Christophe Bardoux: Unreal Fest Bali 2025',
 'Christophe Bardoux describes M2 Animation’s workflow in this official Unreal Fest recording. Focus on automatic shot management and the Movie Render Queue interface. The talk also includes Maya exports, but our colleagues will demonstrate that subject. The important connection here is that external data can drive Unreal objects and saved settings, and artists can use those operations through an interface. This is a production case study, not a claim that the studio’s internal tools are publicly downloadable.',
 'What information would a script need to build one shot?'),
 newSlide('TOOL2','Available toolkit: AYON for Unreal',[
  'Artist tools include Loader, Publisher and Scene Inventory.',
  'Sequence-building and render tools support shot workflows.',
  'The public Python integration shows how these tools connect to Unreal.'
 ],'ayon','Artist guide: screenshots and workflow steps',
 'AYON is a broader production system with an Unreal integration. Show the Loader or Publisher screenshot in the artist guide, then the public client/ayon_unreal source. The Python integration works with an Unreal plugin; this is not a claim that the whole platform is pure Python. It requires an AYON environment and configuration, so this is a possibility showcase rather than an in-class installation. Ask students to identify the input, operation and evidence of success in a finished artist tool.',
 'Where do you see selection, validation and feedback in this interface?'),
 newSlide('SAMPLES','Explore further: Epic Python samples',[
  'Browse the public PythonSamples repository for complete examples.',
  'Compare a sample’s API calls with documentation for your engine version.',
  'Read prerequisites and intended scope before adapting a script.'
 ],'samples','Epic Games: PythonSamples source repository',
 'These are example scripts rather than a packaged artist-facing application. Keep them distinct from the Script Editor and AYON toolkits. Use them for further study after students can identify the host, object, parameters and return value in a short call.',
 'Which small operation could become your own tool?')
];
extra.find(s=>s.id==='TOOL1').refs.push('scriptEditorFork');
extra.find(s=>s.id==='TOOL2').refs.push('ayonCode','ayonPython');
const moved=['S1A','MAT2','09I','MAT3','09','09F','08A','09J','09D','BL02','10','BR-PARITY','10C','10A','UE12'];
for(const id of moved){by(id).hidden=true;by(id).facilitation='Optional depth. Material tools and Maya bridging are covered by colleagues; keep this as a reference, not a duplicate instructor demonstration.';}
extra.find(s=>s.id==='SAMPLES').hidden=true;
sections.blender.name='02  Brief Blender bridge demo';
sections.contributors.name='03  Colleague demonstrations';
by('SB').title='Brief demo\nBlender to Unreal';
by('SB').tag=sections.blender.name;
by('SB').subtitle='The same Python language, a different application API.';
by('SB').next='One Blender selection example, one publish/revision, then colleague demos.';
by('SB').notes='We have focused on Python inside Unreal. Before I hand over, here is a short comparison: Blender also exposes its scene through Python, using bpy. I will inspect one selected object, then send a geometry revision to Unreal. Our colleagues will take us further into materials and a Maya bridge.';
by('SB').facilitation='Keep this as the final instructor demo immediately before the colleague handoff.';
by('BL01').tag=sections.blender.name;
by('BL01').explain='bpy.context.selected_objects supplies Blender Objects. Unreal uses its own editor APIs.';
const bridge=by('10D'), sourceNumber=bridge.sourceNumber;
Object.keys(bridge).forEach(k=>delete bridge[k]);
Object.assign(bridge,{id:'10D',sourceNumber,title:'Blender bridge: one geometry revision',section:'blender',tag:sections.blender.name,
 split:true,image:'Week07UnrealPython/Docs/Bridge/UI-Rehearsal/01-blender-baseline.png',
 bullets:['Select one mesh. Publish & Send to Unreal.','Raise the roof 0.4 m. Send the same asset name.','Verify both blue instances update; placement and materials stay.'],
 caption:'Recorded Blender UI reference. Geometry revision; materials stay in Unreal.',
 question:'Reset: publish the baseline mesh again using the same asset name.',
 refs:[],local:['Week07UnrealPython/Docs/Bridge/UI-Rehearsal/verification.json','Week07UnrealPython/Docs/Bridge/README.md'],
 notes:'This is the short demonstration before the handoff. Start with the prepared Blender mesh, in Object Mode, and the Unreal bridge comparison map. Publish as SM_Compare_Blender and wait for Imported. Use the prepared revised source or raise only the roof vertices by 0.4 metres along Blender Z, return to Object Mode, and publish under the same name. The two blue Unreal instances should update from 180 to 220 centimetres high. Verify their placement and existing materials. Publish the baseline again to restore the shared asset. The Maya objects are comparison fixtures; do not run the Maya publisher in this portion.',
 facilitation:'Use the unified testing walkthrough. Resolve the recent receiver.json access-denied issue before a live send. A fresh bridge success has not been established in this revision. If blocked, use the recorded UI rehearsal and label it as recorded. Do not add a debugging detour to the handoff.'});
by('09K').section='python';by('09K').tag='01  Python in Unreal';by('09K').title='Python in Unreal: questions';
by('11').tag=sections.contributors.name;by('11').title='Colleague demonstrations';
by('11').subtitle='Material tools in Unreal and Maya-to-Unreal workflows';
by('11').next='Watch for the input, the API operation and the result in the editor.';
by('11').notes='We have seen how Python accesses Unreal objects and how a small Blender revision reaches the editor. Now our colleagues will showcase their tools, including material work in Unreal and a Maya bridge. As you watch, connect the interface to the inputs, API operations and evidence of success we just discussed.';
by('02').table[1][1]='01 Python in Unreal, then 02 Brief Blender bridge demo';
by('02').table[2][1]='03 Colleague demonstrations';
by('02').bullets=['Unreal fundamentals first. Blender bridge closes the introduction.'];
const live=['02','S1','03','04','PROD1','DOCS','VSC1','VSC2','CALL','07','UE02R','RUN','TOOL1','07C','06A','UE04','UE04R','PROD2','MAT1','09G','UE05R','09H','TOOL2','07A','09K','SB','BL01','10D'];
const combined=[...all,...extra],map=new Map(combined.map(s=>[s.id,s]));
export const slides=[...live.map(id=>map.get(id)),...combined.filter(s=>!live.includes(s.id)&&!s.hidden),...combined.filter(s=>s.hidden)];
export const bindings=slides.flatMap((s,i)=>s.checkpoint?[{slide:i+2,anchor:s.id,...s.checkpoint,hidden:!!s.hidden}]:[]);
