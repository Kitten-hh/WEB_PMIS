ai_tools = {
    "get_user": {
        "type": "function",
        "function": {
            "name": "get_user",
            "description": "get the user name or contact"
        },
        "parameters": {
            "type": "object",
            "properties": {
                "contact": {
                    "type": "string",
                    "description": "The user name or contact, you can get it from the question, example:sing's project、folow up with hb"
                },
            },
            "required": ["contact"]
        }        
    },
    "get_engineering": {
        "type": "function",
        "function": {
            "name": "get_engineering",
            "description": "get the engineering projects"
        }
    },
    "get_projects": {
        "type": "function",
        "function": {
            "name": "get_projects",
            "description": "get the user's projects",
            "parameters": {
                "type": "object",
                "properties": {
                    "contact": {
                        "type": "string",
                        "description": "The user name, you can get it from the question, example:sing's projects"
                    },
                    "top": {
                        "type": "number",
                        "description": "Get the first few projects"
                    }
                },
                "required": ["contact"]
            }
        }
    },
    "create_project": {
        "type": "function",
        "function": {
            "name": "create_project",
            "description": "create a project",
            "parameters": {
                "type": "object",
                "properties": {
                    "pid": {
                        "type": "string",
                        "description": "The Project id, user is required to enter"
                    },
                    "name": {
                        "type": "string",
                        "description": "The Project Name, user is required to enter"
                    }
                },
                "required": ["pid", "name"]
            }
        }
    },
    "get_sessions": {
        "type": "function",
        "function": {
            "name": "get_sessions",
            "description": "get the sessions in the current project",
            "parameters": {
                "type": "object",
                "properties": {
                    "recordid": {
                        "type": "string",
                        "description": "the current project's recordid, you can get it from the context, example:00390"
                    },
                    "contact": {
                        "type": "string",
                        "description": "The user name, you can get it from the context, example:sing's projects"
                    },
                    "top": {
                        "type": "number",
                        "description": "Get the first few sessions"
                    }
                },
                "required": ["recordid", "contact"]
            }
        }
    },
    "create_session": {
        "type": "function",
        "function": {
            "name": "create_session",
            "description": "create a session, must have create and session in question",
            "parameters": {
                "type": "object",
                "properties": {
                    "recordid": {
                        "type": "string",
                        "description": "the current project's recordid, you can get it from the context, example:00390"
                    },
                    "name": {
                        "type": "string",
                        "description": "The session Name, user is required to enter"
                    }
                },
                "required": ["recordid", "name"]
            }
        }
    },
    "create_task": {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "create a task with current session, must have create and task in question",
            "parameters": {
                "type": "object",
                "properties": {
                    "sessionid": {
                        "type": "string",
                        "description": "the current session id, you can get it from the context, example:01000-10"
                    },
                    "task": {
                        "type": "string",
                        "description": "the task description"
                    }
                },
                "required": ["sessionid", "task"]
            }
        }
    },
    "get_tasks": {
        "type": "function",
        "function": {
            "name": "get_tasks",
            "description": "get the tasks in the current session",
            "parameters": {
                "type": "object",
                "properties": {
                    "sessionid": {
                        "type": "string",
                        "description": "the current session id,you can get it from the context, example:01000-10"
                    },
                    "class1": {
                        "type": "string",
                        "description": "Check if 'class one' is mentioned in the question. If it is, return true; if not, return false.",
                        "enum": ["true", "false"]
                    }
                },
                "required": ["sessionid"]
            }
        }
    },
    "show_project_in_app": {
        "type": "function",
        "function": {
            "name": "show_project_in_app",
            "description": "Show me the project in the application",
            "parameters": {
                "type": "object",
                "properties": {
                    "recordid": {
                        "type": "string",
                        "description": "the current project's recordid, you can get it from the context, example:00390"
                    },
                    "contact": {
                        "type": "string",
                        "description": "The user name, you can get it from the context, example:sing's projects"
                    }
                },
                "required": ["contact"]
            }
        }
    },
    "show_milestone_in_app": {
        "type": "function",
        "function": {
            "name": "show_milestone_in_app",
            "description": "Show me the project's milestone in the application",
            "parameters": {
                "type": "object",
                "properties": {
                    "recordid": {
                        "type": "string",
                        "description": "the current project's recordid, you can get it from the context, example:00390"
                    },
                    "contact": {
                        "type": "string",
                        "description": "The user name, you can get it from the context, example:sing's projects"
                    }
                },
                "required": ["recordid", "contact"]
            }
        }
    },
    "show_gantt_chat_pdf": {
        "type": "function",
        "function": {
            "name": "show_gantt_chat_pdf",
            "description": "Generate and display the Gantt chart in PDF format.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recordid": {
                        "type": "string",
                        "description": "The project ID for generating the Gantt chart."
                    },
                    "sessionid": {
                        "type": "string",
                        "description": "The session ID associated with the project."
                    }
                },
                "required": ["recordid", "sessionid"]
            }
        }
    },

    "show_session_in_app": {
        "type": "function",
        "function": {
            "name": "show_session_in_app",
            "description": "Show me the session in the application",
            "parameters": {
                "type": "object",
                "properties": {
                    "recordid": {
                        "type": "string",
                        "description": "the current project's recordid, you can get it from the context, example:00390"
                    },
                    "sessionid": {
                        "type": "string",
                        "description": "the current session id,you can get it from the context, example:01000-10"
                    }
                },
                "required": ["recordid", "sessionid"]
            }
        }
    },
    "show_mindmap_in_app": {
        "type": "function",
        "function": {
            "name": "show_mindmap_in_app",
            "description": "Show me the project's mindmap in the application",
            "parameters": {
                "type": "object",
                "properties": {
                    "recordid": {
                        "type": "string",
                        "description": "the current project's recordid, you can get it from the context, example:00390"
                    }
                },
                "required": ["recordid"]
            }
        }
    },
    "get_requirement": {
        "type": "function",
        "function": {
            "name": "get_requirement",
            "description": "get the requirement of the session",
            "parameters": {
                "type": "object",
                "properties": {
                    "sessionid": {
                        "type": "string",
                        "description": "the current session id,you can get it from the context, example:01000-10"
                    }
                },
                "required": ["sessionid"]
            }
        }
    },
    "get_talk_about_topic": {
        "type": "function",
        "function": {
            "name": "get_talk_about_topic",
            "description": "get the talk about topic, must has want and talk and about in question, example:I want to talk about meeting, the topic is Meeting",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "the current session id,you can get it from the context, example:01000-10",
                        "enum": ["Projects", "Management", "Progress", "Policies", "Meeting", "Help Desk", "Development", "Knowledge based", "Suggestion", "Pre-conditions", "Personal"]
                    }
                },
                "required": ["topic"]
            }
        }
    },
    "get_document_list": {
        "type": "function",
        "function": {
            "name": "get_document_list",
            "description": "get the document of the session",
            "parameters": {
                "type": "object",
                "properties": {
                    "recordid": {
                        "type": "string",
                        "description": "the current project's recordid, you can get it from the context, example:00390"
                    },
                    "sessionid": {
                        "type": "string",
                        "description": "the current session id,you can get it from the context, example:01000-10"
                    },
                    "part_doc_name": {
                        "type": "string",
                        "description": "the part of document name,you can get it from the context,Please return the document names in English and Traditional Chinese. example:use case"
                    }
                },
                "required": ["recordid", "sessionid"]
            }
        }
    },

    "get_params": {
        "type": "function",
        "function": {
            "name": "get_params",
            "description": "This function retrieves specific parameters from the context based on the provided identifiers. It is used to extract context-specific values, such as user contact, project record ID, and session ID, to assist with further processing or decision-making in an ongoing process.",
            "parameters": {
                "type": "object",
                "properties": {
                    "contact": {
                        "type": "string",
                        "description": "The user name or contact involved in the context. You can extract this from the context or the question. Example: 'sing's project', 'follow up with hb'. This parameter identifies the user related to the current task."
                    },
                    "recordid": {
                        "type": "string",
                        "description": "The unique identifier for the current project. This value can be obtained from the context of the current project. Example: '00390'. It helps to track and differentiate different projects in the system."
                    },
                    "sessionid": {
                        "type": "string",
                        "description": "The session ID representing the current working session. This ID is specific to each session and is retrieved from the context. Example: '01000-10'. It is used to maintain the context of the ongoing work and ensure actions are correctly attributed to the right session."
                    }
                }
            }
        }
    }
}

