function debounce(fn, delay) {
    let timer;

    return function (...args) {
        clearTimeout(timer);

        timer = setTimeout(() => {
            fn.apply(this, args);
        }, delay);
    };
}


class SearchSelect {

    constructor(wrapper) {

        this.wrapper = wrapper;

        this.input = wrapper.querySelector(
            ".search-select-input"
        );

        this.results = wrapper.querySelector(
            ".search-select-results"
        );

        this.url = wrapper.dataset.searchUrl;

        this.hiddenInputId = wrapper.dataset.hiddenInput;

        this.hiddenInput = document.getElementById(
            this.hiddenInputId
        );

        this.search = debounce(
            this.searchItems.bind(this),
            200
        );

        this.init();
    }


    init() {

        // Quand l'utilisateur clique/focus sur le champ
        this.input.addEventListener("focus", () => {

            this.searchItems(
                this.input.value.trim()
            );

        });


        // Quand l'utilisateur tape
        this.input.addEventListener("input", () => {

            // Si l'utilisateur modifie la recherche,
            // on supprime la sélection précédente.
            this.hiddenInput.value = "";

            this.search(
                this.input.value.trim()
            );

        });


        // Sélection d'un résultat
        this.results.addEventListener(
            "click",
            (event) => {

                const item = event.target.closest(
                    ".search-select-item"
                );

                if (!item) {
                    return;
                }

                this.selectItem(item);
            }
        );


        // Fermer les résultats si clic en dehors
        document.addEventListener(
            "click",
            (event) => {

                if (
                    !this.wrapper.contains(
                        event.target
                    )
                ) {
                    this.hideResults();
                }

            }
        );
    }


    async searchItems(query) {

        try {

            const response = await fetch(
                `${this.url}?q=${encodeURIComponent(query)}`
            );

            if (!response.ok) {

                throw new Error(
                    "Erreur lors de la recherche"
                );

            }

            const data = await response.json();

            this.renderResults(
                data.results
            );

        } catch (error) {

            console.error(error);

            this.results.innerHTML =
                '<div class="search-select-item">Erreur lors de la recherche</div>';

            this.results.style.display = "block";
        }
    }


    renderResults(results) {

        if (!results.length) {

            this.results.innerHTML =
                '<div class="search-select-item">Aucun résultat trouvé</div>';

            this.results.style.display = "block";

            return;
        }


        this.results.innerHTML = results.map(
            item => `
                <div
                    class="search-select-item"
                    data-id="${item.id}"
                    data-label="${item.name}"
                >
                    <strong>${item.name}</strong>
                </div>
            `
        ).join("");


        this.results.style.display = "block";
    }


    selectItem(item) {

        this.hiddenInput.value =
            item.dataset.id;

        this.input.value =
            item.dataset.label;

        this.hideResults();
    }


    hideResults() {

        this.results.style.display =
            "none";
    }
}


document.addEventListener(
    "DOMContentLoaded",
    () => {

        document
            .querySelectorAll(
                ".search-select-wrapper"
            )
            .forEach(wrapper => {

                new SearchSelect(wrapper);

            });

    }
);