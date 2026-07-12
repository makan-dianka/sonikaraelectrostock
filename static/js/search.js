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



function renderPayments(payments){
    if(payments.length===0){
        return `
            <tr>
                <td colspan="10">
                    Aucun paiement trouvé
                </td>
            </tr>
        `;
    }

    const payementStatus = (payment, sale) => {
        if (payment.get_remaining !== 0) {
            const type = sale ? 'sale' : 'purchase';
            const id = sale ? payment.sale_id : payment.purchase_id;
            return `<a href="/payments/create?type=${type}&id=${id}">Payer</a>`;
        } else {
            return `<span class="validated">Payé</span>`;
        }
    }

    return payments.map(payment=>`

        <tr>
            <td>${payment.id}</td>
            <td>${payment.sale || payment.purchase}</td>
            <td class="amount">${payment.amount} FCFA</td>
            <td class="text-danger">${payment.get_remaining} FCFA</td>
            <td class="badge method">${payment.payment_method}</td>
            <td>${payment.reference}</td>
            <td>${payment.created_at}</td>
            <td class="comptoir">${payementStatus(payment, payment.sale)}</td>
        </tr>
    `).join("");
}




function renderSales(sales){
    if(sales.length===0){
        return `
            <tr>
                <td colspan="10">
                    Aucune vente trouvé
                </td>
            </tr>
        `;
    }


    const getStatus = (sale) => {
        if (sale.status === "draft") {
            return `<a href="/sales/${sale.id}/update/" style="text-decoration: none;">
                        <span class="draft">
                            Brouillon
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640" width="20" heigth="20" fill="#f39b00"><path d="M416.9 85.2L372 130.1L509.9 268L554.8 223.1C568.4 209.6 576 191.2 576 172C576 152.8 568.4 134.4 554.8 120.9L519.1 85.2C505.6 71.6 487.2 64 468 64C448.8 64 430.4 71.6 416.9 85.2zM338.1 164L122.9 379.1C112.2 389.8 104.4 403.2 100.3 417.8L64.9 545.6C62.6 553.9 64.9 562.9 71.1 569C77.3 575.1 86.2 577.5 94.5 575.2L222.3 539.7C236.9 535.6 250.2 527.9 261 517.1L476 301.9L338.1 164z"/></svg>
                        </span>
                    </a>`;
        }

        if (sale.status === "cancelled") {
            return `<span class="cancelled">Annulé</span>`;
        }

        return `<span class="validated">Validée</span>`;
    }


    const setupActions = (sale) => {
        if (sale.status === "draft") {
            return `<a class="validate" href="/sales/${sale.id}/validate"
                        onclick="return confirm('Valider la vente ?')">
                        Valider
                    </a>`;
        }

        if (sale.status === "validated") {
            return `
                    <a class="btn btn-primary" href="/sales/invoice/${sale.id}" target="_blank">
                        🖨 Facture
                    </a>

                    <a class="cancel" href="/sales/${sale.id}/cancel"
                        onclick="return confirm('Annuler la vente ?')">
                        Annuler
                    </a>
                    `;
        }

        return `<span> — </span>`;
    }


    const setupComptoir = (sale) => {
        if (sale.status === "validated") {
            if (sale.remaining_amount === 0) {
                return `<span class="validated">Payé</span>`;
            }else{
                return `
                        <a class="pay" href="/payments/create?type=sale&id=${sale.id}">
                            Payer
                        </a>
                    `;
            }
        }else{
            return `<span> — </span>`;
        }

    }



    const payementStatus = (sale) => {
        if(sale.remaining_amount !== 0) {
            return `<a href="/payments/create?type=&id=">Payer</a>`;
        }else{
            return `<span class="validated">Payé</span>`                     
        }
    }

    return sales.map(sale=>`

        <tr>
            <td>${sale.created_at}</td>
            <td>${sale.reference}</td>
            <td>${sale.customer || 'Client'}</td>
            <td>${sale.store}</td>
            <td>${sale.total} FCFA</td>
            <td>${sale.remaining_amount} FCFA</td>
            <td>${getStatus(sale)}</td>
            <td>${setupActions(sale)}</td>
            <td>${setupComptoir(sale)}</td>
        </tr>
    `).join("");
}





function renderPurchases(purchases){
    if(purchases.length===0){
        return `
            <tr>
                <td colspan="10">
                    Aucun achat trouvé
                </td>
            </tr>
        `;
    }


    const getStatus = (purchase) => {
        if (purchase.status === "draft") {
            return `<a href="/purchases/${purchase.id}/update/" style="text-decoration: none;">
                        <span class="draft">
                            Brouillon
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640" width="20" heigth="20" fill="#f39b00"><path d="M416.9 85.2L372 130.1L509.9 268L554.8 223.1C568.4 209.6 576 191.2 576 172C576 152.8 568.4 134.4 554.8 120.9L519.1 85.2C505.6 71.6 487.2 64 468 64C448.8 64 430.4 71.6 416.9 85.2zM338.1 164L122.9 379.1C112.2 389.8 104.4 403.2 100.3 417.8L64.9 545.6C62.6 553.9 64.9 562.9 71.1 569C77.3 575.1 86.2 577.5 94.5 575.2L222.3 539.7C236.9 535.6 250.2 527.9 261 517.1L476 301.9L338.1 164z"/></svg>
                        </span>
                    </a>`;
        }

        if (purchase.status === "received") {
            return `<span class="received">Réceptionné</span>`;
        }

        return `<span class="cancelled">Annulé</span>`;
    }


    const setupActions = (purchase) => {
        if (purchase.status === "draft") {
            return `
                    <a class="receive" href="/purchases/${purchase.id}/status/received/"
                    onclick="return confirm('Confirmer la réception ?')">
                        Réceptionner
                    </a>

                    <a class="cancel" href="/purchases/${purchase.id}/status/cancelled/"
                    onclick="return confirm('Annuler cet achat ?')">
                        Annuler
                    </a>
                    `;
        }else{
            return `<span> — </span>`
        }
    }


    const setupComptoir = (purchase) => {
        if (purchase.payment_status === "unpaid" || purchase.payment_status === 'partial') {
            if (purchase.remaining_amount === 0) {
                return `<span class="validated">Payé</span>`;
            }else if (purchase.status === 'cancelled') {
                return `<span class="cancelled">Annulé</span>`
            }else if (purchase.status === 'received') {
                return `
                        <a class="pay" href="/payments/create?type=purchase&id=${purchase.id}">
                            Payer
                        </a>
                    `;
            }
        }else{
            return `<span class="received">Payé</span>`;
        }

        return `<span></span>`;
    }



    const payementStatus = (sale) => {
        if(sale.remaining_amount !== 0) {
            return `<a href="/payments/create?type=&id=">Payer</a>`;
        }else{
            return `<span class="validated">Payé</span>`                     
        }
    }

    return purchases.map(purchase=>`

        <tr>
            <td>${purchase.purchase_date}</td>
            <td>${purchase.supplier || 'Fournisseur'}</td>
            <td>${purchase.store}</td>
            <td>${purchase.reference}</td>
            <td>${purchase.total} FCFA</td>
            <td>${purchase.remaining_amount} FCFA</td>
            <td>${getStatus(purchase)}</td>
            <td>${setupActions(purchase)}</td>
            <td>${setupComptoir(purchase)}</td>
        </tr>
    `).join("");
}