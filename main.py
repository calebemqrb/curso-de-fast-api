from time import sleep
from typing import Any, Dict, Optional

from fastapi import (
    Depends,
    FastAPI,
    Header, 
    HTTPException, 
    Path,
    Query, 
    Response,
    status
)

from models.curso_model import Curso

def fake_db():
    try:
        print('Estabelecendo conexão com o Database')
        sleep(3)
    finally:
        print('Encerrando conexão com o Database')

app = FastAPI(
    title='Curso de FastAPI',
    version='0.0.14',
    description='API desenvolvida para estudos'
    )

cursos = {
}

@app.get('/cursos/',
         summary='Retorna os cursos cadastrados', 
         description='Retorna todos os cursos cadastrados ou uma lista vazia',
         response_model=list[Curso]
         )
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos

@app.get('/cursos/{id}',
         summary='Retorna um único curso',
         description='Busca e retorna um curso pelo seu id, se o curso não existir é retornado 404',
         response_model=Curso)
async def get_curso_pelo_id(id: int = Path(..., title='ID do curso', description='Deve existir', gt=0),db: Any = Depends(fake_db)):
    try:
        curso = cursos[id]
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')
    
@app.post('/cursos',
          status_code=status.HTTP_201_CREATED,
          summary='Insere um novo curso',
          description='Se todas as informações forem passadas corretamente, insere o curso na lista')
async def post_curso(curso: Curso, db: Any = Depends(fake_db)):
    next_id = len(cursos) + 1 
    # curso.id = next_id
    cursos[next_id] = curso 
    del curso.id
    return curso

@app.put('/cursos/{id}',
         summary='Atualiza o curso',
         description='Busca e atualiza um curso pelo seu id, se o curso não existir é retornado 404')
async def put_curso(id: int, curso: Curso, db: Any = Depends(fake_db)):
    if id in cursos:
        cursos[id] = curso
        del curso.id
        return curso
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')
    
@app.delete('/cursos/{id}',
            summary='Deleta o curso',
            description='Busca e deleta um curso pelo seu id, se o curso não existir é retornado 404')
async def delete_curso(id: int, curso: Curso, db: Any = Depends(fake_db)):
    if id in cursos:
        del cursos[id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')
    

@app.get('/calculadora')
async def calcular(a: int = Query(default=None, gt=5), b: int = Query(default=None, gt=10), c: Optional[int] = None, d: str = Header(default=None), db: Any = Depends(fake_db)):
    soma = a + b
    if c:
        soma = soma + c

    print(f'Header: {d}')

    return {"resultado": soma}
    
if  __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)