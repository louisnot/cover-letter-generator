import os;
import openai;
from dotenv import load_dotenv

###############OPTIONS######################

load_dotenv()
api_key = os.environ.get('OPEN_API_KEY')
openai.api_key = api_key


def generate_letter(user_data,already_fed=False,language="English"):
        if not already_fed:
            messages=[]
            messages.append({"role" : "system", "content" : "You are a HR director that knows \
            perfectly the information technology industry"})
            messages = feed_list(messages, user_data)
            messages.append({"role" : "user",
                            "content": "Write me a cover letter in {}".format(language)
                            })
            messages.append({"role":"assistant",
                             "content" : "To whom it may concern,"})
            print("call openAI")
            response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.3,
                    presence_penalty=-1.0,
                    max_tokens=100,
                    stream=False,
            )
            message = response["choices"][0]["message"]["content"]
            messages.append({"role" : "assistant", "content" : message})
            return generate_letter(messages, True)
        else:
             print("call openAI")
             response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=user_data,
                    temperature=0.3,
                    presence_penalty=-1.0,
                    max_tokens=100,
                    stream=False
            )
             message = response["choices"][0]["message"]["content"]
             user_data.append({"role" : "assistant", "content" : message})
             if len(message.split()) < 10:
                return generate_letter(user_data, True)
             elif "Sincerely" in message or len(user_data) > 14:
                return user_data
             else:
                return generate_letter(user_data, True)
            

def feed_list(list_messages,user_data_dict):
    list_messages.append({"role" : "user", 
                         "content" : "My name is {}".format(
                        user_data_dict["name"])
                        })
    list_messages.append({"role" : "user", 
                        "content" : "I want to work {}".format(
                        user_data_dict["company"])
                        })
    if user_data_dict["position"] and not user_data_dict["position"].casefold() == 'spontaneous'.casefold():
        list_messages.append({"role" : "user", 
                            "content" : "I am applying for the {} position".format(
                            user_data_dict["position"])
                            })
    else:
         list_messages.append({"role" : "user", 
                            "content" : "I am sending a spontaneous application"
                            })
    list_messages.append({"role" : "user", 
                        "content" : "I have worked previously {}".format(
                        user_data_dict["experience"])
                        })
    list_messages.append({"role" : "user", 
                        "content" : "I graduated from  {}".format(
                        user_data_dict["education"])
                        })
    return list_messages