from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

livros = {
    1: {"Nome": "Manual de Análise de Dados", "autor": "Luiz Paulo Fávero", "lido": True},
    2: {"Nome": "Harry Potter e a Pedra Filosofal", "autor": "J.k Rowling", "lido": False}
}


def get_new_id():
    return max(livros.keys()) + 1 if livros else 1


# ROUTES
@app.get("/")
def home():
    return livros


@app.get("/livros/{id_livros}")
def get_livros(id_livros: int):
    livro = livros.get(id_livros)
    if livro is None:
        raise HTTPException(status_code=404, detail="O livro não foi encontrado")
    return livro


@app.post("/livros")
async def add_livro(request: Request):
    livro = await request.json()
    novo_id = get_new_id()
    livros[novo_id] = livro
    return {novo_id: livro}


@app.put("/livros/{livro_id}")
async def update_livro(livro_id: int, request: Request):
    livro_existente = livros.get(livro_id)
    if livro_existente is None:
        raise HTTPException(status_code=404, detail="O livro não foi encontrado")
    livro_atualizado = await request.json()
    livros[livro_id] = livro_atualizado
    return {livro_id: livro_atualizado}


@app.delete("/livros/{livro_id}")
async def delete_livro(livro_id: int):
    livro_existente = livros.get(livro_id)
    if livro_existente is None:
        raise HTTPException(status_code=404, detail="O livro não foi encontrado")
    livros.pop(livro_id, None)
    return {"detail": f"Livro {livro_id} deletado com sucesso"}
