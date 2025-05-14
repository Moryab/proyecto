const apiURL = "https://tuapi.com/productos"; // <-- Reemplaza con tu URL real

const stockList = document.getElementById("stock-list");
const sucursalSelect = document.getElementById("sucursal");
const cantidadInput = document.getElementById("cantidad");
const calcBtn = document.getElementById("calc");
const venderBtn = document.getElementById("vender");
const totalSpan = document.getElementById("total");
const totalUsdSpan = document.getElementById("total-usd");

let productos = [];
let tasaCambio = 1.0;

// Simula una consulta a la API y la base de datos
async function cargarDatos() {
  const response = await fetch(apiURL);
  const data = await response.json();

  productos = data;
  mostrarStock(data);
  cargarSucursales(data);
}

// Muestra stock por sucursal
function mostrarStock(data) {
  stockList.innerHTML = "";
  data.forEach(item => {
    const div = document.createElement("div");
    div.textContent = `Sucursal ${item.sucursal} | Cant: ${item.cantidad} | Precio: ${item.precio}`;
    stockList.appendChild(div);
  });

  const casaMatriz = document.createElement("div");
  casaMatriz.innerHTML = `<hr>Cant Casa Matriz: 10 | Precio: 999`;
  stockList.appendChild(casaMatriz);
}

// Llena el select de sucursales
function cargarSucursales(data) {
  const sucursales = [...new Set(data.map(item => item.sucursal))];
  sucursalSelect.innerHTML = "";
  sucursales.forEach(sucursal => {
    const option = document.createElement("option");
    option.value = sucursal;
    option.textContent = sucursal;
    sucursalSelect.appendChild(option);
  });
}

// Calcula el total
calcBtn.addEventListener("click", async () => {
  const sucursal = sucursalSelect.value;
  const cantidad = parseInt(cantidadInput.value);

  const producto = productos.find(p => p.sucursal === sucursal);
  if (!producto) return;

  const total = cantidad * producto.precio;
  totalSpan.textContent = total;

  // Supongamos que la conversión USD viene de otra API
  const usd = await fetch("https://api.exchangerate-api.com/v4/latest/CLP")
    .then(res => res.json())
    .then(data => data.rates.USD);

  tasaCambio = usd;
  totalUsdSpan.textContent = (total * usd).toFixed(2);
});

// Simula venta
venderBtn.addEventListener("click", () => {
  const sucursal = sucursalSelect.value;
  const cantidad = parseInt(cantidadInput.value);

  alert(`Procesando venta de ${cantidad} unidades en ${sucursal}`);

  // Aquí deberías hacer la lógica para disminuir stock e integración con Transbank
});

cargarDatos();
