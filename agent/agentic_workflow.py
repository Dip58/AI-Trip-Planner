from langgraph.graph import StateGraph,MessagesState,  END, START
from langgraph.prebuilt import ToolNode, tools_condition
from prompt_library.prompt import SYSTEM_PROMPT
from utils.model_loader import ModelLoader


class Graphbuilder():
    def __init__(self,model_provider: str='groq'):
        
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()
        
        self.tools = []  # Placeholder for tools, can be extended later
        self.graph = None
        
        self.llm_with_tools = self.llm.bind_tools(self.tools)  # type: ignore
        
        self.system_prompt = SYSTEM_PROMPT
    
    
    def agent_function(self,state: MessagesState):
        """Define the agent function that will be executed in the workflow.
        """
        user_question = state["messages"]
        input_question = [self.system_prompt] + user_question
        response = self.llm_with_tools.invoke(input_question)
        return {"messages": response} # type: ignore
    
    
    def build_graph(self):
        """
        Build the graph for the agentic workflow.
        This method should be implemented in subclasses.
        """
        graph_builder = StateGraph(MessagesState)
        graph_builder.add_node("agent", self.agent_function) # type: ignore
        graph_builder.add_node("tools", ToolNode(self.tools))
        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition)
        graph_builder.add_edge("tools", "agent")
        graph_builder.add_edge("tools", END)
        
        self.graph = graph_builder.compile()
        return self.graph
    
    def __call__(self):
        return self.build_graph()
    