/* Tzadik Azaria — V9.2. Menu, header, reveal, hero (stickers + vector path), lightbox, copy email. */
(()=>{const d=document,root=d.documentElement;root.classList.add('js');
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---- mobile menu ---- */
const menuButton=d.querySelector('.menu-toggle'),nav=d.querySelector('.nav');
const setBtn=()=>{if(menuButton)menuButton.textContent=menuButton.getAttribute('aria-expanded')==='true'?'Close':'Menu'};
function closeMenu(){nav?.classList.remove('is-open');menuButton?.setAttribute('aria-expanded','false');setBtn();d.body.classList.remove('menu-open')}
menuButton?.addEventListener('click',()=>{const open=menuButton.getAttribute('aria-expanded')!=='true';menuButton.setAttribute('aria-expanded',String(open));setBtn();nav.classList.toggle('is-open',open);d.body.classList.toggle('menu-open',open)});
nav?.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
d.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav?.classList.contains('is-open')){closeMenu();menuButton.focus()}});

/* ---- scroll reveal (content is visible without JS) ---- */
const rv=d.querySelectorAll('.rv');
if('IntersectionObserver' in window&&!reduce){const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{rootMargin:'0px 0px -8% 0px'});rv.forEach(el=>io.observe(el))}else rv.forEach(el=>el.classList.add('in'));

/* ---- hero: bézier path. The large middle anchor sets weight (up/down) and width (left/right) of "point of view." ---- */
const hero=d.getElementById('hero'),svg=hero?.querySelector('.vec');
if(hero&&svg){
 const NS='http://www.w3.org/2000/svg',path=svg.querySelector('.vp'),hl=svg.querySelector('.vh'),g=svg.querySelector('.vpts');
 const P={a0:[.04,.22],c0:[.18,.98],c1a:[.34,.92],a1:[.5,.62],c1b:[.66,.32],c2:[.84,.82],a2:[.96,.2]};
 const kind={a0:'a',a1:'a',a2:'a'},follow={a0:['c0'],a1:['c1a','c1b'],a2:['c2']};
 const clamp=(v,a,b)=>Math.min(b,Math.max(a,v));
 let W=0,H=0;const px=k=>[P[k][0]*W,P[k][1]*H];const els={},hits={};
 const selEl=hero.querySelector('.sel'),dimEl=hero.querySelector('.dim');
 const label=()=>{const wt=Math.round(900-600*clamp((P.a1[1]-.1)/.9,0,1)),st=Math.round(78+24*clamp((P.a1[0]-.25)/.5,0,1));return[wt,st]};
 function type(){if(!selEl)return;const[wt,st]=label();selEl.style.fontWeight=wt;selEl.style.fontStretch=st+'%';
  if(dimEl)dimEl.textContent=`Saira · wght ${wt} · wdth ${st}`;
  const key=hits.a1;if(key){key.setAttribute('aria-valuenow',wt);key.setAttribute('aria-valuetext',`weight ${wt}, width ${st}`)}}
 function move(k,nx,ny){const dx=nx-P[k][0],dy=ny-P[k][1];P[k]=[nx,ny];(follow[k]||[]).forEach(h=>{P[h]=[P[h][0]+dx,P[h][1]+dy]});draw()}
 Object.keys(P).forEach(k=>{const isA=kind[k]==='a';
  const shape=d.createElementNS(NS,isA?'rect':'circle');shape.setAttribute('class',isA?'a':'c');
  if(isA){const z=k==='a1'?13:10;shape.setAttribute('width',z);shape.setAttribute('height',z);shape.setAttribute('rx',1.5);if(k==='a1')shape.classList.add('key')}else shape.setAttribute('r',4.5);
  const hit=d.createElementNS(NS,'circle');hit.setAttribute('class','hit');hit.setAttribute('r',22);
  g.appendChild(shape);g.appendChild(hit);els[k]=shape;hits[k]=hit;
  let id=null;
  hit.addEventListener('pointerdown',e=>{id=e.pointerId;hit.setPointerCapture(id);hit.classList.add('on');e.preventDefault()});
  hit.addEventListener('pointermove',e=>{if(e.pointerId!==id)return;const r=svg.getBoundingClientRect();move(k,clamp((e.clientX-r.left)/W,-.04,1.04),clamp((e.clientY-r.top)/H,-.5,1.5))});
  const end=e=>{if(e.pointerId!==id)return;id=null;hit.classList.remove('on')};hit.addEventListener('pointerup',end);hit.addEventListener('pointercancel',end);
  if(k==='a1'){ // keyboard: arrows adjust weight (up/down) and width (left/right)
   hit.setAttribute('tabindex','0');hit.setAttribute('role','slider');hit.setAttribute('aria-label','Headline weight and width. Arrow keys adjust it.');
   hit.setAttribute('aria-valuemin','300');hit.setAttribute('aria-valuemax','900');
   hit.addEventListener('focus',()=>shape.classList.add('kf'));hit.addEventListener('blur',()=>shape.classList.remove('kf'));
   hit.addEventListener('keydown',e=>{const st=.05;let[x,y]=P.a1;
    if(e.key==='ArrowUp')y-=st;else if(e.key==='ArrowDown')y+=st;else if(e.key==='ArrowLeft')x-=st;else if(e.key==='ArrowRight')x+=st;else return;
    e.preventDefault();move('a1',clamp(x,.25,.75),clamp(y,.1,1))})
  }else{hit.setAttribute('aria-hidden','true')}
 });
 function draw(){type();
  const f=k=>px(k).map(v=>v.toFixed(1)).join(' ');
  path.setAttribute('d',`M${f('a0')} C${f('c0')} ${f('c1a')} ${f('a1')} C${f('c1b')} ${f('c2')} ${f('a2')}`);
  hl.setAttribute('d',`M${f('a0')} L${f('c0')} M${f('a1')} L${f('c1a')} M${f('a1')} L${f('c1b')} M${f('a2')} L${f('c2')}`);
  Object.keys(P).forEach(k=>{const[x,y]=px(k),c=els[k],h=hits[k];h.setAttribute('cx',x.toFixed(1));h.setAttribute('cy',y.toFixed(1));
   if(kind[k]==='a'){const z=k==='a1'?6.5:5;c.setAttribute('x',(x-z).toFixed(1));c.setAttribute('y',(y-z).toFixed(1))}else{c.setAttribute('cx',x.toFixed(1));c.setAttribute('cy',y.toFixed(1))}});}
 function layout(){const r=svg.getBoundingClientRect();W=r.width;H=r.height;svg.setAttribute('viewBox',`0 0 ${W} ${H}`);draw()}
 layout();addEventListener('resize',layout);if(d.fonts?.ready)d.fonts.ready.then(layout);
}

