import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';

// Real rectangular crops only. No image generation, retouching, or UI reconstruction.
export async function materialRelationships({root, sharp, colors:c, esc}) {
 const epic='https://dev.epicgames.com/documentation/en-us/unreal-engine/essential-unreal-engine-material-concepts?application_version=5.7';
 const instances='https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-material-instance-editor-ui?application_version=5.7';
 const imageRoot='../Slides/Week02/Review/MaterialsGuide/UE_Images/';
 const urls=JSON.parse(fs.readFileSync(path.join(root,imageRoot,'sources.json'),'utf8'));
 const specs=[
  ['base-color','Base Color',imageRoot+'walnut-floor-material.png',[543,133,66,66],'Magnified Texture Sample preview; not a full-resolution texture export.'],
  ['roughness','Roughness',imageRoot+'simple-material.png',[322,225,47,46],'Magnified Texture Sample preview from the simpler walnut graph.'],
  ['normal','Normal map',imageRoot+'walnut-floor-material.png',[543,408,66,66],'Magnified normal Texture Sample preview. Its blue appearance is not an import-validity test.'],
  ['uv-layout','UV layout','Reference/week2-uv-source.png',[1135,1067,735,735],'Separate headphone-mesh UV example, retained from current slide 54. Not the walnut floor UVs.'],
  ['material-graph','Material graph',imageRoot+'walnut-floor-material.png',[322,0,689,502],'The real M_WalnutFloor graph, including TexCoord, tiling, texture samples, and material inputs.'],
  ['assignment','Mesh assignment',imageRoot+'drag-drop.png',[0,0,706,388],'Original Epic drag-and-drop illustration. Its existing yellow arrow remains intact.'],
  ['instance','Instance controls',imageRoot+'override-params.png',[12,198,332,67],'Separate Material Instance example, cropped to the Roughness override. Not an asserted instance of M_WalnutFloor.'],
  ['surface','Rendered surface',imageRoot+'drag-drop.png',[512,0,194,120],'Unretouched floor crop from the same assignment image. A displayed example, not a newly rendered frame.']
 ];
 const images={},records=[];
 const dir='Diagrams/MaterialImages';fs.mkdirSync(path.join(root,dir),{recursive:true});
 for(const [id,title,source,bounds,note] of specs){
  const bytes=fs.readFileSync(path.join(root,source));
  const meta=await sharp(bytes).metadata();
  const [left,top,width,height]=bounds;
  if(left+width>meta.width||top+height>meta.height)throw Error(`Invalid crop: ${id}`);
  const cropped=await sharp(bytes).extract({left,top,width,height}).png().toBuffer();
  const file=`${dir}/${id}.png`;fs.writeFileSync(path.join(root,file),cropped);
  images[id]='data:image/png;base64,'+cropped.toString('base64');
  records.push({id,title,file,source,source_sha256:createHash('sha256').update(bytes).digest('hex'),source_size:[meta.width,meta.height],crop_xywh:bounds,note,
   source_url:id==='uv-layout'?'https://www.artstation.com/ib_art':urls[path.basename(source)],
   source_page:id==='uv-layout'?'../Slides/Week02/ReviewRefined20260909/index.html#slide-54':id==='instance'?instances:epic,
   credit:id==='uv-layout'?'Existing course deck, slide 54; displayed source credit: artstation.com/ib_art. Original work URL, author identity beyond this handle, license, and software/version are unconfirmed.':'Epic Games, Unreal Engine documentation. Existing source images retrieved September 8, 2026; documentation references UE 5.7, screenshot build not established.',
   rights:'Retained source imagery with its attribution; no new open-content license claimed.'});
 }
 const label=(x,y,s,size=24,color=c.ink,weight=700)=>`<text x="${x}" y="${y}" font-family="Arial, sans-serif" font-size="${size}" font-weight="${weight}" fill="${color}">${esc(s)}</text>`;
 const pic=(id,x,y,w,h)=>`<image data-crop="${id}" x="${x}" y="${y}" width="${w}" height="${h}" preserveAspectRatio="xMidYMid meet" href="${images[id]}"/>`;
 const arrow=(d,optional=false)=>`<path class="connector${optional?' optional':''}" d="${d}" fill="none" stroke="${optional?c.accent:c.ink}" stroke-width="${optional?4:6}" stroke-linecap="round" stroke-linejoin="round" ${optional?'stroke-dasharray="10 9"':''} marker-end="url(#${optional?'optional-arrow':'main-arrow'})"/>`;
 const definitions=`<defs>${[['main-arrow',c.ink],['optional-arrow',c.accent]].map(([id,color])=>`<marker id="${id}" markerWidth="24" markerHeight="22" refX="22" refY="11" markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0 24 11 0 22Z" fill="${color}"/></marker>`).join('')}</defs>`;
 const title='Material → surface';
 const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720" role="img" aria-labelledby="title desc"><title id="title">${esc(title)}</title><desc id="desc">Real cropped texture samples and a separately identified UV layout illustrate inputs to a Unreal Material graph. A Material can be assigned directly to a mesh, or an optional instance can inherit its graph and override exposed parameters. The UE renderer produces the displayed surface using the chosen material, mesh, and scene context. The instance controls are a separate example. Arrows describe relationships, not one continuous captured workflow.</desc>${definitions}
 ${arrow('M260 284H336')}${arrow('M752 284H856')}
 ${arrow('M1092 385V405')}${arrow('M1092 468V508')}
 ${arrow('M552 470V528',true)}
 ${arrow('M740 624H816Q824 624 824 616V416Q824 408 832 408H900Q908 408 908 400V384',true)}
 ${label(32,56,title,40)}
 ${label(32,132,'Inputs',32)}${label(352,132,'Material graph',32)}${label(872,132,'Mesh assignment',32)}
 ${pic('base-color',32,172,96,96)}${pic('roughness',152,172,96,96)}
 ${label(32,302,'Base Color',20)}${label(152,302,'Roughness',20)}
 ${pic('normal',32,344,96,96)}${pic('uv-layout',152,344,96,96)}
 ${label(32,474,'Normal map',18)}${label(160,474,'Mesh UVs*',20)}
 ${pic('material-graph',352,172,400,292)}${label(776,258,'assign',20,c.ink,400)}
 ${pic('assignment',872,172,376,207)}
 ${label(572,504,'inheritance',20,c.accent,400)}
 ${label(396,560,'Instance* · optional',26)}${pic('instance',396,584,344,88)}
 <rect x="944" y="412" width="296" height="52" rx="8" fill="none" stroke="${c.ink}" stroke-width="3"/>${label(1011,447,'UE renderer',24)}
 ${pic('surface',944,516,296,183)}
 ${label(32,656,'* Separate examples',20,c.muted,400)}
 </svg>`;
 return {
  id:'material-relationships',title,slides:[100,102,104],svg_source:svg,
  use:'Current slide 100: use this image-led relationship overview, reveal the main route first, then the optional instance branch. Current slide 102: revisit the parent and assignment distinction. On 104, return briefly to the normal-map input before the actual normals comparison.',
  method:'Original transparent SVG composition using eight unretouched crops of real source images. The UV layout and instance controls are separate examples. No generated UI or reconstructed rendering.',
  transparent:true,revision:'2026-09-09 · concise labels and real imagery',
  context:[
   'The PNG contains short labels and relationships. Its surrounding canvas is genuinely transparent; opaque screenshot rectangles and the checker pattern inside the UV example are original image content.',
   'This is a relationship overview, not a single captured asset build. The walnut material, node previews, assignment, and displayed floor come from Epic’s related documentation examples. The UV layout belongs to a headphone mesh in current slide 54. The instance crop shows a different material’s Roughness override. Asterisks identify these separate examples in the diagram.',
   'UV coordinates belong to the mesh’s attribute data in this example; the material uses them to locate texture samples. They are not another bitmap texture, nor the only possible way to generate sampling coordinates. The screenshot itself retains the TexCoord-to-texture connections.',
   'The solid route shows a Material assigned directly. Dashed arrows show the optional instance route: an instance inherits the parent graph, may override exposed parameters, and may be selected for assignment. A texture swap is only exposed when the parent supports it. The arrows describe relationships, not an exact GPU execution order.',
   'The UE renderer remains a closed box here. Compilation, shader execution, geometry, lighting, camera, and display processing are discussed in narration rather than expanded into extra diagram nodes. Assigning a material does not bake a texture into the mesh.',
   'The small crops support recognition at lecture scale. Use the individual originals below or the live editor to read pins and values. The texture images are small sample-node previews, not full-resolution texture assets. No artificial detail was added.'
  ],
  script:'Let’s follow the solid route first. These images contain stored texture data. The UV layout shows the kind of coordinates that tell the material where to sample. That UV example belongs to a different mesh; we are comparing the roles here. In the Unreal graph, those samples and other values contribute to surface properties. We can assign the Material to a mesh. Unreal then draws it using the mesh and the scene’s lighting and camera. We will keep that renderer box closed today.\n\nNow follow the dashed branch. An instance inherits its parent’s graph and gives us controls for the parameters the parent exposes. The control shown here is a separate example of that interface. We can assign an instance instead of the parent Material. In the museum, a useful first check is to identify exactly which Material or instance the object is using before changing a texture.\n\nIf the pattern is the right image but appears stretched, which relationship would you inspect first, and what evidence would distinguish that from the wrong texture being assigned?',
  rationale:'The real crops give unfamiliar terms a visible referent. The unbroken main route supports a first reading; the dashed branch adds one optional relationship afterwards. Minimal labels let the explanation live in speech and notes. The question asks for an inspection, not a guessed diagnosis.',
  sources:[epic,instances,'https://dev.epicgames.com/documentation/en-us/unreal-engine/using-uv-channels-with-static-meshes-in-unreal-engine'],
  image_sources:records,
  previous_png:'Reference/material-relationships-before.png'
 };
}
