from fastapi import FastAPI
from pydantic import BaseModel
from agent.agentic_workflow import Graphbuilder
from starlette.responses import JSONResponse


app = FastAPI(title="AI Trip Planner",
              description="An AI-powered trip planning application that helps users plan their trips efficiently.",
              version="1.0.0")


class User_Query(BaseModel):
    questions: str
    
    
@app.post("/query")
async def travel_query(query:User_Query):
    """
    Endpoint to handle user queries related to trip planning.
    """
    # Here you would typically process the query and return a response.
    try:
        print(query)
        full_graph = Graphbuilder(model_provider='groq')
        react = full_graph()
        messages = {'messages': [query.questions]}
        output = react.invoke(messages)
        if isinstance(output, dict) and "messages" in output:
            return {"response": output["messages"][-1].content}
        else:
            return {"response": "No valid response from the model."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
