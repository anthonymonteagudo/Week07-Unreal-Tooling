import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const work=path.resolve('..');
const source=path.resolve('../../UnrealFirst20261013/output/Week_7_Python_in_Unreal_v13.pptx');
const p=await PresentationFile.importPptx(await FileBlob.load('candidate.pptx'));
const skill='C:/Users/antho/.codex/plugins/cache/openai-primary-runtime/presentations/26.1011.11113/skills/presentations';
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const tableOwners=p.slides.items.flatMap((s,i)=>s.tables.items.length?[i+1]:[]);
const result=await finalizePresentation({workspaceDir:work,candidatePath:path.join(work,'.build/candidate.pptx'),finalPath:path.join(work,'output/Week_7_Python_in_Unreal_v14.pptx'),pythonExecutable:'C:/Users/antho/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit',...tableOwners.flatMap(n=>['--require-native-table-slide',String(n)])],fontPolicy:{basis:'reference',families:['Arial','Consolas'],referencePath:source,referenceSha256:crypto.createHash('sha256').update(await fs.readFile(source)).digest('hex')},requiredNativeTableOwnerSlides:tableOwners,verifyArtifactToolImport:true,receiptPath:path.join(work,'.build/validation-final.json')});console.log(JSON.stringify({slides:p.slides.items.length,live:p.slides.items.filter(s=>!s.hidden).length,output:result.finalPath}));




