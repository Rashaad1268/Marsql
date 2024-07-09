import os
import json
import cohere
from rest_framework.response import Response

from backend.viewsets import CustomViewSet
from .models import ChatMessage
from notebooks.models import NoteBookCell
from .serializers import ChatMessageCreateSerializer, ChatMessageSerializer
from notebooks.databases import postgres


co = cohere.Client(api_key=os.environ["COHERE_API_KEY"])


class ChatMessageViewSet(CustomViewSet):
    partial_serializer = ChatMessageCreateSerializer
    full_serializer = ChatMessageSerializer

    def get_queryset(self):
        return ChatMessage.objects.filter(
            notebook__id=int(self.kwargs["notebook_pk"])
        ).order_by("id")

    def perform_create(self, serializer):
        return serializer.save(
            notebook_id=int(self.kwargs["notebook_pk"]), author_type=1
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.perform_create(serializer)
        notebook = instance.notebook
        db_conf = notebook.db_config

        functions_map = {
            "run_sql_query": lambda query, do_commit=False: postgres.run_postgres_query(
                db_conf=db_conf, query=query, do_commit=do_commit
            )
        }

        preamble = get_preamble(json.dumps(postgres.get_postgres_db_metadata(db_conf)))

        response = co.chat(
            message=instance.content,
            tools=tools,
            preamble=preamble,
            model="command-r",
            force_single_step=False,
        )

        print("INITIAL RESpoNSE")
        print(response.text + "\n" + str(bool(response.tool_calls)))

        query_generated = None

        while response.tool_calls:
            print("The model recommends doing the following tool calls:")
            print("\n".join(str(tool_call) for tool_call in response.tool_calls))

            tool_results = []
            for tool_call in response.tool_calls:
                # here is where you would call the tool recommended by the model
                # using the parameters recommended by the model
                print(
                    f"= running tool {tool_call.name}, with parameters: {tool_call.parameters}"
                )

                output = functions_map[tool_call.name](**tool_call.parameters)

                if tool_call.name == "run_sql_query" and output["status"] == "success":
                    query_generated = tool_call.parameters["query"]

                # store the output in a list
                outputs = [output]
                print(f"== tool results: {outputs}")
                # store your tool results in this format
                tool_results.append({"call": tool_call, "outputs": outputs})

            response = co.chat(
                force_single_step=False,
                message="",
                tools=tools,
                chat_history=response.chat_history,
                tool_results=tool_results,
                preamble=preamble,
                model="command-r",
                temperature=0.8,
            )

        print("\n\nFINAL RESPONSE\n\n")
        print(response.text)
        response_msg = ChatMessage.objects.create(
            notebook=notebook, author_type=2, content=response.text
        )

        if query_generated:
            response_msg.cell = NoteBookCell.objects.create(
                notebook=notebook, type=1, content=query_generated
            )
            response_msg.save()

        return Response(
            {
                "message": ChatMessageSerializer(instance).data,
                "response": ChatMessageSerializer(response_msg).data,
            }
        )


def get_preamble(db_schema):
    return (
        """
## Task & Context
You help people analyze databases. You must answer questions about the database by generating and running the relevant sql queries and by analysing the data returned by the query.
Make sure the table names and column names in your query reflect the table names and column names in the schema or else the queries won't work

## Instructions for data analysis and query generation
You must understand the database schema when the table names and columns are provided as a list.
From that you must understand which table is responsible for which and also understand the columns of each table.
Also in your queries, make sure to limit the output rows to a maximum of 50.
If you need more context or anything about the database or about the users query, just ask the user for more context

The users schema is provided in the following format
{ // the database schema will be a dictionary, with the table names as the key and the columns as the value
    string: [ // the table name of a table in the schema as the key, list of columns of the table as the value 
        {
            "name": string, // the name of the column
            "data_type": string, // the data type of the column
            "is_nullable": boolean // whether the column is nullable or not
        }
    ]
}

Here is the schema the database that you need to analyse:
%s
"""
        % db_schema
    )


tools = [
    {
        "name": "run_sql_query",
        "description": """Connects to a database runs the given SQL query and returns the data.
        On success the data returned will look like this
          {
              "status": "success",
              "columns": Array<String>, // the column names of the data returned. It is a list of strings.
              "results": Array<Array<Any>>, // A list of lists containing the data of the rows returned. The index of each row matches the index of the colum
              "rows_affected": Integer, // the number of rows affected by the query
              "status_message": String, // the status message returned by the database
           }
        """,
        "parameter_definitions": {
            "query": {
                "description": "The SQL query to run",
                "type": "str",
                "required": True,
            },
            "do_commit": {
                "description": "Whether to commit the database or not after running the query",
                "type": "bool",
                "required": False,
            },
        },
    }
]
