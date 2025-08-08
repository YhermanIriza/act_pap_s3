from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# --------------------
# Modelos
# --------------------
class Producto(BaseModel):
    nombre: str
    precio: float
    categoria: str
    stock: int

class ProductoParcial(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    categoria: Optional[str] = None
    stock: Optional[int] = None

# --------------------
# Base de datos simulada
# --------------------
productos = [
    {"nombre": "Croquetas perro", "precio": 50.0, "categoria": "alimento", "stock": 20},
    {"nombre": "Pelota", "precio": 15.5, "categoria": "juguetes", "stock": 50},
    {"nombre": "Correa", "precio": 25.0, "categoria": "accesorios", "stock": 15},
]

# --------------------
# Endpoints
# --------------------

# GET /productos/ -> Listar todos o filtrar
@app.get("/productos/")
def listar_productos(
    categoria: Optional[str] = Query(None),
    nombre: Optional[str] = Query(None)
):
    resultados = productos
    if categoria:
        resultados = [p for p in resultados if p["categoria"].lower() == categoria.lower()]
    if nombre:
        resultados = [p for p in resultados if nombre.lower() in p["nombre"].lower()]
    return resultados

# GET /productos/{producto_id}
@app.get("/productos/{producto_id}")
def obtener_producto(producto_id: int):
    if 0 <= producto_id < len(productos):
        return productos[producto_id]
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# POST /productos/
@app.post("/productos/")
def crear_producto(producto: Producto):
    productos.append(producto.dict())
    return {"mensaje": "Producto creado", "producto": producto}

# PUT /productos/{producto_id}
@app.put("/productos/{producto_id}")
def actualizar_producto(producto_id: int, producto: Producto):
    if 0 <= producto_id < len(productos):
        productos[producto_id] = producto.dict()
        return {"mensaje": "Producto actualizado", "producto": producto}
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# PATCH /productos/{producto_id}
@app.patch("/productos/{producto_id}")
def actualizar_producto_parcial(producto_id: int, producto: ProductoParcial):
    if 0 <= producto_id < len(productos):
        for campo, valor in producto.dict(exclude_unset=True).items():
            productos[producto_id][campo] = valor
        return {"mensaje": "Producto actualizado parcialmente", "producto": productos[producto_id]}
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# DELETE /productos/{producto_id}
@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int):
    if 0 <= producto_id < len(productos):
        producto_eliminado = productos.pop(producto_id)
        return {"mensaje": "Producto eliminado", "producto": producto_eliminado}
    raise HTTPException(status_code=404, detail="Producto no encontrado")
