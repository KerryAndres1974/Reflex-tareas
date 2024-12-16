import httpx
import reflex as rx
from typing import List, Dict

class FormInputState(rx.State):
    tasks: List[Dict[str, str]] = []

    @rx.event
    def get_tasks(self):
        try:
            respuesta = httpx.get('http://localhost:7000/tareas/')
            if respuesta.status_code == 200:
                self.tasks = respuesta.json()
            else:
                print(f"Error al extraer las tareas: {respuesta.status_code}")
        except Exception as e:
            print(f"Excepcion al obtener las tareas: {e}")

    @rx.event
    def send_task(self, form_data: dict):
        try: 
            respuesta = httpx.post('http://localhost:7000/tareas/', json=form_data)
            if respuesta.status_code == 200:
                self.tasks = respuesta.json()
                return rx.toast.info(
                    f"La tarea ha sido añadida.",
                    position="top-right",
                )
            else:
                print(f"Error al enviar tarea: {respuesta.status_code}")
        except Exception as e:
            print(f"Excepcion al enviar tarea: {e}")

    @rx.event
    def edit_task(self, form_data: dict):
        task_id = form_data['id']
        try:
            respuesta = httpx.put(f'http://localhost:7000/tareas/{task_id}', json=form_data)
            if respuesta.status_code == 200:
                self.tasks = respuesta.json()
                return rx.toast.info(
                    f"La tarea ha sido editada.",
                    position="top-right",
                )
            else:
                print(f"Error al editar tarea: {respuesta.status_code}")
        except Exception as e:
            print(f"Excepcion al editar tarea: {e}")      

    @rx.event
    def delete_task(self, task_id: int):
        try:
            respuesta = httpx.delete(f'http://localhost:7000/tareas/{task_id}')
            if respuesta.status_code == 200:
                self.tasks = respuesta.json()
                return rx.toast.info(
                    f"La tarea ha sido eliminada.",
                    position="top-right",
                )
            else:
                print(f"Error al borrar tarea: {respuesta.status_code}")
        except Exception as e:
            print(f"Excepcion al borrar tarea: {e}")

