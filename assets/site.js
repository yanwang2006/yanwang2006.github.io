'use strict';
const menu=document.querySelector('.menu-toggle');
const nav=document.querySelector('#navigation');
menu?.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open)});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav.classList.contains('open')){nav.classList.remove('open');menu.setAttribute('aria-expanded','false');menu.focus()}});
document.querySelector('#copyright-year').textContent=new Date().getFullYear();
const search=document.querySelector('#search');
if(search){
 const category=document.querySelector('#category'),year=document.querySelector('#year');
 const records=[...document.querySelectorAll('.record')];
 const text=records.map(r=>r.textContent.toLowerCase());
 document.querySelector('.filters').hidden=false;
 function filter(){
  const words=search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);let count=0;
  records.forEach((r,i)=>{const match=words.every(w=>text[i].includes(w))&&(!category.value||r.dataset.category===category.value)&&(!year.value||r.dataset.year===year.value);r.hidden=!match;if(match)count++});
  document.querySelectorAll('.record-group').forEach(g=>g.hidden=![...g.querySelectorAll('.record')].some(r=>!r.hidden));
  document.querySelector('#result-count').textContent=`${count} of ${records.length} records`;
  document.querySelector('.empty-state').hidden=count!==0;
 }
 search.addEventListener('input',filter);category.addEventListener('change',filter);year.addEventListener('change',filter);
 document.querySelector('#reset').addEventListener('click',()=>{search.value='';category.value='';year.value='';filter();search.focus()});
 document.querySelectorAll('.publication-nav a').forEach(a=>a.addEventListener('click',()=>{search.value='';category.value='';year.value='';filter()}));
}
