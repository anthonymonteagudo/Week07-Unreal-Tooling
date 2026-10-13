const input=document.querySelector('#search-input'),form=document.querySelector('.search'),results=document.querySelector('#search-results'),list=document.querySelector('#result-list'),content=document.querySelector('#page-content');
function search(){
  const query=input.value.trim().toLowerCase();
  if(!query){results.hidden=true;content.hidden=false;return}
  const terms=query.split(/\s+/);
  const found=(window.COURSE_INDEX||[]).filter(p=>terms.every(t=>(p.title+' '+p.summary+' '+p.text).toLowerCase().includes(t))).sort((a,b)=>Number(b.title.toLowerCase().includes(query))-Number(a.title.toLowerCase().includes(query)));
  list.replaceChildren();
  for(const p of found){const li=document.createElement('li'),h=document.createElement('h3'),a=document.createElement('a'),desc=document.createElement('p'),group=document.createElement('span');a.href=p.slug+'.html';a.textContent=p.title;desc.textContent=p.summary;group.textContent=p.group;group.className='result-group';h.append(a);li.append(group,h,desc);list.append(li)}
  document.querySelector('#search-count').textContent=found.length?found.length+' matching pages':'No matching pages. Try a shorter term such as “normal”, “UV”, or “Python”.';results.hidden=false;content.hidden=true;
}
form.addEventListener('submit',e=>{e.preventDefault();search();results.scrollIntoView({block:'start',behavior:'smooth'})});
input.addEventListener('input',search);
document.querySelector('#clear-search').addEventListener('click',()=>{input.value='';search();input.focus()});
