from typing import Optional
from fastapi import (
    FastAPI,
    Header, 
    HTTPException, 
    Path,
    Query, 
    Response,
    status
)

from models.curso_model import Curso

app = FastAPI()

cursos = {
}

@app.get('/cursos/')
async def get_cursos():
    return cursos

@app.get('/cursos/{id}')
async def get_curso_pelo_id(id: int = Path(..., title='ID do curso', description='Deve existir', gt=0)):
    try:
        curso = cursos[id]
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')
    
@app.post('/cursos', status_code=status.HTTP_201_CREATED)
async def post_curso(curso: Curso):
    next_id = len(cursos) + 1 
    # curso.id = next_id
    cursos[next_id] = curso 
    del curso.id
    return curso

@app.put('/cursos/{id}')
async def put_curso(id: int, curso: Curso):
    if id in cursos:
        cursos[id] = curso
        del curso.id
        return curso
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')
    
@app.delete('/cursos/{id}')
async def delete_curso(id: int, curso: Curso):
    if id in cursos:
        del cursos[id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')
    

@app.get('/calculadora')
async def calcular(a: int = Query(default=None, gt=5), b: int = Query(default=None, gt=10), c: Optional[int] = None, d: str = Header(default=None)):
    soma = a + b
    if c:
        soma = soma + c

    print(f'Header: {d}')

    return {"resultado": soma}
    
if  __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)