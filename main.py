from fastapi import FastAPI, HTTPException, status

from model import Curso

app = FastAPI()

cursos = {
}

@app.get('/cursos/')
async def get_cursos():
    return cursos

@app.get('/cursos/{id}')
async def get_curso_pelo_id(id: int):
    try:
        curso = cursos[id]
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')
    
@app.post('/cursos', status_code=status.HTTP_201_CREATED)
async def post_curso(curso: Curso):
    next_id = len(cursos) + 1 
    # curso.id = next_id
    del curso.id
    cursos[next_id] = curso 
    return curso

if  __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)