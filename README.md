# Shopping Cart - Backend API (Etapa 1)

API RESTful para gestionar un carrito de compras con persistencia en memoria.

## Instalación y Setup

### Requisitos
- Python 3.11+
- pip

### Pasos

1. Crear entorno virtual:
```bash
python -m venv venv
```

2. Activar entorno virtual:

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

3. Instalar dependencias:
```bash
pip install flask pytest
```

## Estructura del Proyecto

```
TPWEB2/
├── app.py              # Aplicación Flask principal
├── products.json       # Data inicial de productos
├── tests/
│   └── test_app.py    # Tests unitarios
├── README.md          # Este archivo
└── venv/              # Entorno virtual
```

## Ejecutar el Servidor

```bash
python app.py
```

El servidor inicia en `http://127.0.0.1:5000`

## Ejecutar Tests

```bash
# Todos los tests
python -m pytest

# Con verbosidad
python -m pytest -v

# Test específico
python -m pytest tests/test_app.py::test_add_to_cart_adds_new_item -v
```

## Documentación de Endpoints

### 1. Health Check
```
GET /
Response: "I'm alive!"
Status: 200
```

### 2. Listar Productos
```
GET /products
Response: 
{
  "products": [
    {"id": 1, "name": "Product A", "price": 19.99, "description": "..."},
    ...
  ]
}
Status: 200
```

### 3. Obtener Producto por ID
```
GET /products/<product_id>
Response: 
{
  "id": 1, 
  "name": "Product A", 
  "price": 19.99, 
  "description": "..."
}
Status: 200

Error (404):
{
  "error": "Product not found"
}
```

### 4. Ver Carrito
```
GET /cart
Response:
{
  "cart": [
    {"product_id": 1, "quantity": 2},
    {"product_id": 3, "quantity": 1}
  ]
}
Status: 200
```

### 5. Agregar Producto al Carrito
```
POST /cart/items
Content-Type: application/json

Request Body:
{
  "product_id": 2
}

Response: 
{
  "message": "Product added to cart."
}
Status: 200

Errores:
- 400: product_id no es entero o ausente
- 404: producto no existe
```

### 6. Quitar Producto del Carrito
```
DELETE /cart/items/<product_id>

Response:
{
  "message": "Product removed from cart."
}
Status: 200

Error (404):
{
  "error": "Product not in cart"
}
```

### 7. Calcular Total del Carrito
```
GET /cart/total
Response:
{
  "total": 49.97
}
Status: 200
```

## Ejemplos de Uso

### Con cURL
```bash
# Listar productos
curl http://127.0.0.1:5000/products

# Agregar al carrito
curl -X POST http://127.0.0.1:5000/cart/items \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1}'

# Quitar del carrito
curl -X DELETE http://127.0.0.1:5000/cart/items/1

# Ver total
curl http://127.0.0.1:5000/cart/total
```

### Con PowerShell
```powershell
# Listar productos
Invoke-RestMethod -Method Get -Uri http://127.0.0.1:5000/products

# Agregar al carrito
$body = @{ product_id = 1 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/cart/items `
  -ContentType "application/json" -Body $body

# Quitar del carrito
Invoke-RestMethod -Method Delete -Uri http://127.0.0.1:5000/cart/items/1

# Ver total
Invoke-RestMethod -Method Get -Uri http://127.0.0.1:5000/cart/total
```

## Características

- **Persistencia en Memoria**: Carrito y productos se mantienen en RAM durante la ejecución del servidor.
- **Productos desde JSON**: Se cargan de `products.json` al iniciar; no se modifican durante la ejecución.
- **Carrito Aislado**: Cada reinicio del servidor resetea el carrito.
- **Validación**: Se valida que los productos existan y que el carrito sea consistente.

## Códigos de Estado HTTP

- `200 OK`: Operación exitosa
- `400 Bad Request`: Datos inválidos en el request
- `404 Not Found`: Recurso no encontrado

## Tests Incluidos

- ✅ Obtener lista de productos
- ✅ Obtener producto por ID (éxito y 404)
- ✅ Agregar producto al carrito (nuevo y existente)
- ✅ Validación de tipo de dato en agregar
- ✅ Quitar producto del carrito
- ✅ Eliminación automática cuando cantidad = 0
- ✅ Cálculo de total con múltiples items

Total: 11 tests.
