class LiveSearch {

    constructor(options){

        this.input = document.querySelector(options.input);
        this.table = document.querySelector(options.table);
        this.url = options.url;
        this.renderer = options.renderer;
        this.delay = options.delay || 200;

        this.timer = null;

        this.init();
    }

    init(){

        if(!this.input){
            console.error("Input introuvable");
            return;
        }

        if(!this.table){
            console.error("Table introuvable");
            return;
        }

        this.input.addEventListener("input", ()=>{

            clearTimeout(this.timer);

            this.timer = setTimeout(()=>{
                this.search();
            }, this.delay);

        });

    }

    async search(){

        const q = this.input.value.trim();
        const pagination = document.querySelector(".pagination");

        if(q===""){
            pagination.style.display = "flex";
            location.reload();
            return;
        }

        pagination.style.display = "none";

        const response = await fetch(
            `${this.url}?q=${encodeURIComponent(q)}`
        );

        const data = await response.json();

        this.table.innerHTML = this.renderer(data.results);

    }

}




/**
 *  rendu des clients dans le tableau
 * @param {*} customers 
 * @returns 
 */
function renderCustomers(customers){
    if(customers.length===0){
        return `
            <tr>
                <td colspan="6">
                    Aucun client trouvé
                </td>
            </tr>
        `;
    }

    return customers.map(customer=>`

        <tr>
            <td>${customer.id}</td>
            <td>${customer.name}</td>
            <td>${customer.phone}</td>
            <td>${customer.email || "—"}</td>
            <td>${customer.address || "—"}</td>

            <td class="actions">
                <a
                    class="edit"
                    href="/customers/update/${customer.id}">
                    Modifier
                </a>

                <a
                    class="delete"
                    href="/customers/${customer.id}/delete/"
                    onclick="return confirm('Supprimer ce client ?')">
                    Supprimer
                </a>
            </td>
        </tr>
    `).join("");
}




/**
 *  rendu des fournisseurs dans le tableau
 * @param {*} suppliers 
 * @returns 
 */
function renderSuppliers(suppliers){
    if(suppliers.length===0){
        return `
            <tr>
                <td colspan="6">
                    Aucun fournisseur trouvé
                </td>
            </tr>
        `;
    }

    return suppliers.map(supplier=>`

        <tr>
            <td>${supplier.id}</td>
            <td>${supplier.name}</td>
            <td>${supplier.phone}</td>
            <td>${supplier.email || "—"}</td>
            <td>${supplier.address || "—"}</td>

            <td class="actions">
                <a
                    class="edit"
                    href="/suppliers/update/${supplier.id}">
                    Modifier
                </a>

                <a
                    class="delete"
                    href="/suppliers/${supplier.id}/delete/"
                    onclick="return confirm('Supprimer ce fournisseur ?')">
                    Supprimer
                </a>
            </td>
        </tr>
    `).join("");
}




function renderExpenses(expenses){
    if(expenses.length===0){
        return `
            <tr>
                <td colspan="6">
                    Aucune dépense trouvée
                </td>
            </tr>
        `;
    }

    return expenses.map(expense=>`

        <tr>
            <td>${expense.reference}</td>
            <td>${expense.expense_date}</td>
            <td>${expense.store}</td>
            <td>${expense.category}</td>
            <td>${expense.amount} FCFA</td>
            <td>${expense.payment_method}</td>
            <td>${expense.description}</td>

            <td class="actions">
                <a
                    class="delete"
                    href="/expenses/${expense.id}/delete/"
                    onclick="return confirm('Supprimer cette dépense ?')">
                    Supprimer
                </a>
            </td>
        </tr>
    `).join("");
}


function renderCredits(credits){
    if(credits.length===0){
        return `
            <tr>
                <td colspan="10">
                    Aucun crédit trouvé
                </td>
            </tr>
        `;
    }


    const payement = (credit) => {
        if(credit.status !== "paid") {
            return `<a href="/credits/payment/add/">Payer</a>`;
        }else{
            return `<span class="validated">Payé</span>`                     
        }
    }

    const getStatusBadge = (status) => {
        if (status === "paid") {
            return `<span class="badge paid">Remboursé</span>`;
        }

        if (status === "overdue") {
            return `<span class="badge late">En retard</span>`;
        }

        return `<span class="badge pending">En cours</span>`;
    }


    return credits.map(credit=>`

        <tr>
            <td>${credit.reference}</td>
            <td>${credit.customer}</td>
            <td>${credit.store}</td>
            <td>${credit.amount} FCFA</td>
            <td class="text-danger">${credit.remaining} FCFA</td>
            <td>${credit.interest_rate}%</td>
            <td>${credit.note}</td>
            <td>${credit.due_date}</td>
            <td>${getStatusBadge(credit.status)}</td>
            <td class="Comptoir">${payement(credit)}</td>
        </tr>
    `).join("");
}