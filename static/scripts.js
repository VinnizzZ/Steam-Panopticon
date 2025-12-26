document.addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById('search-btn');
    const searchInput = document.getElementById('search-input');

    // Função para executar a busca
    function performSearch() {
        const query = searchInput.value;
        if (query.trim() !== "") {
            alert("Buscando por: " + query);
            // Aqui você poderia redirecionar para: 
            // window.location.href = `/search?q=${query}`;
        } else {
            alert("Por favor, digite algo para buscar.");
        }
    }

    // Evento de clique no botão azul (lupa)
    searchBtn.addEventListener('click', performSearch);

    // Permitir buscar ao apertar "Enter"
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
});