def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.vstack(
            rx.heading("Administrador de Tareas"),
            rx.form.root(
                rx.hstack(
                    rx.input(
                        name="titulo",
                        placeholder="Titulo",
                        type="text",
                        required=True,
                    ),
                    rx.input(
                        name="descripcion",
                        placeholder="Descripción",
                        type="text",
                        required=True,
                    ),
                    rx.input(
                        name="responsable",
                        placeholder="Responsable",
                        type="text",
                        required=True,
                    ),
                    rx.button("Guardar", type="submit"),
                    width="100%",
                ),
                on_submit=FormInputState.send_task,
                reset_on_submit=True,
            ),
            rx.button("Actualizar Tareas", on_click=FormInputState.get_tasks),
            rx.divider(),
            rx.grid(
                rx.foreach(
                    FormInputState.tasks,
                    lambda task: rx.container(
                        rx.heading(task["titulo"], size="6"),
                        rx.text(task["descripcion"]),
                        rx.text(
                            rx.text("responsable:", font_weight="bold", as_="span"),
                            f" {task["responsable"]}"    
                        ),
                        rx.text(
                            rx.text("estado:", font_weight="bold", as_="span"),
                            f" {task["estado"]}"    
                        ),
                        rx.text(
                            rx.text("creación:", font_weight="bold", as_="span"),
                            f" {task["fecha_creacion"]}"    
                        ),
                        rx.text(
                            rx.text("modificación:", font_weight="bold", as_="span"),
                            f" {task["fecha_modificacion"]}"    
                        ),
                        rx.container(
                            rx.hstack(
                                rx.dialog.root(
                                    rx.dialog.trigger(rx.button("Editar Tarea")),
                                    rx.dialog.content(
                                        rx.dialog.title(f"Editar {task["titulo"]}"),
                                        rx.form(
                                            rx.flex(
                                                rx.text(
                                                    "ID tarea",
                                                    as_="div",
                                                    size="2",
                                                    margin_bottom="4px",
                                                    weight="bold",
                                                ),
                                                rx.input(
                                                    name="id",
                                                    type="text",
                                                    read_only=True,
                                                    default_value=task["id"],
                                                ),
                                                rx.text(
                                                    "Titulo",
                                                    as_="div",
                                                    size="2",
                                                    margin_bottom="4px",
                                                    weight="bold",
                                                ),
                                                rx.input(
                                                    name="titulo",
                                                    type="text",
                                                    default_value=task["titulo"],
                                                    placeholder="Titulo",
                                                ),
                                                rx.text(
                                                    "Descripcion",
                                                    as_="div",
                                                    size="2",
                                                    margin_bottom="4px",
                                                    weight="bold",
                                                ),
                                                rx.input(
                                                    name="descripcion",
                                                    type="text",
                                                    default_value=task["descripcion"],
                                                    placeholder="Descripcion",
                                                ),
                                                rx.text(
                                                    "Responsable",
                                                    as_="div",
                                                    size="2",
                                                    margin_bottom="4px",
                                                    weight="bold",
                                                ),
                                                rx.input(
                                                    name="responsable",
                                                    type="text",
                                                    default_value=task["responsable"],
                                                    placeholder="Responsable",
                                                ),
                                                rx.text(
                                                    "Estado",
                                                    as_="div",
                                                    size="2",
                                                    margin_bottom="4px",
                                                    weight="bold",
                                                ),
                                                rx.select.root(
                                                    rx.select.trigger(placeholder=task['estado']),
                                                    rx.select.content(
                                                        rx.select.group(
                                                            rx.select.item("Pendiente", value="Pendiente"),
                                                            rx.select.item("En proceso", value="En proceso"),
                                                            rx.select.item("Realizada", value="Realizada"),
                                                            rx.select.item("Cancelada", value="Cancelada"),
                                                        ),
                                                    ),
                                                    name="estado",
                                                ),
                                                rx.flex(
                                                    rx.dialog.close(
                                                        rx.button(
                                                            "Cancelar",
                                                            color_scheme="gray",
                                                            variant="soft",
                                                        ),
                                                    ),
                                                    rx.dialog.close(
                                                        rx.button(
                                                            "Guardar",
                                                            type="submit"
                                                        ),
                                                    ),
                                                    spacing="3",
                                                    margin_top="16px",
                                                    justify="end",
                                                ),
                                                direction="column",
                                                spacing="3",
                                            ),
                                            on_submit=lambda: FormInputState.edit_task,
                                            reset_on_submit=True
                                        ),
                                    ),
                                ),
                                rx.dialog.root(
                                    rx.dialog.trigger(rx.button("Eliminar")),
                                    rx.dialog.content(
                                        rx.dialog.title(task["titulo"]),
                                        rx.dialog.description(
                                            "¿Estás seguro de que deseas eliminar esta tarea?",
                                        ),
                                        rx.box(
                                            rx.dialog.close(
                                                rx.button(
                                                    "Confirmar",
                                                    size="3",
                                                    on_click=lambda: FormInputState.delete_task(task["id"])
                                                ),
                                            ),
                                            rx.dialog.close(
                                                rx.button("Cancelar", size="3"),
                                            ),
                                            display="flex",
                                            justify_content="space-around",
                                            margin_top="1rem",
                                        ),
                                    ),
                                ),
                                display="flex",
                                justify_content="space-around",
                                margin_top="0.5rem",
                            ),
                        ),
                        width="100%",
                        padding="10px",
                        border_radius="5px",
                        border="1px solid grey",
                    ),
                ),
                grid_template_columns="repeat(3, 1fr)",
                gap="10px",
                width="100%",
            ),
            align_items="left",
            width="100%",
        ),
    )

app = rx.App()
app.add_page(index)