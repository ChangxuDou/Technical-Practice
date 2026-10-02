// Inline confirmation keeps the action visible and works without browser pop-ups.
document.querySelectorAll('[data-confirm]').forEach(button => {
  const original = button.textContent;
  button.addEventListener('click', event => {
    if (button.dataset.confirmed === 'yes') return;
    event.preventDefault();
    button.dataset.confirmed = 'yes';
    button.textContent = 'Click again to confirm';
    const message = document.createElement('p');
    message.className = 'fine';
    message.setAttribute('role', 'status');
    message.textContent = button.dataset.confirm;
    button.after(message);
    window.setTimeout(() => {
      delete button.dataset.confirmed;
      button.textContent = original;
      message.remove();
    }, 10000);
  });
});
const days=document.querySelector('[data-daily]');if(days){const calc=()=>document.querySelector('#estimated').textContent='€'+(Number(days.value)*Number(days.dataset.daily)).toFixed(2);days.addEventListener('change',calc);calc()}
document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(b.dataset.copy);b.textContent='Copied';setTimeout(()=>b.textContent=b.dataset.copy,1200)}catch{b.textContent=b.dataset.copy}}));
