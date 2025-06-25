function validarNombre() {
    const input = document.getElementById("nombre");
    const error = document.getElementById("error-nombre");

    if (input.value.trim() === "") {
        input.classList.add("is-invalid");
        error.style.display = "block";
    } else {
        input.classList.remove("is-invalid");
        error.style.display = "none";
    }
}

function validarPrecio() {
    const input = document.getElementById("precio");
    const error = document.getElementById("error-precio");
    const valor = parseFloat(input.value);

    if (isNaN(valor) || valor <= 0) {
        input.classList.add("is-invalid");
        error.style.display = "block";
    } else {
        input.classList.remove("is-invalid");
        error.style.display = "none";
    }
}

  //validacion Imagenes en adddprouc y edit
  function validarImagen() {
    var input = document.getElementById('imagen');
    var file = input.files[0];
    var allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
  
    if (file && allowedTypes.includes(file.type)) {
        // La selección de archivo es una imagen permitida
        input.setCustomValidity('');
    } else {
        // La selección de archivo no es una imagen permitida
        input.setCustomValidity('Seleccione una imagen válida (JPEG, PNG, GIF, WEBP).');
    }
  }
  