# type: ignore 
from fasthtml.common import *

# when the user click the toggle, the htmx sends a get request to f"/toggle/{todo.id}", and the server will do the staff and send back the updated response 
def render(todo):
    # 创建 HTML 元素 ID
    html_id = f"todo-{todo.id}"
    print("render", html_id)
    toggle = A("Toggle ", hx_get=f"/toggle/{todo.id}", target_id=html_id)
    delete = A("Delete ", hx_delete=f"/{todo.id}", hx_swap="outerHTML", target_id=html_id)
    return Li(toggle, delete, todo.title + ("✅" if todo.done else ""), id=html_id) 

# 因为在 fast_app 中指定了 render 函数，所以 todos 中的数据会自动调用 render 函数
# to deploy, it should be "data/todos.db", live=False
app, rt, todos, Todo = fast_app("todos.db", live=True, render=render, id=int, title=str, done=bool, pk="id")

def mk_input(): return Input(placeholder="Add a todo", id="title", hx_swap_oob="true")

@rt("/")
def get():
    frm = Form(Group(mk_input(), Button("Add")), hx_post="/", target_id="todo-list", hx_swap="beforeend")
    return Titled("Todos", 
                  Card(
                      Ul(*todos(), id="todo-list"),
                      header=frm))

@rt("/")
def post(todo:Todo): return todos.insert(todo), mk_input()

@rt("/{todo_id}")
def delete(todo_id:int):
    todos.delete(todo_id)

# the parameter name can be any name, but it must match the path variable
# for the returned todo object, fasthtml will automatically render it and then send the html to the client
@rt("/toggle/{todo_id}") 
def get(todo_id:int):
    print("toggle", todo_id)
    todo = todos[todo_id]
    todo.done = not todo.done
    return todos.update(todo)

serve() 