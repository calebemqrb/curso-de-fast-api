from fastapi import FastAPI

app = FastAPI()

cursos = {
    1:{
        "titulo": "Curso de FastAPI",
        "aulas": 112,
        "horas": 58
    },
    2:{
        "titulo": "Curso de Git e Github",
        "aulas": 80,
        "horas": 30
    }
}

@app.get('/cursos/')
async def get_cursos():
    return cursos

@app.get('/cursos/{id}')
async def get_curso_pelo_id(id: int):
    curso = cursos[id]
    curso.update({"id": id})

    return curso

if  __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)