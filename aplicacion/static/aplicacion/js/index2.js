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

  // Formatear el total en CLP
  const totalFormateado = total.toLocaleString('es-CL', {
    style: 'currency',
    currency: 'CLP',
    minimumFractionDigits: 0,  // CLP no usa decimales
    maximumFractionDigits: 0
  });

  // Formatear el total en USD con dos decimales
  const totalUSDFormateado = totalUSD.toLocaleString('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });

  document.getElementById('total').textContent = totalFormateado;
  document.getElementById('total-usd').textContent = totalUSDFormateado;
}


// Función para obtener la cookie CSRF
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie('csrftoken');

async function realizarVenta() {
  const productoNombre = document.getElementById('productoNombre').value.trim();
  const sucursalId = document.getElementById('sucursal').value;
  const cantidad = parseInt(document.getElementById('cantidad').value, 10);
  const mensaje = document.getElementById('mensaje');

  mensaje.textContent = '';
  mensaje.style.color = 'black';

  if (!productoNombre || !sucursalId || !cantidad || cantidad <= 0) {
    alert("Completa todos los campos correctamente antes de vender.");
    return;
  }

  try {
    // Paso 1: Buscar producto por nombre
    const buscarUrl = `/api/productos/nombre/${encodeURIComponent(productoNombre)}/`;
    const buscarResp = await fetch(buscarUrl);

    if (!buscarResp.ok) {
      throw new Error("No se pudo buscar el producto.");
    }

    const data = await buscarResp.json();

    if (!data.length) {
      mensaje.textContent = "Producto no encontrado.";
      mensaje.style.color = 'red';
      return;
    }

    // Buscar el producto con el sucursalId exacto (por si hay múltiples)
    const item = data.find(p => p.sucursal_id.toString() === sucursalId);
    if (!item) {
      mensaje.textContent = "Producto no encontrado en esa sucursal.";
      mensaje.style.color = 'red';
      return;
    }

    const productoId = item.producto_id;
    // ✅ Aquí el console.log para ver qué se está enviando
    console.log("Enviando:", {
      producto_id: productoId,
      sucursal_id: sucursalId,
      cantidad: cantidad
    });
    // Paso 2: Enviar la venta
    const ventaResp = await fetch('/api/venta/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      credentials: 'include',
      body: JSON.stringify({
        producto_id: productoId,
        sucursal_id: parseInt(sucursalId),
        cantidad: cantidad
      })
    });

    const resultado = await ventaResp.json();

    if (ventaResp.ok) {
      mensaje.textContent = resultado.mensaje || "Venta realizada correctamente.";
      mensaje.style.color = 'green';
      buscarProducto(); // Refrescar stock
    } else {
      mensaje.textContent = resultado.error || "Error en la venta.";
      mensaje.style.color = 'red';
    }
  } catch (error) {
    mensaje.textContent = "Error al procesar la venta.";
    mensaje.style.color = 'red';
    console.error(error);
  }
}

