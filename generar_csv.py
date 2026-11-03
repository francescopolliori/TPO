import csv

from administrador import (
    analizar_canales,
    analizar_categorias,
    analizar_horarios,
    analizar_streamers,
    cargar_json,
    streamer_con_pico_de_vistas,
)


def exportar_programas_csv():
    programas = cargar_json("lista_programas.json")
    campos = ["nombre_programa", "conductor", "plataforma", "dia", "hora_inicio", "genero"]

    with open("lista_programas.csv", "w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(programas)

    print("\nSe generó correctamente 'lista_programas.csv'.")


def exportar_usuarios_csv():
    usuarios = cargar_json("lista_usuarios.json")
    campos = ["id", "nombre", "edad", "suscripcion", "streamer_favorito", "horario_recurrentes"]

    with open("lista_usuarios.csv", "w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for usuario in usuarios:
            fila = usuario.copy()
            fila["horario_recurrentes"] = ", ".join(usuario.get("horario_recurrentes", []))
            escritor.writerow(fila)

    print("\nSe generó correctamente 'lista_usuarios.csv'.")


def exportar_estadisticas_csv():
    usuarios = cargar_json("lista_usuarios.json")
    programas = cargar_json("lista_programas.json")
    campos = ["tipo", "concepto", "valor"]

    mejor_canal, conteo_canales = analizar_canales(usuarios)
    mejor_categoria, conteo_categorias = analizar_categorias(usuarios, programas)
    mejor_streamer, conteo_streamers = analizar_streamers(usuarios)
    mejor_horario, conteo_horarios = analizar_horarios(usuarios)
    streamer_pico = streamer_con_pico_de_vistas(usuarios, programas)

    filas = [
        {"tipo": "resumen", "concepto": "Total de usuarios registrados", "valor": len(usuarios)},
        {"tipo": "resumen", "concepto": "Canal más visto", "valor": mejor_canal},
        {"tipo": "resumen", "concepto": "Categoría más vista", "valor": mejor_categoria},
        {"tipo": "resumen", "concepto": "Streamer más visto", "valor": mejor_streamer},
        {"tipo": "resumen", "concepto": "Horario pico de visualización", "valor": mejor_horario},
        {"tipo": "resumen", "concepto": "Streamer en racha", "valor": streamer_pico},
    ]

    for tipo, conteo in (
        ("por_categoria", conteo_categorias),
        ("por_streamer", conteo_streamers),
        ("por_canal", conteo_canales),
        ("por_horario", conteo_horarios),
    ):
        filas.extend(
            {"tipo": tipo, "concepto": concepto, "valor": cantidad}
            for concepto, cantidad in sorted(conteo.items(), key=lambda item: item[1], reverse=True)
        )

    with open("estadisticas.csv", "w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(filas)

    print("\nSe generó correctamente 'estadisticas.csv'.")


def menu_exportacion():
    while True:
        print("\n--- Exportar datos a CSV ---")
        print("  1. Exportar lista de programas")
        print("  2. Exportar lista de usuarios")
        print("  3. Exportar estadísticas")
        print("  4. Volver al menú principal")

        opcion = input("\nSeleccione una opción (1-4): ").strip()
        if opcion == "1":
            exportar_programas_csv()
        elif opcion == "2":
            exportar_usuarios_csv()
        elif opcion == "3":
            exportar_estadisticas_csv()
        elif opcion == "4":
            return
        else:
            print("\nOpción inválida. Seleccione un número del 1 al 4.")