def get_condition_data(question, sname_desc):
    return {
        "type": "function",
        "function": {
            "name": "get_condition_data",
            "description": question,
            "parameters": {
                "type": "object",
                "properties": {
                    "sname": {
                        "type": "string",
                        "description": sname_desc
                    },
                },
                "required": ["sname"]
            }
        }
    } 
ai_tools_funcs = {}
"""
ai_tools_funcs = {
    
    "14":[ai_tools['get_user']],
    "15":[ai_tools['get_projects']],
    "17":[ai_tools['get_sessions']],
    "17-13":[ai_tools['get_document_list']],
    "17-14":[ai_tools['get_tasks']],
    "18":[get_condition_data(
        "Do you want to know his outstanding class 1?",
        "The sname format is 'What're the outstanding tasks for {contact}?', The {contact} is user name or contact, you can get it from the question, example:sing's project、folow up with hb",
    )],
    "19":[
     get_condition_data(
        "Do you want to know his next top 10 tasks?",
        "The sname format is '{contact}'s Top Twenty', The {contact} is user name or contact, you can get it from the question, example:sing's project、folow up with hb"        
        )   
    ],
    "23":[
     get_condition_data(
        "我們需要討論昨天的會議嗎？",
        "The sname value is '2. Meeting Management'"        
        )   
    ],
    '21':[
        get_condition_data(
        "我們現在討論外部需求",
        "The sname value is '1. Help Desk Management.'"        
        )   
    ]
}
"""