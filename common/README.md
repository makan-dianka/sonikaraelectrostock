# L'usage de filtre

## 1. Créer le serializer de recherche, exemple à adapter :

```python
from rest_framework import serializers
from .models import Stock

class StockSearchSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_categ = serializers.CharField(source="product.category", read_only=True)
    product_reference = serializers.CharField(source="product.reference", read_only=True)

    class Meta:
        model = Stock
        fields = [
            "id",
            "product_name",
            "product_reference",
            "quantity",
            "alert_threshold",
            'product_categ'
        ]

```



## 2. Ajouter l'objet dans SEARCH_CONFIG dans le fichier search_config.py , exemple à adapter: 

```python
    "customers": {
        "queryset": lambda request: Customer.objects.for_company(
            request.user.company
        ).filter(is_deleted=False),
        "serializer": CustomerSearchSerializer,
        "search_fields": ["name", "phone"],
        "order_by": "name",
    },
```


## 3. ajouter dans l'url : 
pas besoin de l'adapter, ajouter dans la liste des urls de l'application concerné. Cette url est directement lié à la fonction `search_api()` dans common/search.py

```python
path('search/<str:entity>/', search_api, name='search_api'),
```

## 4. inclus la bar de recherche dans la page html concerné et adapter l'id et placeholder :

si la recherche concerne : juste de filtrer le resultat, par une table.

```python
{% include "components/search_bar.html" with id="stock-search" placeholder="Rechercher un produit par nom" %}
```

Si la recherche concerne : faire de recherche instantané et puis selectionné le resultat et l'injecter dans l'input.
Ajouter ce input et adapter le l'id de l'input et l'instance.

puis dans le form.py changer l'input concerné en hidden, exemple : `'supplier': forms.HiddenInput(),`

```html
<div class="customer-search-wrapper">
    <input type="text"
        class="form-control"
        id="customer-search"
        placeholder="Rechercher par nom ou téléphone"
        value="{% if form.instance.supplier %}{{ form.instance.supplier.name }} {% endif %}">

        <div id="customer-results"></div>
</div>
```

## 5. Ajouter les scripts js dans la page html concerné
adapter le appname et le parametre dans l'url. `{% url 'appname:search_api' 'parametre' %}`

Le parametre est la clé de l'objet dans `SEARCH_CONFIG`

adapter le input, table et renderer dans l'objet de la class `LiveSearch`

`input` c'est l'id de la bar de recherche. voir le numero 4, juste en dessus.

`table` C'est l'id à ajouter dans le `tbody` du table dans html si le resultat de la recherche construit une table.

```javascript
    <script src="{% static 'js/search.js' %}"></script>

    <script>
        // script pour bar de recherche de vente
        const STOCK_URL = "{% url 'stocks:search_api' 'stocks' %}";
        new LiveSearch({
            input:"#stock-search",
            table:"#stock-table",
            url:STOCK_URL,
            renderer:this.renderStocks
        });
    </script>
```

## 6. Ajouter la fonction de recherche dans search.js , exemple : 

Ajouter et adapter cette fonction dans le fichier `static/js/search.js`

Cette fonction concerne uniquement la recherche pour une table.

```javascript
function renderStocks(stocks){
    if(stocks.length===0){
        return `
            <tr>
                <td colspan="6">
                    Aucun produit trouvé
                </td>
            </tr>
        `;
    }

    const stockStatus = (stock) => {
        if (stock.quantity === 0) {
            return `<span class="danger">⚠ En rupture</span>`
        }
        else if (stock.quantity < stock.alert_threshold) {
            return `<span class="text-warning">⚠ Stock faible</span>`
        }
        else{
            return `<span class="success">Disponible</span>`
        }
    }

    return stocks.map(stock=>`

        <tr>
            <td> — </td>
            <td>${stock.product_name}</td>
            <td>${stock.product_categ}</td>
            <td>${stock.quantity}</td>
            <td>${stock.alert_threshold}</td>
            <td>${stockStatus(stock)}</td>
        </tr>
    `).join("");
}
```

## 7 Ajouter ce script dans la page html concerné :

Si la recherche concerné une recherche puis selectionner un resultat et l'injecter dans l'input dans html


```javascript
<script>
    // rechercher un fournisseur

    const CUSTOMER_URL = "{% url 'suppliers:supplier_search_api' %}";

    const customerInput = document.getElementById('customer-search');
    const customerHidden = document.getElementById('id_supplier');
    const customerResults = document.getElementById('customer-results');

    const searchCustomer = debounce(async function (query) {
        if (query.length < 1) {
            customerResults.style.display = 'none';
            return;
        }

        const response = await fetch(`${CUSTOMER_URL}?q=${query}`);
        const data = await response.json();
        renderCustomers(data.results);
    }, 200);


    function renderCustomers(results) {
        if (!results.length) {
            customerResults.innerHTML = '<div class="customer-item">Aucun client</div>';
            customerResults.style.display = 'block';
            return;
        }

        customerResults.innerHTML = results.map(c => `
                <div class="customer-item" data-id="${c.id}" data-label="${c.name}">
                    <strong>${c.name}</strong>
                    <span class="customer-phone">${c.phone}</span>
                </div>`
        ).join('');

        customerResults.style.display = 'block';
    }

    customerInput.addEventListener('input', function () {
        searchCustomer(this.value.trim());
    });

    customerResults.addEventListener('click', function (e) {
        const item = e.target.closest('.customer-item');
        if (!item) return;

        customerHidden.value = item.dataset.id;
        customerInput.value = item.dataset.label;
        customerResults.style.display = 'none';
    });

    document.addEventListener('click', function (e) {
        if (!customerInput.contains(e.target) && !customerResults.contains(e.target)) {
            customerResults.style.display = 'none';
        }
    });
    // fin de recherche fournisseur
</script>
```