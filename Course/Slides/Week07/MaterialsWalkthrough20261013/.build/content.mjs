import {S as oldS,slides as oldSlides,sections,catalog,checkpoint,timing as oldTiming} from '../../CheckpointDeck20261013/.build/content.mjs';
export {sections,catalog,checkpoint};
export const S={...oldS,
 textureUI:'https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-asset-editor-in-unreal-engine?application_version=5.7',
 instanceUI:'https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-material-instance-editor-ui?application_version=5.7',
 mayaAssign:'https://help.autodesk.com/cloudhelp/2027/ENU/Maya-LightingShading/files/GUID-D41AF807-F7CB-447E-BACC-7F0867C14E8D.htm',
 blenderAssign:'https://docs.blender.org/manual/en/latest/render/materials/assignment.html'};
const base=oldSlides.map((s,i)=>({...structuredClone(s),sourceNumber:i+2}));
const make=(id,title,section,fields,notes,refs)=>({id,title,section,tag:sections[section].name,...fields,notes,refs,local:['Course/Slides/Week07/MaterialsWalkthrough20261013/walkthrough.html'],facilitation:'Open the matching walkthrough for the exact UI locations, manual steps and expected evidence.'});
const textures=make('MAT1','Texture settings: inspect first','python',{
 table:[['Texture role','sRGB','Compression'],['BaseColor','On','Prepared color texture'],['Normal','Off','Normalmap'],['ORM','Off','Prepared data texture']],
 caption:'Content Browser: open texture > Details. Search sRGB or Compression Settings.',
 question:'Which other materials could use this same texture?'
},'Open one prepared texture. In its Details panel, Texture contains sRGB, and Compression contains Compression Settings. Our tool reads these properties and blocks unsuitable inputs. It does not repair or save shared textures. Base color is color data. Normal and packed ORM are data maps. UE06 now checks the same _Normal suffix as the material tool. A suffix identifies a candidate, not the image contents.', ['textureUI']);
const parameters=make('MAT2','Material instance: set texture inputs','demos',{
 table:[['Instance parameter','Prepared texture','Parent input'],['BaseColorTexture','T_Crate_BaseColor','Base Color'],['NormalTexture','T_Crate_Normal','Normal'],['ORMTexture','T_Crate_ORM','R: AO / G: Roughness / B: Metallic']],
 caption:'Right-click M_PreparedSurface > Create Material Instance. Open it > Parameter Groups.',
 question:'What does the parent graph decide that an instance cannot?'
},'Create a material instance from the prepared parent and open it. Enable each texture parameter override and choose the matching texture. The tool sets the same parent and three texture references, then reads them back. It does not build a shader graph or set separate roughness and metallic sliders. The prepared parent routes the ORM channels. Save intentionally after review; the demo backend leaves the new instance as a draft.', ['instanceUI']);
const slots=make('MAT3','Assign a material manually','demos',{
 table:[['Application','Where','Action'],['Unreal','Actor > mesh component > Details > Materials','Choose Element 0'],['Maya','Select mesh > Hypershade','Assign Material to Selection'],['Blender','Select object > Material Properties','Choose a material in its slot']],
 caption:'UE08 changes a component override. Changing the shared mesh default has wider scope.',
 question:'Which action changes only this placement?'
},'In Unreal select the target Actor, then its mesh component. In Details under Materials, choose the material in Element 0. That is the manual equivalent of set_material with slot zero. Inspect the protected cube and Undo once. Maya assigns a shading network through a shading group. Blender uses material slots, which may link to shared mesh data or the object. These are related tasks with different data models. The bridge preserves Unreal assignments rather than rebuilding source shader networks.', ['mayaAssign','blenderAssign']);
const dcc=make('MATS','Texture inputs in Maya and Blender','appendix',{
 table:[['Application','Image interpretation','Shader connection'],['Maya','File node > Attribute Editor > Color Space','Hypershade: connect to shader input'],['Blender','Image Texture > Color Space','Shader Editor: connect to shader input']],
 caption:'Use the image’s actual encoding. For non-color maps, use Raw / Non-Color as appropriate.',
 question:'Why is a material assignment different from transferring a shader graph?'
},'In Maya inspect the file node Color Space, and in Blender inspect Image Texture Color Space. Color textures need their correct input color space; raw data maps must avoid a color transform. Maya labels depend on the active OCIO configuration. Normal maps need a renderer-appropriate normal node. Packed ORM channels need separate routing. The bridge does not create these networks or convert them to an Unreal material.', ['mayaAssign','blenderAssign']);dcc.hidden=true;
export const slides=[];
for(const s of base){
 if(s.id==='04A'){s.hidden=true;s.section='appendix';continue;}
 if(s.id==='09G')slides.push(textures);
 if(s.id==='09I')slides.push(parameters);
 slides.push(s);
 if(s.id==='09I')slides.push(slots);
 if(s.id==='10D'){
  s.caption='Same mesh identity. Unreal material slots and Actor overrides are preserved.';
  s.notes+=' The receiver disables material and texture import. It restores existing Static Mesh material slots; existing Actors retain their overrides. The source shader graph is not transferred. See the dedicated Maya walkthrough for the matching manual revision and verification.';
  s.local=[...(s.local||[]),'Course/Slides/Week07/MaterialsWalkthrough20261013/maya.html'];
 }
}
const launcher=base.find(s=>s.id==='04A');launcher.hidden=true;launcher.section='appendix';slides.push(launcher,dcc);
const minutes=Object.fromEntries(oldTiming.map(t=>[t.id,t.minutes]));
delete minutes['04A'];minutes.MAT1=.75;minutes.MAT2=.75;minutes.MAT3=.75;
minutes['09K']-=.75;minutes['09D']-=.75;
let elapsed=0;
export const timing=[{id:'01',title:'Week 7',section:'intro'},...slides.filter(s=>!s.hidden)].map(s=>{
 const value=minutes[s.id];if(value===undefined)throw Error('Missing time '+s.id);
 const row={id:s.id,title:s.title,section:s.section,minutes:value,start:elapsed,end:elapsed+value};elapsed+=value;return row;
});
if(elapsed!==150)throw Error('Timing: '+elapsed);
for(const s of slides){
 s.tag=sections[s.section].name;
 const t=timing.find(t=>t.id===s.id);
 s.facilitation=(s.facilitation||'').replace(/ Time: .*$/s,'')+(t?` Time: ${t.minutes} min; elapsed ${t.start}–${t.end}.`:' Optional reference.');
}
export const bindings=slides.flatMap((s,i)=>s.checkpoint?[{slide:i+2,anchor:s.id,...s.checkpoint,hidden:!!s.hidden}]:[]);