/* ---- header state ---- */
const h=d.getElementById('siteheader');if(h){const on=()=>h.classList.toggle('s',scrollY>20);on();addEventListener('scroll',on,{passive:true})}

/* ---- lightbox with previous / next ---- */
const dialog=d.querySelector('.lightbox');
if(dialog){
 const image=dialog.querySelector('.lightbox-inner img'),caption=dialog.querySelector('.lightbox-inner p');
 const items=[...d.querySelectorAll('[data-lightbox]')];let i=0,prevFocus=null;
 const prevB=dialog.querySelector('.lb-nav.prev'),nextB=dialog.querySelector('.lb-nav.next');
 const show=n=>{i=(n+items.length)%items.length;const im=items[i].querySelector('img');image.src=im.getAttribute('src');image.alt=im.alt;
  const fc=items[i].closest('figure')?.querySelector('figcaption');caption.textContent=`${i+1} / ${items.length} — ${im.alt}`};
 items.forEach((b,n)=>b.addEventListener('click',()=>{prevFocus=b;show(n);dialog.showModal();d.body.style.overflow='hidden'}));
 if(items.length<2){prevB?.remove();nextB?.remove()}
 prevB?.addEventListener('click',()=>show(i-1));nextB?.addEventListener('click',()=>show(i+1));
 dialog.addEventListener('keydown',e=>{if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1)});
 let tx=null;dialog.addEventListener('touchstart',e=>{tx=e.touches[0].clientX},{passive:true});dialog.addEventListener('touchend',e=>{if(tx===null)return;const dx=e.changedTouches[0].clientX-tx;tx=null;if(Math.abs(dx)>60&&items.length>1)show(i+(dx<0?1:-1))},{passive:true});
 const close=()=>dialog.close();dialog.querySelector('.lightbox-close').addEventListener('click',close);
 dialog.addEventListener('click',e=>{if(e.target===dialog||e.target.classList.contains('lightbox-inner'))close()});
 dialog.addEventListener('close',()=>{d.body.style.overflow='';prevFocus?.focus()});
}

/* ---- copy email ---- */
d.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',async()=>{
 const t=b.dataset.copy,o=b.textContent;
 try{await navigator.clipboard.writeText(t)}catch(e){const r=d.createRange();const a=b.parentElement.querySelector('a');r.selectNodeContents(a);const s=getSelection();s.removeAllRanges();s.addRange(r)}
 b.textContent='Copied';b.classList.add('done');setTimeout(()=>{b.textContent=o;b.classList.remove('done')},1800)}));
})();
