(function () {
  'use strict';

  // Cabeçalho ganha fundo ao rolar
  var header = document.querySelector('[data-header]');
  function onScroll() {
    var rolou = window.scrollY > 12;
    header.classList.toggle('bg-marfim/90', rolou);
    header.classList.toggle('backdrop-blur-md', rolou);
    header.classList.toggle('shadow-sm', rolou);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Menu mobile
  var toggle = document.querySelector('[data-menu-toggle]');
  var menu = document.getElementById('menu');
  var bar1 = document.querySelector('[data-bar-1]');
  var bar2 = document.querySelector('[data-bar-2]');
  function setMenu(aberto) {
    toggle.setAttribute('aria-expanded', String(aberto));
    toggle.setAttribute('aria-label', aberto ? 'Fechar menu' : 'Abrir menu');
    menu.classList.toggle('hidden', !aberto);
    menu.classList.toggle('flex', aberto);
    bar1.classList.toggle('-translate-y-1', !aberto);
    bar1.classList.toggle('rotate-45', aberto);
    bar2.classList.toggle('translate-y-1', !aberto);
    bar2.classList.toggle('-rotate-45', aberto);
    if (aberto) header.classList.add('bg-marfim');
    else header.classList.remove('bg-marfim');
  }
  toggle.addEventListener('click', function () {
    setMenu(toggle.getAttribute('aria-expanded') !== 'true');
  });
  menu.addEventListener('click', function (e) {
    if (e.target.closest('a') && window.innerWidth < 1024) setMenu(false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') { setMenu(false); toggle.focus(); }
  });

  // Animação de entrada
  var itens = document.querySelectorAll('.revelar');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('visivel'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    itens.forEach(function (el) { io.observe(el); });
  } else {
    itens.forEach(function (el) { el.classList.add('visivel'); });
  }

  // Ano corrente no rodapé
  var ano = document.querySelector('[data-ano]');
  if (ano) ano.textContent = new Date().getFullYear();
})();
