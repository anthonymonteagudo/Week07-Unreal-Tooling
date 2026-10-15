import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {S,slides,sections,timing,bindings} from './content.mjs';
const work=path.resolve('..');
const skill='C:/Users/antho/.codex/plugins/cache/openai-primary-runtime/presentations/26.1011.11113/skills/presentations';
const source=path.resolve('../../CheckpointDeck20261013/output/Week_7_Runnable_API_Checkpoints_v8.pptx');
const tableOwners=slides.flatMap((s,i)=>s.table?[i+2]:[]);
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const version=process.env.DECK_VERSION||'v9',file=`Week_7_Materials_and_Walkthroughs_${version}.pptx`;
const result=await finalizePresentation({workspaceDir:work,candidatePath:path.join(work,'.build/candidate.pptx'),finalPath:path.join(work,'output',file),pythonExecutable:'C:/Users/antho/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit',...tableOwners.flatMap(n=>['--require-native-table-slide',String(n)])],fontPolicy:{basis:'design',families:['Arial','Consolas']},requiredNativeTableOwnerSlides:tableOwners,verifyArtifactToolImport:true,receiptPath:path.join(work,'.build',`validation_${version}.json`)});
console.log(JSON.stringify({slides:slides.length+1,live:1+slides.filter(s=>!s.hidden).length,images:slides.filter(s=>s.image||s.pair||s.strips).length,output:result.finalPath}));
await fs.writeFile('../slide_sources.json',JSON.stringify({sourceDeck:source,sourceKeys:S,slides,timing,sections},null,2));

await fs.writeFile('../timing.json',JSON.stringify(timing,null,2));


await fs.writeFile('../bindings.json',JSON.stringify(bindings,null,2));




