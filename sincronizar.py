import pandas as pd
from woocommerce import API

# 1. Configuración de la conexión con tu sitio en Pantheon
wcapi = API(
    url="https://dev-superlapaloma.pantheonsite.io", # Verifica que sea tu URL exacta
    consumer_key="TU_CLAVE_CK_AQUI",
    consumer_secret="TU_CLAVE_CS_AQUI",
    version="wc/v3"
)

def subir_inventario_desde_excel(archivo_excel):
    # 2. Leer el archivo Excel
    try:
        df = pd.read_excel(archivo_excel)
        print("Excel leído correctamente.")
    except Exception as e:
        print(f"Error al leer el Excel: {e}")
        return

    # 3. Recorrer cada producto del Excel y subirlo a la App
    for index, row in df.iterrows():
        datos_producto = {
            "name": row['Nombre'],
            "type": "simple",
            "regular_price": str(row['Precio']),
            "manage_stock": True,
            "stock_quantity": int(row['Stock']),
            "sku": str(row['SKU']),
            "categories": [{"name": row['Categoria']}]
        }

        # Intentar enviar los datos a WooCommerce
        try:
            response = wcapi.post("products", datos_producto).json()
            if "id" in response:
                print(f"✅ Producto '{row['Nombre']}' creado con éxito. ID: {response['id']}")
            else:
                print(f"❌ Error al subir '{row['Nombre']}': {response['message']}")
        except Exception as e:
            print(f"Error de conexión: {e}")

# Ejecutar la función con tu archivo
subir_inventario_desde_excel("inventario.xlsx")
