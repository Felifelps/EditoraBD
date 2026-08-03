from fastapi import HTTPException


class MateriaNaoEncontradaError(HTTPException):
    pass


class MateriaJaExisteError(HTTPException):
    pass