document.querySelectorAll('.navbar-toggler').forEach(toggler => {
    toggler.addEventListener('click', () => {
        document.querySelector('.navbar-collapse').classList.toggle('show');
    });
});

document.querySelectorAll('.search-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        document.querySelector('#search-form').submit();
    });
});