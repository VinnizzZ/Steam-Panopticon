document.addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById('search-btn');
    const searchInput = document.getElementById('search-input');

    function performSearch() {
        const query = searchInput.value.trim();
        
        if (query !== "") {
            // Redireciona para /search?q=nome_do_jogo
            window.location.href = `/search?q=${encodeURIComponent(query)}`;
        } else {
            alert("Por favor, digite algo para buscar.");
        }
    }

    searchBtn.addEventListener('click', performSearch);

    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
});