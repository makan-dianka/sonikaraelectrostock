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

        this.input = wrapper.querySelector(".search-select-input");
        this.results = wrapper.querySelector(".search-select-results");

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

        this.input.addEventListener("input", () => {
            this.search(this.input.value.trim());
        });


        this.results.addEventListener("click", (event) => {

            const item = event.target.closest(
                ".search-select-item"
            );

            if (!item) {
                return;
            }

            this.selectItem(item);
        });


        document.addEventListener("click", (event) => {

            if (
                !this.wrapper.contains(event.target)
            ) {
                this.hideResults();
            }
        });
    }


    async searchItems(query) {

        if (!query.length) {
            this.hideResults();
            return;
        }

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

            this.renderResults(data.results);

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


        this.results.innerHTML = results.map(item => `
            <div
                class="search-select-item"
                data-id="${item.id}"
                data-label="${item.name}"
            >
                <strong>${item.name}</strong>
            </div>
        `).join("");

        this.results.style.display = "block";
    }


    selectItem(item) {
        this.hiddenInput.value = item.dataset.id;
        this.input.value = item.dataset.label;
        this.hideResults();
    }


    hideResults() {
        this.results.style.display = "none";
    }
}


document.addEventListener("DOMContentLoaded", () => {
    document
        .querySelectorAll(".search-select-wrapper")
        .forEach(wrapper => {
            new SearchSelect(wrapper);
        });
});