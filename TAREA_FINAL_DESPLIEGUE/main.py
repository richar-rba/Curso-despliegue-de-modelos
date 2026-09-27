
from contextlib import asynccontextmanager  # para ver si bundle(modelo) esta cargado
#from typing import Literal : 
import joblib  
import pandas as pd 
from fastapi import FastAPI, HTTPException # para saber el error que se comete 
from pydantic import BaseModel,Field # para manejar las varibles predictoras las validaciones 
from esquemas import EstudianteInput, EstudianteOutput

#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------

 # 2) RUTA DEL BUNDEL DONDE SE ENCUENTRA ALOJADO

NOMBRE_BUNDLE="modelo_ridge_bimestre.pkl" 
estado_servicio={"bundle":None}


# 3) CARGAMOS EL BUNDLE ANTES DE LA API
async def lifespan(app:FastAPI):  
    estado_servicio["bundle"]=joblib.load(NOMBRE_BUNDLE) 
    print("Bundle cargado correctamente")
    yield 
    estado_servicio["bundle"]=None 


 # 4) CONFIGURAMOS LA APLICACIÓN API

app = FastAPI(
    title="API de predicción de rendimiento académico",
    description="Recibe datos de un estudiante y predice su nota final del bimestre",
    version="1.0.0",
    lifespan=lifespan)   

# 5) VARIABLES DE ENTRADA

'''class EstudianteInput(BaseModel):

    Attendance_Rate: float = Field(..., description="Porcentaje de asistencia del estudiante")

    Homework_Completion: float = Field(...,description="Porcentaje de cumplimiento de tareas")

    Quiz_Avg: float = Field(...,description="Promedio de quizzes")

    Midterm_Score: float = Field(...,description="Nota del examen parcial")

    Participation: float = Field(...,description="Nivel de participación")

    Study_Hours_Week: float = Field(...,description="Horas de estudio por semana")

    Internet_Access: str = Field(...,description="Acceso a Internet" )

    Family_Income_Level: str = Field(...,description="Nivel de ingresos familiares")

    Sleep_Hours: float = Field(...,description="Horas de sueño")

    Math_Score: float = Field(..., description="Puntaje en Matemática")

    Commute_Time_Min: float = Field(...,description="Tiempo de traslado en minutos" )

    Class_Size: int = Field(...,description="Cantidad de estudiantes en el aula")

    Teacher_Experience_Years: float = Field(...,description="Años de experiencia del docente")

    School_Type: str = Field(...,description="Tipo de colegio")

    Stress_Level: int = Field(...,description="Nivel de estrés") 


    # 6) SALIDA DE LA PREDICCIÓN

class EstudianteOutput(BaseModel):

    nota_predicha: float = Field(..., description="Nota final del bimestre predicha por el modelo")
'''


    #8) ENDPOINT DE VERIFICACIÓN

@app.get("/")
def estado():
    return {
        "servicio": "API de predicción de rendimiento académico",
        "modelo_cargado": estado_servicio["bundle"] is not None
           }


# 8) ENDPOINT DE PREDICCIÓN

@app.post("/predecir", response_model=EstudianteOutput)
def predecir(estudiante: EstudianteInput):

    # Verificar que el bundle esté cargado
    bundle = estado_servicio["bundle"]

    if bundle is None:
        raise HTTPException(
            status_code=503,
            detail="El modelo aún no está cargado"
        )

    # Convertir los datos recibidos a diccionario
    fila = estudiante.model_dump()

    # Crear DataFrame respetando exactamente
    # el orden de columnas utilizado durante el entrenamiento
    X_nuevo = pd.DataFrame([fila])[bundle["columnas"]]

  


    # Realizar la predicción
    prediccion = bundle["pipeline"].predict(X_nuevo)[0]

    # Devolver resultado
    return EstudianteOutput(
        nota_predicha=round(float(prediccion), 2)
    )
