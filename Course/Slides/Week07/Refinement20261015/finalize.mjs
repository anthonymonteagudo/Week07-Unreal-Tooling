import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
process.env.RUNTIME_NODE_MODULES='C:/Users/antho/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const skill='C:/Users/antho/.codex/plugins/cache/openai-primary-runtime/presentations/26.1011.11113/skills/presentations';
const inv=JSON.parse(await fs.readFile(path.join(dir,'source-inventory.json'),'utf8'));
const plan=JSON.parse(await fs.readFile(path.join(dir,'content-plan.json'),'utf8'));
const map=JSON.parse(await fs.readFile(path.join(dir,'slide-map.json'),'utf8'));
const newTables=plan.slides.filter(s=>s.table).map(s=>map.find(m=>m.key===s.id).number);
const oldTables=[2,13,14,23,26,28,45,46,67].map(n=>map.find(m=>m.key===n)?.number).filter(Boolean);
const owners=[...newTables,...oldTables];
const {finalizePresentation}=await import(pathToFileURL(skill+'/container_tools/artifact_tool_utils.mjs'));
const r=await finalizePresentation({workspaceDir:dir,candidatePath:path.join(dir,'build/candidate.pptx'),finalPath:path.join(dir,'output/Week 7 - Integrated UX and Asset Workflows v6.pptx'),pythonExecutable:'C:/Users/antho/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',integrityValidatorPath:skill+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:skill+'/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit',...owners.flatMap(n=>['--require-native-table-slide',String(n)])],requiredNativeTableOwnerSlides:owners,requiredNativeChartOwnerSlides:[],fontPolicy:{basis:'reference',families:['Neue Haas Grotesk Text Pro','Arial','Consolas'],referencePath:inv.source,referenceSha256:inv.sha256},verifyArtifactToolImport:true,receiptPath:path.join(dir,'qa/presentation-validation-v6.json')});
console.log(JSON.stringify({path:r.finalPath,integrity:r.packageIntegrity.status,layout:r.presentationLayout,bytes:r.byteCount}));


