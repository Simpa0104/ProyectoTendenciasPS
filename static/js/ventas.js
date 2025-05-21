document.addEventListener('DOMContentLoaded', function () {
    // Agregar producto
    document.getElementById('agregarProducto').addEventListener('click', function () {
        const template = document.getElementById('productoTemplate').innerHTML;
        const container = document.getElementById('productosContainer');

        const div = document.createElement('div');
        div.innerHTML = template;
        container.appendChild(div.firstElementChild);

        // Configurar eventos para la nueva fila
        configurarEventosProducto(div.firstElementChild);
        actualizarTotal();
    });

    // Eliminar producto
    document.addEventListener('click', function (e) {
        if (e.target.classList.contains('eliminar-producto')) {
            e.target.closest('.producto-row').remove();
            actualizarTotal();
        }
    });

    // Configurar eventos para productos existentes (si hubiera)
    document.querySelectorAll('.producto-row').forEach(row => {
        configurarEventosProducto(row);
    });

    // Función para configurar eventos de un producto
    function configurarEventosProducto(row) {
        const select = row.querySelector('.producto-select');
        const cantidadInput = row.querySelector('.cantidad-input');
        const precioSpan = row.querySelector('.precio-unitario');

        // Actualizar precio cuando cambia el producto
        select.addEventListener('change', function () {
            const precio = this.options[this.selectedIndex]?.dataset.precio || '0';
            precioSpan.textContent = `$${parseFloat(precio).toFixed(2)}`;
            actualizarTotal();
        });

        // Actualizar total cuando cambia la cantidad
        cantidadInput.addEventListener('input', function () {
            actualizarTotal();
        });
    }

    // Función para calcular el total
    function actualizarTotal() {
        let total = 0;

        document.querySelectorAll('.producto-row').forEach(row => {
            const select = row.querySelector('.producto-select');
            const cantidadInput = row.querySelector('.cantidad-input');
            const precio = parseFloat(select.options[select.selectedIndex]?.dataset.precio || '0');
            const cantidad = parseFloat(cantidadInput.value || '0');

            if (!isNaN(precio) && !isNaN(cantidad)) {
                total += precio * cantidad;
            }
        });

        document.getElementById('totalVenta').textContent = `$${total.toFixed(2)}`;
    }

    // Autocompletado de productos
    const productoSelects = document.querySelectorAll('.producto-select');
    productoSelects.forEach(select => {
        new TomSelect(select, {
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            load: function (query, callback) {
                fetch(`/dashboard/ventas/buscar-producto/?term=${encodeURIComponent(query)}`)
                    .then(response => response.json())
                    .then(json => {
                        callback(json);
                    })
                    .catch(() => {
                        callback();
                    });
            },
            render: {
                option: function (item, escape) {
                    return `
                        <div>
                            <span class="title">${escape(item.nombre)}</span>
                            <span class="text-muted float-end">$${parseFloat(item.precio).toFixed(2)} (Stock: ${item.cantidad})</span>
                        </div>
                    `;
                }
            }
        });
    });
});