import database

def procesar_mensaje(numero, mensaje):
    mensaje = mensaje.lower().strip()
    estado = database.obtener_estado(numero)

    # 🔹 Estado inicial
    if estado == "inicio":
        if "hola" in mensaje:
            database.actualizar_estado(numero, "esperando_nombre")
            return "👋 Hola! ¿Cómo te llamas?"
        return "Escribe 'hola' para comenzar"

    # 🔹 Esperando nombre
    elif estado == "esperando_nombre":
        database.guardar_nombre(numero, mensaje)
        database.actualizar_estado(numero, "menu")
        return f"Mucho gusto {mensaje.capitalize()} 👋\nEscribe 'menu' para ver opciones"

    # 🔹 Menú principal
    elif estado == "menu":
        if "menu" in mensaje:
            return "📋 Menú:\n1. Información\n2. Soporte"

        elif mensaje == "1":
            return "ℹ️ Este bot guarda usuarios, mensajes y estado 😎"

        elif mensaje == "2":
            database.actualizar_estado(numero, "soporte")
            return "🛠️ Describe tu problema"

        else:
            return "Escribe 'menu' para ver opciones"

    # 🔹 Soporte
    elif estado == "soporte":
        database.actualizar_estado(numero, "menu")
        return "✅ Tu mensaje fue recibido, te contactaremos pronto.\nEscribe 'menu' para volver"

    return "❌ Algo salió mal"