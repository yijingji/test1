# Test out the structure in test2

import streamlit as st
import sqlite3
import os
import glob
from pathlib import Path
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
import pandas as pd
from typing import List, Dict, Any
import json
import re

class VehicleDatabase:
    """Handle SQLite database operations for vehicle data"""
    
    def __init__(self, db_path: str = "vehicles.db"):
        self.db_path = db_path
        
    def get_connection(self):
        """Create database connection"""
        return sqlite3.connect(self.db_path)
    
    def get_table_schema(self) -> Dict[str, List[str]]:
        """Get database schema information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        schema = {}
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            schema[table_name] = [col[1] for col in columns]
        
        conn.close()
        return schema
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame"""
        try:
            conn = self.get_connection()
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except Exception as e:
            st.error(f"Database error: {str(e)}")
            return pd.DataFrame()
    
    def get_sample_data(self, table_name: str, limit: int = 5) -> pd.DataFrame:
        """Get sample data from a table for AI as reference to generate SQL queries"""
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        return self.execute_query(query)

class PromptManager:
    """Manage modular prompts from files"""
    
    def __init__(self, prompt_folder: str = "modular_prompt"):
        self.prompt_folder = prompt_folder
        self.prompts = {}
        self.load_prompts()
    
    def load_prompts(self):
        """Load all prompt files from the modular prompt folder"""
        if not os.path.exists(self.prompt_folder):
            st.warning(f"Prompt folder '{self.prompt_folder}' not found. Creating default prompts.")
            self.create_default_prompts()
            return
        
        prompt_files = glob.glob(os.path.join(self.prompt_folder, "*"))
        
        for file_path in prompt_files:
            file_name = Path(file_path).stem
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.prompts[file_name] = f.read().strip()
            except Exception as e:
                st.error(f"Error loading prompt file {file_name}: {str(e)}")
    
    def create_default_prompts(self):
        """Create default prompts if folder doesn't exist"""
        os.makedirs(self.prompt_folder, exist_ok=True)
        
        default_prompts = {
            "system": """You are a helpful vehicle database assistant. You have access to a vehicle database and can help users query and understand vehicle data. 
You can execute SQL queries, analyze data, and provide insights about vehicles.
Always be helpful, accurate, and explain your reasoning.""",
            
            "sql_helper": """You are an expert SQL assistant for a vehicle database. 
Help users write SQL queries to extract information from the database.
Database schema: {schema}
Sample data: {sample_data}
Always provide safe, read-only queries.""",
            
            "data_analyst": """You are a data analyst specializing in vehicle data.
Analyze the provided data and give meaningful insights.
Focus on trends, patterns, and actionable information."""
        }
        
        for name, content in default_prompts.items():
            file_path = os.path.join(self.prompt_folder, f"{name}.txt")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        self.prompts = default_prompts
    
    def get_prompt(self, prompt_name: str) -> str:
        """Get a specific prompt by name"""
        return self.prompts.get(prompt_name, "")
    
    def list_prompts(self) -> List[str]:
        """List all available prompts"""
        return list(self.prompts.keys())

