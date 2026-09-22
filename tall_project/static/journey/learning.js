(() => {
 const root=document.querySelector('.j-learning');if(!root)return;
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const image=root.querySelector('.j-parallax');let pending=false;
 function update(){pending=false;if(!image)return;if(reduced.matches){image.style.transform='none';return;}const rect=image.parentElement.getBoundingClientRect();if(rect.bottom>0&&rect.top<innerHeight){const shift=Math.max(-rect.height*.08,Math.min(rect.height*.08,-rect.top*.1));image.style.transform=`translate3d(0,${shift}px,0)`;}}
 addEventListener('scroll',()=>{if(!pending){pending=true;requestAnimationFrame(update);}},{passive:true});reduced.addEventListener('change',update);update();
})();
