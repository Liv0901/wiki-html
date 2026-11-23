(function(){
  const slides=[...document.querySelectorAll('.slide')], stage=document.getElementById('stage');
  const count=document.getElementById('count'), bar=document.querySelector('#progress i');
  let cur=0;
  function fit(){ if(document.body.classList.contains('overview'))return;
    const s=Math.min(innerWidth/1300, innerHeight/740); stage.style.transform='scale('+s+')'; }
  function show(i){ cur=Math.max(0,Math.min(slides.length-1,i));
    slides.forEach((s,k)=>s.classList.toggle('active',k===cur));
    count.textContent=(cur+1)+' / '+slides.length; bar.style.width=((cur+1)/slides.length*100)+'%';
    if(location.hash!=='#'+(cur+1)) history.replaceState(null,'','#'+(cur+1)); }
  function toggleOverview(){ const on=document.body.classList.toggle('overview');
    if(on){stage.style.transform='none';} else {fit(); show(cur);} }
  document.addEventListener('keydown',e=>{
    if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' '){e.preventDefault();show(cur+1);}
    else if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();show(cur-1);}
    else if(e.key==='Home')show(0); else if(e.key==='End')show(slides.length-1);
    else if(e.key==='o'||e.key==='O')toggleOverview();
    else if(e.key==='f'||e.key==='F'){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen&&document.documentElement.requestFullscreen();}
    else if(e.key==='Escape'&&document.body.classList.contains('overview'))toggleOverview();
  });
  document.getElementById('prev').onclick=()=>show(cur-1);
  document.getElementById('next').onclick=()=>show(cur+1);
  document.getElementById('ov').onclick=toggleOverview;
  slides.forEach((s,k)=>s.addEventListener('click',()=>{ if(document.body.classList.contains('overview')){toggleOverview();show(k);} }));
  document.querySelectorAll('a[href="#src"]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();e.stopPropagation();show(slides.length-1);}));
  let x0=null; addEventListener('touchstart',e=>{x0=e.touches[0].clientX},{passive:true});
  addEventListener('touchend',e=>{ if(x0===null)return; const dx=e.changedTouches[0].clientX-x0; if(Math.abs(dx)>50)show(cur+(dx<0?1:-1)); x0=null; });
  addEventListener('resize',fit);
  const h=parseInt(location.hash.slice(1)); fit(); show(isNaN(h)?0:h-1);
})();
