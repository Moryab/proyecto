// ESTO HACE QUE FUNCIONE EL FORMULARIO

let preciosPorSucursal = {};

async function buscarProducto() {
  const nombreProducto = document.getElementById('productoNombre').value;
  const url = `/api/productos/nombre/${encodeURIComponent(nombreProducto)}/`;
  const response = await fetch(url);
  const data = await response.json();

  const stockList = document.getElementById('stock-list');
  const sucursalSelect = document.getElementById('sucursal');
  stockList.innerHTML = "<h3>Stock por Sucursal:</h3>";
  sucursalSelect.innerHTML = "";
  preciosPorSucursal = {};

  if (data.length === 0) {
    stockList.innerHTML += "<p>No se encontraron productos con ese nombre.</p>";
    return;
  }

  data.forEach(item => {
    stockList.innerHTML += `
      <p><strong>${item.sucursal_nombre}</strong> - Stock: ${item.stock} | Precio: $${item.precio}</p>
    `;

    const option = document.createElement('option');
    option.value = item.sucursal_id;
    option.text = `${item.sucursal_nombre} (Stock: ${item.stock})`;
    sucursalSelect.appendChild(option);

    preciosPorSucursal[item.sucursal_id] = parseFloat(item.precio);
  });

  calcularTotal(); // muestra total inicial
}

function calcularTotal() {
  const cantidad = parseInt(document.getElementById('cantidad').value || 1);
  const sucursalId = document.getElementById('sucursal').value;

  const precio = preciosPorSucursal[sucursalId] || 0;
  const total = precio * cantidad;
  const totalUSD = total * 0.1;

  document.getElementById('total').textContent = total.toFixed(2);
  document.getElementById('total-usd').textContent = totalUSD.toFixed(2);
}

async function realizarVenta() {
  const productoNombre = document.getElementById('productoNombre').value;
  const sucursalId = document.getElementById('sucursal').value;
  const cantidad = document.getElementById('cantidad').value;

  // ⚠️ Necesitas un endpoint que convierta nombre → ID o usar nombre en el backend
  const productoId = await obtenerProductoIdPorNombre(productoNombre);
  if (!productoId) {
    document.getElementById('mensaje').textContent = "Producto no encontrado.";
    return;
  }

  const response = await fetch('/api/venta/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      producto_id: productoId,
      sucursal_id: sucursalId,
      cantidad: cantidad
    })
  });

  const resultado = await response.json();
  document.getElementById('mensaje').textContent = resultado.mensaje || resultado.error;
}

// 🔄 Obtener ID real desde nombre (podrías hacer un fetch aquí)
async function obtenerProductoIdPorNombre(nombre) {
  const url = `/api/productos/id-por-nombre/${encodeURIComponent(nombre)}/`;
  const response = await fetch(url);
  if (!response.ok) return null;

  const data = await response.json();
  return data.producto_id; // necesitas que la vista retorne esto
}