class VehicleChatbot:
    """Main chatbot class integrating LangChain, database, and prompts"""
    
    def __init__(self):
        self.db = VehicleDatabase()
        self.prompt_manager = PromptManager()
        self.setup_langchain()
        
    def setup_langchain(self):
        """Initialize LangChain components"""
        # Get OpenAI API key from Streamlit secrets
        openai_api_key = st.secrets["OPENAI_API_KEY"]
        
        # Initialize the chat model
        self.llm = ChatOpenAI(
            temperature=0.0,
            openai_api_key=openai_api_key,
            model_name="gpt-3.5-turbo"
        )
        
        # Setup memory
        self.memory = ConversationBufferMemory(return_messages=True)
        
        # Setup conversation chain
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            verbose=True
        )
    
    def get_database_context(self) -> str:
        """Get database context for the LLM"""
        schema = self.db.get_table_schema()
        # st.write("Database Schema:", schema)
        context = "Database Schema:\n"
        
        for table_name, columns in schema.items():
            context += f"\nTable: {table_name}\n"
            context += f"Columns: {', '.join(columns)}\n"
            
            # Get sample data
            sample_data = self.db.get_sample_data(table_name, 1)
            if not sample_data.empty:
                context += f"Sample data:\n{sample_data.to_string()}\n"
        
        return context

    def save_chat_history(self, memory, file_path="chat_history.json"):
        """Append new chat messages to the JSON file without duplicates."""
        try:
            # Extract messages from memory
            new_messages = [{"type": msg.type, "content": msg.content} for msg in memory.chat_memory.messages]
            
            # Check if the file exists
            if os.path.exists(file_path):
                try:
                    # Load existing chat history
                    with open(file_path, "r", encoding="utf-8") as f:
                        chat_history = json.load(f)
                except json.JSONDecodeError:
                    # Handle empty or invalid JSON file
                    chat_history = []
            else:
                # Initialize an empty chat history
                chat_history = []
            
            # Filter out messages that already exist in the file
            existing_messages = {json.dumps(msg) for msg in chat_history}  # Convert to JSON strings for comparison
            unique_messages = [msg for msg in new_messages if json.dumps(msg) not in existing_messages]

            st.write(unique_messages)
            
            # Append only unique messages to the existing history
            chat_history.extend(unique_messages)
            
            # Write updated chat history back to the file
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(chat_history, f, indent=4)
            
            st.success(f"Chat history updated in {file_path}")
        except Exception as e:
            st.error(f"Error saving chat history: {str(e)}")
    
    def process_message(self, user_message: str) -> str:
        """Process user message with selected prompt type"""
        # Get the selected prompt
        all_prompts = self.prompt_manager.prompts 

        # Combine all prompts into a single context
        combined_prompts = "\n\n".join([f"{key}:\n{value}" for key, value in all_prompts.items()])
        
        # Add database context
        db_context = self.get_database_context()
        combined_context = f"{combined_prompts}\n\nDatabase Context:\n{db_context}"
        
        # Create messages
        messages = [
            SystemMessage(content=combined_context),
            HumanMessage(content=user_message)
        ]
        
        # Get response from LLM
        llm_response = self.llm(messages).content
        # Extract SQL from the response
        sql_match = re.search(r'Action Input:\s*(SELECT .*?)(?:\n|$)', llm_response, re.IGNORECASE | re.DOTALL)
        st.write(sql_match)
        if sql_match:
            sql_query = sql_match.group(1).strip()
        else:
            # fallback: try to use the whole response (not ideal)
            sql_query = llm_response.strip()
        
        st.write(sql_query)
        
        # Execute the SQL query to fetch data
        try:
            result_df = self.db.execute_query(sql_query)
            if result_df.empty:
                response = "No data found for the given query."
            else:
                response = result_df.to_string(index=False)
        except Exception as e:
            response = f"Error executing query: {str(e)}"
        
        # Store in memory
        self.memory.chat_memory.add_user_message(user_message)
        self.memory.chat_memory.add_ai_message(response)

        # Save chat history to JSON file
        self.save_chat_history(self.memory)
        
        return response
    
    def execute_sql_query(self, query: str) -> pd.DataFrame:
        """Execute SQL query and return results"""
        return self.db.execute_query(query)

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Vehicle Database Chatbot",
        page_icon="🚗",
        layout="wide"
    )
    
    st.title("🚗 Vehicle Database Chatbot")
    st.markdown("Chat with your vehicle database using natural language!")
    
    # Initialize chatbot
    if 'chatbot' not in st.session_state:
        try:
            st.session_state.chatbot = VehicleChatbot()
            st.success("Chatbot initialized successfully!")
        except Exception as e:
            st.error(f"Error initializing chatbot: {str(e)}")
            st.stop()
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        
        # Database info
        st.header("Database Info")
        if st.button("Show Database Schema"):
            schema = st.session_state.chatbot.db.get_table_schema()
            st.json(schema)
        
        # Clear chat history
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.session_state.chatbot.memory.clear()
            st.rerun()
    
    # Main chat interface
    st.header("Chat")
    
    # Display chat history
    for i, (role, message) in enumerate(st.session_state.chat_history):
        if role == "user":
            st.chat_message("user").write(message)
        else:
            st.chat_message("assistant").write(message)
    
    # Chat input
    if prompt := st.chat_input("Ask me about your vehicle database..."):
        # Add user message to chat history
        st.session_state.chat_history.append(("user", prompt))
        st.chat_message("user").write(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.chatbot.process_message(
                        prompt,
                    )
                    st.write(response)
                    
                    # Add bot response to chat history
                    st.session_state.chat_history.append(("assistant", response))
                    
                except Exception as e:
                    error_msg = f"Error processing message: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append(("assistant", error_msg))

if __name__ == "__main__":
    main()
