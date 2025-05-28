document.addEventListener("DOMContentLoaded", function () {
  const source = new EventSource("/sse/stock/");
  const toastContainer = document.getElementById("toast-container");

  function showToast(message) {
    const toast = document.createElement("div");
    toast.textContent = message;
    toast.style.background = "#333";
    toast.style.color = "#fff";
    toast.style.padding = "12px 20px";
    toast.style.marginTop = "10px";
    toast.style.borderRadius = "8px";
    toast.style.boxShadow = "0 4px 6px rgba(0,0,0,0.2)";
    toast.style.opacity = "0";
    toast.style.transition = "opacity 0.5s ease";
    toast.style.fontFamily = "Arial, sans-serif";
    toast.style.minWidth = "250px";

    toastContainer.appendChild(toast);

    // Animar entrada
    setTimeout(() => {
      toast.style.opacity = "1";
    }, 100);

    // Desaparecer después de 4 segundos
    setTimeout(() => {
      toast.style.opacity = "0";
      // Eliminar el nodo después de la transición
      setTimeout(() => {
        toast.remove();
      }, 500);
    }, 4000);
  }

  source.onmessage = function (event) {
    showToast(event.data);
  };

  source.onerror = function (event) {
    console.error("Error en conexión SSE:", event);
    source.close();
  };
});
